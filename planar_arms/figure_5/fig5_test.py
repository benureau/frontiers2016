import experiments
import fig5_cluster

import dotdot
from exp_factory import list_exp


if __name__ == '__main__':
    exps = fig5_cluster.planar(path='frontiers2015/tests', rep=3)
    experiments.run_exps(list_exp(exps))
