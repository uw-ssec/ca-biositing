# ca-biositing
Discussion of general issues related to the project and protyping or research 

## Relevant Links for project documentations and context

- eScience Slack channel: 🔒 [#ssec-ca-biositing](https://escience-institute.slack.com/archives/C098GJCTTFE)
- SSEC Sharepoint (**INTERNAL SSEC ONLY**): 🔒 [Projects/GeospatialBioeconomy](https://uwnetid.sharepoint.com/:f:/r/sites/og_ssec_escience/Shared%20Documents/Projects/GeospatialBioeconomy?csf=1&web=1&e=VBUGQG)

## QGIS

This project includes QGIS for geospatial analysis and visualization. You can run QGIS using pixi with the following command:

```bash
pixi run qgis
```

This will launch QGIS in the `gis` environment with all necessary dependencies installed.

For MacOS, there will be a Python
error about faulthandler, which is expected and can be ignored, see https://github.com/qgis/QGIS/issues/52987.
