# -*- coding: utf-8 -*-
import collections
import explorers
import learners


catalog = {}



    # Learners #

learn_cfg = learners.MutateNNLearner.defcfg._deepcopy()
learn_cfg.operator.name     = 'uniform'
learn_cfg.operator.p_mutate = 1.0
learn_cfg.operator.d        = 0.05


learn2_cfg = learners.MutateNNLearner.defcfg._deepcopy()
learn2_cfg.operator.name     = 'uniformsync'
learn2_cfg.operator.p_mutate = 1.0
learn2_cfg.operator.d        = 0.05

lwlr_cfg = learners.OptimizeLearner.defcfg._deepcopy()
lwlr_cfg.fwd = learners.ESLWLRLearner.defcfg._deepcopy()
lwlr_cfg.algo = 'L-BFGS-B'

plwlr_cfg = learners.PredictMutateNNLearner.defcfg._deepcopy()
plwlr_cfg.attempts   = 10
plwlr_cfg.operator.name = 'uniform'
plwlr_cfg.operator.p_mutate = 1.0
plwlr_cfg.operator.d = 0.05
plwlr_cfg.fwd = learners.ESLWLRLearner.defcfg._deepcopy()

gauss_cfg = learners.MutateNNLearner.defcfg._deepcopy()
gauss_cfg.operator.name     = 'gauss'
gauss_cfg.operator.p_mutate = 1.0
gauss_cfg.operator.d        = 0.05

lrn_catalog = {'p0.05': learn_cfg, '2p0.05': learn2_cfg,
               'lwlr': lwlr_cfg, 'plwlr': plwlr_cfg, 'gauss': gauss_cfg}

for d in [0.001, 0.0025, 0.005, 0.01, 0.025, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.75, 1.0]:
    lrn_cfg = learn_cfg._deepcopy()
    lrn_cfg.operator.d = d
    lrn_catalog['p{}'.format(d)] = lrn_cfg._deepcopy()

    lrn_cfg = learn2_cfg._deepcopy()
    lrn_cfg.operator.d = d
    lrn_catalog['2p{}'.format(d)] = lrn_cfg._deepcopy()

    lrn_cfg = gauss_cfg._deepcopy()
    lrn_cfg.operator.d = d
    lrn_catalog['g{}'.format(d)] = lrn_cfg._deepcopy()


    # Explorers #


# Random Motor Strategies

rm_expl = explorers.RandomMotorExplorer.defcfg._deepcopy()
catalog['random.motor'] = rm_expl


# Random Goal Strategies

base_ex              = explorers.MetaExplorer.defcfg._deepcopy()
base_ex.eras         = (10, None)
base_ex.weights      = ((1.0, 0.0), (0.0, 1.0))
base_ex.ex_0         = explorers.RandomMotorExplorer.defcfg._deepcopy()
base_ex.ex_1         = explorers.RandomGoalExplorer.defcfg._deepcopy()
base_ex.ex_1.learner = learn_cfg

for mb in [1, 10, 20, 25, 50, 100, 200, 250, 300, 400, 500, 1000, 4000, 4500, 4750, 4900, 24000, 24500, 49000]:
    ex_a = base_ex._deepcopy()
    ex_a.eras = (mb, None)
    for d in [0.001, 0.0025, 0.005, 0.01, 0.025, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.75, 1.0]:
        ex_b = ex_a._deepcopy()
        ex_b.ex_1.learner = lrn_catalog['p{}'.format(d)]._deepcopy()
        catalog['rmb{}.rgb.p{}'.format(mb, d)] = ex_b

        ex_c = ex_a._deepcopy()
        ex_c.ex_1.learner = lrn_catalog['2p{}'.format(d)]._deepcopy()
        catalog['rmb{}.rgb.2p{}'.format(mb, d)] = ex_c

        # ex_f = ex_a._deepcopy()
        # ex_f.ex_1.learner = gauss_cfg._deepcopy()
        # ex_f.ex_1.learner.operator.d = d/3 # 0.1 % out of [-d, d]
        # catalog['rmb{}.rgb.g{}'.format(mb, d)] = ex_f

    ex_d = ex_a._deepcopy()
    ex_d.ex_1.learner = lwlr_cfg._deepcopy()
    catalog['rmb{}.rgb.lwlr'.format(mb)] = ex_d

    ex_e = ex_a._deepcopy()
    ex_e.ex_1.learner = plwlr_cfg._deepcopy()
    catalog['rmb{}.rgb.plwlr'.format(mb)] = ex_e

catalog['random.goal'] = catalog['rmb10.rgb.p0.05']
for mb in [1, 10, 20, 25, 50, 100, 200, 250, 300, 400, 500, 1000, 4000, 4500, 4750, 4900, 24000, 24500, 49000]:
    catalog['random.goal_{}'.format(mb)] = catalog['rmb{}.rgb.p0.05'.format(mb)]


# Reuse Strategies

def reuse_ex(mb, p_reuse, algorithm='sensor_uniform', res=20, lrn_name='p0.05'):
    assert 0 <= p_reuse <= 1
    assert 0 <= d

    r_ex          = explorers.MetaExplorer.defcfg._deepcopy()
    r_ex.eras     = (mb, None)
    r_ex.weights  = ((1-p_reuse, 0.0, p_reuse), (0.0, 1.0, 0.0))

    r_ex.ex_0                   = explorers.RandomMotorExplorer.defcfg._deepcopy()

    r_ex.ex_1                   = explorers.RandomGoalExplorer.defcfg._deepcopy()
    r_ex.ex_1.learner           = lrn_catalog[lrn_name]._deepcopy()

    r_ex.ex_2                   = explorers.ReuseExplorer.defcfg._deepcopy()
    r_ex.ex_2.reuse.res         = res
    r_ex.ex_2.reuse.algorithm   = algorithm

    alg_str = '' if algorithm == 'sensor_uniform' else '.' + algorithm
    return 'reuse{}_{}_{}_{}_{}'.format(alg_str, mb, p_reuse, res, lrn_name), r_ex

# 'reuse_200_0.5_20_p0.05'
for mb in [1, 10, 25, 50, 100, 200, 300, 500]:
    for p_reuse in [0.5, 1.0]:
        for res in [10, 20, 40]:
            for algorithm in ['random', 'sensor_uniform']:
                for lrn_name in ['p0.05', 'p0.025', 'lwlr']:
                    reuse_name, reuse_cfg = reuse_ex(mb, p_reuse, algorithm, res, lrn_name)
                    catalog[reuse_name] = reuse_cfg


# Old hardware experiments

hard_src_ex = catalog['rmb300.rgb.lwlr']._deepcopy()
hard_src_ex.weights = ((1.0, 0.0), (0.1, 0.9))
catalog['rmb300.rgb.lwlr.h'] = hard_src_ex

hard_tgt_ex = catalog['reuse_300_0.5_40_lwlr']._deepcopy()
hard_tgt_ex.weights = ((0.5, 0.0, 0.5), (0.05, 0.9, 0.05))
catalog['reuse_300_0.5_40_lwlr.h'] = hard_tgt_ex
