# DH Benelux Journal Templates and Conversion Scripts

## Installation

First install a recent version of [pandoc](https://pandoc.org/). Next install Python >3.6
and `pypandoc` with:

```bash
pip install pypandoc
```

## Example conversions

Assuming we have a directory with submissions in the top folder of this repo, we can
convert the source files using the `converter.py` script. For example, to convert the
submission of Murchison from markdown to HTML, we run the following:

``` bash
python converter.py --source_format markdown --target_format html --input_dir submission/Murchison-Companjen-submission --output_dir public/Murchison-Companjen-submission --css ../../static/css/styles.css --standalone
```

Next start a web server to view the output, e.g.:

``` bash
python -m http.server 8888
```

To convert the submission of Kemman from LaTeX to HTML, run the following:

``` bash
python converter.py --source_format latex --target_format html --input_dir submission/Kemman-final-submission --output_dir public/Kemman-final-submission --css ../../static/css/styles.css --standalone
```
