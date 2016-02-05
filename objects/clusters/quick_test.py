# Code for generating figures of the article:
# "Behavioral Diversity Generation in Autonomous Exploration Through Reuse of Past Experience"
# by Fabien C. Y. Benureau and Pierre-Yves Oudeyer
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import experiments

import dotdot
import exp_cfgs
from exp_factory import make_exp

def quick_test():
    nor_diff = {'exp.path'         : 'frontiers2015/test_oi',
                'exp.prefix'       : ('dov_reuse',),
                'exp.repetitions'  : 3,
                'exploration.steps': 150,
                'meta.run_tests'   : True,
                'provenance.check_dirty'      : False,
                'provenance.check_continuity' : False}

    src_diff = nor_diff
    tgt_diff = nor_diff

    return make_exp([('dov_cube45_0.s', 'dov_ball45_0.s')],
                     cfg=exp_cfgs.dov_cfg._deepcopy(),
                     nor_diff=nor_diff, src_diff=src_diff, tgt_diff=tgt_diff,
                     src_ex_names=('rmb100.rgb.p0.05',),
                     nor_ex_names=('rmb100.rgb.p0.05',),
                     tgt_ex_names=('reuse_100_0.5_20_p0.05',))


if __name__ == '__main__':
    experiments.run_exps(quick_test())
