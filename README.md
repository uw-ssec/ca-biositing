# ca-biositing

Discussion of general issues related to the project and protyping or research

## Relevant Links for project documentations and context

- eScience Slack channel: 🔒
  [#ssec-ca-biositing](https://escience-institute.slack.com/archives/C098GJCTTFE)
- SSEC Sharepoint (**INTERNAL SSEC ONLY**): 🔒
  [Projects/GeospatialBioeconomy](https://uwnetid.sharepoint.com/:f:/r/sites/og_ssec_escience/Shared%20Documents/Projects/GeospatialBioeconomy?csf=1&web=1&e=VBUGQG)
- Shared Sharepoint Directory: 🔒
  [SSEC CA Biositing Shared Folder](https://uwnetid.sharepoint.com/:f:/r/sites/og_ssec_escience/Shared%20Documents/Projects/GeospatialBioeconomy/SSEC%20CA%20Biositing%20Shared%20Folder?csf=1&web=1&e=p5wBel)

## General Discussions

For general discussion, ideas, and resources please use the
[GitHub Discussions](https://github.com/uw-ssec/ca-biositing/discussions).
However, if there's an internal discussion that need to happen, please use the
slack channel provided.

- Meeting Notes in GitHub:
  [discussions/meetings](https://github.com/uw-ssec/ca-biositing/discussions/categories/meetings)

## Questions

If you have any questions about our process, or locations of SSEC resources,
please ask [Anshul Tambay](https://github.com/atambay37).

## QGIS

This project includes QGIS for geospatial analysis and visualization. You can
run QGIS using pixi with the following command:

```bash
pixi run qgis
```

This will launch QGIS in the `gis` environment with all necessary dependencies
installed.

For MacOS, there will be a Python error about faulthandler, which is expected
and can be ignored, see https://github.com/qgis/QGIS/issues/52987.

## Frontend Integration

This repository now includes the **Cal Bioscape Frontend** as a Git submodule
located in the `frontend/` directory.

### Initializing the Submodule

When you first clone this repository, you can initialize and pull only the
`frontend` submodule with:

```bash
pixi run submodule-frontend-init
```

## 📘 Documentation

This project uses
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) for
documentation.

### Local Preview

You can preview the documentation locally using [Pixi](https://pixi.sh/):

```bash
pixi install -e docs
pixi run -e docs docs-serve
```

Then open your browser and go to:

```
http://127.0.0.1:8000
```

### Contributing Documentation

Most documentation should live in the relevant directories within the `docs`
folder.

When adding new pages to the documentation, make sure you update the
[`mkdocs.yml` file](https://github.com/uw-ssec/ca-biositing/blob/main/mkdocs.yml)
so they can be rendered on the website.

If you need to add documentation referencing a file that lives elsewhere in the
repository, you'll need to do the following (this is an example, run from the
package root directory)

```bash
# symlink the file to its destination
# Be sure to use relative paths here, otherwise it won't work!
ln -s ../../deployment/README.md docs/deployment/README.md

# stage your new file
git add docs/deployment/README.md
```

Be sure to preview the documentation to make sure it's accurate before
submitting a PR.
