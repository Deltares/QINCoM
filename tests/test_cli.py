import unittest
from click.testing import CliRunner

from qincm import cli

class test_cli(unittest.TestCase):

    def test_CLI_help(self):
        runner = CliRunner()

        # Test simple help call
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output


    def test_CLI_test1(self):
        runner = CliRunner()

        inputfile = r'data/test1.json'
        result = runner.invoke(cli.main, inputfile)
        assert result.exit_code == 0

        #TODO: Validate data??


if __name__ == '__main__':
    unittest.main()
