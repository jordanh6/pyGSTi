from __future__ import division, print_function, absolute_import, unicode_literals
#*****************************************************************
#    pyGSTi 0.9:  Copyright 2015 Sandia Corporation
#    This Software is released under the GPL license detailed
#    in the file "license.txt" in the top-level pyGSTi directory
#*****************************************************************
""" Defines the Estimate class."""

import numpy       as _np
import collections as _collections
import warnings    as _warnings
import time        as _time

from .. import tools as _tools
from .confidenceregionfactory import ConfidenceRegionFactory as _ConfidenceRegionFactory

#Class for holding confidence region factory keys
CRFkey = _collections.namedtuple('CRFkey', ['gateset','gatestring_list'])

class Estimate(object):
    """
    A class encapsulating the `GateSet` objects related to 
    a single GST estimate up-to-gauge freedoms. 

    Thus, this class holds the "iteration" `GateSet`s leading up to a
    final `GateSet`, and then different gauge optimizations of the final
    set.
    """
    
    def __init__(self, parent, targetGateset=None, seedGateset=None,
                 gatesetsByIter=None, parameters=None):
        """
        Initialize an empty Estimate object.

        Parameters
        ----------
        parent : Results
            The parent Results object containing the dataset and
            gate string structure used for this Estimate.

        targetGateset : GateSet
            The target gateset used when optimizing the objective.

        seedGateset : GateSet
            The initial gateset used to seed the iterative part
            of the objective optimization.  Typically this is
            obtained via LGST.

        gatesetsByIter : list of GateSets
            The estimated gateset at each GST iteration. Typically these are the
            estimated gate sets *before* any gauge optimization is performed.

        parameters : dict
            A dictionary of parameters associated with how these gate sets
            were obtained.
        """
        self.parent = parent
        self.parameters = _collections.OrderedDict()
        self.goparameters = _collections.OrderedDict()
        self.gatesets = _collections.OrderedDict()
        self.confidence_region_factories = _collections.OrderedDict()

        #Set gatesets
        if targetGateset: self.gatesets['target'] = targetGateset
        if seedGateset: self.gatesets['seed'] = seedGateset
        if gatesetsByIter:
            self.gatesets['iteration estimates'] = gatesetsByIter
            self.gatesets['final iteration estimate'] = gatesetsByIter[-1]

        #Set parameters
        if isinstance(parameters, _collections.OrderedDict):
            self.parameters = parameters
        elif parameters is not None:
            for key in sorted(list(parameters.keys())):
                self.parameters[key] = parameters[key]

                
    def add_gaugeoptimized(self, goparams, gateset=None, label=None):
        """
        Adds a gauge-optimized GateSet (computing it if needed) to this object.

        Parameters
        ----------
        goparams : dict
            A dictionary of gauge-optimization parameters, typically arguments
            to :func:`gaugeopt_to_target`, specifying how the gauge optimization
            was (or should be) performed.  When `gateset` is `None` (and this
            function computes the gate set internally) the keys and values of
            this dictionary must correspond to allowed arguments of 
            :func:`gaugeopt_to_target`. By default, :func:`gaugeopt_to_target`'s
            first two arguments, the `GateSet` to optimize and the target,
            are taken to be `self.gatesets['final iteration estimate']` and 
            self.gatesets['target'].

        gateset : GateSet, optional
            The gauge-optimized gate set to store.  If None, then this gate set
            is computed by calling :func:`gaugeopt_to_target` with the contents
            of `goparams` as arguments as described above.

        label : str, optional
            A label for this gauge-optimized gate set, used as the key in
            this object's `gatesets` and `goparameters` member dictionaries.
            If None, then the next available "go<X>", where <X> is a 
            non-negative integer, is used as the label.

        Returns
        -------
        None
        """

        if label is None:
            i = 0
            while True:
                label = "go%d" % i; i += 1
                if (label not in self.goparameters) and \
                   (label not in self.gatesets): break

        if gateset is None:
            from ..algorithms   import gaugeopt_to_target   as _gaugeopt_to_target
            goparams = goparams.copy() #so we don't change the caller's dict
            
            if "gateset" not in goparams:
                if 'final iteration estimate' in self.gatesets:
                    goparams["gateset"] = self.gatesets['final iteration estimate']
                else: raise ValueError("Must supply 'gateset' in 'goparams' argument")
                
            if "targetGateset" not in goparams:
                if 'target' in self.gatesets:
                    goparams["targetGateset"] = self.gatesets['target']
                else: raise ValueError("Must supply 'targetGateset' in 'goparams' argument")

            goparams['returnAll'] = True
            starting_gateset = goparams["gateset"].copy()
            minF, gaugeGroupEl, gateset = _gaugeopt_to_target(**goparams)
            goparams['_gaugeGroupEl'] = gaugeGroupEl # an output stored here for convenience
            
        #sort the parameters by name for consistency
        ordered_goparams = _collections.OrderedDict( 
            [(k,goparams[k]) for k in sorted(list(goparams.keys()))])

        self.gatesets[label] = gateset
        self.goparameters[label] = ordered_goparams

    def add_confidence_region_factory(self, gateset_label='final iteration estimate', gatestrings_label='final'):
        ky = CRFkey(gateset_label, gatestrings_label)
        if ky in self.confidence_region_factories:
            _warnings.warn("Confidence region factory for %s already exists - overwriting!" % str(ky))
            
        newCRF = _ConfidenceRegionFactory(self, gateset_label, gatestrings_label)
        self.confidence_region_factories[ky] = newCRF
        return newCRF
                                                                                    

    def get_confidence_region_factory(self, gateset_label, gatestrings_label='final', createIfNeeded=False):
        ky = CRFkey(gateset_label, gatestrings_label)
        if ky in self.confidence_region_factories:
            return self.confidence_region_factories[ky]
        elif createIfNeeded:
            return self.add_confidence_region_factory(gateset_label, gatestrings_label)
        else:
            raise KeyError("No confidence region factory for key %s exists!" % str(ky))
        
    def gauge_propagate_confidence_region_factory(
            self, to_gateset_label, from_gateset_label='final iteration estimate',
            gatestrings_label = 'final', EPS=1e-3):
        """
        Propagates an existing "reference" confidence region for some GateSet
        "G0" to a new confidence region for a gauge-equivalent gateset "G1".

        When successful, a new confidence region will be created for the 
        gauge-optimized gate set given by `label` and stored internally, as well
        as returned.

        Parameters
        ----------
        label : str
            The key into this `Estimate` object's `gatesets` and `goparameters`
            dictionaries that identifies a gauge optimization result.  This 
            gauge optimization must have begun at the reference gateset, i.e.,
            `gatesets[from_gateset_label]` must equal (by frobeinus distance)
            `goparameters[to_gateset_label]['gateset']`.

        confidenceLevel : float, optional
            The confidence level as a percentage (0-100) of the reference
            confidence region being propagated.

        ref_gateset_key : str, optional
            The key within `gatesets` of the reference gate set.

        EPS : float, optional
            A small offset used for constructing finite-difference derivatives.
            Usually the default value is fine.

        Returns
        -------
        ConfidenceRegionFactory
            Note: this region is also stored internally and as such the return
            value of this function can often be ignored.
        """
        ref_gateset = self.gatesets[from_gateset_label]
        goparams = self.goparameters[to_gateset_label]
        start_gateset = goparams['gateset'].copy()
        final_gateset = self.gatesets[to_gateset_label].copy()

        assert('_gaugeGroupEl' in goparams),"To propagate a confidence " + \
            "region, goparameters must contain the gauge-group-element as `_gaugeGroupEl`"
        gaugeGroupEl = goparams['_gaugeGroupEl']

        assert(start_gateset.frobeniusdist(ref_gateset) < 1e-6), \
            "Gauge-opt starting point must be the 'from' (reference) GateSet"
        
        crf = self.confidence_region_factories.get(
            CRFkey(from_gateset_label, gatestrings_label), None)
            
        assert(crf is not None), "Initial confidence region factory doesn't exist!"
        assert(crf.has_hessian()), "Initial factory must contain a computed Hessian!"
                            
        #Update hessian by TMx = d(diffs in current go'd gateset)/d(diffs in ref gateset)
        TMx = _np.empty( (final_gateset.num_params(), ref_gateset.num_params()), 'd' )
        v0, w0 = ref_gateset.to_vector(), final_gateset.to_vector()
        gs = ref_gateset.copy()
        for iCol in range(ref_gateset.num_params()):
            v = v0.copy(); v[iCol] += EPS # dv is along iCol-th direction 
            gs.from_vector(v)
            gs.transform(gaugeGroupEl)
            w = gs.to_vector()
            dw = (w - w0)/EPS
            if iCol % 10 == 0: print("DB: col %d/%d: %g" % (iCol, ref_gateset.num_params(),_np.linalg.norm(dw)))
            TMx[:,iCol] = dw

        rank = _np.linalg.matrix_rank(TMx)
        #print("DEBUG: constructed TMx: rank = ", rank)
        
        # Hessian is gauge-transported via H -> TMx_inv^T * H * TMx_inv
        TMx_inv = _np.linalg.inv(TMx)
        new_hessian = _np.dot(TMx_inv.T, _np.dot(crf.hessian, TMx_inv))

        #Create a new confidence region based on the new hessian
        new_crf = _ConfidenceRegionFactory(self, to_gateset_label,
                                           gatestrings_label, new_hessian,
                                           crf.nonMarkRadiusSq)
        self.confidence_region_factories[CRFkey(to_gateset_label, gatestrings_label)] = new_crf
        print("DEBUG: Done transporting CI.  Success!")

        return new_crf


    def get_effective_dataset(self, return_subMxs=False):
        """
        Generate a `DataSet` containing the effective counts as dictated by
        the "weights" parameter, which specifies a dict of gate string weights.

        This function rescales the actual data contained in this Estimate's
        parent `Results` object according to the estimate's "weights" parameter.
        The scaled data set is returned, along with (optionall) a list-of-lists
        of matrices containing the scaling values which can be easily plotted
        via a `ColorBoxPlot`.

        Parameters
        ----------
        return_subMxs : boolean
            If true, also return a list-of-lists of matrices containing the
            scaling values, as described above.

        Returns
        -------
        ds : DataSet
            The "effective" (scaled) data set.

        subMxs : list-of-lists
            Only returned if `return_subMxs == True`.  Contains the
            scale values (see above).
        """
        p = self.parent
        gss = p.gatestring_structs['final'] #FUTURE: overrideable?
        weights = self.parameters.get("weights",None)
        
        if weights is not None:
            scaled_dataset = p.dataset.copy_nonstatic()

            subMxs = []
            for y in gss.used_yvals():
                subMxs.append( [] )
                for x in gss.used_xvals():
                    plaq = gss.get_plaquette(x,y).expand_aliases()
                    scalingMx = _np.nan * _np.ones( (plaq.rows,plaq.cols), 'd')
                    
                    for i,j,gstr in plaq:
                        scalingMx[i,j] = weights.get(gstr,1.0)
                        if scalingMx[i,j] != 1.0:
                            scaled_dataset[gstr].scale(scalingMx[i,j])

                    #build up a subMxs list-of-lists as a plotting
                    # function does, so we can easily plot the scaling
                    # factors in a color box plot.
                    subMxs[-1].append(scalingMx)

            scaled_dataset.done_adding_data()
            if return_subMxs:
                return scaled_dataset, subMxs
            else: return scaled_dataset
            
        else: #no weights specified - just return original dataset (no scaling)
            
            if return_subMxs: #then need to create subMxs with all 1's
                subMxs = []
                for y in gss.used_yvals():
                    subMxs.append( [] )
                    for x in gss.used_xvals():
                        plaq = gss.get_plaquette(x,y)
                        scalingMx = _np.nan * _np.ones( (plaq.rows,plaq.cols), 'd')
                        for i,j,gstr in plaq:
                            scalingMx[i,j] = 1.0
                        subMxs[-1].append( scalingMx )
                return p.dataset, subMxs #copy dataset?
            else:
                return p.dataset

    def misfit_sigma(self):
        """
        Returns the number of standard deviations (sigma) of model violation.

        Returns
        -------
        float
        """
        p = self.parent
        obj = self.parameters.get('objective',None)
        assert(obj in ('chi2','logl')),"Invalid objective!"

        gs = self.gatesets['final iteration estimate'] #FUTURE: overrideable?
        gss = p.gatestring_structs['final'] #FUTURE: overrideable?
        mpc = self.parameters.get('minProbClipForWeighting',1e-4)
        ds = self.get_effective_dataset()
        
        if obj == "chi2":
            fitQty = _tools.chi2( ds, gs, gss.allstrs,
                                  minProbClipForWeighting=mpc,
                                  gateLabelAliases=gss.aliases)
        elif obj == "logl":
            logL_upperbound = _tools.logl_max(ds, gss.allstrs, gateLabelAliases=gss.aliases)
            logl = _tools.logl( gs, ds, gss.allstrs, gateLabelAliases=gss.aliases)
            fitQty = 2*(logL_upperbound - logl) # twoDeltaLogL
            
        Ns = len(gss.allstrs)*(len(ds.get_spam_labels())-1) #number of independent parameters in dataset
        Np = gs.num_params() #don't bother with non-gauge only here [FUTURE: add option for this?]
        k = max(Ns-Np,1) #expected chi^2 or 2*(logL_ub-logl) mean
        if Ns <= Np: _warnings.warn("Max-model params (%d) <= gate set params (%d)!  Using k == 1." % (Ns,Np))
        return (fitQty-k)/_np.sqrt(2*k)



    def copy(self):
        """ Creates a copy of this Estimate object. """
        #TODO: check whether this deep copies (if we want it to...) - I expect it doesn't currently
        cpy = Estimate()
        cpy.parameters = self.parameters.copy()
        cpy.goparameters = self.goparameters.copy()
        cpy.gatesets = self.gatesets.copy()
        cpy.confidence_region_factories = self.confidence_regions.copy()
        return cpy

    def __str__(self):
        s  = "----------------------------------------------------------\n"
        s += "---------------- pyGSTi Estimate Object ------------------\n"
        s += "----------------------------------------------------------\n"
        s += "\n"
        s += "How to access my contents:\n\n"
        s += " .gatesets   -- a dictionary of GateSet objects w/keys:\n"
        s += " ---------------------------------------------------------\n"
        s += "  " + "\n  ".join(list(self.gatesets.keys())) + "\n"
        s += "\n"        
        s += " .parameters   -- a dictionary of simulation parameters:\n"
        s += " ---------------------------------------------------------\n"
        s += "  " + "\n  ".join(list(self.parameters.keys())) + "\n"
        s += "\n"
        s += " .goparameters   -- a dictionary of gauge-optimization parameter dictionaries:\n"
        s += " ---------------------------------------------------------\n"
        s += "  " + "\n  ".join(list(self.goparameters.keys())) + "\n"
        s += "\n"
        return s
    
    def __getstate__(self):
        # don't pickle parent (will create circular reference)
        to_pickle = self.__dict__.copy()
        del to_pickle['parent'] 
        return  to_pickle

    def __setstate__(self, stateDict):
        self.__dict__.update(stateDict)
        for crf in self.confidence_region_factories.values():
            crf.set_parent(self)
        self.parent = None # initialize to None upon unpickling

    def set_parent(self, parent):
        """
        Sets the parent Results object of this Estimate.
        """
        self.parent = parent
     

