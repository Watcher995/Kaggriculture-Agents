"""2nd place (Victor @ Tufa Labs) HourFormer + rules D1+A1+W1, CPU."""
import os, sys
_DIR = next((p for p in [os.path.dirname(os.path.abspath(globals().get('__file__', 'x')))] + list(reversed(sys.path)) + [os.getcwd(), '/kaggle_simulations/agent']
             if p and os.path.exists(os.path.join(p, 'player.pt'))), os.getcwd())
sys.path.insert(0, _DIR)
import torch
torch.set_num_threads(int(os.environ.get('NN_THREADS', '2')))
from agent import load_agent
_AGENT = None


def agent(obs, configuration=None):
    global _AGENT
    if _AGENT is None or int(obs['step']) == 0:
        _AGENT = load_agent(os.path.join(_DIR, 'player.pt'), 'cpu', os.environ.get('N2_RULES', 'D1+A1+W1'))
    return _AGENT(obs, configuration)
