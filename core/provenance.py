import os
import subprocess

from experiments import provenance

GIT_DIR = os.path.abspath(os.path.join(__file__, '../..'))
code_commit = provenance.git_commit(GIT_DIR)
code_dirty  = provenance.git_dirty(GIT_DIR)


pa_ownpckgs = ['experiments', 'clusterjobs', 'scicfg',
               'learners', 'fastlearners', 'explorers', 'environments']
pa_thirdparty = ['scipy', 'numpy', 'sklearn', 'shapely']
pa_nonpython = [('geos', 'geos-config --version')]

def planar_arms_data():
    plat = provenance.platform_info()

    # own packages
    own_cfgs = provenance.packages_info(pa_ownpckgs)
    owns = []
    for name, cfg in own_cfgs._branches:
        assert not cfg.dirty
        owns.append((name, cfg.commit))
    owns.sort()

    # third party python packages
    pytp_cfgs = provenance.packages_info(pa_thirdparty)
    pytps = []
    for name, cfg in pytp_cfgs._branches:
        pytps.append((name, cfg.version))
    pytps.sort()

    # third party python packages
    tps = []
    for name, version_cmd in pa_nonpython:
        p = subprocess.Popen(version_cmd.split(), stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        stdout = stdout.decode('utf8').replace('\n', '')
        tps.append((name, stdout))
    tps.sort()


    return plat, owns, pytps, tps

def planar_arms():
    plat, owns, pytps, tps = planar_arms_data()

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

    print('Installed third-party python packages:')
    for name, version in pytps:
        print('    {} {}'.format(name, version))
    print('')

    print('Installed third-party non-python packages:')
    for name, version in tps:
        print('    {} {}'.format(name, version))
    print('')

    print('Executed with:')
    print('    {} {} {}'.format(plat.python.implementation,
                                plat.python.version, plat.python.build))
    print('    [{}]'.format(plat.python.compiler))
    print('    on {}'.format(plat.uname[3]))
