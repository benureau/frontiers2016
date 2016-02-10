# Code for generating figures of the article:
# "Behavioral Diversity Generation in Autonomous Exploration Through Reuse of Past Experience"
# by Fabien C. Y. Benureau and Pierre-Yves Oudeyer
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import experiments

from fig19a_cluster import rgap

def rgap_h():
    return rgap(src_env='dov_ball45_0.k', tgt_env='dov_ball45_0.h',
                path='frontiers2016/objects/rgap_hard', rep=4,
                nor_ex_name='rmb300.rgb.mesh25.p0.07.h',
                tgt_ex_name='reuse_300_0.5_25_rgb.mesh25.p0.07.h')


if __name__ == '__main__':
    experiments.run_exps(rgap_h())

# 'rmb300.rgb.mesh25.p0.07.h'
# 'reuse_300_0.5_25_rgb.mesh25.p0.07.h'
