=====
QINCM
=====


.. image:: https://img.shields.io/pypi/v/qincm.svg
        :target: https://pypi.python.org/pypi/qincm

.. image:: https://img.shields.io/travis/jurjendejong/qincm.svg
        :target: https://travis-ci.com/jurjendejong/qincm

.. image:: https://readthedocs.org/projects/qincm/badge/?version=latest
        :target: https://qincm.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/jurjendejong/qincm/shield.svg
     :target: https://pyup.io/repos/github/jurjendejong/qincm/
     :alt: Updates



Tool for quickly computing the costs of inland shipping due to limited navigational depth


* Free software: MIT license
* Documentation: https://qincm.readthedocs.io.


Features
--------

This tool is meant for quickly assessing the response of the inland navigation to limited water depth. It is driven by input from larger models (like BIVAS) and under the assumption that the ships take the same route under all conditions, the response of the ship is computed.

For application the following methods are possible:

* Level 1: Compute the costs for a given situation. As input this requires either (1) the discharge at reference point or (2) the discharge at each knelpunt
* Level 2: Compute the total costs in a scenario (a year for a given distribution: combition of situation + number of days per year)


The tool builds on the following input:

* For each knelpunt the depth is required. Either directly, or through a discharge-depth relation. Either the local discharge, or the discharge at a reference point (Lobith) (using a given discharge distribution)
* For each combination of knelpunten, the relation between depth and reaction/effect is given


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
