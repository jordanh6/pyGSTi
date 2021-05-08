class StochasticNoiseOp(LinearOperator):
    """
    A stochastic noise operation.

    Implements the stochastic noise map:
    `rho -> (1-sum(p_i))rho + sum_(i>0) p_i * B_i * rho * B_i^dagger`
    where `p_i > 0` and `sum(p_i) < 1`, and `B_i` is basis where `B_0` is the identity.

    In the case of the 'chp' evotype, the `B_i` element is returned with
    probability `p_i`, such that the outcome distribution matches the aforementioned
    stochastic noise map when considered over many samples.

    Parameters
    ----------
    dim : int
        The basis dimension of this operator (4 for a single qubit).

    basis : Basis or {'pp','gm','qt'}, optional
        The basis to use, defining the "principle axes"
        along which there is stochastic noise.  We assume that
        the first element of `basis` is the identity.

    evotype : {"densitymx", "cterm", "svterm"}
        the evolution type being used.

    initial_rates : list or array
        if not None, a list of `basis.size-1` initial error rates along each of
        the directions corresponding to each basis element.  If None,
        then all initial rates are zero.

    seed_or_state : float or RandomState, optional
        Random seed for RandomState (or directly provided RandomState)
        for sampling stochastic superoperators with the 'chp' evotype.
    """
    # Difficult to parameterize and maintain the p_i conditions - Initially just store positive p_i's
    # and don't bother restricting their sum to be < 1?

    def __init__(self, dim, basis="pp", evotype="densitymx", initial_rates=None, seed_or_state=None):
        """
        Create a new StochasticNoiseOp, representing a stochastic noise
        channel with possibly asymmetric noise but only noise that is
        "diagonal" in a particular basis (e.g. Pauli-stochastic noise).

        Parameters
        ----------
        dim : int
            The basis dimension of this operator (4 for a single qubit).

        basis : Basis or {'pp','gm','qt'}, optional
            The basis to use, defining the "principle axes"
            along which there is stochastic noise.  We assume that
            the first element of `basis` is the identity.
            This must be 'pp' for the 'chp' evotype.

        evotype : {"densitymx", "cterm", "svterm", "chp"}
            the evolution type being used.

        initial_rates : list or array
            if not None, a list of `dim-1` initial error rates along each of
            the directions corresponding to each basis element.  If None,
            then all initial rates are zero.

        seed_or_state : float or RandomState, optional
            Random seed for RandomState (or directly provided RandomState)
            for sampling stochastic superoperators with the 'chp' evotype.
        """
        if isinstance(seed_or_state, _RandomState):
            self.rand_state = seed_or_state
        else:
            self.rand_state = _RandomState(seed_or_state)

        if evotype in ['densitymx', 'cterm', 'svterm']:
            self.basis = _Basis.cast(basis, dim, sparse=False)  # sparse??
            assert(dim == self.basis.dim), "Dimension of `basis` must match the dimension (`dim`) of this op."

            self.stochastic_superops = []
            for b in self.basis.elements[1:]:
                std_superop = _lbt.nonham_lindbladian(b, b, sparse=False)
                self.stochastic_superops.append(_bt.change_basis(std_superop, 'std', self.basis))
        elif evotype == 'chp':
            assert (basis == 'pp'), "Only Pauli basis is allowed for 'chp' evotype"
            nqubits = (dim - 1).bit_length()

            self.basis = _Basis.cast(basis, 4**nqubits, sparse=False)

            std_chp_ops = _itgs.standard_gatenames_chp_conversions()

            # For CHP, need to make a Composed + EmbeddedOp for the super operators
            # For lower overhead, make this directly using the rep instead of with objects
            self.stochastic_superops = []
            for label in self.basis.labels[1:]:
                combined_chp_ops = []

                for i, pauli in enumerate(label):
                    name = 'Gi' if pauli == "I" else 'G%spi' % pauli.lower()
                    chp_op = std_chp_ops[name]
                    chp_op_targeted = [op.replace('0', str(i)) for op in chp_op]
                    combined_chp_ops.extend(chp_op_targeted)

                rep = replib.CHPOpRep(combined_chp_ops, nqubits)
                self.stochastic_superops.append(LinearOperator(rep, 'chp'))
        else:
            raise NotImplementedError('Evotype "%s" not available with StochasticNoiseOp' % evotype)

        #Setup initial parameters
        self.params = _np.zeros(self.basis.size - 1, 'd')  # note that basis.dim can be < self.dim (OK)
        if initial_rates is not None:
            assert(len(initial_rates) == self.basis.size - 1), \
                "Expected %d initial rates but got %d!" % (self.basis.size - 1, len(initial_rates))
            self.params[:] = self._rates_to_params(initial_rates)

        if evotype == "densitymx":  # for now just densitymx is supported
            rep = replib.DMOpRepDense(_np.ascontiguousarray(_np.identity(dim, 'd')))
        elif evotype == "chp":
            rep = dim
        else:
            raise ValueError("Invalid evotype '%s' for %s" % (evotype, self.__class__.__name__))

        LinearOperator.__init__(self, rep, evotype)
        self._update_rep()  # initialize self._rep
        self._paramlbls = _np.array(['sqrt(%s error rate)' % bl for bl in self.basis.labels[1:]], dtype=object)

    def _update_rep(self):
        # Create dense error superoperator from paramvec
        if self._evotype == "densitymx":
            errormap = _np.identity(self.dim)
            for rate, ss in zip(self._params_to_rates(self.params), self.stochastic_superops):
                errormap += rate * ss
            self._rep.base[:, :] = errormap

    def _rates_to_params(self, rates):
        return _np.sqrt(_np.array(rates))

    def _params_to_rates(self, params):
        return params**2

    def _get_rate_poly_dicts(self):
        """ Return a list of dicts, one per rate, expressing the
            rate as a polynomial of the local parameters (tuple
            keys of dicts <=> poly terms, e.g. (1,1) <=> x1^2) """
        return [{(i, i): 1.0} for i in range(self.basis.size - 1)]  # rates are just parameters squared

    def copy(self, parent=None, memo=None):
        """
        Copy this object.

        Parameters
        ----------
        parent : Model, optional
            The parent model to set for the copy.

        Returns
        -------
        StochasticNoiseOp
            A copy of this object.
        """
        if memo is not None and id(self) in memo: return memo[id(self)]
        copyOfMe = StochasticNoiseOp(self.dim, self.basis, self._evotype, self._params_to_rates(self.to_vector()))
        return self._copy_gpindices(copyOfMe, parent, memo)

    #to_dense / to_sparse?
    def to_dense(self):
        """
        Return this operation as a dense matrix.

        Returns
        -------
        numpy.ndarray
        """
        if self._evotype == 'densitymx':
            return self._rep.base  # copy?
        else:
            raise NotImplementedError('No to_dense implemented for evotype "%s"' % self._evotype)

    #def torep(self):
    #    """
    #    Return a "representation" object for this operation.
    #
    #    Such objects are primarily used internally by pyGSTi to compute
    #    things like probabilities more efficiently.
    #
    #    Returns
    #    -------
    #    OpRep
    #    """
    #    if self._evotype == "densitymx":
    #        return replib.DMOpRepDense(_np.ascontiguousarray(self.todense(), 'd'))
    #    else:
    #        raise ValueError("Invalid evotype '%s' for %s.torep(...)" %
    #                         (self._evotype, self.__class__.__name__))

    def taylor_order_terms(self, order, max_polynomial_vars=100, return_coeff_polys=False):
        """
        Get the `order`-th order Taylor-expansion terms of this operation.

        This function either constructs or returns a cached list of the terms at
        the given order.  Each term is "rank-1", meaning that its action on a
        density matrix `rho` can be written:

        `rho -> A rho B`

        The coefficients of these terms are typically polynomials of the operation's
        parameters, where the polynomial's variable indices index the *global*
        parameters of the operation's parent (usually a :class:`Model`), not the
        operation's local parameter array (i.e. that returned from `to_vector`).

        Parameters
        ----------
        order : int
            Which order terms (in a Taylor expansion of this :class:`LindbladOp`)
            to retrieve.

        max_polynomial_vars : int, optional
            maximum number of variables the created polynomials can have.

        return_coeff_polys : bool
            Whether a parallel list of locally-indexed (using variable indices
            corresponding to *this* object's parameters rather than its parent's)
            polynomial coefficients should be returned as well.

        Returns
        -------
        terms : list
            A list of :class:`RankOneTerm` objects.
        coefficients : list
            Only present when `return_coeff_polys == True`.
            A list of *compact* polynomial objects, meaning that each element
            is a `(vtape,ctape)` 2-tuple formed by concatenating together the
            output of :method:`Polynomial.compact`.
        """

        def _compose_poly_indices(terms):
            for term in terms:
                term.map_indices_inplace(lambda x: tuple(_modelmember._compose_gpindices(
                    self.gpindices, _np.array(x, _np.int64))))
            return terms

        IDENT = None  # sentinel for the do-nothing identity op
        mpv = max_polynomial_vars
        if order == 0:
            polydict = {(): 1.0}
            for pd in self._get_rate_poly_dicts():
                polydict.update({k: -v for k, v in pd.items()})  # subtracts the "rate" `pd` from `polydict`
            loc_terms = [_term.RankOnePolynomialOpTerm.create_from(_Polynomial(polydict, mpv),
                                                                   IDENT, IDENT, self._evotype)]

        elif order == 1:
            loc_terms = [_term.RankOnePolynomialOpTerm.create_from(_Polynomial(pd, mpv), bel, bel, self._evotype)
                         for i, (pd, bel) in enumerate(zip(self._get_rate_poly_dicts(), self.basis.elements[1:]))]
        else:
            loc_terms = []  # only first order "taylor terms"

        poly_coeffs = [t.coeff for t in loc_terms]
        tapes = [poly.compact(complex_coeff_tape=True) for poly in poly_coeffs]
        if len(tapes) > 0:
            vtape = _np.concatenate([t[0] for t in tapes])
            ctape = _np.concatenate([t[1] for t in tapes])
        else:
            vtape = _np.empty(0, _np.int64)
            ctape = _np.empty(0, complex)
        coeffs_as_compact_polys = (vtape, ctape)

        local_term_poly_coeffs = coeffs_as_compact_polys
        global_param_terms = _compose_poly_indices(loc_terms)

        if return_coeff_polys:
            return global_param_terms, local_term_poly_coeffs
        else:
            return global_param_terms

    @property
    def total_term_magnitude(self):
        """
        Get the total (sum) of the magnitudes of all this operator's terms.

        The magnitude of a term is the absolute value of its coefficient, so
        this function returns the number you'd get from summing up the
        absolute-coefficients of all the Taylor terms (at all orders!) you
        get from expanding this operator in a Taylor series.

        Returns
        -------
        float
        """
        # return exp( mag of errorgen ) = exp( sum of absvals of errgen term coeffs )
        # (unitary postfactor has weight == 1.0 so doesn't enter)
        rates = self._params_to_rates(self.to_vector())
        return _np.sum(_np.abs(rates))

    @property
    def total_term_magnitude_deriv(self):
        """
        The derivative of the sum of *all* this operator's terms.

        Computes the derivative of the total (sum) of the magnitudes of all this
        operator's terms with respect to the operators (local) parameters.

        Returns
        -------
        numpy array
            An array of length self.num_params
        """
        # abs(rates) = rates = params**2
        # so d( sum(abs(rates)) )/dparam_i = 2*param_i
        return 2 * self.to_vector()

    def get_chp_str(self, targets=None):
        """Return a string suitable for printing to a CHP input file after stochastically selecting operation.

        Parameters
        ----------
        targets: list of int
            Qubits to be applied to (if None, uses stored CHP strings directly)

        Returns
        -------
        s : str
            String of CHP code
        """
        assert (self._evotype == 'chp'), "Must have 'chp' evotype to use get_chp_str"

        rates = self._params_to_rates(self.to_vector())
        all_rates = [*rates, 1.0 - sum(rates)]  # Include identity so that probabilities are 1
        index = self.rand_state.choice(self.basis.size, p=all_rates)

        # If first entry, no operation selected
        if index == self.basis.size - 1:
            return ''

        op = self.stochastic_superops[index]
        chp_ops = op._rep.chp_ops
        nqubits = op._rep.nqubits

        if targets is not None:
            assert len(targets) == nqubits, "Got {0} targets instead of required {1}".format(len(targets), nqubits)
            target_map = {str(i): str(t) for i, t in enumerate(targets)}

        s = ""
        for op in chp_ops:
            # Substitute if alternate targets provided
            if targets is not None:
                op_str = ''.join([target_map[c] if c in target_map else c for c in op])
            else:
                op_str = op

            s += op_str + '\n'

        return s

    @property
    def num_params(self):
        """
        Get the number of independent parameters which specify this operation.

        Returns
        -------
        int
            the number of independent parameters.
        """
        return len(self.to_vector())

    def to_vector(self):
        """
        Extract a vector of the underlying operation parameters from this operation.

        Returns
        -------
        numpy array
            a 1D numpy array with length == num_params().
        """
        return self.params

    def from_vector(self, v, close=False, dirty_value=True):
        """
        Initialize the operation using a vector of parameters.

        Parameters
        ----------
        v : numpy array
            The 1D vector of operation parameters.  Length
            must == num_params()

        close : bool, optional
            Whether `v` is close to this operation's current
            set of parameters.  Under some circumstances, when this
            is true this call can be completed more quickly.

        dirty_value : bool, optional
            The value to set this object's "dirty flag" to before exiting this
            call.  This is passed as an argument so it can be updated *recursively*.
            Leave this set to `True` unless you know what you're doing.

        Returns
        -------
        None
        """
        self.params[:] = v
        self._update_rep()
        self.dirty = dirty_value

    #Transform functions? (for gauge opt)

    def __str__(self):
        s = "Stochastic noise operation map with dim = %d, num params = %d\n" % \
            (self.dim, self.num_params)
        s += 'Rates: %s\n' % self._params_to_rates(self.to_vector())
        return s
