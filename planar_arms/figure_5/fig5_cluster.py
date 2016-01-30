# Code for generating figures of the the article:
# "Behavioral Diversity Generation in Autonomous Exploration Through Reuse of Past Experience"
# by Fabien C. Y. Benureau and Pierre-Yves Oudeyer
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import experiments

import dotdot
import exp_cfgs
from exp_factory import make_exp, list_exp


def planar():
    cfg = exp_cfgs.planar_cfg._deepcopy()
    nor_diff = {'exp.path'         : 'frontiers2015/kin_reuse',
                'exp.prefix'       : ('kin_reuse',),
                'exp.repetitions'  : 100,
                'meta.run_tests'   : True}

    src_diff = nor_diff
    tgt_diff = nor_diff

    return make_exp([('kin20_150', 'kin20_150_0.9')],
                     cfg=exp_cfgs.planar_cfg._deepcopy(),
                     nor_diff=nor_diff, src_diff=src_diff, tgt_diff=tgt_diff,
                     #src_ex_names=('rmb50.rgb.p0.05',),
                     src_ex_names=('random.goal_50',),
                     #nor_ex_names=('rmb50.rgb.p0.05',),
                     nor_ex_names=('random.goal_50',),
                     tgt_ex_names=('reuse_50_1.0_20_p0.05',))


if __name__ == '__main__':
    experiments.run_exps(list_exp(planar()))
