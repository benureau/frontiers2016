# Code for generating figures of the article:
# "Behavioral Diversity Generation in Autonomous Exploration Through Reuse of Past Experience"
# by Fabien C. Y. Benureau and Pierre-Yves Oudeyer
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import experiments

import dotdot
import exp_cfgs
from exp_factory import make_exp


def rgap(src_env='dov_ball45_0.k', tgt_env='dov_ball45_0.s',
         nor_ex_name='rmb200.rgb.p0.05', tgt_ex_name='reuse_200_0.5_20_p0.05',
         path='frontiers2016/objects/rgap', rep=25):
    nor_diff = {'exp.path'         : path,
                'exp.prefix'       : ('dov_rgap',),
                'exp.repetitions'  : rep,
                'meta.run_tests'   : True}

    src_diff = dict(nor_diff)
    src_diff['meta.run_tests'] = False
    tgt_diff = nor_diff

    expcfgs =  make_exp([(src_env, tgt_env)],
                        cfg=exp_cfgs.dov_cfg,
                        nor_diff=nor_diff, src_diff=src_diff, tgt_diff=tgt_diff,
                        src_ex_names=(nor_ex_name,),
                        nor_ex_names=(nor_ex_name,),
                        tgt_ex_names=(tgt_ex_name,))

    return expcfgs

if __name__ == '__main__':
    experiments.run_exps(rgap())
