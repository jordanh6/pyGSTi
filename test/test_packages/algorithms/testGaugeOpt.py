import unittest
import pygsti
from pygsti.construction import std1Q_XYI as std
from pygsti.tools.basis import Basis

import numpy as np
from scipy import polyfit
import sys, os

from ..testutils import BaseTestCase, compare_files, temp_files
from ..algorithms.basecase import AlgorithmsBase

class TestCoreMethods(AlgorithmsBase):
    def test_gaugeopt_and_contract(self):
        ds = self.ds_lgst
        #pygsti.construction.generate_fake_data(self.datagen_gateset, self.lgstStrings,
        #                                            nSamples=10000,sampleError='binomial', seed=100)

        gs_lgst = pygsti.do_lgst(ds, self.specs, self.gateset, svdTruncateTo=4, verbosity=0)

        #Gauge Opt to Target
        gs_lgst_target     = self.runSilent(pygsti.optimize_gauge, gs_lgst,"target",targetGateset=self.gateset,verbosity=10) #DEPRECATED
        gs_lgst_target     = self.runSilent(pygsti.gaugeopt_to_target, gs_lgst, self.gateset, verbosity=10, checkJac=True)

        gs_clgst_cp    = self.runSilent(pygsti.contract, gs_lgst_target, "CP",verbosity=10, tol=10.0, useDirectCP=False) #non-direct CP contraction

        #Gauge Opt to Target using non-frobenius metrics
        gs_lgst_targetAlt  = self.runSilent(pygsti.optimize_gauge, gs_lgst_target,"target",targetGateset=self.gateset,
                                            targetGatesMetric='fidelity', verbosity=10) #DEPRECATED
        gs_lgst_targetAlt  = self.runSilent(pygsti.gaugeopt_to_target, gs_lgst_target, self.gateset,
                                            gatesMetric='fidelity', verbosity=10, checkJac=True)

        gs_lgst_targetAlt  = self.runSilent(pygsti.optimize_gauge, gs_lgst_target,"target",targetGateset=self.gateset,
                                            targetGatesMetric='tracedist', verbosity=10) #DEPRECATED
        gs_lgst_targetAlt  = self.runSilent(pygsti.gaugeopt_to_target, gs_lgst_target, self.gateset,
                                            gatesMetric='tracedist', verbosity=10, checkJac=True)

        gs_lgst_targetAlt  = self.runSilent(pygsti.optimize_gauge, gs_lgst_target,"target",targetGateset=self.gateset,
                                            targetSpamMetric='fidelity', verbosity=10) #DEPRECATED
        gs_lgst_targetAlt  = self.runSilent(pygsti.gaugeopt_to_target, gs_lgst_target, self.gateset,
                                            spamMetric='fidelity', verbosity=10, checkJac=True)

        gs_lgst_targetAlt  = self.runSilent(pygsti.optimize_gauge, gs_lgst_target,"target",targetGateset=self.gateset,
                                            targetSpamMetric='tracedist', verbosity=10) #DEPRECATED
        gs_lgst_targetAlt  = self.runSilent(pygsti.gaugeopt_to_target, gs_lgst_target, self.gateset,
                                            spamMetric='tracedist', verbosity=10, checkJac=True)


        with self.assertRaises(ValueError):
            self.runSilent(pygsti.optimize_gauge, gs_lgst_target,"target",targetGateset=self.gateset,
                           targetGatesMetric='foobar', verbosity=10) #bad targetGatesMetric #DEPRECATED
        with self.assertRaises(ValueError):
            self.runSilent(pygsti.gaugeopt_to_target, gs_lgst_target, self.gateset,
                           gatesMetric='foobar', verbosity=10) #bad gatesMetric

        with self.assertRaises(ValueError):
            self.runSilent(pygsti.optimize_gauge, gs_lgst_target,"target",targetGateset=self.gateset,
                           targetSpamMetric='foobar', verbosity=10) #bad targetSpamMetric #DEPRECATED
        with self.assertRaises(ValueError):
            self.runSilent(pygsti.gaugeopt_to_target, gs_lgst_target, self.gateset,
                           spamMetric='foobar', verbosity=10) #bad spamMetric

        with self.assertRaises(ValueError):
            self.runSilent(pygsti.optimize_gauge, gs_lgst_target,"foobar",targetGateset=self.gateset,
                           targetSpamMetric='target', verbosity=10) #bad toGetTo #DEPRECATED

        #Contractions
        gs_clgst_tp    = self.runSilent(pygsti.contract, gs_lgst_target, "TP",verbosity=10, tol=10.0)
        gs_clgst_cp    = self.runSilent(pygsti.contract, gs_lgst_target, "CP",verbosity=10, tol=10.0)
        gs_clgst_cptp  = self.runSilent(pygsti.contract, gs_lgst_target, "CPTP",verbosity=10, tol=10.0)
        gs_clgst_cptp2 = self.runSilent(pygsti.contract, gs_lgst_target, "CPTP",verbosity=10, useDirectCP=False)
        gs_clgst_cptp3 = self.runSilent(pygsti.contract, gs_lgst_target, "CPTP",verbosity=10, tol=10.0, maxiter=0)
        gs_clgst_xp    = self.runSilent(pygsti.contract, gs_lgst_target, "XP", ds,verbosity=10, tol=10.0)
        gs_clgst_xptp  = self.runSilent(pygsti.contract, gs_lgst_target, "XPTP", ds,verbosity=10, tol=10.0)
        gs_clgst_vsp   = self.runSilent(pygsti.contract, gs_lgst_target, "vSPAM",verbosity=10, tol=10.0)
        gs_clgst_none  = self.runSilent(pygsti.contract, gs_lgst_target, "nothing",verbosity=10, tol=10.0)

          #test bad effect vector cases
        gs_bad_effect = gs_lgst_target.copy()
        gs_bad_effect.effects['E0'] = [100.0,0,0,0] # E eigvals all > 1.0
        self.runSilent(pygsti.contract, gs_bad_effect, "vSPAM",verbosity=10, tol=10.0)
        gs_bad_effect.effects['E0'] = [-100.0,0,0,0] # E eigvals all < 0
        self.runSilent(pygsti.contract, gs_bad_effect, "vSPAM",verbosity=10, tol=10.0)

        with self.assertRaises(ValueError):
            self.runSilent(pygsti.contract, gs_lgst_target, "foobar",verbosity=10, tol=10.0) #bad toWhat



        #More gauge optimizations
        TP_gauge_group = pygsti.obj.TPGaugeGroup(gs_lgst.dim)
        gs_lgst_target_cp  = self.runSilent(pygsti.optimize_gauge, gs_clgst_cptp,"target",targetGateset=self.gateset,
                                            constrainToCP=True,constrainToTP=True,constrainToValidSpam=True,verbosity=10) #DEPRECATED
        gs_lgst_target_cp  = self.runSilent(pygsti.gaugeopt_to_target, gs_clgst_cptp, self.gateset, 
                                            CPpenalty=1.0, gauge_group=TP_gauge_group, verbosity=10, checkJac=True)

        gs_lgst.basis = Basis("gm",2) #so CPTP optimizations can work on gs_lgst
        gs_lgst_cptp       = self.runSilent(pygsti.optimize_gauge, gs_lgst,"CPTP",verbosity=10) #DEPRECATED
        gs_lgst_cptp       = self.runSilent(pygsti.gaugeopt_to_target, gs_lgst, None,
                                            CPpenalty=1.0, TPpenalty=1.0, validSpamPenalty=1.0, verbosity=10, checkJac=True)

        gs_lgst_cptp_tp    = self.runSilent(pygsti.optimize_gauge, gs_lgst,"CPTP",verbosity=10, constrainToTP=True) #DEPRECATED
        gs_lgst_cptp_tp    = self.runSilent(pygsti.gaugeopt_to_target, gs_lgst, None,
                                            CPpenalty=1.0, TPpenalty=1.0, validSpamPenalty=1.0, gauge_group=TP_gauge_group, verbosity=10, checkJac=True) #no point? (remove?)

        gs_lgst_tp         = self.runSilent(pygsti.optimize_gauge, gs_lgst,"TP",verbosity=10) #DEPRECATED
        gs_lgst_tp         = self.runSilent(pygsti.gaugeopt_to_target, gs_lgst, None,
                                            TPpenalty=1.0, validSpamPenalty=1.0, verbosity=10, checkJac=True)

        gs_lgst_tptarget   = self.runSilent(pygsti.optimize_gauge, gs_lgst,"TP and target",targetGateset=self.gateset,verbosity=10) #DEPRECATED
        gs_lgst_tptarget   = self.runSilent(pygsti.gaugeopt_to_target, gs_lgst, self.gateset,
                                            TPpenalty=1.0, validSpamPenalty=1.0, verbosity=10, checkJac=True)

        gs_lgst_cptptarget = self.runSilent(pygsti.optimize_gauge, gs_lgst,"CPTP and target",targetGateset=self.gateset,verbosity=10) #DEPRECATED
        gs_lgst_cptptarget = self.runSilent(pygsti.gaugeopt_to_target, gs_lgst, self.gateset,
                                            CPpenalty=1.0, TPpenalty=1.0, validSpamPenalty=1.0, verbosity=10, checkJac=True)

        gs_lgst_cptptarget2= self.runSilent(pygsti.optimize_gauge, gs_lgst,"CPTP and target",targetGateset=self.gateset,
                                            verbosity=10, constrainToTP=True) #DEPRECATED
        gs_lgst_cptptarget2= self.runSilent(pygsti.gaugeopt_to_target, gs_lgst, self.gateset,
                                            CPpenalty=1.0, TPpenalty=1.0, validSpamPenalty=1.0, gauge_group=TP_gauge_group, verbosity=10, checkJac=True) #no point? (remove?)

        gs_lgst_cd         = self.runSilent(pygsti.optimize_gauge, gs_lgst,"Completely Depolarized",targetGateset=self.gateset,verbosity=10) #DEPRECATED

        #TODO: check output lies in space desired

        # big kick that should land it outside XP, TP, etc, so contraction
        # routines are more tested
        gs_bigkick = gs_lgst_target.kick(absmag=1.0)
        gs_badspam = gs_bigkick.copy()
        gs_badspam.effects['E0'] =  np.array( [[2],[0],[0],[4]], 'd') #set a bad evec so vSPAM has to work...

        gs_clgst_tp    = self.runSilent(pygsti.contract,gs_bigkick, "TP", verbosity=10, tol=10.0)
        gs_clgst_cp    = self.runSilent(pygsti.contract,gs_bigkick, "CP", verbosity=10, tol=10.0)
        gs_clgst_cptp  = self.runSilent(pygsti.contract,gs_bigkick, "CPTP", verbosity=10, tol=10.0)
        gs_clgst_xp    = self.runSilent(pygsti.contract,gs_bigkick, "XP", ds, verbosity=10, tol=10.0)
        gs_clgst_xptp  = self.runSilent(pygsti.contract,gs_bigkick, "XPTP", ds, verbosity=10, tol=10.0)
        gs_clgst_vsp   = self.runSilent(pygsti.contract,gs_badspam, "vSPAM", verbosity=10, tol=10.0)
        gs_clgst_none  = self.runSilent(pygsti.contract,gs_bigkick, "nothing", verbosity=10, tol=10.0)

        #TODO: check output lies in space desired

        #Check Errors
        with self.assertRaises(ValueError):
            pygsti.optimize_gauge(gs_lgst,"FooBar",verbosity=0) # bad toGetTo argument

        with self.assertRaises(ValueError):
            pygsti.contract(gs_lgst_target, "FooBar",verbosity=0) # bad toWhat argument

        # No longer raise value error for failure to contract...
        #with self.assertRaises(ValueError):
        #    self.runSilent(pygsti.contract,gs_bigkick, "CP", verbosity=10,
        #                   maxiter=1) # fail to contract to CP


if __name__ == "__main__":
    unittest.main(verbosity=2)
