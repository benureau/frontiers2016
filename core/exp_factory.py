# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import os
import copy
import collections

import experiments

import dotdot
import factored
import exs
import envs

def make_exp(env_pairs,
             cfg=None,
             nor_diff={}, src_diff={}, tgt_diff={},
             path='phd/dov', prefix=('dov',),
             nor_ex_names=(),
             src_ex_names=(),
             tgt_ex_names=()):

    nor_diff = copy.deepcopy(nor_diff)
    src_diff = copy.deepcopy(src_diff)
    tgt_diff = copy.deepcopy(tgt_diff)


    trio_exps = []

    for src_env_name, tgt_env_name in env_pairs:

        # no reuse experiment confs
        nor_exps = []
        if len(nor_ex_names) == 0:
            nor_exps.append(None)
        # else
        for nor_ex_name in nor_ex_names:
            nor_cfg_i = cfg._deepcopy()
            nor_cfg_i.exploration.explorer._update(exs.catalog[nor_ex_name], overwrite=False)
            nor_cfg_i.exploration.env._update(envs.catalog[tgt_env_name], overwrite=False)
            nor_cfg_i.exploration.seeds = factored.src_seeds
            nor_cfg_i._update(nor_diff, overwrite=True)

            nor_cfg_i.exploration.ex_name  = nor_ex_name
            nor_cfg_i.exploration.env_name = tgt_env_name

            nor_exps.append(nor_cfg_i)


        # source experiment confs
        norsrc_exps = []
        for nor_cfg_i in nor_exps:
            if len(src_ex_names) == 0:
                norsrc_exps.append((nor_cfg_i, None))
            # else
            for src_ex_name in src_ex_names:
                src_cfg_i = cfg._deepcopy()
                src_cfg_i.exploration.explorer._update(exs.catalog[src_ex_name], overwrite=False)
                src_cfg_i.exploration.env._update(envs.catalog[src_env_name], overwrite=False)
                src_cfg_i.exploration.seeds = factored.src_seeds
                src_cfg_i._update(src_diff, overwrite=True)

                src_cfg_i.exploration.ex_name  = src_ex_name
                src_cfg_i.exploration.env_name = src_env_name

                norsrc_exps.append((nor_cfg_i, src_cfg_i))


        # target experiment confs
        for nor_cfg_i, src_cfg_i in norsrc_exps:
            if len(tgt_ex_names) == 0:
                trio_exps.append((nor_cfg_i, src_cfg_i, None))
            # else
            for tgt_ex_name in tgt_ex_names:
                tgt_cfg_i = cfg._deepcopy()
                tgt_cfg_i.exploration.explorer._update(exs.catalog[tgt_ex_name], overwrite=False)
                tgt_cfg_i.exploration.env._update(envs.catalog[tgt_env_name], overwrite=False)
                tgt_cfg_i.exploration.seeds = factored.tgt_seeds

                tgt_cfg_i.exploration.deps = (experiments.expkey(src_cfg_i),)
                tgt_cfg_i._update(tgt_diff, overwrite=True)
                tgt_cfg_i.exp.prefix = tuple(tgt_cfg_i.exp.prefix) + (src_cfg_i.exploration.ex_name, src_cfg_i.exploration.env_name)

                tgt_cfg_i.exploration.ex_name  = tgt_ex_name
                tgt_cfg_i.exploration.env_name = tgt_env_name

                trio_exps.append((nor_cfg_i, src_cfg_i, tgt_cfg_i))


    return trio_exps


def list_exp(exps):
    exp_cfgs = collections.OrderedDict()
    for trio_cfgs in exps:
        for exp_cfg in trio_cfgs:
            if exp_cfg is not None:
                exp_cfgs[experiments.expkey(exp_cfg)] = exp_cfg
    return [exp_cfg for exp_cfg in exp_cfgs.values()]
