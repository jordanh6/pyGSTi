"""
Variables for working with the 2-qubit model containing the gates
I*X(pi/2), I*Y(pi/2), X(pi/2)*I, Y(pi/2)*I, and CPHASE.
"""
#***************************************************************************************************
# Copyright 2015, 2019 National Technology & Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights
# in this software.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 or in the LICENSE file in the root pyGSTi directory.
#***************************************************************************************************

from collections import OrderedDict
from pygsti.construction import circuitconstruction as _strc
from pygsti.construction import modelconstruction as _setc

from pygsti.modelpacks._modelpack import GSTModelPack


class _Module(GSTModelPack):
    description = "I*X(pi/2), I*Y(pi/2), X(pi/2)*I, Y(pi/2)*I, and CPHASE gates"

    gates = [('Gxpi2', 1), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 0), ('Gcphase', 0, 1)]

    _sslbls = [0, 1]

    _germs = [(('Gxpi2', 0), ), (('Gypi2', 0), ), (('Gxpi2', 1), ), (('Gypi2', 1), ), (('Gxpi2', 0), ('Gypi2', 0)),
              (('Gxpi2', 1), ('Gypi2', 1)), (('Gypi2', 1), ('Gypi2', 0)), (('Gxpi2', 1), ('Gxpi2', 0)), (('Gxpi2', 1), ('Gypi2', 0)),
              (('Gypi2', 1), ('Gxpi2', 0)), (('Gxpi2', 0), ('Gxpi2', 0), ('Gypi2', 0)), (('Gxpi2', 1), ('Gxpi2', 1), ('Gypi2', 1)),
              (('Gxpi2', 0), ('Gypi2', 0), ('Gypi2', 0)), (('Gxpi2', 1), ('Gypi2', 1), ('Gypi2', 1)), (('Gypi2', 1), ('Gxpi2', 0), ('Gxpi2', 0)),
              (('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 0)), (('Gxpi2', 1), ('Gxpi2', 0), ('Gypi2', 1)), (('Gxpi2', 1), ('Gypi2', 0), ('Gxpi2', 0)),
              (('Gxpi2', 1), ('Gypi2', 0), ('Gypi2', 1)), (('Gxpi2', 1), ('Gypi2', 1), ('Gypi2', 0)), (('Gxpi2', 1), ('Gypi2', 1), ('Gxpi2', 0)),
              (('Gypi2', 1), ('Gypi2', 0), ('Gxpi2', 0)), (('Gypi2', 0), ('Gxpi2', 1), ('Gxpi2', 0), ('Gypi2', 1)),
              (('Gxpi2', 1), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 0)), (('Gxpi2', 1), ('Gxpi2', 1), ('Gxpi2', 1), ('Gypi2', 1)),
              (('Gxpi2', 0), ('Gypi2', 0), ('Gypi2', 0), ('Gypi2', 0)), (('Gypi2', 0), ('Gypi2', 0), ('Gypi2', 1), ('Gypi2', 0)),
              (('Gypi2', 0), ('Gxpi2', 1), ('Gxpi2', 1), ('Gxpi2', 1)), (('Gxpi2', 0), ('Gypi2', 0), ('Gxpi2', 1), ('Gxpi2', 1)),
              (('Gypi2', 1), ('Gypi2', 0), ('Gxpi2', 0), ('Gxpi2', 0), ('Gypi2', 1)),
              (('Gxpi2', 0), ('Gxpi2', 0), ('Gypi2', 1), ('Gypi2', 0), ('Gypi2', 1)),
              (('Gypi2', 1), ('Gxpi2', 1), ('Gxpi2', 0), ('Gxpi2', 1), ('Gxpi2', 0)),
              (('Gypi2', 0), ('Gypi2', 1), ('Gypi2', 0), ('Gxpi2', 1), ('Gxpi2', 1)),
              (('Gypi2', 1), ('Gxpi2', 0), ('Gxpi2', 1), ('Gypi2', 1), ('Gypi2', 0)),
              (('Gypi2', 1), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 0), ('Gxpi2', 0)),
              (('Gxpi2', 0), ('Gxpi2', 1), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 1), ('Gypi2', 0)),
              (('Gxpi2', 0), ('Gypi2', 1), ('Gxpi2', 1), ('Gypi2', 0), ('Gxpi2', 1), ('Gxpi2', 1)),
              (('Gxpi2', 0), ('Gxpi2', 0), ('Gypi2', 0), ('Gxpi2', 0), ('Gypi2', 0), ('Gypi2', 0)),
              (('Gxpi2', 1), ('Gxpi2', 1), ('Gypi2', 1), ('Gxpi2', 1), ('Gypi2', 1), ('Gypi2', 1)),
              (('Gypi2', 0), ('Gxpi2', 0), ('Gxpi2', 1), ('Gypi2', 1), ('Gxpi2', 0), ('Gxpi2', 1)),
              (('Gypi2', 0), ('Gxpi2', 0), ('Gxpi2', 1), ('Gxpi2', 0), ('Gxpi2', 1), ('Gypi2', 1)),
              (('Gxpi2', 0), ('Gxpi2', 1), ('Gypi2', 1), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 0)),
              (('Gxpi2', 1), ('Gypi2', 1), ('Gypi2', 1), ('Gxpi2', 1), ('Gxpi2', 0), ('Gxpi2', 0)),
              (('Gypi2', 0), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 1), ('Gypi2', 1), ('Gypi2', 1)),
              (('Gypi2', 0), ('Gypi2', 0), ('Gypi2', 0), ('Gypi2', 1), ('Gypi2', 0), ('Gxpi2', 1)),
              (('Gypi2', 1), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 1), ('Gxpi2', 1), ('Gypi2', 1)),
              (('Gypi2', 1), ('Gxpi2', 1), ('Gypi2', 0), ('Gypi2', 0), ('Gxpi2', 1), ('Gxpi2', 0), ('Gypi2', 1)),
              (('Gypi2', 0), ('Gxpi2', 0), ('Gypi2', 1), ('Gxpi2', 0), ('Gxpi2', 1), ('Gxpi2', 0), ('Gypi2', 0), ('Gypi2', 1)),
              (('Gxpi2', 1), ('Gxpi2', 1), ('Gypi2', 0), ('Gxpi2', 0), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 1), ('Gypi2', 0))]

    _germs_lite = [(('Gxpi2', 0), ), (('Gypi2', 0), ), (('Gxpi2', 1), ), (('Gypi2', 1), ), (('Gxpi2', 0), ('Gypi2', 0)),
                   (('Gxpi2', 1), ('Gypi2', 1)), (('Gxpi2', 0), ('Gxpi2', 0), ('Gypi2', 0)), (('Gxpi2', 1), ('Gxpi2', 1), ('Gypi2', 1)),
                   (('Gxpi2', 0), ('Gxpi2', 1), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 1), ('Gypi2', 0)),
                   (('Gxpi2', 0), ('Gypi2', 1), ('Gxpi2', 1), ('Gypi2', 0), ('Gxpi2', 1), ('Gxpi2', 1)),
                   (('Gypi2', 0), ('Gxpi2', 0), ('Gypi2', 1), ('Gxpi2', 0), ('Gxpi2', 1), ('Gxpi2', 0), ('Gypi2', 0), ('Gypi2', 1))]

    _fiducials = [(), (('Gxpi2', 1), ), (('Gypi2', 1), ), (('Gxpi2', 1), ('Gxpi2', 1)), (('Gxpi2', 0), ), (('Gxpi2', 0), ('Gxpi2', 1)),
                  (('Gxpi2', 0), ('Gypi2', 1)), (('Gxpi2', 0), ('Gxpi2', 1), ('Gxpi2', 1)), (('Gypi2', 0), ), (('Gypi2', 0), ('Gxpi2', 1)),
                  (('Gypi2', 0), ('Gypi2', 1)), (('Gypi2', 0), ('Gxpi2', 1), ('Gxpi2', 1)), (('Gxpi2', 0), ('Gxpi2', 0)),
                  (('Gxpi2', 0), ('Gxpi2', 0), ('Gxpi2', 1)), (('Gxpi2', 0), ('Gxpi2', 0), ('Gypi2', 1)),
                  (('Gxpi2', 0), ('Gxpi2', 0), ('Gxpi2', 1), ('Gxpi2', 1))]

    _prepfiducials = [(), (('Gxpi2', 1), ), (('Gypi2', 1), ), (('Gxpi2', 1), ('Gxpi2', 1)), (('Gxpi2', 0), ), (('Gxpi2', 0), ('Gxpi2', 1)),
                 (('Gxpi2', 0), ('Gypi2', 1)), (('Gxpi2', 0), ('Gxpi2', 1), ('Gxpi2', 1)), (('Gypi2', 0), ), (('Gypi2', 0), ('Gxpi2', 1)),
                 (('Gypi2', 0), ('Gypi2', 1)), (('Gypi2', 0), ('Gxpi2', 1), ('Gxpi2', 1)), (('Gxpi2', 0), ('Gxpi2', 0)),
                 (('Gxpi2', 0), ('Gxpi2', 0), ('Gxpi2', 1)), (('Gxpi2', 0), ('Gxpi2', 0), ('Gypi2', 1)),
                 (('Gxpi2', 0), ('Gxpi2', 0), ('Gxpi2', 1), ('Gxpi2', 1))]

    _measfiducials = [(), (('Gxpi2', 1), ), (('Gypi2', 1), ), (('Gxpi2', 1), ('Gxpi2', 1)), (('Gxpi2', 0), ), (('Gypi2', 0), ),
                   (('Gxpi2', 0), ('Gxpi2', 0)), (('Gxpi2', 0), ('Gxpi2', 1)), (('Gxpi2', 0), ('Gypi2', 1)), (('Gypi2', 0), ('Gxpi2', 1)),
                   (('Gypi2', 0), ('Gypi2', 1))]

    clifford_compilation = None

    global_fidPairs = [(1, 7), (2, 2), (4, 8), (7, 2), (7, 10), (8, 6), (9, 8), (9, 9), (10, 1), (11, 4), (11, 9),
                       (12, 8), (12, 9), (13, 0), (13, 1), (13, 9)]

    _pergerm_fidPairsDict = {
        (('Gypi2', 0), ): [(3, 1), (4, 1), (4, 2), (5, 0), (5, 1), (5, 7), (6, 0), (6, 8), (7, 2), (7, 4), (7, 9), (8, 0),
                    (8, 7), (9, 2), (9, 3), (10, 9), (10, 10), (14, 7), (14, 9), (15, 10)],
        (('Gxpi2', 1), ): [(0, 5), (1, 0), (1, 1), (2, 2), (2, 5), (2, 9), (3, 3), (3, 4), (3, 8), (4, 0), (4, 2), (4, 7),
                    (4, 8), (4, 10), (5, 0), (5, 1), (5, 2), (5, 6), (5, 8), (6, 7), (6, 8), (6, 9), (7, 0), (7, 4),
                    (8, 5), (8, 9), (9, 5), (10, 8), (10, 10), (12, 2), (12, 4), (12, 7), (13, 2), (13, 3), (13, 9),
                    (14, 0), (14, 5), (14, 6), (15, 5), (15, 8), (15, 9)],
        (('Gxpi2', 0), ): [(0, 7), (1, 1), (1, 7), (2, 7), (3, 3), (4, 9), (5, 4), (7, 2), (7, 10), (8, 2), (9, 2), (9, 8),
                    (9, 9), (10, 1), (10, 10), (11, 2), (11, 5), (11, 6), (13, 2), (14, 7), (15, 2), (15, 3)],
        (('Gypi2', 1), ): [(0, 0), (0, 7), (1, 1), (3, 5), (3, 6), (4, 2), (4, 4), (4, 5), (5, 3), (5, 7), (7, 1), (7, 8),
                    (8, 5), (9, 4), (9, 5), (9, 9), (10, 5), (11, 5), (11, 6), (11, 8), (11, 10), (12, 0), (12, 3),
                    (13, 10), (14, 0), (14, 5), (14, 6), (14, 7), (15, 0), (15, 6), (15, 9)],
        (('Gypi2', 1), ('Gypi2', 0)): [(0, 6), (0, 8), (0, 10), (1, 0), (1, 1), (1, 3), (2, 9), (3, 8), (4, 4), (4, 7), (5, 7),
                         (6, 1), (7, 0), (7, 8), (9, 10), (10, 5), (11, 5), (12, 5), (12, 6), (14, 0), (15, 0), (15, 6),
                         (15, 8)],
        (('Gxpi2', 1), ('Gxpi2', 0)): [(0, 0), (1, 5), (2, 4), (3, 3), (3, 5), (5, 2), (6, 1), (6, 8), (6, 10), (8, 6), (10, 2),
                         (10, 8), (10, 10), (11, 8), (12, 1), (13, 1), (13, 4), (13, 6), (13, 10), (14, 8), (15, 3)],
        (('Gxpi2', 0), ('Gypi2', 0)): [(0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), (3, 8), (5, 5), (7, 0), (9, 3),
                         (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gypi2', 1), ('Gxpi2', 0)): [(1, 1), (2, 8), (3, 0), (3, 2), (3, 6), (4, 7), (7, 2), (8, 6), (9, 1), (9, 7), (9, 9),
                         (10, 2), (10, 10), (11, 8), (12, 6), (13, 2), (13, 7), (14, 2), (15, 5)],
        (('Gxpi2', 1), ('Gypi2', 1)): [(1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5), (7, 6), (8, 9), (9, 9), (10, 2),
                         (10, 8), (11, 10), (12, 6), (12, 9), (13, 9), (15, 1)],
        (('Gxpi2', 1), ('Gypi2', 0)): [(0, 5), (0, 9), (1, 6), (3, 1), (3, 2), (5, 0), (5, 4), (6, 0), (6, 8), (9, 7), (10, 9),
                         (11, 1), (11, 4), (14, 4), (14, 9), (15, 5), (15, 7)],
        (('Gxpi2', 1), ('Gxpi2', 0), ('Gypi2', 1)): [(0, 6), (3, 0), (5, 0), (6, 7), (7, 1), (8, 3), (9, 9), (10, 4), (10, 9), (12, 9),
                                (13, 2), (14, 5), (14, 8), (14, 10), (15, 6)],
        (('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 0)): [(0, 9), (1, 1), (1, 9), (2, 7), (3, 4), (4, 4), (4, 10), (6, 0), (6, 3), (7, 0), (9, 4),
                                (11, 5), (12, 4), (13, 7), (14, 0)],
        (('Gypi2', 1), ('Gypi2', 0), ('Gxpi2', 0)): [(0, 9), (1, 1), (1, 9), (2, 7), (3, 4), (4, 4), (4, 10), (6, 0), (6, 3), (7, 0), (9, 4),
                                (11, 5), (12, 4), (13, 7), (14, 0)],
        (('Gxpi2', 1), ('Gypi2', 1), ('Gxpi2', 0)): [(0, 6), (3, 0), (5, 0), (6, 7), (7, 1), (8, 3), (9, 9), (10, 4), (10, 9), (12, 9),
                                (13, 2), (14, 5), (14, 8), (14, 10), (15, 6)],
        (('Gxpi2', 1), ('Gypi2', 1), ('Gypi2', 0)): [(0, 1), (4, 2), (4, 7), (6, 7), (8, 3), (9, 5), (9, 7), (10, 0), (10, 4), (10, 5),
                                (11, 2), (11, 9), (14, 6), (14, 8), (15, 3)],
        (('Gxpi2', 1), ('Gxpi2', 1), ('Gypi2', 1)): [(0, 0), (0, 6), (1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5), (6, 7), (7, 6),
                                (8, 9), (9, 9), (10, 2), (10, 8), (11, 10), (12, 6), (12, 9), (13, 1), (13, 9),
                                (15, 1)],
        (('Gypi2', 1), ('Gxpi2', 0), ('Gxpi2', 0)): [(1, 7), (2, 2), (4, 8), (7, 2), (7, 10), (8, 6), (9, 8), (9, 9), (10, 1), (11, 4),
                                (11, 9), (12, 8), (12, 9), (13, 0), (13, 1), (13, 9)],
        (('Gxpi2', 1), ('Gypi2', 1), ('Gypi2', 1)): [(0, 4), (0, 5), (0, 7), (1, 1), (1, 6), (2, 3), (4, 10), (5, 4), (6, 8),
                                (7, 4), (7, 10), (8, 8), (8, 9), (10, 5), (11, 5), (11, 6), (11, 9), (13, 10), (14, 1),
                                (14, 9)],
        (('Gxpi2', 1), ('Gypi2', 0), ('Gxpi2', 0)): [(1, 10), (2, 10), (4, 8), (5, 5), (5, 6), (6, 10), (7, 0), (7, 5), (7, 6), (7, 8),
                                (8, 5), (12, 5), (13, 0), (13, 2), (14, 1)],
        (('Gxpi2', 0), ('Gypi2', 0), ('Gypi2', 0)): [(0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8),
                                (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gxpi2', 0), ('Gxpi2', 0), ('Gypi2', 0)): [(0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8),
                                (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gxpi2', 1), ('Gypi2', 0), ('Gypi2', 1)): [(3, 0), (4, 4), (5, 1), (5, 8), (6, 5), (7, 3), (8, 6), (8, 7), (9, 5), (10, 3),
                                (11, 4), (14, 0), (14, 6), (14, 9), (15, 5)],
        (('Gxpi2', 0), ('Gypi2', 0), ('Gxpi2', 1), ('Gxpi2', 1)): [(1, 10), (2, 10), (4, 8), (5, 5), (5, 6), (6, 10), (7, 0), (7, 5), (7, 6),
                                       (7, 8), (8, 5), (12, 5), (13, 0), (13, 2), (14, 1)],
        (('Gxpi2', 1), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 0)): [(0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), (3, 8), (5, 5), (7, 0),
                                       (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gypi2', 0), ('Gxpi2', 1), ('Gxpi2', 1), ('Gxpi2', 1)): [(0, 5), (0, 9), (1, 6), (3, 1), (3, 2), (5, 0), (5, 4), (6, 0), (6, 8), (9, 7),
                                       (10, 9), (11, 1), (11, 4), (14, 4), (14, 9), (15, 5), (15, 7)],
        (('Gxpi2', 0), ('Gypi2', 0), ('Gypi2', 0), ('Gypi2', 0)): [(0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), (3, 8), (5, 5), (7, 0),
                                       (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gypi2', 0), ('Gypi2', 0), ('Gypi2', 1), ('Gypi2', 0)): [(0, 2), (1, 1), (1, 4), (2, 1), (2, 10), (3, 10), (4, 0), (5, 3), (5, 7), (6, 4),
                                       (6, 10), (8, 2), (8, 3), (9, 0), (10, 8), (11, 1), (11, 7), (13, 1), (13, 8)],
        (('Gxpi2', 1), ('Gxpi2', 1), ('Gxpi2', 1), ('Gypi2', 1)): [(1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5), (7, 6), (8, 9), (9, 9),
                                       (10, 2), (10, 8), (11, 10), (12, 6), (12, 9), (13, 9), (15, 1)],
        (('Gypi2', 0), ('Gxpi2', 1), ('Gxpi2', 0), ('Gypi2', 1)): [(0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), (3, 8), (5, 5), (7, 0),
                                       (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gypi2', 1), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 0), ('Gxpi2', 0)): [(0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10),
                                              (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gypi2', 0), ('Gypi2', 1), ('Gypi2', 0), ('Gxpi2', 1), ('Gxpi2', 1)): [(0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10),
                                              (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gypi2', 1), ('Gxpi2', 0), ('Gxpi2', 1), ('Gypi2', 1), ('Gypi2', 0)): [(0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10),
                                              (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gxpi2', 0), ('Gxpi2', 0), ('Gypi2', 1), ('Gypi2', 0), ('Gypi2', 1)): [(0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10),
                                              (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gypi2', 1), ('Gypi2', 0), ('Gxpi2', 0), ('Gxpi2', 0), ('Gypi2', 1)): [(0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10),
                                              (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gypi2', 1), ('Gxpi2', 1), ('Gxpi2', 0), ('Gxpi2', 1), ('Gxpi2', 0)): [(0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), (9, 9), (9, 10),
                                              (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gxpi2', 1), ('Gypi2', 1), ('Gypi2', 1), ('Gxpi2', 1), ('Gxpi2', 0), ('Gxpi2', 0)): [(1, 1), (2, 5), (4, 3), (5, 5), (6, 3), (7, 1), (10, 2), (10, 5),
                                                     (11, 2), (11, 5), (12, 7), (12, 10), (13, 0), (13, 4), (14, 5)],
        (('Gxpi2', 0), ('Gxpi2', 1), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 1), ('Gypi2', 0)): [(0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), (9, 9),
                                                     (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gxpi2', 0), ('Gxpi2', 0), ('Gypi2', 0), ('Gxpi2', 0), ('Gypi2', 0), ('Gypi2', 0)): [(0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), (9, 9),
                                                     (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gypi2', 0), ('Gxpi2', 0), ('Gxpi2', 1), ('Gxpi2', 0), ('Gxpi2', 1), ('Gypi2', 1)): [(0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), (9, 9),
                                                     (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gypi2', 0), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 1), ('Gypi2', 1), ('Gypi2', 1)): [(0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), (3, 8),
                                                     (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6),
                                                     (14, 6), (15, 0), (15, 5)],
        (('Gxpi2', 1), ('Gxpi2', 1), ('Gypi2', 1), ('Gxpi2', 1), ('Gypi2', 1), ('Gypi2', 1)): [(1, 0), (1, 10), (4, 0), (4, 4), (4, 7), (4, 8), (5, 5), (7, 6),
                                                     (8, 9), (9, 9), (10, 2), (10, 8), (11, 10), (12, 6), (12, 9),
                                                     (13, 9), (15, 1)],
        (('Gypi2', 1), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 1), ('Gxpi2', 1), ('Gypi2', 1)): [(0, 4), (0, 6), (1, 1), (2, 2), (4, 1), (4, 3), (5, 1), (5, 3),
                                                     (6, 10), (8, 2), (8, 8), (9, 4), (10, 7), (12, 1), (13, 2),
                                                     (15, 6), (15, 9)],
        (('Gxpi2', 0), ('Gxpi2', 1), ('Gypi2', 1), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 0)): [(0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), (9, 9),
                                                     (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gypi2', 0), ('Gypi2', 0), ('Gypi2', 0), ('Gypi2', 1), ('Gypi2', 0), ('Gxpi2', 1)): [(0, 3), (1, 0), (1, 4), (3, 10), (4, 3), (5, 7), (7, 2), (7, 4),
                                                     (7, 7), (7, 8), (8, 1), (8, 5), (8, 7), (8, 9), (9, 2), (9, 6),
                                                     (10, 3), (14, 10), (15, 4)],
        (('Gxpi2', 0), ('Gypi2', 1), ('Gxpi2', 1), ('Gypi2', 0), ('Gxpi2', 1), ('Gxpi2', 1)): [(0, 1), (0, 2), (0, 5), (1, 3), (1, 9), (2, 4), (2, 10), (3, 8),
                                                     (5, 5), (7, 0), (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6),
                                                     (14, 6), (15, 0), (15, 5)],
        (('Gypi2', 0), ('Gxpi2', 0), ('Gxpi2', 1), ('Gypi2', 1), ('Gxpi2', 0), ('Gxpi2', 1)): [(0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3), (9, 9),
                                                     (9, 10), (10, 8), (12, 2), (12, 6), (14, 6), (15, 0), (15, 5)],
        (('Gypi2', 1), ('Gxpi2', 1), ('Gypi2', 0), ('Gypi2', 0), ('Gxpi2', 1), ('Gxpi2', 0), ('Gypi2', 1)): [(0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0), (9, 3),
                                                            (9, 9), (9, 10), (10, 8), (12, 2), (12, 6), (14, 6),
                                                            (15, 0), (15, 5)],
        (('Gypi2', 0), ('Gxpi2', 0), ('Gypi2', 1), ('Gxpi2', 0), ('Gxpi2', 1), ('Gxpi2', 0), ('Gypi2', 0), ('Gypi2', 1)): [(0, 1), (0, 5), (1, 3), (3, 8), (5, 5), (7, 0),
                                                                   (9, 3), (9, 9), (9, 10), (10, 8), (12, 2), (12, 6),
                                                                   (14, 6), (15, 0), (15, 5)],
        (('Gxpi2', 1), ('Gxpi2', 1), ('Gypi2', 0), ('Gxpi2', 0), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 1), ('Gypi2', 0)): [(1, 1), (2, 5), (4, 3), (5, 5), (6, 3), (7, 1),
                                                                   (10, 2), (10, 5), (11, 2), (11, 5), (12, 7),
                                                                   (12, 10), (13, 0), (13, 4), (14, 5)]
    }

    global_fidPairs_lite = None

    _pergerm_fidPairsDict_lite = None

    def _target_model(self, sslbls):
        return self._build_explicit_target_model(
            sslbls, [('Gxpi2', 1), ('Gypi2', 1), ('Gxpi2', 0), ('Gypi2', 0)],
            ['I({0}):X(pi/2,{1})', 'I({0}):Y(pi/2,{1})', 'X(pi/2,{0}):I({1})', 'Y(pi/2,{0}):I({1})'],
            effectLabels=['00', '01', '10', '11'],
            effectExpressions=['0', '1', '2', '3'])


import sys
sys.modules[__name__] = _Module()
