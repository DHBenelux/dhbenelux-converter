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

```bash
python converter.py --source_format markdown --target_format html --input_dir submission/Murchison-Companjen-submission --output_dir public/Murchison-Companjen-submission --css ../../static/css/1.0.2/styles.css --template dhbenelux.template
```
(Note that stylesheets may be versioned, adapt the path accordingly.)

Next start a web server to view the output, e.g.:

```bash
python -m http.server 8888
```

To convert the submission of Kemman from LaTeX to HTML, run the following:

```bash
python converter.py --source_format latex --target_format html --input_dir submission/Kemman-final-submission --output_dir public/Kemman-final-submission --css ../../static/css/1.0.2/styles.css --template dhbenelux.template
```

To prepend a certain path to media sources in the HTML, use the prepend_path option, e.g.:

```bash
--prepend_path /wp-content/journal/issues/media/
```

### Converting an entire volume

It is possible to convert an entire volume of articles from LaTeX to PDF or HTML. This requires the LaTeX sources of the articles to be in their own directories within an input directory for the volume. The output directory must be a separate directory.

```bash
python3 convert_volume.py --source_format latex --target_format pdf --input_dir latex_dir/ --output_dir pdf_dir/ --template ../../static/latex/dhbenelux.cls
python3 convert_volume.py --source_format latex --target_format html --input_dir latex_dir/ --output_dir html_dir/ --css ../../static/css/1.0.2/styles.css --template dhbenelux.template
```

The volume input directory should have the following structure:

```
volume_format_dir/
.
+-- article-11-surname/
|      +-- main.tex
|      +-- references.bib
|      +-- images/
|          +-- image_1.png
|          +-- ...
+-- article-26-surname/
|    +-- main.tex
|    +-- references.bib
|    +-- images/
|        +-- image_1.png
+-- ...
```