import unittest
from click.testing import CliRunner

from qincm import cli
import json

class test_cli(unittest.TestCase):

    test1_output = {'': 0.0,
                 "{'IJ_Velp'}": 411519.8534753271,
                 "{'BR_Duitsland'}": 0.0,
                 "{'BR_Duitsland', 'IJ_Velp'}": 5761542.594600908,
                 "{'WA_St. Andries'}": 2723179.9491901197,
                 "{'WA_Nijmegen'}": 1014876.6571572875,
                 "{'WA_Nijmegen', 'IJ_Velp'}": 1351983.7958166604,
                 "{'WA_Nijmegen', 'BR_Duitsland'}": 35856392.97613928,
                 "{'WA_Nijmegen', 'WA_St. Andries'}": 3056996.134802712,
                 "{'WA_Nijmegen', 'WA_St. Andries', 'IJ_Velp'}": 1191026.5080204958,
                 "{'WA_Nijmegen', 'WA_St. Andries', 'BR_Duitsland'}": 160468285.41541624}

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
