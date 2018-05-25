#!/usr/bin/env python

__author__ = "Jesse Zaneveld"
__copyright__ = "Copyright 2011-2013, The PICRUSt Project"
__credits__ = ["Jesse Zaneveld"]
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Jesse Zaneveld"
__email__ = "zaneveld@gmail.com"
__status__ = "Development"

import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../karenina'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import unittest
from warnings import catch_warnings
from karenina.experiment import Experiment
from karenina.individual import Individual
from karenina.perturbation import Perturbation
import numpy.testing as npt
from copy import copy

"""
Tests for spatial_ornstein_uhlenbeck.py
"""

class TestExperiment(unittest.TestCase):
    # TODO: Print statements for test status?

    def setUp(self):
        """
        Creates default local variables for use in the tests
        """
        self.TreatmentNames = ['control','destabilizing_treatment']
        self.Treatments = [{'treatment_name': 'control'}, {'treatment_name': 'destabilizing_treatment'}]
        self.BaseParams = {'lambda': 0.2, 'delta': 0.25, 'interindividual_variation': 0.01}
        self.NIndividuals = [35,35]
        self.n_timepoints = 10
        self.treatment_params = [[],[]]
        self.interindividual_variation = 0.01

        self.exp = Experiment(self.TreatmentNames, self.NIndividuals, self.n_timepoints, self.BaseParams,
                         self.treatment_params, self.interindividual_variation)


    def test_check_variable_specified_per_treatment(self):
        """
        Tests that the NIndividuals is equal to the number of Treatment Names.
        Introduces an extra treatment name, and asserts the thrown ValueError
        """
        self.exp.check_variable_specified_per_treatment(self.NIndividuals)
        self.TreatmentNames.append('Error')
        with self.assertRaises(ValueError):
            self.exp = Experiment(self.TreatmentNames, self.NIndividuals, self.n_timepoints, self.BaseParams,
                                  self.treatment_params, self.interindividual_variation)
            self.exp.check_variable_specified_per_treatment(self.NIndividuals)


    def test_check_n_timepoints_is_int(self):
        """
        Tests that the n_timepoints is of the int datatype.
        Introduces a new variable for n_timepoints as a list, asserts the thrown ValueError
        """
        self.exp.check_n_timepoints_is_int(self.n_timepoints)
        self.n_timepoints = [10]
        with self.assertRaises(ValueError):
            self.exp = Experiment(self.TreatmentNames, self.NIndividuals, self.n_timepoints, self.BaseParams,
                                  self.treatment_params, self.interindividual_variation)
            self.exp.check_n_timepoints_is_int(self.n_timepoints)


    def test_simulate_timesteps(self):
        # Can be changed to determine expected output of 700 timesteps.
        # (Not certain why there are 700 data points)
        # Should simulate_timestep be tested or benchmarked?

        """
        Tests that the timesteps are successfully completed, populating the Data variable with 700 new entries.
        """
        assert len(self.exp.Data) == 1
        self.exp.simulate_timesteps(0,self.n_timepoints)
        assert len(self.exp.Data) == 701


    def test_writeToMovieFile(self):
        """
        Tests that the output movie file is successfully written, then removes the file.
        """
        # Travis-CI Uses Xwindows backend, this prevents that issue.
        import matplotlib
        matplotlib.use('Agg')

        self.output_folder = "./"
        Experiment.write_to_movie_file(self.exp,
                                       self.output_folder)
        assert os.path.exists("./simulation_video.mp4")
        os.remove("./simulation_video.mp4")

if __name__ == '__main__':
    unittest.main()


