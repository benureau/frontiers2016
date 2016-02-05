import experiments
import fig5_cluster

import dotdot


if __name__ == '__main__':
    exps = fig5_cluster.planar(path='frontiers2015/tests', rep=3)
    experiments.run_exps(exps)
