"""Console script for qincm."""
import sys
import click
from qincm import QINCM

@click.command()
def main(args=None):
    """Console script for qincm."""
    click.echo("Replace this message by putting your code into "
               "qincm.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
