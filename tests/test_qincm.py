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


    def setUp(self):
        """Set up test fixtures"""
        inputdir = Path('data/testmodel_4p')
        route_depth_costs_file = inputdir / 'route_depth_costs.json'
        knelpunt_discharge_depth_file = inputdir / 'knelpunt_discharge_waterdepth.json'

        self.M = QINCM(
            route_depth_costs_file,
            knelpunt_discharge_depth_file,
            reference='WA_Nijmegen'
        )



    def test_000_global(self):
        # Test global discharge
        discharges = np.linspace(500, 3000, 26)
        a = self.M.costs_per_discharge(discharges)

        self.assertAlmostEqual(a.loc[2000].sum() / a.loc[500].sum(), 0.54731428, 5)

    def test_000_local(self):
        # Test local discharge
        k = self.M.knelpunt_names

        np.random.seed(13)
        discharges = np.random.rand(20, len(k)) * 3000
        a = self.M.costs_per_discharge(discharges)

        self.assertAlmostEqual(a.iloc[0].sum() / a.iloc[-1].sum(), 0.49930185, 5)


    def test_001_global_scenario(self):
        # Create a random occurance so the total sum is a full year
        discharges = np.linspace(500, 3000, 26)

        np.random.seed(13)
        occurance = np.random.rand(*discharges.shape)
        occurance *= 365 / occurance.sum()

        a = self.M.costs_for_scenario(discharges, occurance)

        self.assertAlmostEqual(a.sum(), 211835803.8732196, 5)

    def test_001_local_scenario(self):
        k = self.M.knelpunt_names

        # Create a random occurance so the total sum is a full year
        np.random.seed(13)
        discharge_levels = 20
        discharges = np.random.rand(discharge_levels, len(k)) * 3000

        occurance = np.random.rand(discharge_levels)
        occurance *= 365 / occurance.sum()

        a = self.M.costs_for_scenario(discharges, occurance)

        self.assertAlmostEqual(a.sum(),  766789671.5229554, 5)

    def test_002_global_scenario_timeseries(self):
        discharges = np.linspace(500, 3000, 365)
        dates = pd.date_range('2000-01-01', periods=len(discharges), freq='1D')

        timeseries = pd.Series(index=dates, data=discharges)

        a = self.M.costs_for_scenario(timeseries)

        self.assertAlmostEqual(a.sum(), 126109151.65011567, 5)

    def test_003_stats(self):
        alltrips_sum, mintrips_sum, mintrips_increase_sum = self.M.stats_knelpunten()
        self.assertAlmostEqual(alltrips_sum.loc[500, 'WA_Nijmegen'], 8400926.746089742, 5)
        self.assertAlmostEqual(mintrips_sum.loc[500, 'WA_Nijmegen'], 8400926.746089742, 5)
        self.assertAlmostEqual(mintrips_increase_sum.loc[500, 'WA_Nijmegen'], 5046180.066089741, 5)
