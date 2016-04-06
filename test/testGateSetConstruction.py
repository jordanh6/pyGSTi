import unittest
import pygsti
import numpy as np
import warnings


class GateSetConstructionTestCase(unittest.TestCase):

    def setUp(self):
        #OK for these tests, since we test user interface?
        #Set GateSet objects to "strict" mode for testing
        pygsti.objects.GateSet._strict = False


    def assertArraysAlmostEqual(self,a,b):
        self.assertAlmostEqual( np.linalg.norm(a-b), 0 )

    def assertWarns(self, callable, *args, **kwds):
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter('always')
            result = callable(*args, **kwds)
            self.assertTrue(len(warning_list) > 0)
        return result



class TestGateSetConstructionMethods(GateSetConstructionTestCase):
    
    def test_constructGates(self):
        b = "gm" #basis -- "gm" (Gell-Mann) or "std" (Standard)
        prm = "full" #parameterization "full" or "linear"
        ue = True #unitary embedding

        old_build_gate = pygsti.construction.gatesetconstruction._oldBuildGate
        leakA_old   = old_build_gate( [1,1,1], [('L0',),('L1',),('L2',)], "LX(pi,0,1)",b)
        ident_old   = old_build_gate( [2],[('Q0',)], "I(Q0)",b)
        rotXa_old   = old_build_gate( [2],[('Q0',)], "X(pi/2,Q0)",b)
        rotX2_old   = old_build_gate( [2],[('Q0',)], "X(pi,Q0)",b)
        rotYa_old   = old_build_gate( [2],[('Q0',)], "Y(pi/2,Q0)",b)
        rotZa_old   = old_build_gate( [2],[('Q0',)], "Z(pi/2,Q0)",b)
        rotLeak_old = old_build_gate( [2,1],[('Q0',),('L0',)], "X(pi,Q0):LX(pi,0,2)",b)
        leakB_old   = old_build_gate( [2,1],[('Q0',),('L0',)], "LX(pi,0,2)",b)
        rotXb_old   = old_build_gate( [2,1,1],[('Q0',),('L0',),('L1',)], "X(pi,Q0)",b)
        CnotA_old   = old_build_gate( [4],[('Q0','Q1')], "CX(pi,Q0,Q1)",b)
        CnotB_old   = old_build_gate( [4,1],[('Q0','Q1'),('L0',)], "CX(pi,Q0,Q1)",b)
        CY_old      = old_build_gate( [4],[('Q0','Q1')], "CY(pi,Q0,Q1)",b)
        CZ_old      = old_build_gate( [4],[('Q0','Q1')], "CZ(pi,Q0,Q1)",b)
        rotXstd_old = old_build_gate( [2],[('Q0',)], "X(pi/2,Q0)","std")
        rotXpp_old  = old_build_gate( [2],[('Q0',)], "X(pi/2,Q0)","pp")

        with self.assertRaises(ValueError):
            old_build_gate( [2],[('Q0',)], "X(pi/2,Q0)","FooBar") #bad basis specifier
        with self.assertRaises(ValueError):
            old_build_gate( [2],[('Q0',)], "FooBar(Q0)",b) #bad gate name
        with self.assertRaises(ValueError):
            old_build_gate( [2],[('A0',)], "I(Q0)",b) #bad state specifier (A0)
        with self.assertRaises(ValueError):
            old_build_gate( [4],[('Q0',)], "I(Q0)",b) #state space dim mismatch


        build_gate = pygsti.construction.build_gate
        leakA   = build_gate( [1,1,1], [('L0',),('L1',),('L2',)], "LX(pi,0,1)",b,prm,ue)
        ident   = build_gate( [2],[('Q0',)], "I(Q0)",b,prm,ue)
        rotXa   = build_gate( [2],[('Q0',)], "X(pi/2,Q0)",b,prm,ue)
        rotX2   = build_gate( [2],[('Q0',)], "X(pi,Q0)",b,prm,ue)
        rotYa   = build_gate( [2],[('Q0',)], "Y(pi/2,Q0)",b,prm,ue)
        rotZa   = build_gate( [2],[('Q0',)], "Z(pi/2,Q0)",b,prm,ue)
        rotNa   = build_gate( [2],[('Q0',)], "N(pi/2,1.0,0.5,0,Q0)",b,prm,ue)
        rotLeak = build_gate( [2,1],[('Q0',),('L0',)], "X(pi,Q0):LX(pi,0,2)",b,prm,ue)
        leakB   = build_gate( [2,1],[('Q0',),('L0',)], "LX(pi,0,2)",b,prm,ue)
        rotXb   = build_gate( [2,1,1],[('Q0',),('L0',),('L1',)], "X(pi,Q0)",b,prm,ue)
        CnotA   = build_gate( [4],[('Q0','Q1')], "CX(pi,Q0,Q1)",b,prm,ue)
        CnotB   = build_gate( [4,1],[('Q0','Q1'),('L0',)], "CX(pi,Q0,Q1)",b,prm,ue)
        CY      = build_gate( [4],[('Q0','Q1')], "CY(pi,Q0,Q1)",b,prm,ue)
        CZ      = build_gate( [4],[('Q0','Q1')], "CZ(pi,Q0,Q1)",b,prm,ue)
        rotXstd = build_gate( [2],[('Q0',)], "X(pi/2,Q0)","std",prm,ue)
        rotXpp  = build_gate( [2],[('Q0',)], "X(pi/2,Q0)","pp",prm,ue)

        with self.assertRaises(ValueError):
            build_gate( [2],[('Q0',)], "X(pi/2,Q0)","FooBar",prm,ue) #bad basis specifier
        with self.assertRaises(ValueError):
            build_gate( [2],[('Q0',)], "FooBar(Q0)",b,prm,ue) #bad gate name
        with self.assertRaises(ValueError):
            build_gate( [2],[('A0',)], "I(Q0)",b,prm,ue) #bad state specifier (A0)
        with self.assertRaises(ValueError):
            build_gate( [4],[('Q0',)], "I(Q0)",b,prm,ue) #state space dim mismatch
        with self.assertRaises(ValueError):
            build_gate( [2,2],[('Q0',),('Q1',)], "CZ(pi,Q0,Q1)",b,prm,ue) # Q0 & Q1 must be in same tensor-prod block of state space

        self.assertArraysAlmostEqual(leakA  , leakA_old  )
        self.assertArraysAlmostEqual(ident  , ident_old  )
        self.assertArraysAlmostEqual(rotXa  , rotXa_old  )
        self.assertArraysAlmostEqual(rotX2  , rotX2_old  )
        self.assertArraysAlmostEqual(rotYa  , rotYa_old  )
        self.assertArraysAlmostEqual(rotZa  , rotZa_old  )
        self.assertArraysAlmostEqual(rotLeak, rotLeak_old)
        self.assertArraysAlmostEqual(leakB  , leakB_old  )
        self.assertArraysAlmostEqual(rotXb  , rotXb_old  )
        self.assertArraysAlmostEqual(CnotA  , CnotA_old  )
        self.assertArraysAlmostEqual(CnotB  , CnotB_old  )
        self.assertArraysAlmostEqual(CY     , CY_old     )
        self.assertArraysAlmostEqual(CZ     , CZ_old     )


        #Do it all again with unitary embedding == False
        ue = False #unitary embedding
        leakA   = build_gate( [1,1,1], [('L0',),('L1',),('L2',)], "LX(pi,0,1)",b,prm,ue)
        ident   = build_gate( [2],[('Q0',)], "I(Q0)",b,prm,ue)
        rotXa   = build_gate( [2],[('Q0',)], "X(pi/2,Q0)",b,prm,ue)
        rotX2   = build_gate( [2],[('Q0',)], "X(pi,Q0)",b,prm,ue)
        rotYa   = build_gate( [2],[('Q0',)], "Y(pi/2,Q0)",b,prm,ue)
        rotZa   = build_gate( [2],[('Q0',)], "Z(pi/2,Q0)",b,prm,ue)
        rotNa   = build_gate( [2],[('Q0',)], "N(pi/2,1.0,0.5,0,Q0)",b,prm,ue)
        rotLeak = build_gate( [2,1],[('Q0',),('L0',)], "X(pi,Q0):LX(pi,0,2)",b,prm,ue)
        leakB   = build_gate( [2,1],[('Q0',),('L0',)], "LX(pi,0,2)",b,prm,ue)
        rotXb   = build_gate( [2,1,1],[('Q0',),('L0',),('L1',)], "X(pi,Q0)",b,prm,ue)
        CnotA   = build_gate( [4],[('Q0','Q1')], "CX(pi,Q0,Q1)",b,prm,ue)
        CnotB   = build_gate( [4,1],[('Q0','Q1'),('L0',)], "CX(pi,Q0,Q1)",b,prm,ue)
        CY      = build_gate( [4],[('Q0','Q1')], "CY(pi,Q0,Q1)",b,prm,ue)
        CZ      = build_gate( [4],[('Q0','Q1')], "CZ(pi,Q0,Q1)",b,prm,ue)
        rotXstd = build_gate( [2],[('Q0',)], "X(pi/2,Q0)","std",prm,ue)
        rotXpp  = build_gate( [2],[('Q0',)], "X(pi/2,Q0)","pp",prm,ue)

        self.assertArraysAlmostEqual(leakA  , leakA_old  )
        self.assertArraysAlmostEqual(ident  , ident_old  )
        self.assertArraysAlmostEqual(rotXa  , rotXa_old  )
        self.assertArraysAlmostEqual(rotX2  , rotX2_old  )
        self.assertArraysAlmostEqual(rotYa  , rotYa_old  )
        self.assertArraysAlmostEqual(rotZa  , rotZa_old  )
        self.assertArraysAlmostEqual(rotLeak, rotLeak_old)
        self.assertArraysAlmostEqual(leakB  , leakB_old  )
        self.assertArraysAlmostEqual(rotXb  , rotXb_old  )
        self.assertArraysAlmostEqual(CnotA  , CnotA_old  )
        self.assertArraysAlmostEqual(CnotB  , CnotB_old  )
        self.assertArraysAlmostEqual(CY     , CY_old     )
        self.assertArraysAlmostEqual(CZ     , CZ_old     )

        


        leakA_ans = np.array( [[ 0.,  1.,  0.],
                               [ 1.,  0.,  0.],
                               [ 0.,  0.,  1.]], 'd')
        self.assertArraysAlmostEqual(leakA, leakA_ans)

        rotXa_ans = np.array([[ 1.,  0.,  0.,  0.],
                              [ 0.,  1.,  0.,  0.],
                              [ 0.,  0.,  0,  -1.],
                              [ 0.,  0.,  1.,  0]], 'd')
        self.assertArraysAlmostEqual(rotXa, rotXa_ans)

        rotX2_ans = np.array([[ 1.,  0.,  0.,  0.],
                              [ 0.,  1.,  0.,  0.],
                              [ 0.,  0., -1.,  0.],
                              [ 0.,  0.,  0., -1.]], 'd')
        self.assertArraysAlmostEqual(rotX2, rotX2_ans)
        
        rotLeak_ans = np.array([[ 0.5,         0.,          0.,         -0.5,         0.70710678],
                                [ 0.,          0.,          0.,          0.,          0.        ],
                                [ 0.,          0.,          0.,          0.,          0.        ],
                                [ 0.5,         0.,          0.,         -0.5,        -0.70710678],
                                [ 0.70710678,  0.,          0.,          0.70710678,  0.        ]], 'd')
        self.assertArraysAlmostEqual(rotLeak, rotLeak_ans)

        leakB_ans = np.array(  [[ 0.5,         0.,          0.,         -0.5,         0.70710678],
                                [ 0.,          0.,          0.,          0.,          0.        ],
                                [ 0.,          0.,          0.,          0.,          0.        ],
                                [-0.5,         0.,          0.,          0.5,         0.70710678],
                                [ 0.70710678,  0.,          0.,          0.70710678,  0.        ]], 'd')
        self.assertArraysAlmostEqual(leakB, leakB_ans)

        rotXb_ans = np.array( [[ 1.,  0.,  0.,  0.,  0.,  0.],
                               [ 0.,  1.,  0.,  0.,  0.,  0.],
                               [ 0.,  0., -1.,  0.,  0.,  0.],
                               [ 0.,  0.,  0., -1.,  0.,  0.],
                               [ 0.,  0.,  0.,  0.,  1.,  0.],
                               [ 0.,  0.,  0.,  0.,  0.,  1.]], 'd')
        self.assertArraysAlmostEqual(rotXb, rotXb_ans)

        A = 9.42809042e-01
        B = 3.33333333e-01
        CnotA_ans = np.array( [[ 1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,  1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,    0,  1.0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,  1.0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,  1.0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,  1.0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,  1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,  1.0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0, -1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0, -1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0, -1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0, -1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0, -1.0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,  1.0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    B,    A ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    A,   -B ]], 'd')
        self.assertArraysAlmostEqual(CnotA, CnotA_ans)

        CnotB_ans = np.array( [[ 1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,  1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,    0,  1.0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,  1.0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,  1.0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,  1.0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,  1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,  1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0, -1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0, -1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0, -1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0, -1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0, -1.0,    0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,  1.0,    0,    0,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    B,    A,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    A,   -B,    0 ],
                               [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    1 ]], 'd')
        self.assertArraysAlmostEqual(CnotB, CnotB_ans)

    def test_parameterized_gate(self):

        # A single-qubit gate on a 2-qubit space, parameterizes so that there are only 16 gate parameters
        gate = pygsti.construction.build_gate( [4],[('Q0','Q1')], "X(pi,Q0)","gm",
                                               parameterization="linear")
        gate2 = pygsti.construction.build_gate( [2],[('Q0',)], "D(Q0)","gm", parameterization="linear")
        gate3 = pygsti.construction.build_gate( [4],[('Q0','Q1')], "X(pi,Q0):D(Q1)","gm",
                                               parameterization="linear") #composes parameterized gates


        
        with self.assertRaises(ValueError):
            gate = pygsti.construction.build_gate( [4],[('Q0','Q1')], "X(pi,Q0)","gm",
                                                   parameterization="linear",unitaryEmbedding=True) 
            #no unitary embedding support for "linear"

        with self.assertRaises(ValueError):
            gate = pygsti.construction.build_gate( [4],[('Q0','Q1')], "X(pi,Q0)","gm", 
                                                   parameterization="FooBar") # bad parameterization



        A = -5.77350269e-01
        B = 8.16496581e-01
        C = -6.66666667e-01
        D = -4.71404521e-01
        E = -3.33333333e-01
        gate_ans = np.array( [[ 1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                              [   0,    0,    0,    0,    0,    0,  1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                              [   0,    0,  1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                              [   0,    0,    0,    0,  1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                              [   0,    0,    0,  1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                              [   0,    0,    0,    0,    0,  1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                              [   0,  1.0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                              [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,  1.0,    0,    0,    0 ],
                              [   0,    0,    0,    0,    0,    0,    0,    0, -1.0,    0,    0,    0,    0,    0,    0,    0 ],
                              [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0, -1.0,    0,    0,    0,    0,    0 ],
                              [   0,    0,    0,    0,    0,    0,    0,    0,    0, -1.0,    0,    0,    0,    0,    0,    0 ],
                              [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0, -1.0,    0,    0,    0,    0 ],
                              [   0,    0,    0,    0,    0,    0,    0,  1.0,    0,    0,    0,    0,    0,    0,    0,    0 ],
                              [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    A,    B ],
                              [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    A,    C,    D ],
                              [   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    B,    D,    E ]], 'd')
        self.assertArraysAlmostEqual(gate, gate_ans)

        vec = gate.to_vector()
        self.assertEqual(vec.shape, (16,)) #should only have 16 parameters
        self.assertEqual(gate.dtype, np.float64)  #should be real-valued

        #Note: answer is all zeros b/c parameters give *deviation* from base matrix, and this case has no deviation
        vec_ans = np.array([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0., 0.,  0.,  0.,  0.,  0., 0.], 'd')
        self.assertArraysAlmostEqual(vec, vec_ans)


    def test_build_gatesets(self):

        stateSpace = [2] #density matrix is a 2x2 matrix
        spaceLabels = [('Q0',)] #interpret the 2x2 density matrix as a single qubit named 'Q0'
        gateset1 = pygsti.objects.GateSet()
        gateset1['rho0'] = pygsti.construction.build_vector(stateSpace,spaceLabels,"0")
        gateset1['E0']   = pygsti.construction.build_vector(stateSpace,spaceLabels,"1")
        gateset1['Gi'] = pygsti.construction.build_gate(stateSpace,spaceLabels,"I(Q0)")
        gateset1['Gx'] = pygsti.construction.build_gate(stateSpace,spaceLabels,"X(pi/2,Q0)")
        gateset1['Gy'] = pygsti.construction.build_gate(stateSpace,spaceLabels,"Y(pi/2,Q0)")
        gateset1['identity'] = pygsti.construction.build_identity_vec(stateSpace)
        gateset1.spamdefs['plus']  = ('rho0','E0')
        gateset1.spamdefs['minus_take_one'] = ('rho0','remainder')
        gateset1.spamdefs['minus'] = ('rho0','remainder') #tests replacement of spam label
        
        #Removed checks for unset labels for now.
        #with self.assertRaises(ValueError):
        #    gateset1.spamdefs['badspam'] = ('rhoNonExistent','E0') # bad rho index
        #with self.assertRaises(ValueError):
        #    gateset1.spamdefs['bade'] = ('rho0','ENonExistent') # bad E index


        gateset_evec_first = pygsti.objects.GateSet() #set identity vector first
        gateset_evec_first['E0'] = pygsti.construction.build_vector(stateSpace,spaceLabels,"1")

        gateset_id_first = pygsti.objects.GateSet() #set identity vector first
        gateset_id_first['identity'] =  pygsti.construction.build_identity_vec(stateSpace)
        with self.assertRaises(ValueError):
            gateset_id_first['identity'] = np.array([1,2,3],'d') #wrong dimension
        with self.assertRaises(ValueError):
            gateset_id_first['rhoBad'] =  np.array([1,2,3],'d') #wrong dimension
        with self.assertRaises(ValueError):
            gateset_id_first['E0'] =  np.array([1,2,3],'d') #wrong dimension

        gateset2 = pygsti.construction.build_gateset( [2], [('Q0',)],['Gi','Gx','Gy'], 
                                                      [ "I(Q0)","X(pi/2,Q0)", "Y(pi/2,Q0)"],
                                                      prepLabels=['rho0'], prepExpressions=["0"],
                                                      effectLabels=['E0'], effectExpressions=["1"], 
                                                      spamdefs={'plus': ('rho0','E0'),
                                                                     'minus': ('rho0','remainder') })
#HERE
        gateset3 = self.assertWarns(pygsti.construction.build_gateset, 
                                    [2], [('Q0',)],['Gi','Gx','Gy'], 
                                    [ "I(Q0)","X(pi/2,Q0)", "Y(pi/2,Q0)"],
                                    prepLabels=['rho0'], prepExpressions=["0"],
                                    effectLabels=['E0'], effectExpressions=["1"], 
                                    spamdefs={'plus': ('rho0','E0'),
                                                   'minus': ('remainder','remainder') })

        gateset4_txt = \
"""
# Test text file describing a gateset

# State prepared, specified as a state in the Pauli basis (I,X,Y,Z)
rho
PauliVec
1/sqrt(2) 0 0 1/sqrt(2)

# State measured as yes outcome, also specified as a state in the Pauli basis
E
PauliVec
1/sqrt(2) 0 0 -1/sqrt(2)

Gi
PauliMx
1 0 0 0
0 1 0 0
0 0 1 0
0 0 0 1

Gx
PauliMx
1 0 0 0
0 1 0 0
0 0 0 1
0 0 -1 0

Gy
PauliMx
1 0 0 0
0 0 0 -1
0 0 1 0
0 1 0 0

IDENTITYVEC sqrt(2) 0 0 0
SPAMLABEL plus = rho E
SPAMLABEL minus = rho remainder
"""
        open("temp_test_files/Test_Gateset.txt","w").write(gateset4_txt)
        gateset4 = pygsti.io.load_gateset("temp_test_files/Test_Gateset.txt")

        std_gateset = pygsti.construction.build_gateset( [2], [('Q0',)],['Gi','Gx','Gy'], 
                                                         [ "I(Q0)","X(pi/8,Q0)", "Y(pi/8,Q0)"],
                                                         prepLabels=['rho0'], prepExpressions=["0"],
                                                         effectLabels=['E0'], effectExpressions=["1"], 
                                                         spamdefs={'plus': ('rho0','E0'),
                                                                        'minus': ('rho0','remainder') },
                                                         basis="std")

        pp_gateset = pygsti.construction.build_gateset( [2], [('Q0',)],['Gi','Gx','Gy'], 
                                                        [ "I(Q0)","X(pi/8,Q0)", "Z(pi/8,Q0)"],
                                                        prepLabels=['rho0'], prepExpressions=["0"],
                                                        effectLabels=['E0'], effectExpressions=["1"], 
                                                        spamdefs={'plus': ('rho0','E0'),
                                                                       'minus': ('rho0','remainder') },
                                                        basis="pp")

        with self.assertRaises(ValueError):
            pygsti.construction.build_gateset( [2], [('A0',)],['Gi','Gx','Gy'], 
                                               [ "I(Q0)","X(pi/8,Q0)", "Y(pi/8,Q0)"],
                                               prepLabels=['rho0'], prepExpressions=["0"],
                                               effectLabels=['E0'], effectExpressions=["1"], 
                                               spamdefs={'plus': ('rho0','E0'),
                                                              'minus': ('rho0','remainder') })
                                               # invalid state specifier (A0)

        with self.assertRaises(ValueError):
            pygsti.construction.build_gateset( [4], [('Q0',)],['Gi','Gx','Gy'], 
                                               [ "I(Q0)","X(pi/8,Q0)", "Y(pi/8,Q0)"],
                                               prepLabels=['rho0'], prepExpressions=["0"],
                                               effectLabels=['E0'], effectExpressions=["1"], 
                                               spamdefs={'plus': ('rho0','E0'),
                                                              'minus': ('rho0','remainder') })
                                               # state space dimension mismatch (4 != 2)
            
        with self.assertRaises(ValueError):
            pygsti.construction.build_gateset( [2], [('Q0',)],['Gi','Gx','Gy'], 
                                               [ "I(Q0)","X(pi/8,Q0)", "Y(pi/8,Q0)"],
                                               prepLabels=['rho0'], prepExpressions=["0"],
                                               effectLabels=['E0'], effectExpressions=["1"], 
                                               spamdefs={'plus': ('rho0','E0'),
                                                              'minus': ('rho0','remainder') },
                                               basis="FooBar") #Bad basis

        with self.assertRaises(ValueError):
            pygsti.construction.build_gateset( [2], [('Q0',)],['Gi','Gx','Gy'], 
                                               [ "I(Q0)","X(pi/8,Q0)", "Y(pi/8,Q0)"],
                                               prepLabels=['rho0'], prepExpressions=["FooBar"],
                                               effectLabels=['E0'], effectExpressions=["1"], 
                                               spamdefs={'plus': ('rho0','E0'),
                                                              'minus': ('rho0','remainder') })
                                               #Bad rhoExpression
        with self.assertRaises(ValueError):
            pygsti.construction.build_gateset( [2], [('Q0',)],['Gi','Gx','Gy'], 
                                               [ "I(Q0)","X(pi/8,Q0)", "Y(pi/8,Q0)"],
                                               prepLabels=['rho0'], prepExpressions=["0"],
                                               effectLabels=['E0'], effectExpressions=["FooBar"], 
                                               spamdefs={'plus': ('rho0','E0'),
                                                              'minus': ('rho0','remainder') })
                                               #Bad EExpression


    def test_two_qubit_gate(self):
        gate = pygsti.two_qubit_gate(xx=0.5, xy=0.5, xz=0.5, yy=0.5, yz=0.5, zz=0.5)

        
    def test_gateset_tools(self):

        gateset = pygsti.construction.build_gateset( [2], [('Q0',)],['Gi','Gx','Gy'], 
                                                     [ "I(Q0)","X(pi/2,Q0)", "Y(pi/2,Q0)"],
                                                     prepLabels=['rho0'], prepExpressions=["0"],
                                                     effectLabels=['E0'], effectExpressions=["1"], 
                                                     spamdefs={'plus': ('rho0','E0'),
                                                                    'minus': ('rho0','remainder') })

        gateset_2q = pygsti.construction.build_gateset( 
            [4], [('Q0','Q1')],['GIX','GIY','GXI','GYI','GCNOT'], 
            [ "I(Q0):X(pi/2,Q1)", "I(Q0):Y(pi/2,Q1)", "X(pi/2,Q0):I(Q1)", "Y(pi/2,Q0):I(Q1)", "CX(pi,Q0,Q1)" ],
            prepLabels=['rho0'], prepExpressions=["0"], effectLabels=['E0','E1','E2'], effectExpressions=["0","1","2"], 
            spamdefs={'upup': ('rho0','E0'), 'updn': ('rho0','E1'),
                           'dnup': ('rho0','E2'), 'dndn': ('rho0','remainder') }, basis="pp")

        gateset_rot = gateset.rotate( (np.pi/2,0,0) ) #rotate all gates by pi/2 about X axis
        gateset_randu = gateset.randomize_with_unitary(0.01)
        gateset_randu = gateset.randomize_with_unitary(0.01,seed=1234)
        #print gateset_rot

        rotXPi   = pygsti.construction.build_gate( [2],[('Q0',)], "X(pi,Q0)")
        rotXPiOv2   = pygsti.construction.build_gate( [2],[('Q0',)], "X(pi/2,Q0)")
        rotYPiOv2   = pygsti.construction.build_gate( [2],[('Q0',)], "Y(pi/2,Q0)")

        self.assertArraysAlmostEqual(gateset_rot['Gi'], rotXPiOv2)
        self.assertArraysAlmostEqual(gateset_rot['Gx'], rotXPi)
        self.assertArraysAlmostEqual(gateset_rot['Gx'], np.dot(rotXPiOv2,rotXPiOv2))
        self.assertArraysAlmostEqual(gateset_rot['Gy'], np.dot(rotXPiOv2,rotYPiOv2))

        gateset_2q_rot = gateset_2q.rotate(rotate=list(np.zeros(15,'d')))
        gateset_2q_randu = gateset_2q.randomize_with_unitary(0.01)
        gateset_2q_randu = gateset_2q.randomize_with_unitary(0.01,seed=1234)

        #TODO: test 2q rotated gates??

        gateset_dep = gateset.depolarize(gate_noise=0.1)
        #print gateset_dep

        Gi_dep = np.array([[ 1,   0,   0,   0 ],
                           [ 0, 0.9,   0,   0 ],
                           [ 0,   0, 0.9,   0 ],
                           [ 0,   0,   0, 0.9 ]], 'd')
        Gx_dep = np.array([[ 1,   0,   0,   0 ],
                           [ 0, 0.9,   0,   0 ],
                           [ 0,   0,   0,-0.9 ],
                           [ 0,   0, 0.9,   0 ]], 'd')
        Gy_dep = np.array([[ 1,   0,   0,   0 ],
                           [ 0,   0,   0, 0.9 ],
                           [ 0,   0, 0.9,   0 ],
                           [ 0,-0.9,   0,   0 ]], 'd')

        self.assertArraysAlmostEqual(gateset_dep['Gi'], Gi_dep)
        self.assertArraysAlmostEqual(gateset_dep['Gx'], Gx_dep)
        self.assertArraysAlmostEqual(gateset_dep['Gy'], Gy_dep)


        gateset_spam = gateset.depolarize(spam_noise=0.1)
        #print gateset_spam
        self.assertAlmostEqual(np.dot(gateset['E0'].T,gateset['rho0']), 0)
        self.assertAlmostEqual(np.dot(gateset_spam['E0'].T,gateset_spam['rho0']),0.095)
        self.assertArraysAlmostEqual(gateset_spam['rho0'], 1/np.sqrt(2)*np.array([1,0,0,0.9]).reshape(-1,1) )
        self.assertArraysAlmostEqual(gateset_spam['E0'], 1/np.sqrt(2)*np.array([1,0,0,-0.9]).reshape(-1,1) )

        gateset_rand_rot = gateset.rotate(max_rotate=0.2)
        gateset_rand_rot = gateset.rotate(max_rotate=0.2,seed=1234)
        with self.assertRaises(ValueError):
            gateset.rotate(rotate=0.2,max_rotate=0.2) #can't specify both
        with self.assertRaises(ValueError):
            gateset.rotate() #must specify rotate or max_rotate
        with self.assertRaises(ValueError):
            gateset.rotate( (1,2,3,4) ) #tuple must be length 3 (or a float)
        with self.assertRaises(ValueError):
            gateset.rotate( "a string!" ) #must be a 3-tuple or float
        with self.assertRaises(ValueError):
            gateset_2q.rotate(rotate=(0,0,0)) #wrong dimension gateset


        gateset_2q_rand_rot = gateset_2q.rotate(max_rotate=0.2)
        gateset_2q_rand_rot = gateset_2q.rotate(max_rotate=0.2,seed=1234)
        with self.assertRaises(ValueError):
            gateset_2q.rotate(rotate=0.2,max_rotate=0.2) #can't specify both
        with self.assertRaises(ValueError):
            gateset_2q.rotate() #must specify rotate or max_rotate
        with self.assertRaises(ValueError):
            gateset_2q.rotate( (1,2,3,4) ) #tuple must be length 15 (or a float)
        with self.assertRaises(ValueError):
            gateset_2q.rotate( "a string!" ) #must be a 3-tuple or float
        with self.assertRaises(ValueError):
            gateset.rotate( rotate=np.zeros(15,'d')) #wrong dimension gateset

        gateset_rand_dep = gateset.depolarize(max_gate_noise=0.1)
        gateset_rand_dep = gateset.depolarize(max_gate_noise=0.1, seed=1234)
        with self.assertRaises(ValueError):
            gateset.depolarize(gate_noise=0.1,max_gate_noise=0.1, spam_noise=0) #can't specify both

        gateset_rand_spam = gateset.depolarize(max_spam_noise=0.1)
        gateset_rand_spam = gateset.depolarize(max_spam_noise=0.1,seed=1234)
        with self.assertRaises(ValueError):
            gateset.depolarize(spam_noise=0.1,max_spam_noise=0.1) #can't specify both

        
    def test_spamspecs(self):
        strs = pygsti.construction.gatestring_list( [('Gx',),('Gy',),('Gx','Gx')] )
        prepSpecs, effectSpecs = pygsti.construction.build_spam_specs(fiducialGateStrings=strs)

        with self.assertRaises(ValueError):
            pygsti.construction.build_spam_specs(prepSpecs=prepSpecs, prepStrs=strs) #can't specify both...
            
        with self.assertRaises(ValueError):
            pygsti.construction.build_spam_specs(prepStrs=strs, fiducialGateStrings=strs) #can't specify both...

        with self.assertRaises(ValueError):
            pygsti.construction.build_spam_specs() # must specify something!

        with self.assertRaises(ValueError):
            pygsti.construction.build_spam_specs(prepStrs=strs, effectSpecs=effectSpecs, effectStrs=strs) #can't specify both...
            
        with self.assertRaises(ValueError):
            pygsti.construction.build_spam_specs(effectStrs=strs, fiducialGateStrings=strs) #can't specify both...
            
        with self.assertRaises(ValueError):
            pygsti.construction.build_spam_specs(prepStrs=strs) # must specify some E-thing!

    def test_gate_object(self):
        gate_full = pygsti.construction.build_gate( [2],[('Q0',)], "I(Q0)","gm", parameterization="full")
        gate_linear = pygsti.construction.build_gate( [2],[('Q0',)], "D(Q0)","gm", parameterization="linear")
        gate_linear_copy = gate_linear.copy()
        gate_full_copy = gate_full.copy()

        full_as_str = str(gate_full)
        linear_as_str = str(gate_linear)

        #Linear from scratch
        baseMx = np.zeros( (2,2) )
        paramArray = np.array( [1.0,1.0] )
        parameterToBaseIndicesMap = { 0: [(0,0)], 1: [(1,1)] } #parameterize only the diagonal els
        gate_linear_B = pygsti.obj.LinearlyParameterizedGate(baseMx, paramArray,
                                                             parameterToBaseIndicesMap, real=True)
        with self.assertRaises(ValueError):
            pygsti.obj.LinearlyParameterizedGate(baseMx, np.array( [1.0+1j, 1.0] ),
                                                 parameterToBaseIndicesMap, real=True) #must be real
            
        numParams = gate_linear_B.num_params()
        v = gate_linear_B.to_vector()
        gate_linear_B.from_vector(v)
        deriv = gate_linear_B.deriv_wrt_params()

        #Full from scratch
        mx = np.array( [[1,0],[0,1]], 'd' )
        gate_full_B = pygsti.obj.FullyParameterizedGate(mx)
            
        numParams = gate_full_B.num_params()
        v = gate_full_B.to_vector()
        gate_full_B.from_vector(v)
        deriv = gate_full_B.deriv_wrt_params()

        
      
if __name__ == "__main__":
    unittest.main(verbosity=2)