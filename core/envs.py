# sympy throws DeprecationWarning in jupyter under 3.5
import warnings
warnings.filterwarnings('ignore')

import environments.envs


catalog = {}

try:
    import envs_dov # dovecot
    catalog.update(envs_dov.catalog)
except (ImportError, DeprecationWarning):
    pass


def kin(dim=20, limit=150, lengths=None, syn=None):
    """Create a configuration of a 2D arm"""
    kin_name = None

    if syn is None:
        kin_cfg = environments.envs.KinematicArm2D.defcfg._deepcopy()
    else:
        kin_cfg = environments.envs.KinArmSynergies2D.defcfg._deepcopy()
        kin_cfg.syn_span = syn
        kin_cfg.syn_res  = syn

    if lengths is None:
        kin_name = 'kin{}_{}'.format(dim, limit)
        if syn is not None:
            kin_name += '_syn{}'.format(syn)

    kin_cfg.dim = dim
    if lengths is None:
        kin_cfg.lengths = 1.0/kin_cfg.dim
    else:
        assert len(lengths) == dim
        kin_cfg.lengths = lengths
    kin_cfg.limits  = (-limit, limit)

    return kin_name, kin_cfg

# cataloging some common configurations
for dim in [2, 3, 5, 7, 8, 9, 10, 15, 20, 30, 40, 50, 60, 80, 100]:
    env_name, env_cfg = kin(dim=dim, limit=150)
    catalog[env_name] = env_cfg

    env9_cfg = env_cfg._deepcopy()
    env9_cfg.lengths = [0.9**i for i in range(env9_cfg.dim)]
    env9_cfg.lengths = [s/sum(env9_cfg.lengths) for s in env9_cfg.lengths]
    catalog[env_name + '_0.9'] = env9_cfg


catalog['vowels'] = environments.envs.VowelModel.defcfg._copy()
