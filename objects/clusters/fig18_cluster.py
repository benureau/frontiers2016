# Code for generating figures of the article:
# "Behavioral Diversity Generation in Autonomous Exploration Through Reuse of Past Experience"
# by Fabien C. Y. Benureau and Pierre-Yves Oudeyer
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import experiments

import dotdot
import exp_cfgs
from exp_factory import make_exp


def ball_cube_hard(path='frontiers2016/objects/hard', rep=4):
    nor_diff = {'exp.path'         : path,
                'exp.prefix'       : ('dov_hard',),
                'exp.repetitions'  : rep,
                'meta.run_tests'   : True}

    src_diff = nor_diff
    tgt_diff = nor_diff

    expcfgs =  make_exp([('dov_ball45_0_a20.h', 'dov_ball45_0_a20.h'),
                         ('dov_cube45_0_a20.h', 'dov_ball45_0_a20.h'),
                         ('dov_ball45_0_a20.h', 'dov_cube45_0_a20.h'),
                         ('dov_cube45_0_a20.h', 'dov_cube45_0_a20.h')],
                        cfg=exp_cfgs.dov_cfg,
                        nor_diff=nor_diff, src_diff=src_diff, tgt_diff=tgt_diff,
                        src_ex_names=('rmb300.rgb.lwlr.h',),
                        nor_ex_names=('rmb300.rgb.lwlr.h',),
                        tgt_ex_names=('reuse_300_0.5_40_lwlr.h',))

    # one repetion of the ball -> cube experiment got its data corrupted.
    for nor_cfg, src_cfg, tgt_cfg in expcfgs:
        src_env_name = tgt_cfg.exp.prefix[2]
        tgt_env_name = tgt_cfg.exploration.env_name
        if (src_env_name, tgt_env_name) == ('dov_ball45_0_a20.h', 'dov_cube45_0_a20.h'):
            tgt_cfg.exp.repetitions = 3

    return expcfgs


if __name__ == '__main__':
    experiments.run_exps(ball_cube_hard())
