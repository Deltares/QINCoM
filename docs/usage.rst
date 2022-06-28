=====
Usage
=====

The tool can be run in both in CLI-mode by calling qincm.exe or by usage in python.

CLI
###

In CLI-mode is currently only available for scenario mode. This function requires the input of both discharges and occurances::

    qincm
          --route_depth_costs_file data\testmodel_4p\route_depth_costs.json
          --knelpunt_discharge_depth_file data\testmodel_4p\knelpunt_discharge_waterdepth.json
          --discharges [900,1000,1100,1200]
          --occurance [5,10,20,40]
          --mode scenario


Python
######

To use QINCM in a project. 

Initiate the model::

    import qincm
    from pathlib import Path


    inputdir = Path('data/testmodel_4p')
    route_depth_costs_file = inputdir / 'route_depth_costs.json'
    knelpunt_discharge_depth_file = inputdir / 'knelpunt_discharge_waterdepth.json'

    M = QINCM(
        route_depth_costs_file,
        knelpunt_discharge_depth_file,
        reference='WA_Nijmegen'
    )

Calculate costs per discharge::

    import numpy as np
    
    discharges = np.linspace(500, 3000, 26)
    M.costs_per_discharge(discharges)


Calculate for timeseries::

    import pandas as pd
    
    discharges = np.linspace(500, 3000, 365)
    dates = pd.date_range('2000-01-01', periods=len(discharges), freq='1D')

    timeseries = pd.Series(index=dates, data=discharges)

    M.costs_for_scenario(timeseries)
