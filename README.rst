=====
QINCM
=====

.. image:: https://readthedocs.org/projects/qincom/badge/?version=latest
        :target: https://qincom.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

Tool for quickly computing the costs of inland shipping due to limited navigational depth

* Free software: MIT license
* Documentation: https://qincom.readthedocs.io.


How to install
--------------
With these instructions you can create a new environment and install the package::

    conda create --name test_qincm
    activate test_qincm

    pip install .

    qincm --help

    qincm
          --route_depth_costs_file data\testmodel_4p\route_depth_costs.json
          --knelpunt_discharge_depth_file data\testmodel_4p\knelpunt_discharge_waterdepth.json
          --discharges [900,1000,1100,1200]
          --occurance [5,10,20,40]

Features
--------

This tool is meant for quickly assessing the response of the inland navigation to limited water depth. It is driven by input from larger models (like BIVAS) and under the assumption that the ships take the same route under all conditions, the response of the ship is computed.

For application the following methods are possible:

* Level 1: Compute the costs for a given situation. As input this requires either (1) the discharge at reference point or (2) the discharge at each knelpunt
* Level 2: Compute the total costs in a scenario (a year for a given distribution: combition of situation + number of days per year)


The tool builds on the following input:

* For each knelpunt the depth is required. Either directly, or through a discharge-depth relation. Either the local discharge, or the discharge at a reference point (Lobith) (using a given discharge distribution)
* For each combination of knelpunten, the relation between depth and reaction/effect is given

For further information, a memo is available.
