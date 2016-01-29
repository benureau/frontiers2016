import os

import experiments
import scicfg

import dotdot
import paths


GIT_DIR = os.path.abspath(os.path.join(__file__, '../..'))

dov_cfg = experiments.desc._deepcopy()
dov_cfg._update(paths.cfg)

dov_cfg.provenance.package_names = ('experiments', 'clusterjobs', 'scicfg',
                                    'learners', 'fastlearners', 'explorers', 'environments',
                                    'scipy', 'numpy',
                                    'dovecot')
dov_cfg.provenance.code._branch('frontiers2015', strict=False)

dov_cfg.provenance.code.frontiers2015.commit = experiments.provenance.git_commit(GIT_DIR)
dov_cfg.provenance.code.frontiers2015.dirty  = experiments.provenance.git_dirty(GIT_DIR)
dov_cfg.provenance.check_dirty          = True
dov_cfg.provenance.check_continuity     = True

dov_cfg.exploration.steps = 1000
dov_cfg.exploration.deps  = ()
dov_cfg.exploration.metadata = (['raw_sensors', 'salient_contacts'],)

dov_cfg.tests.tcov = experiments.testcov_cfg._deepcopy()
dov_cfg.tests.tcov.kind = 'cov'
dov_cfg.tests.tcov.ticks = [1, 2, 3, 4, 5, 10, 15, 20] + [i for i in range(25, dov_cfg.exploration.steps+1, 25)]
dov_cfg.tests.tcov.buffer_size = 45/2.0
