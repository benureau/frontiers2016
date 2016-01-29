from __future__ import print_function, division, absolute_import

import os
import scicfg


# You should modify this file to your folder/architecture layout

cfg = scicfg.SciConfig()
cfg._describe('meta.user', instanceof=str, docstring='the name of the user (used on clusters by qstat)')
cfg._describe('meta.rootpath', instanceof=str, docstring='the path towards the data')

uname = os.uname()
if uname[0] == 'Linux':
    cfg.meta.user     = 'fbenurea'
    cfg.meta.rootpath = '/scratch/fbenurea/'
    testset_dir       = '/home/fbenurea/code/testsets/'

elif uname[0] == 'Darwin':
    cfg.meta.user     = 'fabien'
    cfg.meta.rootpath = '~/research/data/'
    testset_dir       = '/Users/fabien/research/enc/projects/phd/code/testsets/'

else:
    raise ValueError('Platform not known, please setup user and rootpath.')

testset_filepaths  = {'kin_one': testset_dir + 'testset_kinone',
                      'dmp2d'  : testset_dir + 'testset_dmp2d',
                      'dov_a6' : testset_dir + 'testset_dov_a6',
                     }
