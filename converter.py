import argparse
import os
import shutil
import regex
import pypandoc


EXTENSIONS = {"markdown": (".md", ".markdown"), "latex": (".tex", ".latex"), "latex+raw_tex": (".tex", ".latex")}


def get_bibtex_file(directory):
    try:
        return next(
            f for f in os.scandir(directory) if f.name.endswith((".bib", ".bibtex"))
        )
    except StopIteration:
        return None


def get_manuscript_file(directory, extension):
    files = [f for f in os.scandir(directory) if f.name.endswith(extension)]
    if len(files) > 1:
        print("Multiple candidate files... Searching for `main` or `manuscript`")
        try:
            manuscript = next(f for f in files if f.name.startswith(('main', 'manuscript')))
        except StopIteration:
            raise ValueError(
                "No manuscript file found. Name the main manuscript as either `main.(tex|md)`")
    else:
        manuscript = files[0]
    return manuscript


def post_process_html( latex_file_path, html_file_path ):
    author_boiler_plate = '<p class="author">{}<sup>{}</sup></p>\n'
    affil_boiler_plate = '<p class="author"><sup>{}</sup>{}</p>\n'

    with open( latex_file_path, 'r' ) as latex_file:
        latex = latex_file.read()
    authors = regex.findall( r'\\author\[(\d+.*?)\](\{.*)', latex )
    affiliations = regex.findall( r'\\affil\[(\d+)\](\{.*)', latex )
    author_html = ''
    affil_html = ''
    for author in authors:
        author_name = pypandoc.convert_text( author[1], 'plain', format='latex' )
        author_name = regex.sub( '\n', ' ', author_name )
        author_html += author_boiler_plate.format( author_name.strip(), author[0] )
    for affiliation in affiliations:
        affil = pypandoc.convert_text( affiliation[1], 'plain', format='latex' )
        affil = regex.sub( '\n', ' ', affil )
        affil_html += affil_boiler_plate.format( affiliation[0], affil.strip() )

    with open( html_file_path, 'r' ) as html_file:
        html = html_file.read()
    header = regex.search( r'\<header.*?\>.*</header>', html, regex.DOTALL )
    header_span = header.span()
    header = header.group(0)
    header = regex.sub( r'<p class="author".*?>\n', '', header )
    insertion_idx = regex.search( r'</h1>\n', header ).span()[1]
    header = header[0:insertion_idx] + author_html + affil_html + header[insertion_idx:]
    html = html[0:header_span[0]] + header + html[header_span[1]:]
    with open( html_file_path, 'w' ) as html_file:
        html_file.write( html )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source_format",
        type=str,
        required=True,
        choices=["markdown", "latex", "latex+raw_tex"],
        help="Source file format.",
    )
    parser.add_argument(
        "--target_format",
        type=str,
        required=True,
        choices=[ "pdf", "html", "native" ],
        help="Target file format.",
    )
    parser.add_argument("--input_dir", type=str, required=True, help="Input path.")
    parser.add_argument("--output_dir", type=str, required=True, help="Output path.")
    parser.add_argument("--css", type=str, help="Path to css file.")
    parser.add_argument("--standalone", action="store_true")
    parser.add_argument("--template", type=str)
    parser.add_argument("--lua", type=str)
    parser.add_argument("--prepend_path", type=str, default="")
    args = parser.parse_args()

    if not os.path.exists("public"):
        os.mkdir("public")

    if os.path.exists(args.output_dir):
        shutil.rmtree(args.output_dir)
    os.makedirs(args.output_dir)

    manuscript = get_manuscript_file(args.input_dir, EXTENSIONS[args.source_format])
    bibtex = get_bibtex_file(args.input_dir)

    lua = """function Image( element )
      prepend_path = "{%PREPEND_PATH_PLACEHOLDER%}"
      image = pandoc.Image( element.caption, element.src, element.title )
      image.src = prepend_path .. element.src
      image.identifier = element.identifier
      return image
    end
    """

    with open( "image-filter.lua", "w" ) as file:
        lua = lua.replace( "{%PREPEND_PATH_PLACEHOLDER%}", args.prepend_path )
        file.write( lua )

    # filters = ["pandoc-citeproc"]
    filters = []
    extra_args = ["--mathjax", "--citeproc"]
    if bibtex is not None:
        extra_args += ["--bibliography", bibtex.path]
    if args.standalone:
        extra_args += ["--standalone", "--lua-filter=image-filter.lua"]
    if args.lua:
        extra_args += ["--lua-filter={}".format( args.lua ) ]
    if args.css is not None:
        extra_args += ["--css", args.css]
    if args.template:
        extra_args += ["--template={}".format( args.template ) ]

    output_format = ".pdf"
    if args.target_format == "html":
        output_format = ".html"
    elif args.target_format == "native":
        output_format = ".ast.txt"

    outputfile = os.path.basename(manuscript.name) + output_format

    # copy contents of submission folder to public
    for fp in os.scandir(args.input_dir):
        if os.path.isdir(fp.path):
            shutil.copytree(fp.path, f"{args.output_dir}/{fp.name}")
        else:
            shutil.copy(fp.path, f"{args.output_dir}/{fp.name}")

    output = pypandoc.convert_file(
        manuscript.path,
        to=args.target_format,
        format=args.source_format,
        extra_args=extra_args,
        filters=filters,
        outputfile=f"{args.output_dir}/{outputfile}",
    )

    if args.source_format == 'latex' and args.target_format == 'html':
        post_process_html( manuscript.path, '{}/{}'.format( args.output_dir, outputfile ) )
