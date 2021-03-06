*******************   
Watershed Workflow
*******************

.. image:: static/watershed_workflow.png

:Author: Ethan Coon, <coonet@ornl.gov>
:License: This work, including code, images, and documentation, unless
   otherwise specified, is copyright UT Battelle/Oak Ridge National
   Laboratory, and is licensed under the 3-clause BSD license.

Watershed Workflow is a python-based, open source chain of tools for
generating meshes and other data inputs for hyper-resolution
hydrology, anywhere in the (conterminous + Alaska?) US.

Hyper-resolution hydrologic models have huge data requirements, thanks
to their large extent (full river basins) and very high resolution
(often ~10-100 meters).  Furthermore, most process-rich models of
integrated, distributed hydrology at this scale require meshes that
understand both surface land cover and subsurface structure.  Typical
data needs for simulations such as these include:

* Watershed delineation (what is your domain?)
* Hydrography data (river network geometry, hydrographs for model evaluation)
* A digital elevation model (DEM) for surface topography
* Surface land use / land cover
* Subsurface soil types and properties
* Meterological data,

and more.

This package is a python library of tools and a set of jupyter
notebooks for interacting with these types of data streams using free
and open (both free as in freedom and free as in free beer) python and
GIS libraries and data.  Critically, this package aims to provide a way for
**automatically and quickly** downloading, interpreting, and
processing data needed to **generate a "first" hyper-resolution
simulation on any watershed** in the conterminous United States (and
most of Alaska/Hawaii/Puerto Rico).

To do this, this package provides tools to automate finding and
downloading a wide range of **open data streams,** including data from
United States governmental agencies, including USGS, USDA, DOE, and
others.  These data streams are then colocated on a mesh which is
generated based on a watershed delineation and a river network, and
that mesh is written in one of a variety of mesh formats for use in
hyper-resolution simulation tools.

Note: Hypothetically, this package works on all of Linux, Mac, and
Windows.  It has been tested on the first two, but not the third.


Workflows via Jupyter notebooks
------------------------------------

Workflows are the composition of partially automated steps to
accomplish a range of tasks.  Watershed Workflow provides tools for,
given a watershed, finding, downloading, pre-processing, interpolating
onto meshes, and writing data for use in hyper-resolution hydrologic
simulations.  Combining these tools into a full product is reasonably
supported by Jupyter notebooks.

Note that the majority of code is NOT in notebooks.  Notebooks have
`all sorts of issues for software development, demonstration, and
reproducibility
<https://docs.google.com/presentation/d/1n2RlMdmv1p25Xy5thJUhkKGvjtV-dkAIsUXP-AL4ffI/>`_
but they are great for providing a template for **modifiable**
tutorials.

Here I assume you know a little about Jupyter notebooks, and python.


Acknowledgements, citation, etc
-----------------------------------

This work was supported by multiple US Department of Energy projects
at the Oak Ridge National Laboratory.  Use of this codebase in the
academic literature should cite this repository (paper in
preparation).

Collaborators and contributions are very welcome!

