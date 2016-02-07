#!/usr/bin/env python

import experiments

import fig11_cluster
import fig12_cluster
import fig13_cluster
import fig14_cluster
import fig15_cluster
import fig19a_cluster
import fig20_cluster


if __name__ == "__main__":
    exps = (fig11_cluster.ball_cube()
            + fig12_cluster.rmb_reuse()
            + fig13_cluster.rmb_reuse_short()
            + fig14_cluster.dissimilar()
            + fig15_cluster.pool()
            + fig19a_cluster.rgap()
            + fig20_cluster.rgap_crude())

    experiments.run_exps(exps)
