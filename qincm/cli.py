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

#TODO: Better help
@click.command()
@click.argument('input', type=click.File('rb'))
def main(input):

    # Allow both reading a json as inputstring and input as filepath
    if not isinstance(input, dict):
        logger.info(f'Loading configuration: {input.name}')

        file_mode = True
        with open(input.name) as fin:
            input_data = json.load(fin)
    else:
        # TODO: Test this mode. Does it need conversion?
        file_mode = False
        input_data = input.name

    logger.debug(input_data)

    logger.info('Running configuration')

    M = QINCM(
        route_depth_costs_file=input_data['route_depth_costs_file'],
        knelpunt_discharge_depth_file=input_data['knelpunt_discharge_depth_file'],
        reference=input_data['reference']
    )

    if input_data['mode'] == 'scenario':
        result = M.costs_for_scenario(
            discharges=input_data['discharges'],
            occurance=input_data['occurance']
        )

    else:
        NotImplementedError()
        result = None

    # Make results better readable
    result_pretty = result.copy()
    result_pretty.index = [str(i).replace('frozenset(', '').replace(')', '') for i in result_pretty.index]
    result_pretty = result_pretty.to_json()

    logger.debug('\n' + result_pretty)

    # If we read a file, than also output as file
    if file_mode:
        outputfile = str(input.name).replace('.json', '_output.json')
        with open(outputfile, 'w') as fout:
            fout.write(result_pretty)

    return result


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
