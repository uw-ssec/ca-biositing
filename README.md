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

When you first clone this repository, initialize and pull the submodule with:

```bash
git submodule update --init --recursive
```
