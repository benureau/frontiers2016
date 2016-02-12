import experiments

import dotdot
import exp_cfgs
from exp_factory import make_exp


def planar_test():
    cfg = exp_cfgs.planar_cfg._deepcopy()
    nor_diff = {'exp.path'         : 'test/planar_test',
                'exp.prefix'       : ('test',),
                'exp.repetitions'  : 1,
                'exploration.steps': 10000,
                'provenance.check_dirty'     : False,
                'provenance.check_continuity': True,
                'meta.run_tests'             : True}

    src_diff = nor_diff
    tgt_diff = nor_diff

    return make_exp([('kin20_150', 'kin20_150_p_0.9')],
                    cfg=exp_cfgs.planar_cfg._deepcopy(),
                    nor_diff=nor_diff, src_diff=src_diff, tgt_diff=tgt_diff,
                    src_ex_names=('rmb50.rgb.p0.05',),
                    nor_ex_names=('rmb50.rgb.p0.05',),
                    tgt_ex_names=('reuse_50_1.0_20_p0.05',))

if __name__ == '__main__':
    experiments.run_exps(planar_test())
