import copy
import json
import unittest
from app.economics import calculate, bridge, DEFAULTS, validate
from app.pedagogy import catalog
from app.units import dashboard, indicator, radar, percent, proportion

class LabTests(unittest.TestCase):
    def calc(self, model, p=None, **kwargs):
        return calculate({'model':model,'parameters':p or {},**kwargs})

    def test_wsps_compatibility_and_units(self):
        result=self.calc('wsps')['result']
        self.assertAlmostEqual(result['raw']['u'],.1)
        self.assertAlmostEqual(result['metrics'][1]['value'],100)
        self.assertAlmostEqual(percent(proportion(20)),20)
        self.assertGreater(self.calc('wsps',{'mu':40})['result']['raw']['u'],.1)

    def test_phillips_direction_and_neutral_point(self):
        base=self.calc('phillips')['result']
        self.assertAlmostEqual(base['raw']['pi'],2)
        self.assertAlmostEqual(self.calc('phillips',{'u':8})['result']['raw']['pi'],3)
        self.assertAlmostEqual(self.calc('phillips',{'expected':4})['result']['raw']['pi'],4)
        result=self.calc('phillips',{'cost':2})['result']
        self.assertAlmostEqual(result['raw']['neutral_u'],14)
        self.assertAlmostEqual(result['raw']['pi'],4)
        neutral=self.calc('phillips',{'cost':2,'u':14})['result']
        self.assertAlmostEqual(neutral['raw']['pi'],2)

    def test_fixed_and_adaptive_trajectories(self):
        fixed=self.calc('phillips',{'u':8},expectation='fixed')['result']['trajectory']
        adaptive=self.calc('phillips',{'u':8},expectation='adaptive')['result']['trajectory']
        self.assertEqual(len(fixed),13)
        self.assertTrue(all(row['inflation']==3 and row['expected']==2 for row in fixed))
        self.assertAlmostEqual(adaptive[1]['expected'],2.5)
        self.assertAlmostEqual(adaptive[1]['inflation'],3.5)
        self.assertAlmostEqual(adaptive[12]['inflation'],9)
        no_adaptation=self.calc('phillips',{'u':8,'adaptation':0},expectation='adaptive')['result']['trajectory']
        self.assertEqual(no_adaptation,fixed)

    def test_okun_threshold_units_and_initial_level(self):
        for growth,expected in [(1,.4),(2,0),(4,-.8),(-2,1.6)]:
            r=self.calc('okun',{'growth':growth})['result']
            self.assertAlmostEqual(r['raw']['delta_u'],expected)
            self.assertAlmostEqual(r['raw']['next_u'],10+expected)
        a=self.calc('okun',{'initial_u':5})['result']
        b=self.calc('okun',{'initial_u':15})['result']
        self.assertEqual(a['curves'],b['curves'])
        self.assertNotEqual(a['metrics'][1]['value'],b['metrics'][1]['value'])

    def test_outside_domain_not_clamped(self):
        r=self.calc('okun',{'initial_u':0,'growth':12})['result']
        self.assertLess(r['raw']['next_u'],0)
        self.assertIsNone(r['indicators']['unemployment']['value'])
        self.assertTrue(r['warnings'])
        r=self.calc('wsps',{'z':-1})['result']
        self.assertLess(r['raw']['u'],0)
        self.assertFalse(r['points'])
        self.assertTrue(r['warnings'])

    def test_only_computed_dimensions(self):
        for model in DEFAULTS:
            indicators=self.calc(model)['result']['indicators']
            self.assertIsNone(indicators['external']['value'])
            self.assertIsNone(indicators['debt']['value'])
        self.assertIsNone(self.calc('okun')['result']['indicators']['inflation']['value'])
        self.assertIsNone(self.calc('wsps')['result']['indicators']['inflation']['value'])
        self.assertEqual(self.calc('phillips')['result']['indicators']['unemployment']['status'],'donnée')

    def test_axis_invariance(self):
        u=self.calc('wsps')['result'];e=self.calc('wsps',axis='employment')['result']
        self.assertEqual(u['raw'],e['raw'])
        self.assertAlmostEqual(u['points'][0]['x']+e['points'][0]['x'],100)

    def test_reference_and_interpolation(self):
        data=self.calc('okun',{'growth':4},fraction=.5)
        self.assertEqual(data['current_parameters']['growth'],3)
        self.assertAlmostEqual(data['result']['raw']['delta_u'],-.4)
        a=self.calc('wsps',{'A':2},reference={'A':2})
        self.assertAlmostEqual(a['result']['raw']['index'],200)
        for fraction in [0,.25,.5,.75,1]:
            data=self.calc('phillips',{'cost':2},fraction=fraction)
            self.assertAlmostEqual(data['result']['raw']['pi'],2+2*fraction)
            self.assertEqual(data['extent_y'],self.calc('phillips',{'cost':2})['extent_y'])

    def test_radar_normalization_and_missing_values(self):
        result=radar(dashboard(inflation=indicator(2),growth=indicator(20),unemployment=indicator(10)))
        self.assertEqual(result['inflation']['score'],1)
        self.assertEqual(result['unemployment']['score'],.5)
        self.assertGreater(result['growth']['score'],1)
        self.assertTrue(result['growth']['outside'])
        self.assertIsNone(result['external']['score'])
        self.assertLess(radar(dashboard(inflation=indicator(-2)))['inflation']['score'],1)

    def test_bridge_requires_explicit_assumption(self):
        with self.assertRaises(ValueError):bridge({'parameters':{}})
        r=bridge({'accepted':True,'parameters':{'mu':40}})
        self.assertAlmostEqual(r['ustar'],100*(13/12-1/1.4)/2.5)
        with self.assertRaises(ValueError):bridge({'accepted':True,'parameters':{'z':-1}})
        with self.assertRaises(ValueError):bridge({'accepted':True,'parameters':{'alpha':.3}})

    def test_invalid_requests(self):
        for payload in [{'model':'unknown'},{'model':[]},{'model':'okun','parameters':{'reaction':0}},
                        {'model':'phillips','parameters':{'u':float('nan')}}, {'fraction':True},
                        {'period':1.2},{'period':13},{'period':True},{'axis':'wrong'},{'expectation':'rational'}]:
            with self.assertRaises(ValueError):calculate(payload)

    def test_keynesian_cross_multiplier_and_leakages(self):
        closed=self.calc('multiplier',{'t':0,'m':0,'c':.8})['result']['raw']
        self.assertAlmostEqual(closed['multiplier'],1/(1-.8))
        raised_data=self.calc('multiplier',{'G':15});raised=raised_data['result']
        self.assertAlmostEqual(raised['raw']['delta_Y'],5*raised['raw']['multiplier'])
        self.assertAlmostEqual(raised['raw']['delta_trade_balance'],-raised['raw']['delta_imports'])
        closed_k=self.calc('multiplier',{'m':0})['result']['raw']['multiplier']
        open_k=self.calc('multiplier',{'m':.25})['result']['raw']['multiplier']
        self.assertGreater(closed_k,open_k)
        self.assertEqual(len(raised['trajectory']),12)
        self.assertAlmostEqual(raised['trajectory'][0]['contribution'],5)
        self.assertAlmostEqual(raised['metrics'][5]['value'],raised_data['reference']['raw']['Y'])
        outside=self.calc('multiplier',{'c':.2,'m':.5})['result']
        self.assertFalse(outside['raw']['wave_valid'])
        self.assertEqual(outside['trajectory'],[])
        self.assertIn('0 ≤ b < 1',outside['warnings'][0])

    def test_policy_equilibria_and_monetary_expansion(self):
        for variant in ('lm','mp'):
            result=self.calc('policy',variant=variant)['result']['raw']
            self.assertAlmostEqual(result['IS_residual'],0,places=9)
            self.assertAlmostEqual(result['other_residual'],0,places=9)
        base=self.calc('policy')['result']['raw']
        ease=self.calc('policy',{'real_money':35},variant='lm')['result']['raw']
        self.assertGreater(ease['Y'],base['Y'])
        self.assertLess(ease['r'],base['r'])
        # Same IS and G shock: a positive MP reaction moderates the output response.
        constant=self.calc('policy',{'G':30,'phi':0},reference={'G':20,'phi':0},variant='mp')
        reacting=self.calc('policy',{'G':30,'phi':.8},reference={'G':20,'phi':.8},variant='mp')
        dy0=constant['result']['raw']['Y']-constant['reference']['raw']['Y']
        dy1=reacting['result']['raw']['Y']-reacting['reference']['raw']['Y']
        self.assertGreater(dy0,dy1)

    def test_aggregate_demand_supply_shock_directions(self):
        base=self.calc('ad_as')['result']['raw']
        demand=self.calc('ad_as',{'d':8})['result']['raw']
        cost=self.calc('ad_as',{'s':8})['result']['raw']
        self.assertGreater(demand['Y'],base['Y']);self.assertGreater(demand['P'],base['P'])
        self.assertLess(cost['Y'],base['Y']);self.assertGreater(cost['P'],base['P'])
        self.assertLess(cost['output_gap'],base['output_gap'])
        with self.assertRaisesRegex(ValueError,'production d’équilibre doit être positive'):
            self.calc('multiplier',{'C0':0,'I0':0,'G':0,'X0':0})

    def test_no_shared_user_state(self):
        defaults=copy.deepcopy(DEFAULTS)
        a=self.calc('phillips',{'u':8,'expected':10})
        b=self.calc('phillips')
        self.assertNotEqual(a['result']['raw']['pi'],b['result']['raw']['pi'])
        self.assertEqual(defaults,DEFAULTS)
        json.dumps(catalog(),allow_nan=False)

if __name__=='__main__':unittest.main()
