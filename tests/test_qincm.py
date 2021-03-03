#!/usr/bin/env python

"""Tests for `qincm` package."""

import unittest

from pathlib import Path
import pandas as pd
import numpy as np

from qincm.qincm import QINCM
# from qincm import cli

class test_pyFIS(unittest.TestCase):
    """Tests for `klimaatbestendige_netwerken` package."""

    export_dir = Path('export_pyFIS')


    def setUp(self):
        """Set up test fixtures"""
        inputdir = Path('../data')
        route_depth_costs_file = inputdir / 'route_depth_costs.json'
        knelpunt_discharge_depth_file = inputdir / 'knelpunt_discharge_waterdepth.json'

        self.M = QINCM(
            route_depth_costs_file,
            knelpunt_discharge_depth_file,
            reference='WA_Nijmegen'
        )

        # if not self.export_dir.exists():
        #     self.export_dir.mkdir()

    def test_000_global(self):
        # Test global discharge
        discharges = np.linspace(500, 3000, 26)
        a = self.M.costs_per_discharge(discharges)

    def test_000_local(self):
        # Test local discharge
        k = self.M.knelpunt_names

        np.random.seed(13)
        discharges = np.random.rand(20, len(k)) * 3000
        a = self.M.costs_per_discharge(discharges)



    def test_001_global_scenario(self):
        # Create a random occurance so the total sum is a full year
        discharges = np.linspace(500, 3000, 26)

        np.random.seed(13)
        occurance = np.random.rand(*discharges.shape)
        occurance *= 365 / occurance.sum()

        a = self.M.costs_for_scenario(discharges, occurance)


    def test_001_local_scenario(self):
        k = self.M.knelpunt_names

        # Create a random occurance so the total sum is a full year
        np.random.seed(13)
        discharge_levels = 20
        discharges = np.random.rand(discharge_levels, len(k)) * 3000

        occurance = np.random.rand(discharge_levels)
        occurance *= 365 / occurance.sum()

        a = self.M.costs_for_scenario(discharges, occurance)


    def test_002_global_scenario_timeseries(self):
        discharges = np.linspace(500, 3000, 365)
        dates = pd.date_range('2000-01-01', periods=len(discharges), freq='1D')

        timeseries = pd.Series(index=dates, data=discharges)

        a = self.M.costs_for_scenario(timeseries)

