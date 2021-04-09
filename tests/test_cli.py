import unittest
from click.testing import CliRunner

from qincm import cli
import json

class test_cli(unittest.TestCase):

    test1_output = {"":0.0,"{'IJ_Velp'}":317320.0089127324,"{'BR_Duitsland'}":0.0,"{'BR_Duitsland', 'IJ_Velp'}":4170689.2257926492,"{'WA_St. Andries'}":2010338.7697387554,"{'WA_Nijmegen'}":742437.8811139499,"{'IJ_Velp', 'WA_Nijmegen'}":992321.9731033762,"{'BR_Duitsland', 'WA_Nijmegen'}":27051328.0352801345,"{'WA_St. Andries', 'WA_Nijmegen'}":2142949.61544467,"{'WA_St. Andries', 'IJ_Velp', 'WA_Nijmegen'}":698496.8471291377,"{'BR_Duitsland', 'WA_St. Andries', 'WA_Nijmegen'}":122862236.0855599493}

    def test_CLI_help(self):
        runner = CliRunner()

        # Test simple help call
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output


    def test_CLI_test1_config(self):
        runner = CliRunner()

        inputfile = r'data/test1.json'
        result = runner.invoke(cli.main, ['--config', inputfile])
        assert result.exit_code == 0

        output = json.loads(result.output)
        self.assertEqual(output["{'WA_Nijmegen'}"], self.test1_output["{'WA_Nijmegen'}"])

    def test_CLI_test1_configstring(self):
        runner = CliRunner()

        inputfile = r'data/test1.json'
        with open(inputfile, 'r') as fin:
            inputfile_data = json.load(fin)
        inputfile_string = json.dumps(inputfile_data)

        result = runner.invoke(cli.main, ['--config', inputfile_string])
        assert result.exit_code == 0

        output = json.loads(result.output)
        self.assertEqual(output["{'WA_Nijmegen'}"], self.test1_output["{'WA_Nijmegen'}"])


    def test_CLI_test1_params(self):
        runner = CliRunner()

        inputfile = r'data/test1.json'
        with open(inputfile, 'r') as fin:
            inputfile_data = json.load(fin)

        discharges = inputfile_data['discharges']
        occurance = inputfile_data['occurance']

        result = runner.invoke(cli.main, [
            '--discharges', json.dumps(discharges),
            '--occurance', json.dumps(occurance)
        ])

        assert result.exit_code == 0

        output = json.loads(result.output)
        self.assertEqual(output["{'WA_Nijmegen'}"], self.test1_output["{'WA_Nijmegen'}"])


if __name__ == '__main__':
    unittest.main()
