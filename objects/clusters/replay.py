from __future__ import division, print_function

import os

import environments
import experiments

import dotdot
import gfx


def dovecot_replay(exp_cfg, rep=0, exp_cfgs=(), collision_only=True, headless=False):
    """
    :param exp_cfgs:  If exp_cfg represent an experiments that reuse the results
                      of another, these should be provided in exp_cfgs.
    :param headless:  Open V-REP in headless mode.
    """
    job_data = experiments.load_exploration(exp_cfg, exp_cfgs=exp_cfgs, rep=rep)

    job_cfg = job_data.job.jobcfg._deepcopy()
    job_cfg._freeze(False)
    print(job_cfg)

    env_cfg = job_cfg.exploration.env
    #env_cfg = envs.catalog[env_name]
    env_cfg.execute.prefilter = False
    env_cfg.execute.simu.calibr_check = False
    if headless:
        env_cfg.execute.simu.ppf = 200
        env_cfg.execute.simu.headless = True
    else:
        env_cfg.execute.simu.ppf = 1
        env_cfg.execute.simu.headless = False

    env = environments.Environment.create(env_cfg)

    raw_input()
    assert job_data['observations'] is not None, "motor signals (observations) could not be loaded (datafiles probably missing)."
    print('obs from file: {}{}{}'.format(gfx.green, job_cfg.hardware.datafile, gfx.end))

    for step, (expl, fback) in enumerate(job_data['explorations']):
        s_vector = environments.tools.to_vector(fback['s_signal'], job_data.s_channels)
        print('{}:{: 5.0f}: {}{}  {}'.format(step, s_vector[-1], expl['from'],
                                       (20-len(expl['from']))*' ', fback['s_signal']))

    step = -1
    while True:
        print('choose a step: ', end='')
        inp = raw_input()
        if inp == '':
            step += 1
        elif inp == '=':
            step += 0 # no change
        else:
            step = int(inp)

        expl, fback = job_data['explorations'][step]
        m_signal = expl['m_signal']
        s_signal = fback['s_signal']

        print('{:04d} {}'.format(step, expl['from']))

        print('{:04d} {}{}{} [recorded]'.format(step, gfx.cyan, s_signal, gfx.end))
        meta = {}
        feedback = env.execute(m_signal, meta=meta)
        print('     {}'.format(feedback['s_signal']))


if __name__ == '__main__':
    env_name = 'dov_ball45_0.s'
    env_name = 'dov_cube45_0.s'

    from fig12_cluster import rmb_reuse
    exp_cfgs = rmb_reuse(path='frontiers2016/objects/reuse', rep=25)
    dovecot_replay(exp_cfgs[0][2], rep=3, exp_cfgs=exp_cfgs, collision_only=True, headless=False)
