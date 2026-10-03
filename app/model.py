"""Modèle WS-PS pédagogique pur : aucun état utilisateur partagé."""
from dataclasses import dataclass, asdict
import math

B = 13 / 12
SCALE = 120

@dataclass(frozen=True)
class Parameters:
    A: float = 1
    mu: float = .2
    z: float = 0
    alpha: float = 2.5
    beta: float = 1
    observed: float = .1

    @classmethod
    def parse(cls, values):
        if not isinstance(values, dict):
            raise ValueError('Les paramètres doivent être un objet JSON.')
        limits = {'A': (.2, 3), 'mu': (0, 1.5), 'z': (-1, 1),
                  'alpha': (.1, 6), 'beta': (0, 1), 'observed': (0, 1)}
        if set(values) - set(limits):
            raise ValueError('Paramètre inconnu.')
        parsed = {}
        for key, value in values.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f'{key} doit être un nombre.')
            lo, hi = limits[key]
            if not math.isfinite(value) or not lo <= value <= hi:
                raise ValueError(f'{key} doit être compris entre {lo} et {hi}.')
            parsed[key] = float(value)
        return cls(**parsed)


def ws(p, u):
    return p.A ** p.beta * (B + p.z - p.alpha * u)


def solve(p):
    w = p.A / (1 + p.mu)
    u = (B + p.z - p.A ** (1 - p.beta) / (1 + p.mu)) / p.alpha
    return {'u': u, 'employment': 1 - u, 'w': w, 'index': SCALE * w,
            'interior': 0 < u < 1, 'in_domain': 0 <= u <= 1,
            'observed_ws': SCALE * ws(p, p.observed),
            'gap': SCALE * (ws(p, p.observed) - w),
            'ws': [SCALE * ws(p, i / 100) for i in range(101)]}


def describe(p, before):
    changes = []
    if p.z != before.z:
        changes.append('z ' + ('augmente : WS monte' if p.z > before.z else 'diminue : WS descend') +
                       ' à chômage donné, car les facteurs de négociation changent. PS reste inchangée si A et μ sont constants.')
    if p.mu != before.mu:
        changes.append('La marge sur coût ' + ('augmente : PS descend' if p.mu > before.mu else 'diminue : PS monte') +
                       '. À productivité donnée, le salaire compatible avec les prix varie ; WS reste inchangée si ses paramètres sont constants.')
    if p.A != before.A:
        changes.append('La productivité ' + ('augmente' if p.A > before.A else 'diminue') +
                       '. PS varie proportionnellement à A ; WS est multipliée par Aᵝ. '
                       'À β = 1 constant, le chômage d’équilibre est invariant ; à β = 0, WS reste inchangée et une hausse de A réduit u*, toutes choses égales par ailleurs.')
    if p.alpha != before.alpha:
        changes.append('α change : la pente de WS varie autour de son ordonnée à u = 0 ; PS reste inchangée si A et μ sont constants. Une hausse de α réduit u* lorsque son numérateur est positif.')
    if p.beta != before.beta:
        changes.append('β change : la transmission de A à WS varie. PS ne dépend pas de β. Si A = 1, modifier β seul ne change aucune courbe.')
    if p.observed != before.observed:
        changes.append('Le chômage observé change : le repère se déplace le long des relations. Ce changement seul ne déplace ni WS, ni PS, ni E.')
    if not changes:
        changes.append('Situation de référence : E égalise le salaire négocié WS et le salaire compatible avec les prix PS.')
    old, new = solve(before), solve(p)
    if new['interior'] and old['interior']:
        for key, label, unit in [('u', 'Le chômage d’équilibre', 'point(s) de %'), ('index', 'Le salaire réel d’équilibre', 'point(s) d’indice')]:
            diff = (new[key] - old[key]) * (100 if key == 'u' else 1)
            amount = f'{abs(diff):.2f}'.replace('.', ',')
            changes.append(label + (' reste inchangé.' if abs(diff) < 1e-9 else f' {"augmente" if diff > 0 else "diminue"} de {amount} {unit}.'))
    if not new['interior']:
        changes.append('Aucun équilibre intérieur avec ces paramètres. L’intersection algébrique n’est pas ramenée à une borne.')
    changes.append('Résultats conditionnels à ces équations, à population active donnée. Une variation de E sur une relation inchangée est un déplacement le long de cette relation, pas son déplacement.')
    return ' '.join(changes)


def simulate(payload):
    p = Parameters.parse(payload.get('parameters', {}))
    ref = Parameters.parse(payload.get('reference', {}))
    before = Parameters.parse(payload.get('before', asdict(ref)))
    axis = payload.get('axis', 'unemployment')
    if axis not in ('unemployment', 'employment'):
        raise ValueError('Convention d’axe inconnue.')
    result, reference = solve(p), solve(ref)
    for data in (result, reference):
        data['x'] = 100 * (data['u'] if axis == 'unemployment' else data['employment'])
    return {'parameters': asdict(p), 'result': result, 'reference': reference,
            'explanation': describe(p, before)}
