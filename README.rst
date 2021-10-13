==================
gars-field
==================

- GARS - `Global Area Reference System <https://en.wikipedia.org/wiki/Global_Area_Reference_System>`__
- Field - Corteva Agriscience farming reference.


.. image:: https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square
    :alt: All Contributors
    :target: https://github.com/corteva/gars-field/blob/main/AUTHORS.rst

.. image:: https://img.shields.io/badge/License-BSD%203--Clause-yellow.svg
    :target: https://github.com/corteva/gars-field/blob/main/LICENSE

.. image:: https://img.shields.io/pypi/v/gars_field.svg
    :target: https://pypi.python.org/pypi/gars_field

.. image:: https://pepy.tech/badge/gars_field
    :target: https://pepy.tech/project/gars_field

.. image:: https://img.shields.io/conda/vn/conda-forge/gars_field.svg
    :target: https://anaconda.org/conda-forge/gars_field

.. image:: https://github.com/corteva/gars-field/workflows/Tests/badge.svg
    :target: https://github.com/corteva/gars-field/actions?query=workflow%3ATests

.. image:: https://codecov.io/gh/corteva/gars-field/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/corteva/gars-field

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
    :target: https://github.com/pre-commit/pre-commit

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black


Bugs/Questions
--------------

- Report bugs/feature requests: https://github.com/corteva/gars-field/issues
- Ask questions: https://github.com/corteva/gars-field/discussions


Usage
-----

.. note:: See the module docstrings for more details.


GARSField: determine GARS grids based on bounding box
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import geopandas
    import shapely.geometry
    from gars_field import GARSField


    geom_bounds = shapely.geometry.box(minx=-175, miny=-76, maxx=-174, maxy=-75)
    garsf = GARSField(geom_bounds)
    # 6 deg grids (extension)
    grids_6deg = garsf.gars_6deg
    # 3 deg grids (extension)
    grids_3deg = garsf.gars_3deg
    # 1 deg grids (extension)
    grids_1deg = garsf.gars_1deg
    # 30 min grids
    grids_30min = garsf.gars_30min
    # 15 min grids
    grids_15min = garsf.gars_15min
    # 5 min grids
    grids_5min = garsf.gars_5min
    # 1 min grids (extension)
    grids_1min = garsf.gars_1min

    # convert to geopandas
    geopandas.GeoDataFrame(
        {"gars_id": [str(grid) for grid in field.gars_1min]},
        geometry=[grid.polygon for grid in field.gars_1min],
        crs="EPSG:4326",
    )


GARSGrid
~~~~~~~~~~~~~~~~~~~~~~~~~~

Grid cell sizes: 1, 5, 15, 30 minutes

.. code-block:: python

    from gars_field import GARSGrid

    # from latlon
    ggrid = GARSGrid.from_latlon(-89.55, -179.57, resolution=5)

    # from GARS ID
    ggrid = GARSGrid("001AA23")

    # get bounding poly
    grid_poly = ggrid.polygon

    # get GARS ID
    gars_id = str(ggrid)

    # UTM CRS EPSG Code
    epsg_code = ggrid.utm_epsg


EDGARSGrid
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the extended degree grid system.

Grid cell sizes: 1, 3, 6 degrees

.. code-block:: python

    from gars_field import EDGARSGrid

    # from latlon
    ggrid = EDGARSGrid.from_latlon(-89.55, -179.57, resolution=3)

    # from GARS ID
    ggrid = EDGARSGrid("D01AA23")

    # get bounding poly
    grid_poly = ggrid.polygon

    # get GARS ID
    gars_id = str(ggrid)

    # UTM CRS EPSG Code
    epsg_code = ggrid.utm_epsg


GEDGARSGrid
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the giant extended degree grid system

Grid cell sizes: 30, 60 degrees

.. code-block:: python

    from gars_field import GEDGARSGrid

    # from latlon
    ggrid = GEDGARSGrid.from_latlon(-89.55, -179.57, resolution=3)

    # from GARS ID
    ggrid = GEDGARSGrid("GD1A")

    # get bounding poly
    grid_poly = ggrid.polygon

    # get GARS ID
    gars_id = str(ggrid)


Credits
--------

``GARSGrid`` was inspired by:

- https://github.com/mil-oss/GARSutils
- https://github.com/Moustikitos/gryd/blob/c79edde94f19d46e3b3532ae14eb351e91d55322/Gryd/geodesy.py
