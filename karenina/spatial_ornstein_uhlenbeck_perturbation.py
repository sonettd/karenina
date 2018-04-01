#/usr/bin/env python

from __future__ import division

__author__ = "Jesse Zaneveld"
__copyright__ = "Copyright 2016, The Karenina Project"
__credits__ = ["Jesse Zaneveld"]
__license__ = "GPL"
__version__ = "0.0.1-dev"
__maintainer__ = "Jesse Zaneveld"
__email__ = "zaneveld@gmail.com"
__status__ = "Development"

from copy import copy

class Perturbation(object):
    def __init__(self,start,end,params,update_mode="replace",axes=["x","y","z"]):
        """Alter a simulation to impose a press disturbance,
           shifting the microbiome torwards a new configuration

           start --inclusive timepoint to start perturbation.  Note that this is read at the
             Experiment level, not by underlying Process objects.

           end -- inclusive timepoint to end perturbation. Note that this is read at the
             Experiment level, not by underlying Process objects.

           params -- dict of parameter values altered by the disturbance

           mode -- how the perturbation updates parameter values.
                'replace' -- replace old value with new one
                'add' -- add new value to old one
                'multiply' -- multiply the two values

           axes -- axes to which the perturbation applies.  Like Start and End this is a
            'dumb' value, read externally by the Experiment object
        """
        self.Start = start
        self.End = end
        self.Params = params
        self.UpdateMode = update_mode
        self.Axes = axes

    def isActive(self,t):
        return self.Start <= t <= self.End

    def updateParams(self,params):
        if self.UpdateMode == "replace":
            update_f = self.updateByReplacement
        elif self.UpdateMode == "add":
            update_f = self.updateByAddition
        elif self.UpdateMode == "multiply":
            update_f = self.updateByMultiplication
        else:
            raise ValueError("Invalid update mode for perturbation: %s" %self.UpdateMode)

        #If we set new_params = params
        #we modify the input dict, which
        #isn't what we want
        new_params = copy(params)
        for k,v in iter(self.Params.items()):
            new_params[k] = update_f(params[k],v)

        return new_params

    def updateByReplacement(self,curr_param, perturbation_param):
        return perturbation_param

    def updateByAddition(self,curr_param, perturbation_param):
        return curr_param + perturbation_param

    def updateByMultiplication(self,curr_param, perturbation_param):
        return curr_param * perturbation_param
