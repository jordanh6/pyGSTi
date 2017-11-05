from __future__ import division, print_function, absolute_import, unicode_literals
#*****************************************************************
#    pyGSTi 0.9:  Copyright 2015 Sandia Corporation
#    This Software is released under the GPL license detailed
#    in the file "license.txt" in the top-level pyGSTi directory
#*****************************************************************
"""
Variables for working with the 2-qubit gate set containing the gates
I*X(pi/2), I*Y(pi/2), X(pi/2)*I, Y(pi/2)*I, and CPHASE.
"""

import numpy as _np
from . import gatestringconstruction as _strc
from . import gatesetconstruction as _setc
from . import spamspecconstruction as _spamc
from ..tools import gatetools as _gt

description = "I*X(pi/2), I*Y(pi/2), X(pi/2)*I, Y(pi/2)*I, and CPHASE gates"

gates = ['Gix','Giy','Gxi','Gyi','Gcphase']

fiducials16 = _strc.gatestring_list(
    [ (), ('Gix',), ('Giy',), ('Gix','Gix'),
      ('Gxi',), ('Gxi','Gix'), ('Gxi','Giy'), ('Gxi','Gix','Gix'),
      ('Gyi',), ('Gyi','Gix'), ('Gyi','Giy'), ('Gyi','Gix','Gix'),
      ('Gxi','Gxi'), ('Gxi','Gxi','Gix'), ('Gxi','Gxi','Giy'), ('Gxi','Gxi','Gix','Gix') ] )

fiducials36 = _strc.gatestring_list(
    [ (), ('Gix',), ('Giy',), ('Gix','Gix'), ('Gix','Gix','Gix'), ('Giy','Giy','Giy'),
      ('Gxi',), ('Gxi','Gix'), ('Gxi','Giy'), ('Gxi','Gix','Gix'), ('Gxi','Gix','Gix','Gix'), ('Gxi','Giy','Giy','Giy'),
      ('Gyi',), ('Gyi','Gix'), ('Gyi','Giy'), ('Gyi','Gix','Gix'), ('Gyi','Gix','Gix','Gix'), ('Gyi','Giy','Giy','Giy'),
      ('Gxi','Gxi'), ('Gxi','Gxi','Gix'), ('Gxi','Gxi','Giy'), ('Gxi','Gxi','Gix','Gix'), ('Gxi','Gxi','Gix','Gix','Gix'),
      ('Gxi','Gxi','Giy','Giy','Giy'), ('Gxi','Gxi','Gxi'), ('Gxi','Gxi','Gxi','Gix'), ('Gxi','Gxi','Gxi','Giy'),
      ('Gxi','Gxi','Gxi','Gix','Gix'), ('Gxi','Gxi','Gxi','Gix','Gix','Gix'), ('Gxi','Gxi','Gxi','Giy','Giy','Giy'),
      ('Gyi','Gyi','Gyi'), ('Gyi','Gyi','Gyi','Gix'), ('Gyi','Gyi','Gyi','Giy'), ('Gyi','Gyi','Gyi','Gix','Gix'),
      ('Gyi','Gyi','Gyi','Gix','Gix','Gix'), ('Gyi','Gyi','Gyi','Giy','Giy','Giy') ] )

fiducials = fiducials16
prepStrs = fiducials16

effectStrs = _strc.gatestring_list(
    [(), ('Gix',), ('Giy',), 
     ('Gix','Gix'), ('Gxi',), 
     ('Gyi',), ('Gxi','Gxi'), 
     ('Gxi','Gix'), ('Gxi','Giy'), 
     ('Gyi','Gix'), ('Gyi','Giy')] )

legacy_germs = _strc.gatestring_list(
[ ('Gii',),
  ('Gxi',),
  ('Gyi',),
  ('Gix',),
  ('Giy',),
  ('Gxi', 'Gyi'),
  ('Gix', 'Giy'),
  ('Gxi', 'Gcphase'),
  ('Gix', 'Gcphase'),
  ('Gix', 'Gyi'),
  ('Gix', 'Gxi'),
  ('Gxi', 'Gyi', 'Gii'),
  ('Gxi', 'Gii', 'Gyi'),
  ('Gxi', 'Gii', 'Gii'),
  ('Gyi', 'Gii', 'Gii'),
  ('Gix', 'Giy', 'Gii'),
  ('Gix', 'Gii', 'Giy'),
  ('Gix', 'Gii', 'Gii'),
  ('Giy', 'Gii', 'Gii'),
  ('Gix', 'Gyi', 'Gcphase'),
  ('Giy', 'Gcphase', 'Gyi'),
  ('Giy', 'Gxi', 'Gcphase'),
  ('Gyi', 'Gyi', 'Gcphase'),
  ('Gix', 'Gcphase', 'Gyi'),
  ('Gix', 'Gyi', 'Giy'),
  ('Gix', 'Gcphase', 'Gxi'),
  ('Gii', 'Gcphase', 'Gcphase'),
  ('Giy', 'Gyi', 'Gcphase'),
  ('Gii', 'Giy', 'Gxi'),
  ('Gxi', 'Gcphase', 'Gcphase'),
  ('Gix', 'Gcphase', 'Gcphase'),
  ('Gix', 'Gyi', 'Gxi'),
  ('Gii', 'Gcphase', 'Giy'),
  ('Gix', 'Gcphase', 'Giy'),
  ('Gii', 'Giy', 'Gyi'),
  ('Gxi', 'Gxi', 'Gii', 'Gyi'),
  ('Gxi', 'Gyi', 'Gyi', 'Gii'),
  ('Gix', 'Gix', 'Gii', 'Giy'),
  ('Gix', 'Giy', 'Giy', 'Gii'),
  ('Gcphase', 'Gcphase', 'Giy', 'Gcphase'),
  ('Giy', 'Gcphase', 'Gxi', 'Giy'),
  ('Giy', 'Gix', 'Gyi', 'Giy'),
  ('Gyi', 'Gix', 'Gix', 'Gcphase', 'Gxi'),
  ('Gix', 'Gcphase', 'Gxi', 'Gxi', 'Giy'),
  ('Gyi', 'Gyi', 'Giy', 'Gcphase', 'Giy'),
  ('Gcphase', 'Gcphase', 'Gcphase', 'Gix', 'Gxi'),
  ('Giy', 'Gxi', 'Gcphase', 'Gxi', 'Gxi'),
  ('Gyi', 'Gcphase', 'Giy', 'Gix', 'Giy'),
  ('Gyi', 'Gcphase', 'Gix', 'Gyi', 'Gxi'),
  ('Gcphase', 'Gix', 'Gyi', 'Gii', 'Gii'),
  ('Gcphase', 'Gyi', 'Giy', 'Gcphase', 'Gyi'),
  ('Gxi', 'Gxi', 'Gyi', 'Gxi', 'Gyi', 'Gyi'),
  ('Gix', 'Gix', 'Giy', 'Gix', 'Giy', 'Giy'),
  ('Gxi', 'Giy', 'Giy', 'Gyi', 'Giy', 'Gcphase'),
  ('Gyi', 'Gxi', 'Giy', 'Gyi', 'Gcphase', 'Gyi'),
  ('Gcphase', 'Gyi', 'Gii', 'Gix', 'Gxi', 'Gix'),
  ('Gix', 'Gyi', 'Giy', 'Giy', 'Gxi', 'Gxi'),
  ('Gyi', 'Gcphase', 'Gii', 'Gix', 'Gxi', 'Gii'),
  ('Gcphase', 'Gii', 'Gxi', 'Gyi', 'Gyi', 'Giy'),
  ('Gcphase', 'Gii', 'Gxi', 'Gcphase', 'Gix', 'Gxi'),
  ('Gxi', 'Gyi', 'Gyi', 'Gcphase', 'Gix', 'Gix', 'Giy'),
  ('Gcphase', 'Gcphase', 'Gcphase', 'Gxi', 'Gix', 'Gii', 'Giy'),
  ('Giy', 'Gxi', 'Gxi', 'Gcphase', 'Gii', 'Gxi', 'Gxi'),
  ('Gyi', 'Gii', 'Giy', 'Gyi', 'Gcphase', 'Gxi', 'Gii'),
  ('Gix', 'Giy', 'Gix', 'Gyi', 'Gxi', 'Gii', 'Gxi'),
  ('Gxi', 'Giy', 'Gix', 'Gcphase', 'Giy', 'Gix', 'Gii'),
  ('Giy', 'Gxi', 'Gyi', 'Gxi', 'Gcphase', 'Gyi', 'Gix'),
  ('Giy', 'Giy', 'Gix', 'Gii', 'Gix', 'Gxi', 'Gxi'),
  ('Gii', 'Gyi', 'Gxi', 'Gcphase', 'Gcphase', 'Gix', 'Gcphase'),
  ('Gcphase', 'Gyi', 'Gcphase', 'Gix', 'Gxi', 'Gcphase', 'Gxi', 'Gcphase'),
  ('Giy', 'Gcphase', 'Gxi', 'Gcphase', 'Gix', 'Gxi', 'Gxi', 'Gyi'),
  ('Gxi', 'Giy', 'Giy', 'Giy', 'Gcphase', 'Gix', 'Gyi', 'Gyi'),
  ('Gii', 'Gii', 'Gcphase', 'Gxi', 'Gix', 'Gxi', 'Gix', 'Gyi'),
  ('Gxi', 'Giy', 'Gix', 'Gcphase', 'Gii', 'Gyi', 'Gyi', 'Giy'),
  ('Gyi', 'Gyi', 'Gcphase', 'Gxi', 'Gix', 'Gyi', 'Gix', 'Gyi'),
  ('Gii', 'Giy', 'Gix', 'Gcphase', 'Gcphase', 'Gii', 'Gyi', 'Gxi'),
  ('Gix', 'Gii', 'Gxi', 'Gix', 'Gii', 'Giy', 'Gxi', 'Gii')
  ])

germs = _strc.gatestring_list(
[ ('Gii',),
  ('Gxi',),
  ('Gyi',),
  ('Gix',),
  ('Giy',),
  ('Gcphase',),
  ('Gxi', 'Gyi'),
  ('Gix', 'Giy'),
  ('Giy', 'Gyi'),
  ('Gix', 'Gyi'),
  ('Gyi', 'Gcphase'),
  ('Giy', 'Gcphase'),
  ('Gxi', 'Gyi', 'Gii'),
  ('Gxi', 'Gii', 'Gyi'),
  ('Gxi', 'Gii', 'Gii'),
  ('Gyi', 'Gii', 'Gii'),
  ('Gix', 'Giy', 'Gii'),
  ('Gix', 'Gii', 'Giy'),
  ('Gix', 'Gii', 'Gii'),
  ('Giy', 'Gii', 'Gii'),
  ('Gxi', 'Gcphase', 'Gcphase'),
  ('Giy', 'Gxi', 'Gcphase'),
  ('Giy', 'Gcphase', 'Gyi'),
  ('Giy', 'Gyi', 'Gcphase'),
  ('Gix', 'Gxi', 'Gcphase'),
  ('Giy', 'Giy', 'Gcphase'),
  ('Giy', 'Gcphase', 'Gxi'),
  ('Gix', 'Giy', 'Gcphase'),
  ('Giy', 'Gxi', 'Gyi'),
  ('Gix', 'Giy', 'Gyi'),
  ('Gii', 'Gxi', 'Gix'),
  ('Gxi', 'Gxi', 'Gii', 'Gyi'),
  ('Gxi', 'Gyi', 'Gyi', 'Gii'),
  ('Gix', 'Gix', 'Gii', 'Giy'),
  ('Gix', 'Giy', 'Giy', 'Gii'),
  ('Gyi', 'Gyi', 'Gyi', 'Gxi'),
  ('Giy', 'Giy', 'Giy', 'Gix'),
  ('Gxi', 'Gyi', 'Gix', 'Giy'),
  ('Gcphase', 'Gix', 'Gyi', 'Gyi'),
  ('Gcphase', 'Gix', 'Gix', 'Gcphase'),
  ('Gxi', 'Gcphase', 'Gyi', 'Gyi'),
  ('Gyi', 'Gyi', 'Gyi', 'Gix'),
  ('Gii', 'Giy', 'Gxi', 'Gcphase'),
  ('Gyi', 'Gii', 'Giy', 'Gii'),
  ('Giy', 'Gii', 'Gcphase', 'Gii'),
  ('Gix', 'Gix', 'Giy', 'Gcphase', 'Gcphase'),
  ('Gcphase', 'Giy', 'Giy', 'Gix', 'Giy'),
  ('Gyi', 'Gcphase', 'Gix', 'Giy', 'Gyi'),
  ('Giy', 'Gxi', 'Gcphase', 'Gxi', 'Gcphase'),
  ('Gyi', 'Gcphase', 'Gxi', 'Gcphase', 'Gxi'),
  ('Gcphase', 'Gix', 'Gyi', 'Gii', 'Gii'),
  ('Gxi', 'Gxi', 'Gyi', 'Gxi', 'Gyi', 'Gyi'),
  ('Gix', 'Gix', 'Giy', 'Gix', 'Giy', 'Giy'),
  ('Gyi', 'Gxi', 'Gyi', 'Gxi', 'Gxi', 'Gxi'),
  ('Gyi', 'Gxi', 'Gyi', 'Gyi', 'Gxi', 'Gxi'),
  ('Gyi', 'Gyi', 'Gyi', 'Gxi', 'Gyi', 'Gxi'),
  ('Giy', 'Gix', 'Giy', 'Gix', 'Gix', 'Gix'),
  ('Giy', 'Gix', 'Giy', 'Giy', 'Gix', 'Gix'),
  ('Giy', 'Giy', 'Giy', 'Gix', 'Giy', 'Gix'),
  ('Gcphase', 'Gyi', 'Giy', 'Gxi', 'Gix', 'Gcphase'),
  ('Gxi', 'Giy', 'Gxi', 'Gcphase', 'Gyi', 'Gix'),
  ('Gxi', 'Giy', 'Giy', 'Giy', 'Gcphase', 'Gxi'),
  ('Gcphase', 'Gxi', 'Gcphase', 'Gxi', 'Giy', 'Gix'),
  ('Gyi', 'Gix', 'Gyi', 'Gix', 'Gxi', 'Gxi'),
  ('Gix', 'Gcphase', 'Gxi', 'Gix', 'Gxi', 'Gcphase'),
  ('Gxi', 'Giy', 'Gyi', 'Gxi', 'Gcphase', 'Gcphase'),
  ('Gyi', 'Gcphase', 'Gii', 'Gix', 'Gxi', 'Gii'),
  ('Gix', 'Gix', 'Giy', 'Gcphase', 'Giy', 'Gcphase', 'Gxi'),
  ('Giy', 'Gxi', 'Gcphase', 'Gix', 'Gix', 'Giy', 'Giy'),
  ('Gxi', 'Gcphase', 'Giy', 'Gyi', 'Gxi', 'Gix', 'Giy'),
  ('Gcphase', 'Gcphase', 'Gix', 'Gxi', 'Giy', 'Gxi', 'Gxi'),
  ('Gxi', 'Gix', 'Giy', 'Gyi', 'Gix', 'Gix', 'Gix'),
  ('Gxi', 'Gix', 'Gyi', 'Gix', 'Gyi', 'Giy', 'Gyi'),
  ('Gix', 'Gix', 'Gix', 'Gix', 'Gxi', 'Gxi', 'Gyi'),
  ('Giy', 'Gcphase', 'Gxi', 'Gyi', 'Gyi', 'Gcphase', 'Gix', 'Gcphase'),
  ('Gxi', 'Gyi', 'Gxi', 'Giy', 'Gxi', 'Giy', 'Gix', 'Giy'),
  ('Giy', 'Giy', 'Gyi', 'Gix', 'Gcphase', 'Gxi', 'Gyi', 'Gyi'),
  ('Gxi', 'Gix', 'Gcphase', 'Gyi', 'Gix', 'Gcphase', 'Gix', 'Giy'),
  ('Gix', 'Gxi', 'Gxi', 'Giy', 'Gxi', 'Gyi', 'Gix', 'Gcphase'),
  ('Gix', 'Gix', 'Gyi', 'Gxi', 'Giy', 'Gix', 'Gcphase', 'Gyi'),
  ('Gix', 'Giy', 'Gix', 'Gxi', 'Gix', 'Giy', 'Gxi', 'Gxi'),
  ('Giy', 'Gix', 'Gcphase', 'Gxi', 'Gcphase', 'Gxi', 'Gcphase', 'Gyi'),
  ('Gxi', 'Giy', 'Gix', 'Gix', 'Gxi', 'Giy', 'Gxi', 'Gcphase'),
  ('Gyi', 'Gyi', 'Gyi', 'Gyi', 'Gix', 'Giy', 'Gix', 'Gyi')
  ])

#Construct the target gateset
gs_target = _setc.build_gateset(
    [4], [('Q0','Q1')],['Gii','Gix','Giy','Gxi','Gyi','Gcphase'],
    [ "I(Q0):I(Q1)", "I(Q0):X(pi/2,Q1)", "I(Q0):Y(pi/2,Q1)", "X(pi/2,Q0):I(Q1)", "Y(pi/2,Q0):I(Q1)", "CPHASE(Q0,Q1)" ],
    prepLabels=['rho0'], prepExpressions=["0"],
    effectLabels=['E0','E1','E2'], effectExpressions=["0","1","2"],
    spamdefs={'00': ('rho0','E0'), '01': ('rho0','E1'),
              '10': ('rho0','E2'), '11': ('rho0','remainder') }, basis="pp")


specs16x10 = _spamc.build_spam_specs(
    prepStrs=prepStrs,
    effectStrs=effectStrs,
    prep_labels=gs_target.get_prep_labels(),
    effect_labels=gs_target.get_effect_labels() )

specs16 = _spamc.build_spam_specs(
    fiducials16,
    prep_labels=gs_target.get_prep_labels(),
    effect_labels=gs_target.get_effect_labels() )

specs36 = _spamc.build_spam_specs(
    fiducials36,
    prep_labels=gs_target.get_prep_labels(),
    effect_labels=gs_target.get_effect_labels() )

specs = specs16x10 #use smallest specs set as "default"

#Wrong CPHASE (bad 1Q phase factor)
legacy_gs_target = _setc.build_gateset(
    [4], [('Q0','Q1')],['Gix','Giy','Gxi','Gyi','Gcphase'],
    [ "I(Q0):X(pi/2,Q1)", "I(Q0):Y(pi/2,Q1)", "X(pi/2,Q0):I(Q1)", "Y(pi/2,Q0):I(Q1)", "CZ(pi,Q0,Q1)" ],
    prepLabels=['rho0'], prepExpressions=["0"],
    effectLabels=['E0','E1','E2'], effectExpressions=["0","1","2"],
    spamdefs={'00': ('rho0','E0'), '01': ('rho0','E1'),
              '10': ('rho0','E2'), '11': ('rho0','remainder') }, basis="pp")


global_fidPairs =  [
    (0, 1), (0, 5), (1, 3), (2, 4), (3, 8), (5, 5), (7, 0), (9, 3), 
    (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), 
    (15, 5)]

pergerm_fidPairsDict = {
  ('Gii',): [
        (0, 8), (1, 0), (1, 1), (1, 3), (1, 10), (2, 5), (2, 9), 
        (3, 3), (3, 9), (4, 3), (4, 8), (5, 0), (5, 5), (5, 7), 
        (6, 4), (6, 6), (6, 8), (6, 10), (7, 0), (7, 2), (7, 3), 
        (7, 4), (7, 6), (7, 10), (8, 3), (8, 5), (9, 3), (9, 4), 
        (9, 5), (9, 6), (9, 8), (9, 9), (10, 3), (10, 9), (10, 10), 
        (11, 1), (11, 5), (12, 5), (12, 7), (12, 9), (13, 0), 
        (13, 10), (14, 0), (14, 1), (14, 2), (14, 6), (15, 0), 
        (15, 5), (15, 6), (15, 7), (15, 8)],
  ('Gix',): [
        (0, 5), (1, 0), (1, 1), (2, 2), (2, 5), (2, 9), (3, 3), 
        (3, 4), (3, 8), (4, 0), (4, 2), (4, 7), (4, 8), (4, 10), 
        (5, 0), (5, 1), (5, 2), (5, 6), (5, 8), (6, 7), (6, 8), 
        (6, 9), (7, 0), (7, 4), (8, 5), (8, 9), (9, 5), (10, 8), 
        (10, 10), (12, 2), (12, 4), (12, 7), (13, 2), (13, 3), 
        (13, 9), (14, 0), (14, 5), (14, 6), (15, 5), (15, 8), 
        (15, 9)],
  ('Giy',): [
        (0, 0), (0, 7), (1, 1), (3, 5), (3, 6), (4, 2), (4, 4), 
        (4, 5), (5, 3), (5, 7), (7, 1), (7, 8), (8, 5), (9, 4), 
        (9, 5), (9, 9), (10, 5), (11, 5), (11, 6), (11, 8), (11, 10), 
        (12, 0), (12, 3), (13, 10), (14, 0), (14, 5), (14, 6), 
        (14, 7), (15, 0), (15, 6), (15, 9)],
  ('Gxi',): [
        (0, 7), (1, 1), (1, 7), (2, 7), (3, 3), (4, 9), (5, 4), 
        (7, 2), (7, 10), (8, 2), (9, 2), (9, 8), (9, 9), (10, 1), 
        (10, 10), (11, 2), (11, 5), (11, 6), (13, 2), (14, 7), 
        (15, 2), (15, 3)],
  ('Gyi',): [
        (3, 1), (4, 1), (4, 2), (5, 0), (5, 1), (5, 7), (6, 0), 
        (6, 8), (7, 2), (7, 4), (7, 9), (8, 0), (8, 7), (9, 2), 
        (9, 3), (10, 9), (10, 10), (14, 7), (14, 9), (15, 10)],
  ('Gix', 'Gyi'): [
        (0, 5), (0, 9), (1, 6), (3, 1), (3, 2), (5, 0), (5, 4), 
        (6, 0), (6, 8), (9, 7), (10, 9), (11, 1), (11, 4), (14, 4), 
        (14, 9), (15, 5), (15, 7)],
  ('Gix', 'Gcphase'): [
        (1, 10), (2, 5), (2, 10), (4, 3), (4, 8), (5, 5), (6, 10), 
        (7, 8), (8, 5), (10, 2), (10, 5), (11, 2), (12, 5), (12, 10), 
        (13, 0), (13, 2), (14, 5)],
  ('Gix', 'Gxi'): [
        (0, 0), (1, 5), (2, 4), (3, 3), (3, 5), (5, 2), (6, 1), 
        (6, 8), (6, 10), (8, 6), (10, 2), (10, 8), (10, 10), 
        (11, 8), (12, 1), (13, 1), (13, 4), (13, 6), (13, 10), 
        (14, 8), (15, 3)],
  ('Gxi', 'Gyi'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), 
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
  ('Gxi', 'Gcphase'): [
        (1, 1), (2, 1), (2, 8), (4, 9), (5, 3), (5, 8), (7, 10), 
        (8, 0), (8, 2), (8, 6), (8, 8), (9, 3), (9, 10), (11, 2), 
        (12, 4), (13, 0), (13, 1), (13, 5), (13, 8), (14, 2), 
        (14, 8)],
  ('Gix', 'Giy'): [
        (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5), 
        (7, 6), (8, 9), (9, 9), (10, 2), (10, 8), (11, 10), (12, 6), 
        (12, 9), (13, 9), (15, 1)],
  ('Gxi', 'Gii', 'Gyi'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), 
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
  ('Giy', 'Gyi', 'Gcphase'): [
        (0, 1), (0, 5), (1, 3), (2, 4), (2, 10), (3, 8), (5, 5), 
        (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), 
        (14, 6), (15, 0), (15, 5)],
  ('Gxi', 'Gii', 'Gii'): [
        (0, 7), (1, 1), (1, 7), (2, 7), (3, 3), (4, 9), (5, 4), 
        (7, 2), (7, 10), (8, 2), (9, 2), (9, 8), (9, 9), (10, 1), 
        (10, 10), (11, 2), (11, 5), (11, 6), (13, 2), (14, 7), 
        (15, 2), (15, 3)],
  ('Gii', 'Giy', 'Gyi'): [
        (0, 6), (0, 8), (0, 10), (1, 0), (1, 1), (1, 3), (2, 9), 
        (3, 8), (4, 4), (4, 7), (5, 7), (6, 1), (7, 0), (7, 8), 
        (9, 10), (10, 5), (11, 5), (12, 5), (12, 6), (14, 0), 
        (15, 0), (15, 6), (15, 8)],
  ('Gii', 'Gcphase', 'Gcphase'): [
        (0, 8), (1, 0), (1, 1), (1, 3), (1, 10), (2, 5), (2, 9), 
        (3, 3), (3, 9), (4, 3), (4, 8), (5, 0), (5, 5), (5, 7), 
        (6, 4), (6, 6), (6, 8), (6, 10), (7, 0), (7, 2), (7, 3), 
        (7, 4), (7, 6), (7, 10), (8, 3), (8, 5), (9, 3), (9, 4), 
        (9, 5), (9, 6), (9, 8), (9, 9), (10, 3), (10, 9), (10, 10), 
        (11, 1), (11, 5), (12, 5), (12, 7), (12, 9), (13, 0), 
        (13, 10), (14, 0), (14, 1), (14, 2), (14, 6), (15, 0), 
        (15, 5), (15, 6), (15, 7), (15, 8)],
  ('Gix', 'Gcphase', 'Gyi'): [
        (0, 2), (1, 0), (1, 4), (1, 9), (3, 10), (4, 3), (5, 7), 
        (7, 4), (7, 7), (7, 8), (8, 7), (8, 9), (9, 2), (9, 6), 
        (10, 3), (14, 10), (15, 4)],
  ('Gyi', 'Gii', 'Gii'): [
        (3, 1), (4, 1), (4, 2), (5, 0), (5, 1), (5, 7), (6, 0), 
        (6, 8), (7, 2), (7, 4), (7, 9), (8, 0), (8, 7), (9, 2), 
        (9, 3), (10, 9), (10, 10), (14, 7), (14, 9), (15, 10)],
  ('Gii', 'Giy', 'Gxi'): [
        (1, 1), (2, 8), (3, 0), (3, 2), (3, 6), (4, 7), (7, 2), 
        (8, 6), (9, 1), (9, 7), (9, 9), (10, 2), (10, 10), (11, 8), 
        (12, 6), (13, 2), (13, 7), (14, 2), (15, 5)],
  ('Giy', 'Gcphase', 'Gyi'): [
        (0, 2), (1, 0), (1, 4), (1, 9), (3, 10), (4, 3), (5, 7), 
        (7, 4), (7, 7), (7, 8), (8, 7), (8, 9), (9, 2), (9, 6), 
        (10, 3), (14, 10), (15, 4)],
  ('Gix', 'Gii', 'Gii'): [
        (0, 5), (1, 0), (1, 1), (2, 2), (2, 5), (2, 9), (3, 3), 
        (3, 4), (3, 8), (4, 0), (4, 2), (4, 7), (4, 8), (4, 10), 
        (5, 0), (5, 1), (5, 2), (5, 6), (5, 8), (6, 7), (6, 8), 
        (6, 9), (7, 0), (7, 4), (8, 5), (8, 9), (9, 5), (10, 8), 
        (10, 10), (12, 2), (12, 4), (12, 7), (13, 2), (13, 3), 
        (13, 9), (14, 0), (14, 5), (14, 6), (15, 5), (15, 8), 
        (15, 9)],
  ('Gxi', 'Gyi', 'Gii'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), 
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
  ('Giy', 'Gii', 'Gii'): [
        (0, 0), (0, 7), (1, 1), (3, 5), (3, 6), (4, 2), (4, 4), 
        (4, 5), (5, 3), (5, 7), (7, 1), (7, 8), (8, 5), (9, 4), 
        (9, 5), (9, 9), (10, 5), (11, 5), (11, 6), (11, 8), (11, 10), 
        (12, 0), (12, 3), (13, 10), (14, 0), (14, 5), (14, 6), 
        (14, 7), (15, 0), (15, 6), (15, 9)],
  ('Gxi', 'Gcphase', 'Gcphase'): [
        (0, 7), (1, 1), (1, 7), (2, 7), (3, 3), (4, 9), (5, 4), 
        (7, 2), (7, 10), (8, 2), (9, 2), (9, 8), (9, 9), (10, 1), 
        (10, 10), (11, 2), (11, 5), (11, 6), (13, 2), (14, 7), 
        (15, 2), (15, 3)],
  ('Giy', 'Gxi', 'Gcphase'): [
        (0, 1), (0, 5), (1, 3), (2, 4), (2, 10), (3, 8), (5, 5), 
        (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), 
        (14, 6), (15, 0), (15, 5)],
  ('Gix', 'Giy', 'Gii'): [
        (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5), 
        (7, 6), (8, 9), (9, 9), (10, 2), (10, 8), (11, 10), (12, 6), 
        (12, 9), (13, 9), (15, 1)],
  ('Gix', 'Gii', 'Giy'): [
        (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5), 
        (7, 6), (8, 9), (9, 9), (10, 2), (10, 8), (11, 10), (12, 6), 
        (12, 9), (13, 9), (15, 1)],
  ('Gix', 'Gcphase', 'Gxi'): [
        (0, 1), (0, 5), (1, 3), (2, 4), (2, 10), (3, 8), (5, 5), 
        (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), 
        (14, 6), (15, 0), (15, 5)],
  ('Gix', 'Gcphase', 'Gcphase'): [
        (0, 5), (1, 0), (1, 1), (2, 2), (2, 5), (2, 9), (3, 3), 
        (3, 4), (3, 8), (4, 0), (4, 2), (4, 7), (4, 8), (4, 10), 
        (5, 0), (5, 1), (5, 2), (5, 6), (5, 8), (6, 7), (6, 8), 
        (6, 9), (7, 0), (7, 4), (8, 5), (8, 9), (9, 5), (10, 8), 
        (10, 10), (12, 2), (12, 4), (12, 7), (13, 2), (13, 3), 
        (13, 9), (14, 0), (14, 5), (14, 6), (15, 5), (15, 8), 
        (15, 9)],
  ('Gix', 'Gyi', 'Gcphase'): [
        (0, 1), (0, 5), (1, 3), (2, 4), (2, 10), (3, 8), (5, 5), 
        (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), 
        (14, 6), (15, 0), (15, 5)],
  ('Gyi', 'Gyi', 'Gcphase'): [
        (1, 10), (2, 10), (4, 8), (5, 5), (5, 6), (6, 10), (7, 0), 
        (7, 5), (7, 6), (7, 8), (8, 5), (12, 5), (13, 0), (13, 2), 
        (14, 1)],
  ('Gix', 'Gyi', 'Gxi'): [
        (1, 10), (2, 10), (4, 8), (5, 5), (5, 6), (6, 10), (7, 0), 
        (7, 5), (7, 6), (7, 8), (8, 5), (12, 5), (13, 0), (13, 2), 
        (14, 1)],
  ('Gix', 'Gcphase', 'Giy'): [
        (0, 7), (1, 10), (2, 10), (4, 8), (5, 5), (5, 6), (6, 1), 
        (6, 10), (7, 0), (7, 5), (7, 6), (7, 8), (8, 5), (10, 2), 
        (10, 5), (12, 5), (13, 0), (13, 2), (14, 1)],
  ('Gii', 'Gcphase', 'Giy'): [
        (0, 2), (1, 0), (1, 4), (1, 9), (3, 10), (4, 3), (5, 7), 
        (7, 4), (7, 7), (7, 8), (8, 7), (8, 9), (9, 2), (9, 6), 
        (10, 3), (14, 10), (15, 4)],
  ('Gix', 'Gyi', 'Giy'): [
        (3, 0), (4, 4), (5, 1), (5, 8), (6, 5), (7, 3), (8, 6), 
        (8, 7), (9, 5), (10, 3), (11, 4), (14, 0), (14, 6), (14, 9), 
        (15, 5)],
  ('Gxi', 'Gyi', 'Gyi', 'Gii'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Giy', 'Gcphase', 'Gxi', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gix', 'Giy', 'Giy', 'Gii'): [
        (0, 4), (0, 5), (0, 7), (1, 1), (1, 6), (2, 3), (4, 10), 
        (5, 4), (6, 8), (7, 4), (7, 10), (8, 8), (8, 9), (10, 5), 
        (11, 5), (11, 6), (11, 9), (13, 10), (14, 1), (14, 9)],
  ('Gix', 'Gix', 'Gii', 'Giy'): [
        (0, 0), (0, 6), (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), 
        (4, 8), (5, 5), (6, 7), (7, 6), (8, 9), (9, 9), (10, 2), 
        (10, 8), (11, 10), (12, 6), (12, 9), (13, 1), (13, 9), 
        (15, 1)],
  ('Gcphase', 'Gcphase', 'Giy', 'Gcphase'): [
        (0, 2), (1, 0), (1, 4), (1, 9), (3, 10), (4, 3), (5, 7), 
        (7, 4), (7, 7), (7, 8), (8, 7), (8, 9), (9, 2), (9, 6), 
        (10, 3), (14, 10), (15, 4)],
  ('Gxi', 'Gxi', 'Gii', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Giy', 'Gix', 'Gyi', 'Giy'): [
        (2, 0), (2, 1), (3, 0), (3, 9), (5, 4), (5, 7), (7, 6), 
        (7, 8), (8, 8), (11, 1), (11, 4), (12, 3), (12, 6), (14, 9), 
        (15, 3)],
  ('Gyi', 'Gyi', 'Giy', 'Gcphase', 'Giy'): [
        (0, 2), (1, 0), (1, 4), (1, 9), (2, 4), (2, 10), (4, 3), 
        (7, 4), (7, 8), (8, 7), (8, 9), (9, 2), (9, 6), (10, 3), 
        (15, 4)],
  ('Gcphase', 'Gyi', 'Giy', 'Gcphase', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Giy', 'Gxi', 'Gcphase', 'Gxi', 'Gxi'): [
        (0, 1), (0, 5), (1, 3), (2, 4), (2, 10), (3, 8), (5, 5), 
        (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), 
        (14, 6), (15, 0), (15, 5)],
  ('Gyi', 'Gcphase', 'Gix', 'Gyi', 'Gxi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gix', 'Gcphase', 'Gxi', 'Gxi', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gcphase', 'Gix', 'Gyi', 'Gii', 'Gii'): [
        (0, 2), (1, 0), (1, 4), (1, 9), (3, 10), (4, 3), (5, 7), 
        (7, 4), (7, 7), (7, 8), (8, 7), (8, 9), (9, 2), (9, 6), 
        (10, 3), (14, 10), (15, 4)],
  ('Gyi', 'Gix', 'Gix', 'Gcphase', 'Gxi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gyi', 'Gcphase', 'Giy', 'Gix', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gcphase', 'Gcphase', 'Gcphase', 'Gix', 'Gxi'): [
        (1, 10), (2, 5), (2, 10), (4, 3), (4, 8), (5, 5), (6, 10), 
        (7, 8), (8, 5), (10, 2), (10, 5), (11, 2), (12, 5), (12, 10), 
        (13, 0), (13, 2), (14, 5)],
  ('Gcphase', 'Gii', 'Gxi', 'Gcphase', 'Gix', 'Gxi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gix', 'Gyi', 'Giy', 'Giy', 'Gxi', 'Gxi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gcphase', 'Gyi', 'Gii', 'Gix', 'Gxi', 'Gix'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gxi', 'Gxi', 'Gyi', 'Gxi', 'Gyi', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gyi', 'Gxi', 'Giy', 'Gyi', 'Gcphase', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gyi', 'Gcphase', 'Gii', 'Gix', 'Gxi', 'Gii'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), 
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
  ('Gxi', 'Giy', 'Giy', 'Gyi', 'Giy', 'Gcphase'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gcphase', 'Gii', 'Gxi', 'Gyi', 'Gyi', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (2, 4), (2, 10), (3, 8), (5, 5), 
        (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), 
        (14, 6), (15, 0), (15, 5)],
  ('Gix', 'Gix', 'Giy', 'Gix', 'Giy', 'Giy'): [
        (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5), 
        (7, 6), (8, 9), (9, 9), (10, 2), (10, 8), (11, 10), (12, 6), 
        (12, 9), (13, 9), (15, 1)],
  ('Giy', 'Gxi', 'Gyi', 'Gxi', 'Gcphase', 'Gyi', 'Gix'): [
        (0, 1), (0, 5), (1, 3), (2, 4), (2, 10), (3, 8), (5, 5), 
        (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), 
        (14, 6), (15, 0), (15, 5)],
  ('Giy', 'Giy', 'Gix', 'Gii', 'Gix', 'Gxi', 'Gxi'): [
        (0, 4), (0, 6), (1, 1), (2, 2), (3, 5), (4, 9), (6, 10), 
        (8, 0), (8, 2), (10, 7), (11, 1), (12, 1), (14, 6), (15, 6), 
        (15, 9)],
  ('Gcphase', 'Gcphase', 'Gcphase', 'Gxi', 'Gix', 'Gii', 'Giy'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), 
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
  ('Gix', 'Giy', 'Gix', 'Gyi', 'Gxi', 'Gii', 'Gxi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Giy', 'Gxi', 'Gxi', 'Gcphase', 'Gii', 'Gxi', 'Gxi'): [
        (0, 9), (1, 1), (1, 9), (2, 7), (3, 4), (4, 1), (4, 4), 
        (4, 10), (6, 0), (6, 3), (6, 4), (6, 6), (6, 9), (7, 0), 
        (7, 7), (9, 4), (10, 10), (11, 5), (12, 4), (13, 7), 
        (14, 0)],
  ('Gxi', 'Giy', 'Gix', 'Gcphase', 'Giy', 'Gix', 'Gii'): [
        (0, 1), (0, 2), (0, 5), (0, 10), (1, 3), (1, 7), (2, 1), 
        (2, 7), (3, 6), (5, 1), (6, 10), (7, 0), (7, 6), (9, 0), 
        (9, 2), (10, 4), (11, 7), (11, 9), (13, 7), (14, 3), 
        (14, 7), (15, 5), (15, 10)],
  ('Gii', 'Gyi', 'Gxi', 'Gcphase', 'Gcphase', 'Gix', 'Gcphase'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), 
        (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
  ('Gyi', 'Gii', 'Giy', 'Gyi', 'Gcphase', 'Gxi', 'Gii'): [
        (0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), 
        (3, 8), (5, 5), (7, 0), (7, 8), (9, 3), (9, 9), (9, 10), 
        (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 4), 
        (15, 5)],
  ('Gxi', 'Gyi', 'Gyi', 'Gcphase', 'Gix', 'Gix', 'Giy'): [
        (0, 1), (0, 2), (0, 5), (0, 10), (1, 3), (1, 7), (2, 1), 
        (2, 7), (3, 6), (5, 1), (6, 5), (6, 10), (7, 0), (7, 6), 
        (8, 3), (9, 0), (9, 2), (10, 4), (11, 7), (11, 9), (13, 7), 
        (14, 3), (14, 7), (15, 5), (15, 10)],
  ('Gyi', 'Gyi', 'Gcphase', 'Gxi', 'Gix', 'Gyi', 'Gix', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gcphase', 'Gyi', 'Gcphase', 'Gix', 'Gxi', 'Gcphase', 'Gxi', 'Gcphase'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Giy', 'Gcphase', 'Gxi', 'Gcphase', 'Gix', 'Gxi', 'Gxi', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gii', 'Giy', 'Gix', 'Gcphase', 'Gcphase', 'Gii', 'Gyi', 'Gxi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gxi', 'Giy', 'Gix', 'Gcphase', 'Gii', 'Gyi', 'Gyi', 'Giy'): [
        (0, 1), (0, 5), (1, 3), (2, 4), (2, 10), (3, 8), (5, 5), 
        (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), 
        (14, 6), (15, 0), (15, 5)],
  ('Gxi', 'Giy', 'Giy', 'Giy', 'Gcphase', 'Gix', 'Gyi', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gix', 'Gii', 'Gxi', 'Gix', 'Gii', 'Giy', 'Gxi', 'Gii'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
  ('Gii', 'Gii', 'Gcphase', 'Gxi', 'Gix', 'Gxi', 'Gix', 'Gyi'): [
        (0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), 
        (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), 
        (15, 0), (15, 5)],
}