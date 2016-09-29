#!/usr/bin/env python

__author__ = "Jesse Zaneveld"
__copyright__ = "Copyright 2011-2013, The PICRUSt Project"
__credits__ = ["Jesse Zaneveld"]
__license__ = "GPL"
__version__ = "1.0.0-dev"
__maintainer__ = "Jesse Zaneveld"
__email__ = "zaneveld@gmail.com"
__status__ = "Development"

import unittest 
from warnings import catch_warnings
from karenina.spatial_ornstein_uhlenbeck  import Process,Individual,Experiment
import numpy.testing as npt
  
"""
Tests for spatial_ornstein_uhlenbeck.py
"""



class TestProcess(unittest.TestCase):
    """Tests of the Process class"""

    def setUp(self):
        self.TestProcesses ={}
        #Note that each Process is 1d
        
        #typical parameters
        start_coord = 0.0
        attractor_pos = 0.0
        history = None
        process_type = "Ornstein-Uhlenbeck"
    
        #specific parameters

        #First let's generate a stable process that has lambda = 1
        #This should mean that the process ALWAYS revers to its attractor
        #at every timestep.  So delta shouldn't matter.  
        params = {"lambda":1.0,"delta":0.0,"mu":attractor_pos}
        stable_process = Process(start_coord,attractor_pos,\
          motion=process_type,params=params)
        self.TestProcesses["stable_process"]=stable_process

    def test_stable_process_update(self):
        """A stable OU process (lambda =1) is invariable in position"""
        
        stable_process = self.TestProcesses["stable_process"]
        start_coord = stable_process.Coord
        a_long_time = 1000
        for i in range(a_long_time):
            stable_process.update(1.0)
        end_coord = stable_process.Coord
        npt.assert_almost_equal(start_coord,end_coord)


         
        
if __name__ == '__main__':
    unittest.main()


