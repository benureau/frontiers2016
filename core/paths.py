from __future__ import print_function, division, absolute_import

import os
import scicfg


# You should modify this file to your folder/architecture layout

cfg = scicfg.SciConfig()
cfg._describe('meta.user', instanceof=str,
              docstring='the name of the user (used on clusters by qstat)')
cfg._describe('meta.rootpath', instanceof=str,
              docstring='the path towards the data')

if 'BENUREAU_FRONTIERS2016_DATA' in os.environ:
    cfg.meta.rootpath = os.environ['BENUREAU_FRONTIERS2016_DATA']
    if 'BENUREAU_FRONTIERS2016_USER' in os.environ:
        cfg.meta.user = os.environ['BENUREAU_FRONTIERS2016_USER']
else:
    uname = os.uname()
    if uname[0] == 'Linux':
        cfg.meta.user     = 'fbenurea'
        cfg.meta.rootpath = '/scratch/fbenurea/'
    elif uname[0] == 'Darwin':
        cfg.meta.user     = 'fabien'
        cfg.meta.rootpath = '~/research/data/'
    else:
        raise ValueError('Platform not known, please setup user and rootpath.')
