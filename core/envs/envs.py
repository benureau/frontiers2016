import environments.envs
import envs_dov # objects environments


catalog = {}
catalog.update(envs_dov.catalog)


def kin(dim=20, limit=150, lengths=None, polar=False):
    """Create a configuration of a 2D arm"""
    kin_name = 'kin{}_{}'.format(dim, limit)
    if polar:
        kin_cfg = environments.envs.KinArmPolar.defcfg._deepcopy()
        kin_name += '_p'
    else:
        kin_cfg = environments.envs.KinArmEuclidean.defcfg._deepcopy()

    kin_cfg.dim = dim
    if lengths is None:
        kin_cfg.lengths = 1.0/kin_cfg.dim
    else:
        assert len(lengths) == dim
        kin_cfg.lengths = lengths
    kin_cfg.limits  = (-limit, limit)

    return kin_name, kin_cfg

# cataloging used configurations
for dim in [2, 3, 5, 7, 8, 9, 10, 15, 20, 30, 40, 50, 60, 80, 100]:
    env_name, env_cfg = kin(dim=dim, limit=150)
    catalog[env_name] = env_cfg

    for polar in [True, False]:
        env_name, env9_cfg = kin(dim=dim, limit=150, polar=polar)
        env9_cfg.lengths = [0.9**i for i in range(env9_cfg.dim)]
        env9_cfg.lengths = [s/sum(env9_cfg.lengths) for s in env9_cfg.lengths]
        catalog[env_name + '_0.9'] = env9_cfg
