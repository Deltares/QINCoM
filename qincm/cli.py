"""Console script for qincm."""
import sys
import click
from qincm.qincm import QINCM
import logging
import json

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S')

logger = logging.getLogger(__name__)

@click.command()
@click.option('--config', default=None, help="Load a configuration json file or give a json string with all configuration")
@click.option('--route_depth_costs_file', default="../data/testmodel_4p/route_depth_costs.json", help='input file of costs per route')
@click.option('--knelpunt_discharge_depth_file', default="../data/testmodel_4p/knelpunt_discharge_waterdepth.json", help='input file (or json string) of discharge depth relations')
@click.option('--reference', default="WA_Nijmegen", help='Name of reference point for global mode')
@click.option('--mode', default="scenario", help="Type of data input (only [scenario] is implemented)")
@click.option('--discharges', default=None, help="Required if config not given")
@click.option('--occurance', default=None, help="Required if config not given")
def main(config, route_depth_costs_file, knelpunt_discharge_depth_file, reference, mode, discharges, occurance):

    file_mode = False  # Output to file or return code

    if config is not None:
        # Allow both reading a json as inputstring and input as filepath

        # Approximation to check if string is path or dict...
        isFile = "discharges" not in config

        if isFile:
            logger.info(f'Loading configuration: {config}')

            file_mode = True
            with open(config) as fin:
                input_data = json.load(fin)
        else:
            input_data = json.loads(config)

        logger.debug(input_data)

        route_depth_costs_file = input_data["route_depth_costs_file"]
        knelpunt_discharge_depth_file = input_data["knelpunt_discharge_depth_file"]
        reference = input_data["reference"]
        mode = input_data["mode"]
        discharges = input_data["discharges"]
        occurance = input_data["occurance"]
    else:
        assert discharges is not None, '[discharges] not given'
        assert occurance is not None, '[occurance] not given'

        discharges = json.loads(discharges)
        occurance = json.loads(occurance)

    logger.info('Running configuration')

    M = QINCM(
        route_depth_costs_file=route_depth_costs_file,
        knelpunt_discharge_depth_file=knelpunt_discharge_depth_file,
        reference=reference
    )

    if mode == 'scenario':
        result = M.costs_for_scenario(
            discharges=discharges,
            occurance=occurance
        )

    else:
        NotImplementedError()
        result = None

    # Make results better readable
    result_pretty = result.copy()
    result_pretty.index = [str(i).replace('frozenset(', '').replace(')', '') for i in result_pretty.index]
    result_pretty = result_pretty.to_json()

    click.echo(result_pretty)

    # If we read a file, than also output as file
    if file_mode:
        outputfile = str(config).replace('.json', '_output.json')
        with open(outputfile, 'w') as fout:
            fout.write(result_pretty)

    return result


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
