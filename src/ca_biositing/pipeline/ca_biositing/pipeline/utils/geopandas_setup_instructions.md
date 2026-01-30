# Geopandas Notebook Setup Instructions

This file explains the key Pixi commands you need to run in order to use the
**geopandas_shapefile_extraction.ipynb** notebook.

## 1. Install the GIS environment

```
pixi install -e gis
```

- `-e gis` tells Pixi to install the _extra_ environment named **gis**. This
  environment contains all heavy geospatial dependencies such as `geopandas`,
  `shapely`, `pyproj`, `rasterio`, `matplotlib`, as well as Jupyter (`jupyter`,
  `ipykernel`).

## 2. Verify that the packages are available

```
pixi run -e gis pip list | grep -E "geopandas|ipykernel|jupyter"
```

- `pixi run -e gis …` runs the command inside the **gis** environment.
- `pip list` shows the packages installed; the `grep` part filters the output to
  the packages we care about.

## 3. Register a Jupyter kernel for the GIS environment (one‑time step)

```
pixi run -e gis python -m ipykernel install --user --name gis --display-name "Python (gis)"
```

- This creates a Jupyter kernel called **Python (gis)** that VS Code or Jupyter
  Notebook can select.

## 4. Start Jupyter / VS Code with the GIS kernel

- **Jupyter Notebook / Lab**
  ```
  pixi run -e gis jupyter notebook   # or `jupyter lab`
  ```
- **VS Code**
  1. Open a terminal and run the command above to launch the Jupyter server.
  2. In VS Code, open `geopandas_shapefile_extraction.ipynb`.
  3. At the top‑right of the notebook, click the kernel picker and choose
     **Python (gis)**.

## 5. Run the notebook cells

Now the imports will work:

```python
import geopandas as gpd
import matplotlib.pyplot as plt
```

If you get `ModuleNotFoundError`, double‑check that you are using the **Python
(gis)** kernel.

---

**Tip:** If you later add more GIS‑related packages, just run
`pixi add --feature gis --pypi <package>` and reinstall the environment with
`pixi install -e gis`.
