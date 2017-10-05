from __future__ import division, print_function, absolute_import, unicode_literals
#*****************************************************************
#    pyGSTi 0.9:  Copyright 2015 Sandia Corporation
#    This Software is released under the GPL license detailed
#    in the file "license.txt" in the top-level pyGSTi directory
#*****************************************************************
"""
Functions which compute named quantities for GateSets and Datasets.

Named quantities as well as their confidence-region error bars are
 computed by the functions in this module. These quantities are
 used primarily in reports, so we refer to these quantities as
 "reportables".
"""
import numpy as _np
import scipy.linalg as _spl
import warnings as _warnings
from collections import OrderedDict as _OrderedDict

from .. import tools as _tools
from .. import algorithms as _alg
from ..objects import smart_cached as _smart_cached
from ..objects.reportableqty import ReportableQty
from ..objects import gatesetfunction as _gsf

import functools as _functools

from pprint import pprint

FINITE_DIFF_EPS = 1e-7

def _projectToValidProb(p, tol=1e-9):
    if p < tol: return tol
    if p > 1-tol: return 1-tol
    return p

def _make_reportable_qty_or_dict(f0, df=None, nonMarkovianEBs=False):
    """ Just adds special processing with f0 is a dict, where we 
        return a dict or ReportableQtys rather than a single
        ReportableQty of the dict.
    """
    if isinstance(f0,dict):
        #special processing for dict -> df is dict of error bars
        # and we return a dict of ReportableQtys
        if df:
            return { ky: ReportableQty(f0[ky], df[ky], nonMarkovianEBs) for ky in f0 }
        else:
            return { ky: ReportableQty(f0[ky], None, False) for ky in f0 }
    else:
        return ReportableQty(f0, df, nonMarkovianEBs)

def evaluate(gatesetFn, cri=None, verbosity=0):
    if gatesetFn is None: # so you can set fn to None when they're missing (e.g. diamond norm)
        return ReportableQty(_np.nan)
    
    if cri:
        nmEBs = bool(cri.get_errobar_type() == "non-markovian")
        df, f0 =  cri.get_fn_confidence_interval(
            gatesetFn, returnFnVal=True,
            verbosity=verbosity)
        return _make_reportable_qty_or_dict(f0, df, nmEBs)
    else:
        return _make_reportable_qty_or_dict( gatesetFn.evaluate(gatesetFn.base_gateset) )


## ------------------------------------------------------------- OLD
#
#def _getGateQuantity(fnOfGate, gateset, gateLabel, eps, confidenceRegionInfo, verbosity=0):
#    """ For constructing a ReportableQty from a function of a gate. """
#
#    if confidenceRegionInfo is None: # No Error bars
#        return ReportableQty(fnOfGate(gateset.gates[gateLabel]))
#
#    # make sure the gateset we're given is the one used to generate the confidence region
#    if(gateset.frobeniusdist(confidenceRegionInfo.get_gateset()) > 1e-6):
#        raise ValueError("Prep quantity confidence region is being requested for " +
#                         "a different gateset than the given confidenceRegionInfo")
#
#    df, f0 = confidenceRegionInfo.get_gate_fn_confidence_interval(fnOfGate, gateLabel,
#                                                              eps, returnFnVal=True,
#                                                              verbosity=verbosity)
#    return ReportableQty(f0,df)
#
#def _getPrepQuantity(fnOfPrep, gateset, prepLabel, eps, confidenceRegionInfo, verbosity=0):
#    """ For constructing a ReportableQty from a function of a state preparation. """
#
#    if confidenceRegionInfo is None: # No Error bars
#        return ReportableQty(fnOfPrep(gateset.preps[prepLabel]))
#
#    # make sure the gateset we're given is the one used to generate the confidence region
#    if(gateset.frobeniusdist(confidenceRegionInfo.get_gateset()) > 1e-6):
#        raise ValueError("Gate quantity confidence region is being requested for " +
#                         "a different gateset than the given confidenceRegionInfo")
#
#    df, f0 = confidenceRegionInfo.get_prep_fn_confidence_interval(fnOfPrep, prepLabel,
#                                                              eps, returnFnVal=True,
#                                                              verbosity=verbosity)
#    return ReportableQty(f0,df)
#
#def _getEffectQuantity(fnOfEffect, gateset, effectLabel, eps, confidenceRegionInfo, verbosity=0):
#    """ For constructing a ReportableQty from a function of a POVM effect. """
#
#    if confidenceRegionInfo is None: # No Error bars
#        return ReportableQty(fnOfEffect(gateset.effects[effectLabel]))
#
#    # make sure the gateset we're given is the one used to generate the confidence region
#    if(gateset.frobeniusdist(confidenceRegionInfo.get_gateset()) > 1e-6):
#        raise ValueError("Effect quantity confidence region is being requested for " +
#                         "a different gateset than the given confidenceRegionInfo")
#
#    df, f0 = confidenceRegionInfo.get_effect_fn_confidence_interval(
#        fnOfEffect, effectLabel, eps, returnFnVal=True, verbosity=verbosity)
#    return ReportableQty(f0,df)
#
#def _getGateSetQuantity(fnOfGateSet, gateset, eps, confidenceRegionInfo, verbosity=0):
#    """ For constructing a ReportableQty from a function of a gate. """
#
#    if confidenceRegionInfo is None: # No Error bars
#        return ReportableQty(fnOfGateSet(gateset))
#
#    # make sure the gateset we're given is the one used to generate the confidence region
#    if(gateset.frobeniusdist(confidenceRegionInfo.get_gateset()) > 1e-6):
#        raise ValueError("GateSet quantity confidence region is being requested for " +
#                         "a different gateset than the given confidenceRegionInfo")
#
#    df, f0 = confidenceRegionInfo.get_gateset_fn_confidence_interval(
#        fnOfGateSet, eps, returnFnVal=True, verbosity=verbosity)
#
#    return ReportableQty(f0,df)
#
#@_tools.parameterized # This decorator takes arguments:
#def spam_quantity(fnOfSpamVecs, eps=FINITE_DIFF_EPS, verbosity=0):
#    """ For constructing a ReportableQty from a function of a spam vectors."""
#    # Since smart_cached is unparameterized, it needs no following parens
#    @_smart_cached # nested decorators = decOut(decIn(f(x)))
#    @_functools.wraps(fnOfSpamVecs) # Retain metadata of wrapped function
#    def compute_quantity(gateset, confidenceRegionInfo=None):
#        if confidenceRegionInfo is None: # No Error bars
#            f0 = fnOfSpamVecs(gateset.get_preps(), gateset.get_effects())
#            return _make_reportable_qty_or_dict(f0)
#
#        # make sure the gateset we're given is the one used to generate the confidence region
#        if(gateset.frobeniusdist(confidenceRegionInfo.get_gateset()) > 1e-6):
#            raise ValueError("Spam quantity confidence region is being requested for " +
#                             "a different gateset than the given confidenceRegionInfo")
#
#        nmEBs = bool(confidenceRegionInfo.get_errobar_type() == "non-markovian")
#        df, f0 = confidenceRegionInfo.get_spam_fn_confidence_interval(fnOfSpamVecs,
#                                                                  eps, returnFnVal=True,
#                                                                  verbosity=verbosity)
#        return _make_reportable_qty_or_dict(f0, df, nmEBs)
#
#    return compute_quantity
#
#@_tools.parameterized
#def gate_quantity(fnOfGate, eps=FINITE_DIFF_EPS, verbosity=0):
#    """ For constructing a ReportableQty from a function of a gate. """
#    # Since smart_cached is unparameterized, it needs no following parens
#    @_smart_cached # nested decorators = decOut(decIn(f(x)))
#    @_functools.wraps(fnOfGate) # Retain metadata of wrapped function
#    def compute_quantity(gateLabel, gateset, confidenceRegionInfo=None):
#        mxBasis = gateset.basis
#        if confidenceRegionInfo is None: # No Error bars
#            f0 = fnOfGate(gateset.gates[gateLabel], mxBasis)
#            return _make_reportable_qty_or_dict(f0)
#
#        # make sure the gateset we're given is the one used to generate the confidence region
#        if(gateset.frobeniusdist(confidenceRegionInfo.get_gateset()) > 1e-6):
#            raise ValueError("Prep quantity confidence region is being requested for " +
#                             "a different gateset than the given confidenceRegionInfo")
#
#        nmEBs = bool(confidenceRegionInfo.get_errobar_type() == "non-markovian")
#        curriedFnOfGate = _functools.partial(fnOfGate, mxBasis=mxBasis)
#        df, f0 = confidenceRegionInfo.get_gate_fn_confidence_interval(curriedFnOfGate, gateLabel,
#                                                                  eps, returnFnVal=True,
#                                                                  verbosity=verbosity)
#        return _make_reportable_qty_or_dict(f0, df, nmEBs)
#
#    return compute_quantity
#
#
#@_tools.parameterized
#def gateset_quantity(fnOfGateSet, eps=FINITE_DIFF_EPS, verbosity=0):
#    """ For constructing a ReportableQty from a function of a gateset. """
#    # Since smart_cached is unparameterized, it needs no following parens
#    @_smart_cached # nested decorators = decOut(decIn(f(x)))
#    @_functools.wraps(fnOfGateSet) 
#    def compute_quantity(gateset, confidenceRegionInfo=None):
#        if confidenceRegionInfo is None: # No Error bars
#            return _make_reportable_qty_or_dict( fnOfGateSet(gateset) )
#        # make sure the gateset we're given is the one used to generate the confidence region
#        if(gateset.frobeniusdist(confidenceRegionInfo.get_gateset()) > 1e-6):
#            raise ValueError("GateSet quantity confidence region is being requested for " +
#                             "a different gateset than the given confidenceRegionInfo")
#        nmEBs = bool(confidenceRegionInfo.get_errobar_type() == "non-markovian")
#        df, f0 = confidenceRegionInfo.get_gateset_fn_confidence_interval(
#            fnOfGateSet, eps, returnFnVal=True, verbosity=verbosity)
#
#        return _make_reportable_qty_or_dict(f0, df, nmEBs)
#
#    return compute_quantity
#
#
#@_tools.parameterized
#def gatestring_quantity(fnOfGatestringAndSet, eps=FINITE_DIFF_EPS, verbosity=0):
#    """ For constructing a ReportableQty from a function of a GateString and a GateSet. """
#    # Since smart_cached is unparameterized, it needs no following parens
#    @_smart_cached # nested decorators = decOut(decIn(f(x)))
#    @_functools.wraps(fnOfGatestringAndSet)
#    def compute_quantity(gatestring, gateset, confidenceRegionInfo=None):
#        if confidenceRegionInfo is None: # No Error bars
#            return _make_reportable_qty_or_dict( fnOfGatestringAndSet(gatestring, gateset) )
#        # make sure the gateset we're given is the one used to generate the confidence region
#        if(gateset.frobeniusdist(confidenceRegionInfo.get_gateset()) > 1e-6):
#            raise ValueError("GateSet quantity confidence region is being requested for " +
#                             "a different gateset than the given confidenceRegionInfo")
#        nmEBs = bool(confidenceRegionInfo.get_errobar_type() == "non-markovian")
#        df, f0 = confidenceRegionInfo.get_gatestring_fn_confidence_interval(
#            fnOfGatestringAndSet, gatestring, eps, returnFnVal=True, verbosity=verbosity)
#
#        return _make_reportable_qty_or_dict(f0, df, nmEBs)
#
#    return compute_quantity
#
#@_tools.parameterized
#def gatestrings_quantity(fnOfGatestringAndSets, eps=FINITE_DIFF_EPS, verbosity=0):
#    """ For constructing a ReportableQty from a function of a GateString and two GateSets. """
#    # Since smart_cached is unparameterized, it needs no following parens
#    @_smart_cached # nested decorators = decOut(decIn(f(x)))
#    @_functools.wraps(fnOfGatestringAndSets)
#    def compute_quantity(gatestring, gatesetA, gatesetB, confidenceRegionInfo=None):
#        if confidenceRegionInfo is None: # No Error bars
#            return _make_reportable_qty_or_dict( fnOfGatestringAndSets(gatestring, gatesetA, gatesetB) )
#        # make sure the gateset we're given is the one used to generate the confidence region
#        if(gatesetA.frobeniusdist(confidenceRegionInfo.get_gateset()) > 1e-6):
#            raise ValueError("GateSet quantity confidence region is being requested for " +
#                             "a different gateset than the given confidenceRegionInfo")
#        nmEBs = bool(confidenceRegionInfo.get_errobar_type() == "non-markovian")
#        curriedFnOfGateString = _functools.partial(fnOfGatestringAndSets, gatesetB=gatesetB)
#        df, f0 = confidenceRegionInfo.get_gatestring_fn_confidence_interval(
#            curriedFnOfGateString, gatestring, eps, returnFnVal=True, verbosity=verbosity)
#
#        return _make_reportable_qty_or_dict(f0, df, nmEBs)
#
#    return compute_quantity
#
#
#@_tools.parameterized
#def gatesets_quantity(fnOfGateSets, eps=FINITE_DIFF_EPS, verbosity=0):
#    """ For constructing a ReportableQty from a function of two gatesets. """
#    # Since smart_cached is unparameterized, it needs no following parens
#    @_smart_cached # nested decorators = decOut(decIn(f(x)))
#    @_functools.wraps(fnOfGateSets) 
#    def compute_quantity(gatesetA, gatesetB, confidenceRegionInfo=None):
#        if confidenceRegionInfo is None: # No Error bars
#            return _make_reportable_qty_or_dict( fnOfGateSets(gatesetA, gatesetB) )
#        # make sure the gateset we're given is the one used to generate the confidence region
#        if(gatesetA.frobeniusdist(confidenceRegionInfo.get_gateset()) > 1e-6):
#            raise ValueError("GateSet quantity confidence region is being requested for " +
#                             "a different gateset than the given confidenceRegionInfo")
#
#        nmEBs = bool(confidenceRegionInfo.get_errobar_type() == "non-markovian")
#        curriedFnOfGateSets = _functools.partial(fnOfGateSets, gatesetB=gatesetB)
#        df, f0 = confidenceRegionInfo.get_gateset_fn_confidence_interval(
#            curriedFnOfGateSets, eps, returnFnVal=True, verbosity=verbosity)
#
#        return _make_reportable_qty_or_dict(f0, df, nmEBs)
#
#    return compute_quantity

def spam_dotprods(rhoVecs, EVecs):
    ret = _np.empty( (len(rhoVecs), len(EVecs)), 'd')
    for i,rhoVec in enumerate(rhoVecs):
        for j,EVec in enumerate(EVecs):
            ret[i,j] = _np.dot(_np.transpose(EVec), rhoVec)
    return ret
Spam_dotprods = _gsf.spamfn_factory(spam_dotprods) #init args == (gateset)


def choi_matrix(gate, mxBasis):
    return _tools.jamiolkowski_iso(gate, mxBasis, mxBasis)
Choi_matrix = _gsf.gatefn_factory(choi_matrix) # init args == (gateset, gateLabel)


def choi_evals(gate, mxBasis):
    choi = _tools.jamiolkowski_iso(gate, mxBasis, mxBasis)
    choi_eigvals = _np.linalg.eigvals(choi)
    return _np.array(sorted(choi_eigvals))
Choi_evals = _gsf.gatefn_factory(choi_evals) # init args == (gateset, gateLabel)


def choi_trace(gate, mxBasis):
    choi = _tools.jamiolkowski_iso(gate, mxBasis, mxBasis)
    return _np.trace(choi)
Choi_trace = _gsf.gatefn_factory(choi_trace) # init args == (gateset, gateLabel)


def gate_eigenvalues(gate, mxBasis):
    return _np.linalg.eigvals(gate)
Gate_eigenvalues = _gsf.gatefn_factory(gate_eigenvalues)
# init args == (gateset, gateLabel)


def gatestring_eigenvalues(gateset, gatestring):
    return _np.linalg.eigvals(gateset.product(gatestring))
Gatestring_eigenvalues = _gsf.gatesetfn_factory(gatestring_eigenvalues)
# init args == (gateset, gatestring)

  
def rel_gatestring_eigenvalues(gatesetA, gatesetB, gatestring):
    A = gatesetA.product(gatestring) # "gate"
    B = gatesetB.product(gatestring) # "target gate"
    rel_gate = _np.dot(_np.linalg.inv(B), A) # "relative gate" == target^{-1} * gate
    return _np.linalg.eigvals(rel_gate)
Rel_gatestring_eigenvalues = _gsf.gatesetfn_factory(rel_gatestring_eigenvalues)
# init args == (gatesetA, gatesetB, gatestring) 


def gatestring_gaugeinv_diamondnorm(gatesetA, gatesetB, gatestring):
    A = gatesetA.product(gatestring) # "gate"
    B = gatesetB.product(gatestring) # "target gate"
    evA = _np.linalg.eigvals(A)
    evB = _np.linalg.eigvals(B)
    return _np.max(_tools.minweight_match(evA,evB, lambda x,y: abs(x-y), return_pairs=False ))
Gatestring_gaugeinv_diamondnorm = _gsf.gatesetfn_factory(gatestring_gaugeinv_diamondnorm)
# init args == (gatesetA, gatesetB, gatestring)
  

def gatestring_gaugeinv_infidelity(gatesetA, gatesetB, gatestring):
    A = gatesetA.product(gatestring) # "gate"
    B = gatesetB.product(gatestring) # "target gate"
    evA = _np.linalg.eigvals(A)
    evB = _np.linalg.eigvals(B)
    return _np.mean(_tools.minweight_match(evA,evB, lambda x,y: 1.0-_np.real(_np.conjugate(y)*x),
                                  return_pairs=False))
Gatestring_gaugeinv_infidelity = _gsf.gatesetfn_factory(gatestring_gaugeinv_infidelity)
# init args == (gatesetA, gatesetB, gatestring)


def gatestring_process_infidelity(gatesetA, gatesetB, gatestring):
    A = gatesetA.product(gatestring) # "gate"
    B = gatesetB.product(gatestring) # "target gate"
    return 1.0 - _tools.process_fidelity(A, B, gatesetB.basis)
Gatestring_process_infidelity = _gsf.gatesetfn_factory(gatestring_process_infidelity)
# init args == (gatesetA, gatesetB, gatestring)


def gatestring_fro_diff(gatesetA, gatesetB, gatestring):
    A = gatesetA.product(gatestring) # "gate"
    B = gatesetB.product(gatestring) # "target gate"
    return _tools.frobeniusdist(A, B)
Gatestring_fro_diff = _gsf.gatesetfn_factory(gatestring_fro_diff)
# init args == (gatesetA, gatesetB, gatestring)


def gatestring_jt_diff(gatesetA, gatesetB, gatestring):
    A = gatesetA.product(gatestring) # "gate"
    B = gatesetB.product(gatestring) # "target gate"
    return _tools.jtracedist(A, B, gatesetB.basis)
Gatestring_jt_diff = _gsf.gatesetfn_factory(gatestring_jt_diff)
# init args == (gatesetA, gatesetB, gatestring)

try:
    import cvxpy as _cvxpy
    def gatestring_half_diamond_norm(gatesetA, gatesetB, gatestring):
        A = gatesetA.product(gatestring) # "gate"
        B = gatesetB.product(gatestring) # "target gate"
        return 0.5 * _tools.diamonddist(A, B, gatesetB.basis)
    Gatestring_half_diamond_norm = _gsf.gatesetfn_factory(gatestring_half_diamond_norm)
      # init args == (gatesetA, gatesetB, gatestring)

except ImportError:
    gatestring_half_diamond_norm = None
    Gatestring_half_diamond_norm = None


def gatestring_unitarity_infidelity(gatesetA, gatesetB, gatestring):
    """ Returns 1 - sqrt(U), where U is the unitarity of A*B^{-1} """
    A = gatesetA.product(gatestring) # "gate"
    B = gatesetB.product(gatestring) # "target gate"
    from ..extras.rb import rbutils as _rbutils
    return 1.0 - _np.sqrt( _rbutils.unitarity( _np.dot(A, _np.linalg.inv(B)), gatesetB.basis) )
Gatestring_unitarity_infidelity = _gsf.gatesetfn_factory(gatestring_unitarity_infidelity)
  # init args == (gatesetA, gatesetB, gatestring)


def gatestring_avg_gate_infidelity(gatesetA, gatesetB, gatestring):
    """ Returns the average gate infidelity between A and B, where B is the "target" operation."""
    A = gatesetA.product(gatestring) # "gate"
    B = gatesetB.product(gatestring) # "target gate"
    d = _np.sqrt(A.shape[0])
    from ..extras.rb import rbutils as _rbutils
    return _rbutils.average_gate_infidelity(A,B, d, gatesetB.basis)
Gatestring_avg_gate_infidelity = _gsf.gatesetfn_factory(gatestring_avg_gate_infidelity)
  # init args == (gatesetA, gatesetB, gatestring)


#OLD ---------------------------
##@gate_quantity() # This function changes arguments to (gateLabel, gateset confidenceRegionInfo)
#def decomp_angle(gate):
#    decomp = _tools.decompose_gate_matrix(gate)
#    return decomp.get('pi rotations',0)
#
##@gate_quantity() # This function changes arguments to (gateLabel, gateset confidenceRegionInfo)
#def decomp_decay_diag(gate):
#    decomp = _tools.decompose_gate_matrix(gate)
#    return decomp.get('decay of diagonal rotation terms',0)
#
##@gate_quantity() # This function changes arguments to (gateLabel, gateset, confidenceRegionInfo)
#def decomp_decay_offdiag(gate):
#    decomp = _tools.decompose_gate_matrix(gate)
#    return decomp.get('decay of off diagonal rotation terms',0)
#
##@gate_quantity() # This function changes arguments to (gateLabel, gateset, confidenceRegionInfo)
#def decomp_cu_angle(gate):
#    closestUGateMx = _alg.find_closest_unitary_gatemx(gate)
#    decomp = _tools.decompose_gate_matrix(closestUGateMx)
#    return decomp.get('pi rotations', 0)
#
##@gate_quantity() # This function changes arguments to (gateLabel, gateset, confidenceRegionInfo)
#def decomp_cu_decay_diag(gate):
#    closestUGateMx = _alg.find_closest_unitary_gatemx(gate)
#    decomp = _tools.decompose_gate_matrix(closestUGateMx)
#    return decomp.get('decay of diagonal rotation terms', 0)
#
##@gate_quantity() # This function changes arguments to (gateLabel, gateset, confidenceRegionInfo)
#def decomp_cu_decay_offdiag(gate):
#    closestUGateMx = _alg.find_closest_unitary_gatemx(gate)
#    decomp = _tools.decompose_gate_matrix(closestUGateMx)
#    return decomp.get('decay of off diagonal rotation terms', 0)

def decomposition(gate):
    decompDict = _tools.decompose_gate_matrix(gate)
    if decompDict['isValid']:
        angleQty   = decompDict.get('pi rotations',0)
        diagQty    = decompDict.get('decay of diagonal rotation terms',0)
        offdiagQty = decompDict.get('decay of off diagonal rotation terms',0)
        errBarDict = { 'pi rotations': None,
                       'decay of diagonal rotation terms': None,
                       'decay of off diagonal rotation terms': None }
        return ReportableQty(decompDict, errBarDict)
    else:
        return ReportableQty({})

def upper_bound_fidelity(gate, mxBasis):
    return _tools.fidelity_upper_bound(gate)[0]
Upper_bound_fidelity = _gsf.gatefn_factory(upper_bound_fidelity)
# init args == (gateset, gateLabel)


def closest_ujmx(gate, mxBasis):
    closestUGateMx = _alg.find_closest_unitary_gatemx(gate)
    return _tools.jamiolkowski_iso(closestUGateMx, mxBasis, mxBasis)
Closest_ujmx = _gsf.gatefn_factory(closest_ujmx)
# init args == (gateset, gateLabel)


def maximum_fidelity(gate, mxBasis):
    closestUGateMx = _alg.find_closest_unitary_gatemx(gate)
    closestUJMx = _tools.jamiolkowski_iso(closestUGateMx, mxBasis, mxBasis)
    choi = _tools.jamiolkowski_iso(gate, mxBasis, mxBasis)
    return _tools.fidelity(closestUJMx, choi)
Maximum_fidelity = _gsf.gatefn_factory(maximum_fidelity)
# init args == (gateset, gateLabel)


def maximum_trace_dist(gate, mxBasis):
    closestUGateMx = _alg.find_closest_unitary_gatemx(gate)
    #closestUJMx = _tools.jamiolkowski_iso(closestUGateMx, mxBasis, mxBasis)
    _tools.jamiolkowski_iso(closestUGateMx, mxBasis, mxBasis)
    return _tools.jtracedist(gate, closestUGateMx)
Maximum_trace_dist = _gsf.gatefn_factory(maximum_trace_dist)
# init args == (gateset, gateLabel)


def angles_btwn_rotn_axes(gateset):
    gateLabels = list(gateset.gates.keys())
    angles_btwn_rotn_axes = _np.zeros( (len(gateLabels), len(gateLabels)), 'd' )

    for i,gl in enumerate(gateLabels):
        decomp = _tools.decompose_gate_matrix(gateset.gates[gl])
        rotnAngle = decomp.get('pi rotations','X')
        axisOfRotn = decomp.get('axis of rotation',None)

        for j,gl_other in enumerate(gateLabels[i+1:],start=i+1):
            decomp_other = _tools.decompose_gate_matrix(gateset.gates[gl_other])
            rotnAngle_other = decomp_other.get('pi rotations','X')

            if str(rotnAngle) == 'X' or abs(rotnAngle) < 1e-4 or \
               str(rotnAngle_other) == 'X' or abs(rotnAngle_other) < 1e-4:
                angles_btwn_rotn_axes[i,j] =  _np.nan
            else:
                axisOfRotn_other = decomp_other.get('axis of rotation',None)
                if axisOfRotn is not None and axisOfRotn_other is not None:
                    real_dot =  _np.clip( _np.real(_np.dot(axisOfRotn,axisOfRotn_other)), -1.0, 1.0)
                    angles_btwn_rotn_axes[i,j] = _np.arccos( real_dot ) / _np.pi
                else:
                    angles_btwn_rotn_axes[i,j] = _np.nan

            angles_btwn_rotn_axes[j,i] = angles_btwn_rotn_axes[i,j]
    return angles_btwn_rotn_axes
Angles_btwn_rotn_axes = _gsf.gatesetfn_factory(angles_btwn_rotn_axes)
# init args == (gateset)


# ------------------------------ OLD
#@_tools.deprecated_fn(replacement='individual functions from the reportables module')
#def compute_gateset_qtys(qtynames, gateset, confidenceRegionInfo=None):
#    """
#    Compute the named "GateSet" quantities.
#
#    Parameters
#    ----------
#    qtynames : list of strings
#        Names of the quantities to compute.
#
#    gateset : GateSet
#        Gate set used to compute the quantities.
#
#    confidenceRegionInfo : ConfidenceRegion, optional
#        If not None, specifies a confidence-region used to compute the error bars
#        contained in the returned quantities.  If None, then no error bars are
#        computed.
#
#    Returns
#    -------
#    dict
#        Dictionary whose keys are the requested quantity names and values are
#        ReportableQty objects.
#    """
#    ret = _OrderedDict()
#    possible_qtys = [ ]
#    eps = FINITE_DIFF_EPS
#    mxBasis = gateset.basis
#
#    def choi_matrix(gate):
#        return _tools.jamiolkowski_iso(gate, mxBasis, mxBasis)
#
#    def choi_evals(gate):
#        choi = _tools.jamiolkowski_iso(gate, mxBasis, mxBasis)
#        choi_eigvals = _np.linalg.eigvals(choi)
#        return _np.array(sorted(choi_eigvals))
#
#    def choi_trace(gate):
#        choi = _tools.jamiolkowski_iso(gate, mxBasis, mxBasis)
#        return _np.trace(choi)
#
#
#    def decomp_cu_angle(gate):
#        closestUGateMx = _alg.find_closest_unitary_gatemx(gate)
#        decomp = _tools.decompose_gate_matrix(closestUGateMx)
#        return decomp.get('pi rotations',0)
#
#    def decomp_cu_decay_diag(gate):
#        closestUGateMx = _alg.find_closest_unitary_gatemx(gate)
#        decomp = _tools.decompose_gate_matrix(closestUGateMx)
#        return decomp.get('decay of diagonal rotation terms',0)
#
#    def decomp_cu_decay_offdiag(gate):
#        closestUGateMx = _alg.find_closest_unitary_gatemx(gate)
#        decomp = _tools.decompose_gate_matrix(closestUGateMx)
#        return decomp.get('decay of off diagonal rotation terms',0)
#
#    def upper_bound_fidelity(gate):
#        return _tools.fidelity_upper_bound(gate)[0]
#
#    def closest_ujmx(gate):
#        closestUGateMx = _alg.find_closest_unitary_gatemx(gate)
#        return _tools.jamiolkowski_iso(closestUGateMx, mxBasis, mxBasis)
#
#    def maximum_fidelity(gate):
#        closestUGateMx = _alg.find_closest_unitary_gatemx(gate)
#        closestUJMx = _tools.jamiolkowski_iso(closestUGateMx, mxBasis, mxBasis)
#        choi = _tools.jamiolkowski_iso(gate, mxBasis, mxBasis)
#        return _tools.fidelity(closestUJMx, choi)
#
#    def maximum_trace_dist(gate):
#        closestUGateMx = _alg.find_closest_unitary_gatemx(gate)
#        #closestUJMx = _tools.jamiolkowski_iso(closestUGateMx, mxBasis, mxBasis)
#        _tools.jamiolkowski_iso(closestUGateMx, mxBasis, mxBasis)
#        return _tools.jtracedist(gate, closestUGateMx)
#
#    def spam_dotprods(rhoVecs, EVecs):
#        ret = _np.empty( (len(rhoVecs), len(EVecs)), 'd')
#        for i,rhoVec in enumerate(rhoVecs):
#            for j,EVec in enumerate(EVecs):
#                ret[i,j] = _np.dot(_np.transpose(EVec), rhoVec)
#        return ret
#
#    def angles_btwn_rotn_axes(gateset):
#        gateLabels = list(gateset.gates.keys())
#        angles_btwn_rotn_axes = _np.zeros( (len(gateLabels), len(gateLabels)), 'd' )
#
#        for i,gl in enumerate(gateLabels):
#            decomp = _tools.decompose_gate_matrix(gateset.gates[gl])
#            rotnAngle = decomp.get('pi rotations','X')
#            axisOfRotn = decomp.get('axis of rotation',None)
#
#            for j,gl_other in enumerate(gateLabels[i+1:],start=i+1):
#                decomp_other = _tools.decompose_gate_matrix(gateset.gates[gl_other])
#                rotnAngle_other = decomp_other.get('pi rotations','X')
#
#                if str(rotnAngle) == 'X' or abs(rotnAngle) < 1e-4 or \
#                   str(rotnAngle_other) == 'X' or abs(rotnAngle_other) < 1e-4:
#                    angles_btwn_rotn_axes[i,j] =  _np.nan
#                else:
#                    axisOfRotn_other = decomp_other.get('axis of rotation',None)
#                    if axisOfRotn is not None and axisOfRotn_other is not None:
#                        real_dot =  _np.clip( _np.real(_np.dot(axisOfRotn,axisOfRotn_other)), -1.0, 1.0)
#                        angles_btwn_rotn_axes[i,j] = _np.arccos( real_dot ) / _np.pi
#                    else:
#                        angles_btwn_rotn_axes[i,j] = _np.nan
#
#                angles_btwn_rotn_axes[j,i] = angles_btwn_rotn_axes[i,j]
#        return angles_btwn_rotn_axes
#
#    key = "Gateset Axis Angles"; possible_qtys.append(key)
#    if key in qtynames:
#        ret[key] = _getGateSetQuantity(angles_btwn_rotn_axes, gateset, eps, confidenceRegionInfo)
#
#    # Quantities computed per gate
#    for (label,gate) in gateset.gates.items():
#
#        #Gate quantities
#        suffixes = ('eigenvalues', 'eigenvectors', 'choi eigenvalues', 'choi trace',
#                    'choi matrix', 'decomposition')
#        gate_qtys = _OrderedDict( [ ("%s %s" % (label,s), None) for s in suffixes ] )
#        possible_qtys += list(gate_qtys.keys())
#
#        if any( [qtyname in gate_qtys for qtyname in qtynames] ):
#            #gate_evals,gate_evecs = _np.linalg.eig(gate)
#            evalsQty  = _getGateQuantity(_np.linalg.eigvals, gateset, label, eps, confidenceRegionInfo)
#            choiQty   = _getGateQuantity(choi_matrix, gateset, label, eps, confidenceRegionInfo)
#            choiEvQty = _getGateQuantity(choi_evals, gateset, label, eps, confidenceRegionInfo)
#            choiTrQty = _getGateQuantity(choi_trace, gateset, label, eps, confidenceRegionInfo)
#
#            decompDict = _tools.decompose_gate_matrix(gate)
#            if decompDict['isValid']:
#                angleQty   = _getGateQuantity(decomp_angle, gateset, label, eps, confidenceRegionInfo)
#                diagQty    = _getGateQuantity(decomp_decay_diag, gateset, label, eps, confidenceRegionInfo)
#                offdiagQty = _getGateQuantity(decomp_decay_offdiag, gateset, label, eps, confidenceRegionInfo)
#                errBarDict = { 'pi rotations': angleQty.get_err_bar(),
#                               'decay of diagonal rotation terms': diagQty.get_err_bar(),
#                               'decay of off diagonal rotation terms': offdiagQty.get_err_bar() }
#                decompQty = ReportableQty(decompDict, errBarDict)
#            else:
#                decompQty = ReportableQty({})
#
#            gate_qtys[ '%s eigenvalues' % label ]      = evalsQty
#            #gate_qtys[ '%s eigenvectors' % label ]     = gate_evecs
#            gate_qtys[ '%s choi matrix' % label ]      = choiQty
#            gate_qtys[ '%s choi eigenvalues' % label ] = choiEvQty
#            gate_qtys[ '%s choi trace' % label ]       = choiTrQty
#            gate_qtys[ '%s decomposition' % label]     = decompQty
#
#            for qtyname in qtynames:
#                if qtyname in gate_qtys:
#                    ret[qtyname] = gate_qtys[qtyname]
#
#        #Closest unitary quantities
#        suffixes = ('max fidelity with unitary',
#                    'max trace dist with unitary',
#                    'upper bound on fidelity with unitary',
#                    'closest unitary choi matrix',
#                    'closest unitary decomposition')
#        closestU_qtys = _OrderedDict( [ ("%s %s" % (label,s), None) for s in suffixes ] )
#        possible_qtys += list(closestU_qtys.keys())
#        if any( [qtyname in closestU_qtys for qtyname in qtynames] ):
#            ubFQty = _getGateQuantity(upper_bound_fidelity, gateset, label, eps, confidenceRegionInfo)
#            closeUJMxQty = _getGateQuantity(closest_ujmx, gateset, label, eps, confidenceRegionInfo)
#            maxFQty = _getGateQuantity(maximum_fidelity, gateset, label, eps, confidenceRegionInfo)
#            maxJTDQty = _getGateQuantity(maximum_trace_dist, gateset, label, eps, confidenceRegionInfo)
#
#            closestUGateMx = _alg.find_closest_unitary_gatemx(gate)
#            decompDict = _tools.decompose_gate_matrix(closestUGateMx)
#            if decompDict['isValid']:
#                angleQty = _getGateQuantity(decomp_cu_angle, gateset, label, eps, confidenceRegionInfo)
#                diagQty = _getGateQuantity(decomp_cu_decay_diag, gateset, label, eps, confidenceRegionInfo)
#                offdiagQty = _getGateQuantity(decomp_cu_decay_offdiag, gateset, label, eps, confidenceRegionInfo)
#                errBarDict = { 'pi rotations': angleQty.get_err_bar(),
#                               'decay of diagonal rotation terms': diagQty.get_err_bar(),
#                               'decay of off diagonal rotation terms': offdiagQty.get_err_bar() }
#                decompQty = ReportableQty(decompDict, errBarDict)
#            else:
#                decompQty = ReportableQty({})
#
#            closestU_qtys[ '%s max fidelity with unitary' % label ]                  = maxFQty
#            closestU_qtys[ '%s max trace dist with unitary' % label ]                = maxJTDQty
#            closestU_qtys[ '%s upper bound on fidelity with unitary' % label ]       = ubFQty
#            closestU_qtys[ '%s closest unitary choi matrix' % label ]                = closeUJMxQty
#            closestU_qtys[ '%s closest unitary decomposition' % label ]              = decompQty
#
#            for qtyname in qtynames:
#                if qtyname in closestU_qtys:
#                    ret[qtyname] = closestU_qtys[qtyname]
#
#    if qtynames[0] is None:
#        return possible_qtys
#    return ret
#
#@_tools.deprecated_fn(replacement='individual functions from the reportables module')
#def compute_dataset_qty(qtyname, dataset, gatestrings=None):
#    """
#    Compute the named "Dataset" quantity.
#
#    Parameters
#    ----------
#    qtyname : string
#        Name of the quantity to compute.
#
#    dataset : DataSet
#        Data used to compute the quantity.
#
#    gatestrings : list of tuples or GateString objects, optional
#        A list of gatestrings used in the computation of certain quantities.
#        If None, all the gatestrings in the dataset are used.
#
#    Returns
#    -------
#    ReportableQty
#        The quantity requested, or None if quantity could not be computed.
#    """
#    ret = compute_dataset_qtys([qtyname], dataset, gatestrings)
#    if qtyname is None: return ret
#    elif qtyname in ret: return ret[qtyname]
#    else: return None
#
#@_tools.deprecated_fn(replacement='individual functions from the reportables module')
#def compute_dataset_qtys(qtynames, dataset, gatestrings=None):
#    """
#    Compute the named "Dataset" quantities.
#
#    Parameters
#    ----------
#    qtynames : list of strings
#        Names of the quantities to compute.
#
#    dataset : DataSet
#        Data used to compute the quantity.
#
#    gatestrings : list of tuples or GateString objects, optional
#        A list of gatestrings used in the computation of certain quantities.
#        If None, all the gatestrings in the dataset are used.
#
#    Returns
#    -------
#    dict
#        Dictionary whose keys are the requested quantity names and values are
#        ReportableQty objects.
#    """
#    ret = _OrderedDict()
#    possible_qtys = [ ]
#
#    #Quantities computed per gatestring
#    per_gatestring_qtys = _OrderedDict( [('gate string', []), ('gate string index', []), ('gate string length', []), ('count total', [])] )
#    spamLabels = dataset.get_spam_labels()
#    for spl in spamLabels:
#        per_gatestring_qtys['Exp prob(%s)' % spl] = []
#        per_gatestring_qtys['Exp count(%s)' % spl] = []
#
#    if any( [qtyname in per_gatestring_qtys for qtyname in qtynames ] ):
#        if gatestrings is None: gatestrings = list(dataset.keys())
#        for (i,gs) in enumerate(gatestrings):
#            if gs in dataset: # skip gate strings given that are not in dataset
#                dsRow = dataset[gs]
#            else:
#                #print "Warning: skipping gate string %s" % str(gs)
#                continue
#
#            N = dsRow.total()
#            per_gatestring_qtys['gate string'].append(  ''.join(gs)  )
#            per_gatestring_qtys['gate string index'].append( i )
#            per_gatestring_qtys['gate string length'].append(  len(gs)  )
#            per_gatestring_qtys['count total'].append(  N  )
#
#            for spamLabel in spamLabels:
#                pExp = _projectToValidProb( dsRow[spamLabel] / N, tol=1e-10 )
#                per_gatestring_qtys['Exp prob(%s)' % spamLabel].append( pExp )
#                per_gatestring_qtys['Exp count(%s)' % spamLabel].append( dsRow[spamLabel] )
#
#        for qtyname in qtynames:
#            if qtyname in per_gatestring_qtys:
#                ret[qtyname] = ReportableQty(per_gatestring_qtys[qtyname])
#
#
#    #Quantities computed per dataset
#    qty = "max logl"; possible_qtys.append(qty)
#    if qty in qtynames:
#        ret[qty] = ReportableQty( _tools.logl_max(dataset))
#
#    qty = "number of gate strings"; possible_qtys.append(qty)
#    if qty in qtynames:
#        ret[qty] = ReportableQty( len(dataset) )
#
#    if qtynames[0] is None:
#        return possible_qtys + list(per_gatestring_qtys.keys())
#    return ret
#
#@_tools.deprecated_fn(replacement='individual functions from the reportables module')
#def compute_gateset_qty(qtyname, gateset, confidenceRegionInfo=None):
#    """
#    Compute the named "GateSet" quantity.
#
#    Parameters
#    ----------
#    qtyname : string
#        Name of the quantity to compute.
#
#    gateset : GateSet
#        Gate set used to compute the quantity.
#
#    confidenceRegionInfo : ConfidenceRegion, optional
#        If not None, specifies a confidence-region used to compute the error bars
#        contained in the returned quantity.  If None, then no error bars are
#        computed.
#
#    Returns
#    -------
#    ReportableQty
#        The quantity requested, or None if quantity could not be computed.
#    """
#    ret = compute_gateset_qtys( [qtyname], gateset, confidenceRegionInfo)
#    if qtyname is None: return ret
#    elif qtyname in ret: return ret[qtyname]
#    else: return None
#
#@_tools.deprecated_fn(replacement='individual functions from the reportables module')
#def compute_gateset_dataset_qty(qtyname, gateset, dataset, gatestrings=None):
#    """
#    Compute the named "GateSet & Dataset" quantity.
#
#    Parameters
#    ----------
#    qtyname : string
#        Name of the quantity to compute.
#
#    gateset : GateSet
#        Gate set used to compute the quantity.
#
#    dataset : DataSet
#        Data used to compute the quantity.
#
#    gatestrings : list of tuples or GateString objects, optional
#        A list of gatestrings used in the computation of certain quantities.
#        If None, all the gatestrings in the dataset are used.
#
#    Returns
#    -------
#    ReportableQty
#        The quantity requested, or None if quantity could not be computed.
#    """
#    ret = compute_gateset_dataset_qtys( [qtyname], gateset, dataset, gatestrings )
#    if qtyname is None: return ret
#    elif qtyname in ret: return ret[qtyname]
#    else: return None
#
#@_tools.deprecated_fn(replacement='individual functions from the reportables module')
#def compute_gateset_dataset_qtys(qtynames, gateset, dataset, gatestrings=None):
#    """
#    Compute the named "GateSet & Dataset" quantities.
#
#    Parameters
#    ----------
#    qtynames : list of strings
#        Names of the quantities to compute.
#
#    gateset : GateSet
#        Gate set used to compute the quantities.
#
#    dataset : DataSet
#        Data used to compute the quantities.
#
#    gatestrings : list of tuples or GateString objects, optional
#        A list of gatestrings used in the computation of certain quantities.
#        If None, all the gatestrings in the dataset are used.
#
#    Returns
#    -------
#    dict
#        Dictionary whose keys are the requested quantity names and values are
#        ReportableQty objects.
#    """
#
#    #Note: no error bars computed for these quantities yet...
#
#    ret = _OrderedDict()
#    possible_qtys = [ ]
#
#    #Quantities computed per gatestring
#    per_gatestring_qtys = _OrderedDict() # OLD qtys: [('logl term diff', []), ('score', [])]
#    for spl in gateset.get_spam_labels():
#        per_gatestring_qtys['prob(%s) diff' % spl] = []
#        per_gatestring_qtys['count(%s) diff' % spl] = []
#        per_gatestring_qtys['Est prob(%s)' % spl] = []
#        per_gatestring_qtys['Est count(%s)' % spl] = []
#        per_gatestring_qtys['gatestring chi2(%s)' % spl] = []
#
#    if any( [qtyname in per_gatestring_qtys for qtyname in qtynames ] ):
#        if gatestrings is None: 
#            gatestrings = list(dataset.keys())
#        for gs in gatestrings:
#            if gs in dataset: # skip gate strings given that are not in dataset
#                dsRow = dataset[gs]
#            else: continue
#
#            p = gateset.probs(gs)
#            pExp = { }; N = dsRow.total()
#            for spamLabel in p:
#                p[spamLabel] = _projectToValidProb( p[spamLabel], tol=1e-10 )
#                pExp[spamLabel] = _projectToValidProb( dsRow[spamLabel] / N, tol=1e-10 )
#
#            #OLD
#            #per_gatestring_qtys['logl term diff'].append(  _tools.logL_term(dsRow, pExp) - _tools.logL_term(dsRow, p)  )
#            #per_gatestring_qtys['score'].append(  (_tools.logL_term(dsRow, pExp) - _tools.logL_term(dsRow, p)) / N  )
#
#            for spamLabel in p:
#                per_gatestring_qtys['prob(%s) diff' % spamLabel].append( abs(p[spamLabel] - pExp[spamLabel]) )
#                per_gatestring_qtys['count(%s) diff' % spamLabel].append( int( round(p[spamLabel] * N) - dsRow[spamLabel]) )
#                per_gatestring_qtys['Est prob(%s)' % spamLabel].append( p[spamLabel] )
#                per_gatestring_qtys['Est count(%s)' % spamLabel].append( int(round(p[spamLabel] * N)) )
#                per_gatestring_qtys['gatestring chi2(%s)' % spamLabel].append( _tools.chi2fn( N, p[spamLabel], pExp[spamLabel], 1e-4 ) )
#
#        for qtyname in qtynames:
#            if qtyname in per_gatestring_qtys:
#                ret[qtyname] = ReportableQty( per_gatestring_qtys[qtyname] )
#
#    #Quantities which take a single value for a given gateset and dataset
#    qty = "logl"; possible_qtys.append(qty)
#    if qty in qtynames:
#        ret[qty] = ReportableQty( _tools.logl(gateset, dataset) )
#
#    qty = "logl diff"; possible_qtys.append(qty)
#    if qty in qtynames:
#        ret[qty] = ReportableQty( _tools.logl_max(dataset) - _tools.logl(gateset, dataset) )
#
#    qty = "chi2"; possible_qtys.append(qty)
#    if qty in qtynames:
#        ret[qty] = ReportableQty( _tools.chi2( dataset, gateset, minProbClipForWeighting=1e-4) )
#
#    #Quantities which take a single value per spamlabel for a given gateset and dataset
#    #for spl in gateset.get_spam_labels():
#    #    qty = "chi2(%s)" % spl; possible_qtys.append(qty)
#    #    if qty in qtynames:
#    #        ret[qty] = _tools.chi2( dataset, gateset, minProbClipForWeighting=1e-4)
#
#    if qtynames[0] is None:
#        return possible_qtys + list(per_gatestring_qtys.keys())
#    return ret



#@_tools.parameterized
#def gates_quantity(fnOfGates, eps=FINITE_DIFF_EPS, verbosity=0):
#    """ For constructing a ReportableQty from a function of two gates and a basis."""
#    # Since smart_cached is unparameterized, it needs no following parens
#    @_smart_cached # nested decorators = decOut(decIn(f(x)))
#    @_functools.wraps(fnOfGates) # Retain metadata of wrapped function
#    def compute_quantity(gateLabel, gatesetA, gatesetB, confidenceRegionInfo=None):
#        mxBasis = gatesetB.basis #because gatesetB is usually the target which has a well defined basis
#        A = gatesetA.gates[gateLabel]
#        B = gatesetB.gates[gateLabel]
#        if confidenceRegionInfo is None: # No Error bars
#            return _make_reportable_qty_or_dict( fnOfGates(A, B, mxBasis) )
#
#        # make sure the gateset we're given is the one used to generate the confidence region
#        if(gatesetA.frobeniusdist(confidenceRegionInfo.get_gateset()) > 1e-6):
#            raise ValueError("Prep quantity confidence region is being requested for " +
#                             "a different gateset than the given confidenceRegionInfo")
#
#        nmEBs = bool(confidenceRegionInfo.get_errobar_type() == "non-markovian")
#        curriedFnOfGates = _functools.partial(fnOfGates, B=B, mxBasis=mxBasis)
#        df, f0 = confidenceRegionInfo.get_gate_fn_confidence_interval(curriedFnOfGates, gateLabel,
#                                                                  eps, returnFnVal=True,
#                                                                  verbosity=verbosity)
#
#        return _make_reportable_qty_or_dict(f0, df, nmEBs)
#        
#    return compute_quantity

def process_fidelity(A, mxBasis, B):
    return _tools.process_fidelity(A, B, mxBasis)
Process_fidelity = _gsf.gatesfn_factory(process_fidelity)
# init args == (gateset1, gateset2, gateLabel)


def process_infidelity(A, B, mxBasis):
    return 1 - _tools.process_fidelity(A, B, mxBasis)
Process_infidelity = _gsf.gatesfn_factory(process_infidelity)
# init args == (gateset1, gateset2, gateLabel)


def closest_unitary_fidelity(A, B, mxBasis): # assume vary gateset1, gateset2 fixed
    decomp1 = _tools.decompose_gate_matrix(A)
    decomp2 = _tools.decompose_gate_matrix(B)

    if decomp1['isUnitary']:
        closestUGateMx1 = A
    else: closestUGateMx1 = _alg.find_closest_unitary_gatemx(A)

    if decomp2['isUnitary']:
        closestUGateMx2 = B
    else: closestUGateMx2 = _alg.find_closest_unitary_gatemx(A)

    closeChoi1 = _tools.jamiolkowski_iso(closestUGateMx1)
    closeChoi2 = _tools.jamiolkowski_iso(closestUGateMx2)
    return _tools.fidelity(closeChoi1, closeChoi2)
Closest_unitary_fidelity = _gsf.gatesfn_factory(closest_unitary_fidelity)
# init args == (gateset1, gateset2, gateLabel)


def fro_diff(A, B, mxBasis): # assume vary gateset1, gateset2 fixed
    return _tools.frobeniusdist(A, B)
Fro_diff = _gsf.gatesfn_factory(fro_diff)
# init args == (gateset1, gateset2, gateLabel)


def jt_diff(A, B, mxBasis): # assume vary gateset1, gateset2 fixed
    return _tools.jtracedist(A, B, mxBasis)
Jt_diff = _gsf.gatesfn_factory(jt_diff)
# init args == (gateset1, gateset2, gateLabel)


try:
    import cvxpy as _cvxpy
    def half_diamond_norm(A, B, mxBasis):
        return 0.5 * _tools.diamonddist(A, B, mxBasis)
    Half_diamond_norm = _gsf.gatesfn_factory(half_diamond_norm)
    # init args == (gateset1, gateset2, gateLabel)

except ImportError:
    half_diamond_norm = None
    Half_diamond_norm = None

    
def unitarity_infidelity(A, B, mxBasis):
    """ Returns 1 - sqrt(U), where U is the unitarity of A*B^{-1} """
    from ..extras.rb import rbutils as _rbutils
    return 1.0 - _np.sqrt( _rbutils.unitarity( _np.dot(A, _np.linalg.inv(B)), mxBasis) )
Unitarity_infidelity = _gsf.gatesfn_factory(unitarity_infidelity)
# init args == (gateset1, gateset2, gateLabel)


def gaugeinv_diamondnorm(A, B, mxBasis):
    evA = _np.linalg.eigvals(A)
    evB = _np.linalg.eigvals(B)
    return _np.max(_tools.minweight_match(evA,evB, lambda x,y: abs(x-y), return_pairs=False))
Gaugeinv_diamondnorm = _gsf.gatesfn_factory(gaugeinv_diamondnorm)
# init args == (gateset1, gateset2, gateLabel)


def gaugeinv_infidelity(A, B, mxBasis):
    evA = _np.linalg.eigvals(A)
    evB = _np.linalg.eigvals(B)
    return _np.mean(_tools.minweight_match(evA,evB, lambda x,y: 1.0-_np.real(_np.conjugate(y)*x),
                                  return_pairs=False))
Gaugeinv_infidelity = _gsf.gatesfn_factory(gaugeinv_infidelity)
# init args == (gateset1, gateset2, gateLabel)



#OLD: TIMS FN... seems perhaps better motivated, but for now keep this simple and equal to gatestring_ version
#@gate_quantity() # This function changes arguments to (gateLabel, gateset, confidenceRegionInfo)
#def gaugeinv_infidelity(gate, mxBasis):
#    """ 
#    Returns gauge-invariant "version" of the unitary fidelity in which
#    the unitarity is replaced with the gauge-invariant quantity
#    `(lambda^dagger lambda - 1) / (d**2 - 1)`, where `lambda` is the spectrum 
#    of A, which equals the unitarity in at least one particular gauge.
#    """
#    d2 = gate.shape[0]
#    lmb = _np.linalg.eigvals(gate)
#    Uproxy = (_np.real(_np.vdot(lmb,lmb)) - 1.0) / (d2 - 1.0)
#    return 1.0 - _np.sqrt( Uproxy )

def avg_gate_infidelity(A, B, mxBasis):
    """ Returns the average gate infidelity between A and B, where B is the "target" operation."""
    d = _np.sqrt(A.shape[0])
    from ..extras.rb import rbutils as _rbutils
    return _rbutils.average_gate_infidelity(A,B, d, mxBasis)
Avg_gate_infidelity = _gsf.gatesfn_factory(avg_gate_infidelity)
# init args == (gateset1, gateset2, gateLabel)



def gateset_gateset_angles_btwn_axes(A, B, mxBasis): #Note: default 'gm' basis
    decomp = _tools.decompose_gate_matrix(A)
    decomp2 = _tools.decompose_gate_matrix(B)
    axisOfRotn = decomp.get('axis of rotation', None)
    rotnAngle = decomp.get('pi rotations','X')
    axisOfRotn2 = decomp2.get('axis of rotation', None)
    rotnAngle2 = decomp2.get('pi rotations','X')

    if rotnAngle == 'X' or abs(rotnAngle) < 1e-4 or \
       rotnAngle2 == 'X' or abs(rotnAngle2) < 1e-4:
        return _np.nan

    if axisOfRotn is None or axisOfRotn2 is None:
        return _np.nan

    real_dot =  _np.clip( _np.real(_np.dot(axisOfRotn, axisOfRotn2)), -1.0, 1.0)
    return _np.arccos( abs(real_dot) ) / _np.pi
      #Note: abs() allows axis to be off by 180 degrees -- if showing *angle* as
      #      well, must flip sign of angle of rotation if you allow axis to
      #      "reverse" by 180 degrees.

Gateset_gateset_angles_btwn_axes = _gsf.gatesfn_factory(gateset_gateset_angles_btwn_axes)
# init args == (gateset1, gateset2, gateLabel)


def rel_eigvals(A, B, mxBasis):
    target_gate_inv = _np.linalg.inv(B)
    rel_gate = _np.dot(target_gate_inv, A)
    return _np.linalg.eigvals(rel_gate)
Rel_eigvals = _gsf.gatesfn_factory(rel_eigvals)
# init args == (gateset1, gateset2, gateLabel)

def rel_logTiG_eigvals(A, B, mxBasis):
    rel_gate = _tools.error_generator(A, B, "logTiG")
    return _np.linalg.eigvals(rel_gate)
Rel_logTiG_eigvals = _gsf.gatesfn_factory(rel_logTiG_eigvals)
# init args == (gateset1, gateset2, gateLabel)


def rel_logGmlogT_eigvals(A, B, mxBasis):
    rel_gate = _tools.error_generator(A, B, "logG-logT")
    return _np.linalg.eigvals(rel_gate)
Rel_logGmlogT_eigvals = _gsf.gatesfn_factory(rel_logGmlogT_eigvals)
# init args == (gateset1, gateset2, gateLabel)


def rel_gate_eigenvalues(A, B, mxBasis):
    rel_gate = _np.dot(_np.linalg.inv(B), A) # "relative gate" == target^{-1} * gate
    return _np.linalg.eigvals(rel_gate)
Rel_gate_eigenvalues = _gsf.gatesfn_factory(rel_gate_eigenvalues)
# init args == (gateset1, gateset2, gateLabel)


def logTiG_and_projections(A, B, mxBasis):
    ret = {}
    ret['error generator'] = \
        _tools.error_generator(A, B, mxBasis, "logTiG")
    ret['hamiltonian projections'] = \
        _tools.std_errgen_projections(
            ret['error generator'], "hamiltonian",
            mxBasis.name, mxBasis) # mxBasis.name because projector dim is not the same as gate dim
    ret['stochastic projections'] = \
        _tools.std_errgen_projections(
            ret['error generator'], "stochastic",
            mxBasis.name, mxBasis) # mxBasis.name because projector dim is not the same as gate dim
    return ret
LogTiG_and_projections = _gsf.gatesfn_factory(logTiG_and_projections)
# init args == (gateset1, gateset2, gateLabel)



def logGmlogT_and_projections(A, B, mxBasis):
    ret = {}
    ret['error generator'] = \
        _tools.error_generator(A, B, mxBasis, "logG-logT")
    ret['hamiltonian projections'] = \
        _tools.std_errgen_projections(
            ret['error generator'], "hamiltonian",
            mxBasis.name, mxBasis) # mxBasis.name because projector dim is not the same as gate dim
    ret['stochastic projections'] = \
        _tools.std_errgen_projections(
            ret['error generator'], "stochastic",
            mxBasis.name, mxBasis) # mxBasis.name because projector dim is not the same as gate dim
    return ret
LogGmlogT_and_projections = _gsf.gatesfn_factory(logGmlogT_and_projections)
# init args == (gateset1, gateset2, gateLabel)



def general_decomposition(gatesetA, gatesetB): # B is target gateset usually but must be "gatsetB" b/c of decorator coding...
    decomp = {}
    gateLabels = list(gatesetA.gates.keys())  # gate labels
    mxBasis = gatesetB.basis # B is usually the target which has a well-defined basis
    
    for gl in gateLabels:
        gate = gatesetA.gates[gl]
        targetGate = gatesetB.gates[gl]

        target_evals = _np.linalg.eigvals(targetGate)
        if _np.any(_np.isclose(target_evals,-1.0)):
            target_logG = _tools.unitary_superoperator_matrix_log(targetGate, mxBasis)        
            logG = _tools.approximate_matrix_log(gate, target_logG)
        else:
            logG = _tools.real_matrix_log(gate, "warn")
            if _np.linalg.norm(logG.imag) > 1e-6:
                _warnings.warn("Truncating imaginary logarithm!")
                logG = _np.real(logG)
                
        decomp[gl + ' log inexactness'] = _np.linalg.norm(_spl.expm(logG)-gate)
    
        hamProjs, hamGens = _tools.std_errgen_projections(
            logG, "hamiltonian", mxBasis.name, mxBasis, return_generators=True)
        norm = _np.linalg.norm(hamProjs)
        decomp[gl + ' axis'] = hamProjs / norm if (norm > 1e-15) else hamProjs
        
        #angles[gl] = norm * (gateset.dim**0.25 / 2.0) / _np.pi
        # const factor to undo sqrt( sqrt(dim) ) basis normalization (at
        # least of Pauli products) and divide by 2# to be consistent with
        # convention:  rotn(theta) = exp(i theta/2 * PauliProduct ), with
        # theta in units of pi.
    
        dim = gatesetA.dim
        decomp[gl + ' angle'] = norm * (2.0/dim)**0.5 / _np.pi
        #Scratch...
        # 1Q dim=4 -> sqrt(2) / 2.0 = 1/sqrt(2) ^4= 1/4  ^2 = 1/2 = 2/dim
        # 2Q dim=16 -> 2.0 / 2.0 but need  1.0 / (2 sqrt(2)) ^4= 1/64 ^2= 1/8 = 2/dim
        # so formula that works for 1 & 2Q is sqrt(2/dim), perhaps
        # b/c convention is sigma-mxs in exponent, which are Pauli's/2.0 but our
        # normalized paulis are just /sqrt(2), so need to additionally divide by
        # sqrt(2)**nQubits == 2**(log2(dim)/4) == dim**0.25  ( nQubits = log2(dim)/2 )
        # and convention adds another sqrt(2)**nQubits / sqrt(2) => dim**0.5 / sqrt(2) (??)
    
        basis_mxs = mxBasis.get_composite_matrices()
        scalings = [ ( _np.linalg.norm(hamGens[i]) / _np.linalg.norm(_tools.hamiltonian_to_lindbladian(mx))
                       if _np.linalg.norm(hamGens[i]) > 1e-10 else 0.0 )
                     for i,mx in enumerate(basis_mxs) ]
        hamMx = sum([s*c*bmx for s,c,bmx in zip(scalings,hamProjs,basis_mxs)])
        decomp[gl + ' hamiltonian eigenvalues'] = _np.array(_np.linalg.eigvals(hamMx))

    for gl in gateLabels:
        for gl_other in gateLabels:            
            rotnAngle = decomp[gl + ' angle']
            rotnAngle_other = decomp[gl_other + ' angle']

            if gl == gl_other or abs(rotnAngle) < 1e-4 or abs(rotnAngle_other) < 1e-4:
                decomp[gl + "," + gl_other + " axis angle"] = 10000.0 #sentinel for irrelevant angle
    
            real_dot = _np.clip(
                _np.real(_np.dot(decomp[gl + ' axis'].flatten(),
                                 decomp[gl_other + ' axis'].flatten())),
            -1.0, 1.0)
            angle = _np.arccos( real_dot ) / _np.pi
            decomp[gl + "," + gl_other + " axis angle"] = angle

    return decomp
General_decomposition = _gsf.gatesetfn_factory(general_decomposition)
# init args == (gatesetA, gatesetB)


def average_gateset_infidelity(gatesetA, gatesetB): # B is target gateset usually but must be "gatesetB" b/c of decorator coding...
    from ..extras.rb import rbutils as _rbutils
    return _rbutils.average_gateset_infidelity(gatesetA,gatesetB)
Average_gateset_infidelity = _gsf.gatesetfn_factory(average_gateset_infidelity)
# init args == (gatesetA, gatesetB)


def predicted_rb_number(gatesetA, gatesetB):
    from ..extras.rb import rbutils as _rbutils
    return _rbutils.predicted_RB_number(gatesetA, gatesetB)
Predicted_rb_number = _gsf.gatesetfn_factory(predicted_rb_number)
# init args == (gatesetA, gatesetB)


#@_tools.parameterized
#def vectors_quantity(fnOfVectors, eps=FINITE_DIFF_EPS, verbosity=0):
#    """ For constructing a ReportableQty from a function of two vectors and a basis."""
#    # Since smart_cached is unparameterized, it needs no following parens
#    @_smart_cached # nested decorators = decOut(decIn(f(x)))
#    @_functools.wraps(fnOfVectors) # Retain metadata of wrapped function
#    def compute_quantity(label, gatesetA, gatesetB, typ='prep', confidenceRegionInfo=None):
#        assert typ in ['prep', 'effect'], 'type must be either "prep" or "effect", got {}'.format(typ)
#        mxBasis = gatesetA.basis
#        if typ == 'prep':
#            A = gatesetA.preps[label]
#            B = gatesetB.preps[label]
#        else:
#            A = gatesetA.effects[label]
#            B = gatesetB.effects[label]
#
#        if confidenceRegionInfo is None: # No Error bars
#            return _make_reportable_qty_or_dict( fnOfVectors(A, B, mxBasis) )
#
#        # make sure the gateset we're given is the one used to generate the confidence region
#        if(gatesetA.frobeniusdist(confidenceRegionInfo.get_gateset()) > 1e-6):
#            raise ValueError("Prep quantity confidence region is being requested for " +
#                             "a different gateset than the given confidenceRegionInfo")
#
#        nmEBs = bool(confidenceRegionInfo.get_errobar_type() == "non-markovian")
#        curriedFnOfVectors = _functools.partial(fnOfVectors, B=B, mxBasis=mxBasis)
#        if typ == 'prep':
#            df, f0 = confidenceRegionInfo.get_prep_fn_confidence_interval(curriedFnOfVectors, label,
#                                                                      eps, returnFnVal=True,
#                                                                      verbosity=verbosity)
#        else:
#            df, f0 = confidenceRegionInfo.get_effect_fn_confidence_interval(curriedFnOfVectors, label,
#                                                                      eps, returnFnVal=True,
#                                                                      verbosity=verbosity)
#        return _make_reportable_qty_or_dict(f0, df, nmEBs)
#
#    return compute_quantity

def vec_fidelity(A, B, mxBasis):
    rhoMx1 = _tools.vec_to_stdmx(A, mxBasis)
    rhoMx2 = _tools.vec_to_stdmx(B, mxBasis)
    return _tools.fidelity(rhoMx1, rhoMx2)
Vec_fidelity = _gsf.vecsfn_factory(vec_fidelity)
# init args == (gateset1, gateset2, label, typ)


def vec_infidelity(A, B, mxBasis):
    rhoMx1 = _tools.vec_to_stdmx(A, mxBasis)
    rhoMx2 = _tools.vec_to_stdmx(B, mxBasis)
    return 1 - _tools.fidelity(rhoMx1, rhoMx2)
Vec_infidelity = _gsf.vecsfn_factory(vec_infidelity)
# init args == (gateset1, gateset2, label, typ)


def vec_tr_diff(A, B, mxBasis): # assume vary gateset1, gateset2 fixed
    rhoMx1 = _tools.vec_to_stdmx(A, mxBasis)
    rhoMx2 = _tools.vec_to_stdmx(B, mxBasis)
    return _tools.tracedist(rhoMx1, rhoMx2)
Vec_tr_diff = _gsf.vecsfn_factory(vec_tr_diff)
# init args == (gateset1, gateset2, label, typ)


def labeled_data_rows(labels, confidenceRegionInfo, *reportableQtyLists):
    for items in zip(labels, *reportableQtyLists):
        # Python2 friendly unpacking
        label          = items[0]
        reportableQtys = items[1:]
        rowData = [label]
        if confidenceRegionInfo is None:
            rowData.extend([(reportableQty.get_value(), None) for reportableQty in reportableQtys])
        else:
            rowData.extend([reportableQty.get_value_and_err_bar() for reportableQty in reportableQtys])
        yield rowData
        

#@_tools.deprecated_fn(replacement='individual functions from the reportables module')
#def compute_gateset_gateset_qty(qtyname, gateset1, gateset2,
#                                confidenceRegionInfo=None):
#    """
#    Compute the named "GateSet vs. GateSet" quantity.
#
#    Parameters
#    ----------
#    qtyname : string
#        Name of the quantity to compute.
#
#    gateset1 : GateSet
#        First gate set used to compute the quantity.
#
#    gateset2 : GateSet
#        Second gate set used to compute the quantity.
#
#    confidenceRegionInfo : ConfidenceRegion, optional
#        If not None, specifies a confidence-region used to compute the error bars
#        contained in the returned quantity.  If None, then no error bars are
#        computed.
#
#    Returns
#    -------
#    ReportableQty
#        The quantity requested, or None if quantity could not be computed.
#    """
#    ret = compute_gateset_gateset_qtys( [qtyname], gateset1, gateset2, confidenceRegionInfo)
#    if qtyname is None: return ret
#    elif qtyname in ret: return ret[qtyname]
#    else: return None

# --------------------------------- OLD
#@_tools.deprecated_fn(replacement='individual functions from the reportables module')
#def compute_gateset_gateset_qtys(qtynames, gateset1, gateset2,
#                                 confidenceRegionInfo=None):
#    """
#    Compute the named "GateSet vs. GateSet" quantities.
#
#    Parameters
#    ----------
#    qtynames : list of strings
#        Names of the quantities to compute.
#
#    gateset1 : GateSet
#        First gate set used to compute the quantities.
#
#    gateset2 : GateSet
#        Second gate set used to compute the quantities.
#
#    confidenceRegionInfo : ConfidenceRegion, optional
#        If not None, specifies a confidence-region used to compute the error bars
#        contained in the returned quantities.  If None, then no error bars are
#        computed.
#
#    Returns
#    -------
#    dict
#        Dictionary whose keys are the requested quantity names and values are
#        ReportableQty objects.
#    """
#    print('compute_gateset_gateset_qtys:')
#    print(qtynames)
#    ret = _OrderedDict()
#    possible_qtys = [ ]
#    eps = FINITE_DIFF_EPS
#
#    for gateLabel in gateset1.gates:
#        if gateLabel not in gateset2.gates:
#            raise ValueError("%s gate is missing from second gateset - cannot compare gatesets", gateLabel)
#    for gateLabel in gateset2.gates:
#        if gateLabel not in gateset1.gates:
#            raise ValueError("%s gate is missing from first gateset - cannot compare gatesets", gateLabel)
#
#    mxBasis = gateset1.basis
#    if mxBasis.name != gateset2.basis.name:
#        raise ValueError("Basis mismatch: %s != %s" %
#                         (mxBasis.name, gateset2.basis.name))
#
#    ### per gate quantities
#    #############################################
#    for gateLabel in gateset1.gates:
#
#        key = '%s fidelity' % gateLabel; possible_qtys.append(key)
#        key2 = '%s infidelity' % gateLabel; possible_qtys.append(key)
#        if key in qtynames or key2 in qtynames:
#
#            def process_fidelity(gate):
#                return _tools.process_fidelity(gate, gateset2.gates[gateLabel], mxBasis)
#                  #vary elements of gateset1 (assume gateset2 is fixed)
#
#            #print "DEBUG: fidelity(%s)" % gateLabel
#            FQty = _getGateQuantity(process_fidelity, gateset1, gateLabel,
#                                    eps, confidenceRegionInfo)
#
#            InFQty = ReportableQty( 1.0-FQty.get_value(), FQty.get_err_bar() )
#            if key in qtynames: ret[key] = FQty
#            if key2 in qtynames: ret[key2] = InFQty
#
#        key = '%s closest unitary fidelity' % gateLabel; possible_qtys.append(key)
#        if key in qtynames:
#
#            #Note: default 'gm' basis
#            def closest_unitary_fidelity(gate): # assume vary gateset1, gateset2 fixed
#                decomp1 = _tools.decompose_gate_matrix(gate)
#                decomp2 = _tools.decompose_gate_matrix(gateset2.gates[gateLabel])
#
#                if decomp1['isUnitary']:
#                    closestUGateMx1 = gate
#                else: closestUGateMx1 = _alg.find_closest_unitary_gatemx(gate)
#
#                if decomp2['isUnitary']:
#                    closestUGateMx2 = gateset2.gates[gateLabel]
#                else: closestUGateMx2 = _alg.find_closest_unitary_gatemx(gateset2.gates[gateLabel])
#
#                closeChoi1 = _tools.jamiolkowski_iso(closestUGateMx1)
#                closeChoi2 = _tools.jamiolkowski_iso(closestUGateMx2)
#                return _tools.fidelity(closeChoi1,closeChoi2)
#
#            ret[key] = _getGateQuantity(closest_unitary_fidelity, gateset1, gateLabel, eps, confidenceRegionInfo)
#
#        key = "%s Frobenius diff" % gateLabel; possible_qtys.append(key)
#        if key in qtynames:
#            def fro_diff(gate): # assume vary gateset1, gateset2 fixed
#                return _tools.frobeniusdist(gate,gateset2.gates[gateLabel])
#            #print "DEBUG: frodist(%s)" % gateLabel
#            ret[key] = _getGateQuantity(fro_diff, gateset1, gateLabel, eps, confidenceRegionInfo)
#
#        key = "%s Jamiolkowski trace dist" % gateLabel; possible_qtys.append(key)
#        if key in qtynames:
#            def jt_diff(gate): # assume vary gateset1, gateset2 fixed
#                return _tools.jtracedist(gate,gateset2.gates[gateLabel], mxBasis)
#            #print "DEBUG: jtdist(%s)" % gateLabel
#            ret[key] = _getGateQuantity(jt_diff, gateset1, gateLabel, eps, confidenceRegionInfo)
#
#        key = '%s diamond norm' % gateLabel; possible_qtys.append(key)
#        if key in qtynames:
#
#            def half_diamond_norm(gate):
#                return 0.5 * _tools.diamonddist(gate, gateset2.gates[gateLabel], mxBasis)
#                  #vary elements of gateset1 (assume gateset2 is fixed)
#
#            try:
#                ret[key] = _getGateQuantity(half_diamond_norm, gateset1, gateLabel,
#                                            eps, confidenceRegionInfo)
#            except ImportError: #if failed to import cvxpy (probably b/c it's not installed)
#                ret[key] = ReportableQty(_np.nan) # report NAN for diamond norms
#
#        key = '%s angle btwn rotn axes' % gateLabel; possible_qtys.append(key)
#        if key in qtynames:
#
#            def angles_btwn_axes(gate): #Note: default 'gm' basis
#                decomp = _tools.decompose_gate_matrix(gate)
#                decomp2 = _tools.decompose_gate_matrix(gateset2.gates[gateLabel])
#                axisOfRotn = decomp.get('axis of rotation',None)
#                rotnAngle = decomp.get('pi rotations','X')
#                axisOfRotn2 = decomp2.get('axis of rotation',None)
#                rotnAngle2 = decomp2.get('pi rotations','X')
#
#                if rotnAngle == 'X' or abs(rotnAngle) < 1e-4 or \
#                   rotnAngle2 == 'X' or abs(rotnAngle2) < 1e-4:
#                    return _np.nan
#
#                if axisOfRotn is None or axisOfRotn2 is None:
#                    return _np.nan
#
#                real_dot =  _np.clip( _np.real(_np.dot(axisOfRotn,axisOfRotn2)), -1.0, 1.0)
#                return _np.arccos( abs(real_dot) ) / _np.pi
#                  #Note: abs() allows axis to be off by 180 degrees -- if showing *angle* as
#                  #      well, must flip sign of angle of rotation if you allow axis to
#                  #      "reverse" by 180 degrees.
#
#            ret[key] = _getGateQuantity(angles_btwn_axes, gateset1, gateLabel,
#                                    eps, confidenceRegionInfo)
#
#        key = '%s relative eigenvalues' % gateLabel; possible_qtys.append(key)
#        if key in qtynames:
#            def rel_eigvals(gate):
#                target_gate_inv = _np.linalg.inv(gateset2.gates[gateLabel])
#                rel_gate = _np.dot(target_gate_inv,gate)
#                return _np.linalg.eigvals(rel_gate)
#                  #vary elements of gateset1 (assume gateset2 is fixed)
#
#            ret[key] = _getGateQuantity(rel_eigvals, gateset1, gateLabel,
#                                        eps, confidenceRegionInfo)
#
#        key = '%s logTiG eigenvalues' % gateLabel; possible_qtys.append(key)
#        if key in qtynames:
#            def rel_logTiG_eigvals(gate):
#                rel_gate = _tools.error_generator(gate, gateset2.gates[gateLabel], gateset2.basis, "logTiG")
#                return _np.linalg.eigvals(rel_gate)
#                  #vary elements of gateset1 (assume gateset2 is fixed)
#
#            ret[key] = _getGateQuantity(rel_logTiG_eigvals, gateset1, gateLabel,
#                                        eps, confidenceRegionInfo)
#
#        key = '%s logG-logT eigenvalues' % gateLabel; possible_qtys.append(key)
#        if key in qtynames:
#            def rel_logGmlogT_eigvals(gate):
#                rel_gate = _tools.error_generator(gate, gateset2.gates[gateLabel], gateset2.basis, "logG-logT")
#                return _np.linalg.eigvals(rel_gate)
#                  #vary elements of gateset1 (assume gateset2 is fixed)
#
#            ret[key] = _getGateQuantity(rel_logGmlogT_eigvals, gateset1, gateLabel,
#                                        eps, confidenceRegionInfo)
#
#
#    ### per prep vector quantities
#    #############################################
#    for prepLabel in gateset1.get_prep_labels():
#
#        key = '%s prep state fidelity' % prepLabel; possible_qtys.append(key)
#        key2 = '%s prep state infidelity' % prepLabel; possible_qtys.append(key)
#        if key in qtynames or key2 in qtynames:
#
#            def fidelity(vec):
#                rhoMx1 = _tools.vec_to_stdmx(vec, mxBasis)
#                rhoMx2 = _tools.vec_to_stdmx(gateset2.preps[prepLabel], mxBasis)
#                return _tools.fidelity(rhoMx1, rhoMx2)
#                  #vary elements of gateset1 (assume gateset2 is fixed)
#
#            FQty = _getPrepQuantity(fidelity, gateset1, prepLabel,
#                                    eps, confidenceRegionInfo)
#
#            InFQty = ReportableQty( 1.0-FQty.get_value(), FQty.get_err_bar() )
#            if key in qtynames: ret[key] = FQty
#            if key2 in qtynames: ret[key2] = InFQty
#
#        key = "%s prep trace dist" % prepLabel; possible_qtys.append(key)
#        if key in qtynames:
#            def tr_diff(vec): # assume vary gateset1, gateset2 fixed
#                rhoMx1 = _tools.vec_to_stdmx(vec, mxBasis)
#                rhoMx2 = _tools.vec_to_stdmx(gateset2.preps[prepLabel], mxBasis)
#                return _tools.tracedist(rhoMx1, rhoMx2)
#            ret[key] = _getPrepQuantity(tr_diff, gateset1, prepLabel,
#                                        eps, confidenceRegionInfo)
#
#
#    ### per effect vector quantities
#    #############################################
#    for effectLabel in gateset1.get_effect_labels():
#
#        key = '%s effect state fidelity' % effectLabel; possible_qtys.append(key)
#        key2 = '%s effect state infidelity' % effectLabel; possible_qtys.append(key)
#        if key in qtynames or key2 in qtynames:
#
#            def fidelity(vec):
#                EMx1 = _tools.vec_to_stdmx(vec, mxBasis)
#                EMx2 = _tools.vec_to_stdmx(gateset2.effects[effectLabel], mxBasis)
#                return _tools.fidelity(EMx1,EMx2)
#                  #vary elements of gateset1 (assume gateset2 is fixed)
#
#            FQty = _getEffectQuantity(fidelity, gateset1, effectLabel,
#                                      eps, confidenceRegionInfo)
#
#            InFQty = ReportableQty( 1.0-FQty.get_value(), FQty.get_err_bar() )
#            if key in qtynames: ret[key] = FQty
#            if key2 in qtynames: ret[key2] = InFQty
#
#        key = "%s effect trace dist" % effectLabel; possible_qtys.append(key)
#        if key in qtynames:
#            def tr_diff(vec): # assume vary gateset1, gateset2 fixed
#                EMx1 = _tools.vec_to_stdmx(vec, mxBasis)
#                EMx2 = _tools.vec_to_stdmx(gateset2.effects[effectLabel], mxBasis)
#                return _tools.tracedist(EMx1, EMx2)
#            ret[key] = _getEffectQuantity(tr_diff, gateset1, effectLabel,
#                                          eps, confidenceRegionInfo)
#
#
#    ###  per gateset quantities
#    #############################################
#    key = "Gateset Frobenius diff"; possible_qtys.append(key)
#    if key in qtynames: ret[key] = ReportableQty( gateset1.frobeniusdist(gateset2) )
#
#    key = "Max Jamiolkowski trace dist"; possible_qtys.append(key)
#    if key in qtynames: ret[key] = ReportableQty(
#        max( [ _tools.jtracedist(gateset1.gates[l],gateset2.gates[l])
#               for l in gateset1.gates ] ) )
#
#
#    #Special case: when qtyname is None then return a list of all possible names that can be computed
#    if qtynames[0] is None:
#        return possible_qtys
#    return ret
