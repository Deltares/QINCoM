"""Main module."""

from scipy.interpolate import interp1d
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Union, Any, Sequence
import json

class QINCM:
    # Quick Inland Navigation Cost Model

    # Under keel clearance
    ukc = 0.20


    def __init__(self,
                 route_depth_costs_file: Union[str, Path] = None,
                 knelpunt_discharge_depth_file: Union[str, Path] = None,
                 reference: str = None,
                 ):
        """
        Initialise

        :param route_depth_costs_file:
        :param knelpunt_discharge_depth_file:
        :param reference_point_mode: set True if the discharge in the earlier point links to a single discharge
        """

        # Initialise model
        self._read_routes_depth_costs(route_depth_costs_file)
        self._read_knelpunt_discharge_depth(knelpunt_discharge_depth_file, reference=reference)

    def _compute_knelpunt_depth(self, discharges):
        depths = {}
        for k in self.knelpunt_names:
            depths[k] = self.knelpunt_discharge_depth[k](discharges[k])
        depths = pd.DataFrame(data=depths, index=discharges.index)

        # if isinstance(discharges, pd.DataFrame):
        #     depths = {}
        #     for k in self.knelpunt_names:
        #         depths[k] = self.knelpunt_discharge_depth[k](discharges[k])
        #     depths = pd.DataFrame(data=depths, index=discharges.index)
        # else:
        #     depths = {}
        #     for k in self.knelpunt_names:
        #         depths[k] = self.knelpunt_discharge_depth[k](discharges)
        #     depths = pd.DataFrame(data=depths, index=discharges)

        return depths


    def _costs_at_routes_at_discharge(self, discharges: pd.DataFrame) -> pd.DataFrame:
        """
        Compute costs per route per discharge

        param discharges: list of unique discharges. dim1: unique discharges, dim2: knelpunten

        returns: DataFrame (index: routes, columns: discharges)
        """

        depths = self._compute_knelpunt_depth(discharges)

        # For each r (=FrozenList of knelpunten)
        r_costs = {}
        for r in self.routes:

            # Get the limiting depth on the route
            r_depth = depths.reindex(r, axis=1).min(axis=1).fillna(999999)

            # Depth to draught/draft
            r_draughts = r_depth - self.ukc

            # Get costs
            r_costs[r] = self.routes_depth_costs[r](r_draughts)

        costs = pd.DataFrame(r_costs, index=discharges.index)

        return costs

    def _compute_local_discharge(self, discharges):
        if np.ndim(discharges) == 1:
            # Only reference discharge is given, compute local discharge from Q-Q-relation
            Q_ref = discharges

            if isinstance(discharges, pd.Series):
                Q_local = pd.DataFrame(index=discharges.index)
            else:
                Q_local = pd.DataFrame(index=Q_ref)  # The index is only for convenience.

            for k, QQ in self.knelpunt_discharge_distribution.items():
                Q_local[k] = QQ(Q_ref)
        else:
            k_names = self.knelpunt_names

            if isinstance(discharges, pd.DataFrame):
                Q_local = pd.DataFrame(data=discharges, columns=k_names, index=discharges.index)
            else:
                Q_local = pd.DataFrame(data=discharges, columns=k_names)

                Q_local.index = Q_local[self.knelpunt_reference]  # The index is only for convenience.
        return Q_local

    def costs_per_discharge(self, discharges: Union) -> pd.DataFrame:
        """
        Compute total costs per discharge

        param discharges: list of unique discharges. ALso supports timeseries

        returns: Series (index=discharges)
        """
        Q_local = self._compute_local_discharge(discharges)

        costs = self._costs_at_routes_at_discharge(Q_local)
        return costs


    def costs_for_scenario(self, discharges, occurance=None, delta: bool = True):
        """
        Compute total costs in scenario

        param discharge: list of unique discharges
        param occurance: float, or list with for each discharge the number of days. If none, it assumes every discharges occured one day
        """

        # TODO: Discharge may also be a pandas
        if occurance is not None:
            # Validate input
            # if isinstance(occurance, float):
            #     occurance = np.ones(np.shape(discharges)) * occurance
            # assert len(discharges) == len(occurance), 'Input should have same length'

            # Compute total costs
            costs = self.costs_per_discharge(discharges)

            # Compute delta costs
            if delta:
                costs_no_problems = self.costs_per_discharge([99999999])  #TODO: This way is not good for depths that are included as constants...
                costs = costs.subtract(costs_no_problems.values, axis=1)

            costs_occurance = costs.multiply(occurance, axis=0)


        else:
            costs = self.costs_per_discharge(discharges)


            if delta:
                costs_no_problems = self.costs_per_discharge([99999999])
                costs = costs.subtract(costs_no_problems.values, axis=1)

            costs_occurance = costs


        total_costs_per_route = costs_occurance.sum(axis=0)
        # total_costs_per_discharge = costs_occurance.sum(axis=1) # Or per day if that's the index
        # total_costs = total_costs_per_route.sum()

        return total_costs_per_route

    def _read_routes_depth_costs(self, routes_depth_costs_file: Union[str, Path]):
        """
        # Set for each route (combination of knelpunten) the function of [draught]-[response].

        Read json file with following format:

        {
          'routes': {route_index, list of knelpunten per route}
          {list_of_depth, {route_index, costs_per_route_at_depth_per_day}}
        }

        e.g. (truncated notation)

        {
          'routes': {0: [], 1: [A, B], 2: [B,C]},
          2: {0: 1000, 1: 2000, 2: 1500},
          3: {0: 2000, 1: 3000, 2: 1800}
        }

        """
        # Read output
        routes_depth_costs = pd.read_json(routes_depth_costs_file, convert_dates=False, convert_axes=False)
        routes_depth_costs = routes_depth_costs.set_index('routes').T
        routes_depth_costs.index = [float(c) for c in routes_depth_costs.index]
        routes_depth_costs.columns = [frozenset(i) for i in routes_depth_costs.columns]

        self.routes = routes_depth_costs.columns

        # Convert into interpolation function
        depth_costs_functions = {}
        for r in self.routes:
            depth_costs = routes_depth_costs.xs(r, axis=1)
            # Test this also: depth_costs = routes_depth_costs.xs(r)

            depth_costs_function = interp1d(
                x=depth_costs.index,
                y=depth_costs.values,
                kind='linear',
                bounds_error=False,
                fill_value=tuple(depth_costs.values[[0, -1]]),
            )
            depth_costs_functions[r] = depth_costs_function

        self.routes_depth_costs = depth_costs_functions

    def _read_knelpunt_discharge_depth(self, knelpunt_discharge_depth_file: Union[str, Path], reference=None):
        """
        Read json file with for each knelpunt the discharge-depth relation. The discharges for all knelpunten (probably)
        need to be identical

        {
               knelpunt1: {discharge: depth}
               knelpunt2: {discharge: depth}
        }

        e.g.
        {
          'k1': {500: 2.5, 1000: 3, 2000: 4},
          'k2': {200, 5, 800: 6, 1500: 7}
        }

        :param knelpunt_discharge_depth_file: path to json file

        """
        if not isinstance(knelpunt_discharge_depth_file, dict):
            with open(knelpunt_discharge_depth_file) as fin:
                discharge_depth = json.load(fin)
        else:
            discharge_depth = knelpunt_discharge_depth_file

        if reference is None:
            # If not set, take the first
            self.knelpunt_reference = list(discharge_depth.keys())[0]
        else:
            self.knelpunt_reference = reference


        self.knelpunt_names = list(discharge_depth.keys())

        self.knelpunt_discharge_depth = {}
        knelpunt_discharge = {}
        for k, QD in discharge_depth.items():
            Q, D = zip(*QD.items())
            Q = [float(q) for q in Q]
            D = [float(d) for d in D]

            # Make this an interpolation function, incl. extrapolation
            discharge_depth_function = interp1d(
                x=Q,
                y=D,
                kind='linear',
                bounds_error=False,
                fill_value='extrapolate',
            )
            self.knelpunt_discharge_depth[k] = discharge_depth_function
            knelpunt_discharge[k] = Q

        # Make lookup function of discharge at reference, to local discharge
        Q_ref = knelpunt_discharge[self.knelpunt_reference]

        self.knelpunt_discharge_distribution = {}
        for k in discharge_depth:
            Q = knelpunt_discharge[k]

            # Make this an interpolation function, extrapolation=constant
            Qref_Q = interp1d(
                x=Q_ref,
                y=Q,
                kind='linear',
                bounds_error=False,
                fill_value='extrapolate',
            )

            self.knelpunt_discharge_distribution[k] = Qref_Q


    def stats_knelpunten(self, Qmin=500, Qmax=2000):
        """
        for each discharge determine the number of trips that is influenced by the knelpunt (alltrips)
        for each knelpunt show only the trips that are limited by that specific point

        return alltrips, mintrips
        """

        alltrips = {}
        mintrips = {}
        mintrips_increase = {}
        
        routes = self.routes_depth_costs.keys()

        discharge_series = np.linspace(Qmin, Qmax, 100)
        
        # Get discharge per knelpunt
        Q_local = self._compute_local_discharge(discharge_series)
        
        # Get depth per knelpunt and convert to draught by using ukc
        QH = self._compute_knelpunt_depth(Q_local) - self.ukc

        for r in routes:
            # Depth on route
            r_QH = QH[r]
            
            # Get total costs on this route
            depth_for_route = r_QH.min(axis=1).fillna(999)
            costs_for_route = pd.Series(
                data = self.routes_depth_costs[r](depth_for_route),
                index = discharge_series
            )
            costs_for_route_increase = costs_for_route - costs_for_route.iloc[-1]
            
            for k in r:

                depth = r_QH[k].values

                # Get number of affected trips (per waterdepth)
                costs_for_all_passing_trips = self.routes_depth_costs[r](depth)
                alltrips[(r, k)] = pd.Series(
                    data=costs_for_all_passing_trips,
                    index=discharge_series
                )
                
                # Only select those levels where k is the minimum depth on the route
                k_minimal = r_QH.idxmin(axis=1) == k
                mintrips[(r, k)] = costs_for_route.multiply(k_minimal, axis=0)
                mintrips_increase[(r, k)] = costs_for_route_increase.multiply(k_minimal, axis=0)

        alltrips = pd.concat(alltrips)
        mintrips = pd.concat(mintrips)
        mintrips_increase = pd.concat(mintrips_increase)

        alltrips_sum = alltrips.unstack(level=1).sum(axis=0, level=1)
        mintrips_sum = mintrips.unstack(level=1).sum(axis=0, level=1)
        mintrips_increase_sum = mintrips_increase.unstack(level=1).sum(axis=0, level=1)
        return alltrips_sum, mintrips_sum, mintrips_increase_sum

if __name__ == '__main__':

    inputdir = Path('../data')

    M = QINCM(inputdir / 'route_depth_costs.json',
              inputdir / 'knelpunt_discharge_waterdepth.json',
              reference='WA_Nijmegen'
              )

    discharges = np.linspace(500, 3000, 26)

    # print('Costs per route per discharge')
    # a1 = M.costs_per_route_per_discharge(discharges)
    # print(a1.head())

    print('Costs per discharge')
    a2 = M.costs_per_discharge(discharges)
    print(a2.head())

    # Create a random occurance so the total sum is a full year
    occurance = np.random.rand(*discharges.shape)
    occurance *= 365 / occurance.sum()

    print('Costs per year')
    a3 = M.costs_for_scenario(discharges, occurance)
    print(a3)
