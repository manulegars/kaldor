"""Conventions centrales : taux macro en %, écarts en points, WS–PS en proportions."""
from math import isfinite


def percent(proportion):
    return 100 * proportion


def proportion(percent_value):
    return percent_value / 100


INDICATORS = {
    'growth': {'label': 'Croissance du PIB réel', 'unit': '% par période', 'direction': 'north'},
    'inflation': {'label': 'Inflation', 'unit': '% par période', 'direction': 'west'},
    'unemployment': {'label': 'Chômage', 'unit': '% des actifs', 'direction': 'south'},
    'external': {'label': 'Solde commercial', 'unit': '% du PIB', 'direction': 'east'},
    'debt': {'label': 'Dette publique', 'unit': '% du PIB', 'direction': 'separate'},
}


def indicator(value=None, status='non calculé dans cet atelier', detail=''):
    return {'value': value, 'status': status, 'detail': detail}


def dashboard(**values):
    return {key: values.get(key, indicator()) for key in INDICATORS}


def radar(indicators):
    """Scores de lecture explicites, sans écrêtage silencieux ni score agrégé."""
    result = {}
    for key in ('growth', 'inflation', 'unemployment', 'external'):
        v = indicators[key]['value']
        if v is None:
            result[key] = {'score': None, 'outside': False}
            continue
        score = {'growth': lambda x: (x + 4) / 12,
                 'inflation': lambda x: 1 - abs(x - 2) / 8,
                 'unemployment': lambda x: 1 - x / 20,
                 'external': lambda x: 1 - abs(x) / 10}[key](v)
        result[key] = {'score': score, 'outside': not 0 <= score <= 1}
    return result
