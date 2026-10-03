import unittest
from dataclasses import replace
from app.model import Parameters, solve, ws, simulate, describe

class ModelTests(unittest.TestCase):
    def setUp(self):
        self.p = Parameters()

    def test_initial_and_intersection(self):
        r=solve(self.p)
        self.assertAlmostEqual(r['u'], .1)
        self.assertAlmostEqual(r['index'], 100)
        self.assertAlmostEqual(r['employment'], .9)
        for p in [self.p, replace(self.p,z=.15),replace(self.p,A=1.1,beta=0),replace(self.p,alpha=.1)]:
            r=solve(p)
            self.assertAlmostEqual(ws(p,r['u']),r['w'])

    def test_six_scenarios(self):
        baseline=solve(self.p)
        for updates, direction, wage_direction in [({'z':.15},1,0),({'z':-.15},-1,0),({'mu':.4},1,-1),({'mu':.05},-1,1),({'A':1.1},0,1),({'A':1.1,'beta':0},-1,1)]:
            r=solve(replace(self.p,**updates))
            if direction: self.assertGreater(direction*(r['u']-baseline['u']),0)
            else: self.assertAlmostEqual(r['u'],baseline['u'])
            if wage_direction: self.assertGreater(wage_direction*(r['w']-baseline['w']),0)
            else: self.assertAlmostEqual(r['w'],baseline['w'])

    def test_productivity_invariance(self):
        for A in [.2,.8,1,1.1,3]:
            self.assertAlmostEqual(solve(replace(self.p,A=A))['u'],.1)

    def test_axes(self):
        a=simulate({'axis':'unemployment'})['result']
        b=simulate({'axis':'employment'})['result']
        self.assertAlmostEqual(a['x']+b['x'],100)
        self.assertEqual(a['u'],b['u']);self.assertEqual(a['index'],b['index'])

    def test_observed_independence(self):
        a=solve(self.p);b=solve(replace(self.p,observed=.35))
        for key in ['u','index','ws','employment']: self.assertEqual(a[key],b[key])
        self.assertGreater(solve(replace(self.p,observed=.05))['gap'],0)
        self.assertLess(b['gap'],0)

    def test_outside_domain_and_boundary(self):
        for p in [replace(self.p,z=-1),replace(self.p,z=1,alpha=.1)]:
            r=solve(p);self.assertFalse(r['in_domain']);self.assertFalse(r['interior'])
            self.assertIn('Aucun équilibre intérieur',describe(p,self.p))
        self.assertLess(solve(replace(self.p,z=-1))['u'],0)
        self.assertGreater(solve(replace(self.p,z=1,alpha=.1))['u'],1)

    def test_validation(self):
        for x in [{'alpha':0},{'A':0},{'beta':1.1},{'mu':float('nan')},{'z':True},{'observed':2},{'A':'1'},{'oops':1}]:
            with self.assertRaises(ValueError): Parameters.parse(x)

    def test_requests_independent_and_base_fixed(self):
        a=simulate({'parameters':{'A':2},'reference':{'A':2}})
        b=simulate({})
        self.assertAlmostEqual(a['result']['index'],200)
        self.assertAlmostEqual(b['result']['index'],100)
        self.assertAlmostEqual(b['result']['u'],.1)

if __name__=='__main__': unittest.main()
