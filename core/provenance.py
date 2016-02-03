import os

from experiments import provenance

pa_ownpckgs = ['experiments', 'clusterjobs', 'scicfg',
               'learners', 'fastlearners', 'explorers', 'environments']
pa_thirdparty = ['scipy', 'numpy', 'sklearn', 'shapely']

GIT_DIR = os.path.abspath(os.path.join(__file__, '../..'))
code_commit = provenance.git_commit(GIT_DIR)
code_dirty  = provenance.git_dirty(GIT_DIR)

def planar_arms_data():
    plat = provenance.platform_info()

    # own packages
    own_cfgs = provenance.packages_info(pa_ownpckgs)
    owns = []
    for name, cfg in own_cfgs._branches:
        assert not cfg.dirty
        owns.append((name, cfg.commit))
    owns.sort()

    # third party packages
    tp_cfgs = provenance.packages_info(pa_thirdparty)
    tps = []
    for name, cfg in tp_cfgs._branches:
        tps.append((name, cfg.version))
    tps.sort()

    return plat, owns, tps

def planar_arms():
    plat, owns, tps = planar_arms_data()

    if not code_dirty:
        print('All the code involved in the computation is commited (no git repository in dirty state).')
    else:
        print('Some code involved in the computation has not been commited (some git repository in dirty state).')
    print('This code was executed with commit {}.'.format(code_commit))
    print('')

    print('Installed research packages (available in the submodules/ directory):')
    max_name = max(len(name) for name, commit in owns)
    for name, commit in owns:
        print('    {}{} [{}]'.format(name, ' '*(max_name - len(name)), commit))
    print('')

    print('Installed third-party packages:')
    for name, version in tps:
        print('    {} {}'.format(name, version))
    print('')

    print('{} {} {}'.format(plat.python.implementation,
                            plat.python.version, plat.python.build))
    print('[{}]'.format(plat.python.compiler))
    print('on {}'.format(plat.uname[3]))
