conda create --name test_qincm
activate test_qincm

cd qincm
pip install -e .

qincm --help

qincm --route_depth_costs_file data\testmodel_4p\route_depth_costs.json --knelpunt_discharge_depth_file data\testmodel_4p\knelpunt_discharge_waterdepth.json --discharges [900,1000,1100,1200] --occurance [5,10,20,40]