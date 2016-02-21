import os

import experiments
import scicfg

import dotdot
import paths

import provenance

GIT_DIR = os.path.abspath(os.path.join(__file__, '../..'))


    # Base configuration

base_cfg = experiments.desc._deepcopy()
base_cfg._update(paths.cfg)

base_cfg.provenance.check_dirty          = True
base_cfg.provenance.check_continuity     = True



    # Base configuration for planar arm experiments (based on base_cfg)

planar_cfg = base_cfg._deepcopy()

planar_cfg.meta.run_tests = True

planar_cfg.provenance.desc = provenance.planar_arms(populate=False).desc()

planar_cfg.exploration.steps = 5000
planar_cfg.exploration.deps     = ()

planar_cfg.tests.tcov = experiments.testcov_cfg._deepcopy()
planar_cfg.tests.tcov.kind = 'cov'
planar_cfg.tests.tcov.ticks = ([1, 2, 3, 4, 5, 10, 15, 20] +
                               [i for i in range(25, planar_cfg.exploration.steps+1, 25)])
planar_cfg.tests.tcov.buffer_size = 0.05


    # Base configuration for object interaction experiments  (based on base_cfg)

dov_cfg = base_cfg._deepcopy()

dov_cfg.provenance.desc = provenance.objects(populate=False).desc()

dov_cfg.exploration.steps = 1000
dov_cfg.exploration.deps  = ()
dov_cfg.exploration.metadata = (['raw_sensors', 'salient_contacts'],)

dov_cfg.tests.tcov = experiments.testcov_cfg._deepcopy()
dov_cfg.tests.tcov.kind = 'cov'
dov_cfg.tests.tcov.ticks = ([1, 2, 3, 4, 5, 10, 15, 20] +
                            [i for i in range(25, dov_cfg.exploration.steps+1, 25)])
dov_cfg.tests.tcov.buffer_size = 45/2.0
