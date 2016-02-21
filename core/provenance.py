import os

import experiments.execute
from experiments import provenance as prv
from clusterjobs import jobgroup, context


GIT_DIR = os.path.abspath(os.path.join(__file__, '../..'))

# dependencies for planar arms experiments
PA_RESEARCH_PKGS = ['experiments', 'clusterjobs', 'scicfg',
                    'learners', 'fastlearners', 'explorers', 'environments']
PA_THIRDPARTY_PY = [prv.PkgDesc('numpy', link='https://github.com/scipy/scipy'),
                    prv.PkgDesc('scipy', link='https://github.com/scipy/scipy'),
                    prv.PkgDesc('sklearn', link='https://github.com/scikit-learn/scikit-learn'),
                    prv.PkgDesc('shapely', link='https://github.com/toblerity/shapely')]
PA_THIRDPARTY    = [prv.PkgDesc('geos', python=False, version_cmd='geos-config --version',
                                link='http://trac.osgeo.org/geos/')]

# dependencies for object interaction experiments
OI_RESEARCH_PKGS = PA_RESEARCH_PKGS + ['fastlearners', 'dovecot']
OI_THIRDPARTY_PY = (PA_THIRDPARTY_PY +
                    [prv.PkgDesc('sympy', link='https://github.com/sympy/sympy')])
OI_THIRDPARTY    = (PA_THIRDPARTY +
                    [prv.PkgDesc('Eigen',  python=False, version_cmd='pkg-config eigen3 --modversion',
                                 link='http://eigen.tuxfamily.org/index.php?title=Main_Page'),
                     prv.PkgDesc('libccd', python=False, version_cmd='pkg-config ccd    --modversion',
                                 link='https://github.com/danfis/libccd'),
                     prv.PkgDesc('FCL',    python=False, version_cmd='pkg-config fcl    --modversion',
                                 link='https://github.com/flexible-collision-library/fcl'),
                     prv.PkgDesc('FLANN',  python=False, version_cmd='pkg-config flann  --modversion',
                                 link='https://github.com/mariusmuja/flann'),
                     prv.PkgDesc('dmpbbo', python=False, desc='[4bbb90ae679053e04bb4604bee0acbaf75f64875]',
                                 link='https://github.com/stulp/dmpbbo'),
                     prv.PkgDesc('VREP',   python=False, desc='3.2.3, rev 4',
                                 link='http://www.coppeliarobotics.com'),
                     prv.PkgDesc('Boost',  python=False, desc='1.55')])



def planar_arms(populate=True):
    return prv.ProvenanceData('frontiers2016',
                              GIT_DIR, PA_RESEARCH_PKGS,
                              PA_THIRDPARTY_PY, PA_THIRDPARTY,
                              populate=populate)

def objects(populate=True):
    return prv.ProvenanceData('frontiers2016',
                              GIT_DIR, OI_RESEARCH_PKGS,
                              OI_THIRDPARTY_PY, OI_THIRDPARTY,
                              populate=populate)

def cluster(expcfgs):
    prov_acc = prv.ProvenanceAccumulator(code_dir=GIT_DIR)

    expcfgs = experiments.execute.flatten_exps(expcfgs)
    jobgrp = jobgroup.JobBatch(context.Env(user=None))

    for expcfg in expcfgs:
        for i in range(expcfg.exp.repetitions):
            data = experiments.load_exploration(expcfg, rep=i, jobgrp=jobgrp, verbose=False)
            prov_cfg = data.meta['jobcfg'].provenance.data
            prov_acc.add_cfg(prov_cfg._deepcopy())
    return prov_acc

if __name__ == '__main__':
    prov_data = objects()
    print(prov_data.message())

    # prov_desc = prov_data.desc()
    # prov_data2 = prv.ProvenanceData.from_desc(prov_desc)
    #
    # assert prov_data.same_cfg(prov_data2.cfg())
    #
    # prov_acc = prv.ProvenanceAccumulator()
    # prov_acc.add_cfg(prov_data.cfg())
