import argparse
import os
import shutil
import pypandoc


from converter import parse_arguments, get_bibtex_file, get_manuscript_file, post_process_html


EXTENSIONS = {"markdown": (".md", ".markdown"), "latex": (".tex", ".latex"), "latex+raw_tex": (".tex", ".latex")}


def get_volume_article_dirs(args):
    article_dirs = []
    for fname in os.listdir(args.input_dir):
        if not os.path.isdir(os.path.join(args.input_dir, fname)):
            continue
        article_dir = {
            "dir_name": fname,
            "input_dir": str(os.path.join(args.input_dir, fname)),
            "output_dir": str(os.path.join(args.output_dir, fname)),
        }
        article_dirs.append(article_dir)
    return article_dirs


def convert_volume(args):
    for article in get_volume_article_dirs(args):
        if os.path.exists(article["output_dir"]):
            shutil.rmtree(article["output_dir"])
        os.makedirs(article["output_dir"])

        manuscript = get_manuscript_file(article["input_dir"], EXTENSIONS[args.source_format])
        bibtex = get_bibtex_file(article["input_dir"])

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
        for fp in os.scandir(article["input_dir"]):
            if os.path.isdir(fp.path):
                shutil.copytree(fp.path, f"{article['output_dir']}/{fp.name}")
            else:
                shutil.copy(fp.path, f"{article['output_dir']}/{fp.name}")

        pypandoc.convert_file(
            manuscript.path,
            to=args.target_format,
            format=args.source_format,
            extra_args=extra_args,
            filters=filters,
            outputfile=f"{article['output_dir']}/{outputfile}",
        )

        if args.source_format == 'latex' and args.target_format == 'html':
            post_process_html( manuscript.path, '{}/{}'.format( article['output_dir'], outputfile ) )


def do_conversion():
    # parse arguments and convert volume
    args = parse_arguments()
    convert_volume(args)


if __name__ == "__main__":
    # keep global space empty, put every thing in functions
    do_conversion()

