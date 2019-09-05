import argparse
import os
import shutil

import pypandoc


EXTENSIONS = {"markdown": (".md", ".markdown"), "latex": (".tex", ".latex")}


def get_bibtex_file(directory):
    return next(
        f for f in os.scandir(directory) if f.name.endswith((".bib", ".bibtex"))
    )


def get_manuscript_file(directory, extension):
    return next(f for f in os.scandir(directory) if f.name.endswith(extension))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source_format",
        type=str,
        required=True,
        choices=["markdown", "latex"],
        help="Source file format.",
    )
    parser.add_argument(
        "--target_format",
        type=str,
        required=True,
        choices=["pdf", "html"],
        help="Target file format.",
    )
    parser.add_argument("--input_dir", type=str, required=True, help="Input path.")
    parser.add_argument("--output_dir", type=str, required=True, help="Output path.")
    parser.add_argument("--css", type=str, help="Path to css file.")
    parser.add_argument("--standalone", action="store_true")
    parser.add_argument("--template", type=str)
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
      image.attributes.style = "width: " .. tostring( element.attributes.width ) .. ", height: " .. tostring( element.attributes.height ) .. ";"
      return image
    end
    """

    with open( "image-filter.lua", "w" ) as file:
        lua = lua.replace( "{%PREPEND_PATH_PLACEHOLDER%}", args.prepend_path )
        file.write( lua )

    filters = ["pandoc-citeproc"]
    extra_args = ["--mathjax", "--bibliography", bibtex.path]
    if args.standalone:
        extra_args += ["--standalone", "--lua-filter=image-filter.lua"]
    if args.css is not None:
        extra_args += ["--css", args.css]
    if args.template:
        extra_args += ["--template", args.template]

    outputfile = os.path.basename(manuscript.name) + (
        ".pdf" if args.target_format == "pdf" else ".html"
    )

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
