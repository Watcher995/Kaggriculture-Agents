"""Hybrid: a top-team neural policy (folder net/) for steps < SWITCH_STEP, then the 1st-place
search solver (folder s1/) from SWITCH_STEP (a dawn) to the end. This is the structure of the
1st-place Final A: network + rules for days 0-28, search for the last day (a routing problem).
"""
import os, sys, importlib.util

SWITCH_STEP = 696
USE_W1 = False   # 2nd-place wheat trading rule (folder w1/)


def _find_here():
    cands = []
    f = globals().get('__file__')
    if f:
        cands.append(os.path.dirname(os.path.abspath(f)))
    cands += [p for p in reversed(sys.path) if p]
    cands += [os.getcwd(), '/kaggle_simulations/agent']
    for d in cands:
        if os.path.isdir(os.path.join(d, 'net')) and os.path.isdir(os.path.join(d, 's1')):
            return os.path.abspath(d)
    raise FileNotFoundError('net/ and s1/ not found beside main.py')


_HERE = _find_here()
_NET_DIR = os.path.join(_HERE, 'net')
sys.path.insert(0, _NET_DIR)
_net_main = os.path.join(_NET_DIR, 'main.py')
_net_ns = {'__file__': _net_main, '__name__': 'hy_net_main'}
exec(compile(open(_net_main).read(), _net_main, 'exec'), _net_ns)
_net_agent = _net_ns['agent']

_W1 = None
if USE_W1:
    sys.path.insert(0, os.path.join(_HERE, 'w1'))
    import rules as _w1rules
    _W1 = _w1rules.Rules(_w1rules.parse('W1'))

_spec = importlib.util.spec_from_file_location('hy_s1_main', os.path.join(_HERE, 's1', 'main.py'))
_s1 = importlib.util.module_from_spec(_spec)
_s1.__file__ = os.path.join(_HERE, 's1', 'main.py')
_spec.loader.exec_module(_s1)


def agent(observation, configuration=None):
    if int(observation['step']) < SWITCH_STEP:
        if _W1 is None:
            return _net_agent(observation, configuration)
        view = _W1.observe(observation)          # network does not see the trade wheat
        action = _net_agent(view, configuration)
        action = {'farmer': action.get('farmer', ['PASS']), 'hands': action.get('hands', []), 'market': action.get('market', [])}
        return _W1(observation, action)
    return _s1.agent(observation, configuration)
