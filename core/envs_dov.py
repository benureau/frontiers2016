import platform

from dovecot import desc
from dovecot import objdesc


def_cfg = desc._deepcopy()
def_cfg.classname = 'dovecot.HardwareEnvironment'

# Execute config
def_cfg.execute.prefilter             = True
def_cfg.execute.check_self_collisions = False
def_cfg.execute.partial_mvt           = False
def_cfg.execute.is_simulation         = False
def_cfg.execute.scene.name            = 'vanilla'

# Hardware kin config
def_cfg.execute.kin.force        = 50.0

# Hardware stem config
def_cfg.execute.hard.uid         = 1000 # to be redefined.
def_cfg.execute.hard.verbose_com = True
def_cfg.execute.hard.verbose_dyn = True
def_cfg.execute.hard.powerswitch = True


# V-REP config
def_cfg.execute.simu.load          = True
def_cfg.execute.simu.physic_engine = 'ode'
def_cfg.execute.simu.ppf           = 200
def_cfg.execute.simu.headless      = False if platform.system() == 'Darwin' else True
def_cfg.execute.simu.calibrdir     = '~/.dovecot/tttcal/'
def_cfg.execute.simu.mac_folder    = '/Applications/VRep/vrep.app/Contents/MacOS/'


# Sensory primitives
def_cfg.sprims.names      = []
def_cfg.sprims.tip        = False
def_cfg.sprims.uniformize = False
def_cfg.sprims.max_force  = 150 # Newtons (squared). Experimentally determined.


# Motor primitives
def_cfg.mprims.name          = 'dmp_sharedwidth'
def_cfg.mprims.dt            = 0.020
def_cfg.mprims.target_end    = 250
def_cfg.mprims.traj_end      = 500
def_cfg.mprims.sim_end       = 500
def_cfg.mprims.uniformize    = True
def_cfg.mprims.n_basis       = 2
def_cfg.mprims.max_speed     = 50
def_cfg.mprims.init_states   = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
def_cfg.mprims.target_states = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
def_cfg.mprims.angle_ranges  = ((110.0,  110.0), (99.0, 99.0), (99.0, 99.0), (120.0, 120.0), (99.0, 99.0), (99.0, 99.0))


unset = set([])
#assert def_cfg.execute.prefilter == False
assert set(def_cfg._unset()) == unset, 'leaves {} have not beend defined'.format(set(def_cfg._unset()).difference(unset))


    ## Creating a catalog ##

catalog = {}

def add(cfg, name):
    hard_cfg = cfg._deepcopy()
    catalog[name+'.h'] = hard_cfg
    catalog['dov_'+name+'.h'] = hard_cfg

    simu_cfg = cfg._deepcopy()
    simu_cfg.classname = 'dovecot.SimulationEnvironment'
    simu_cfg.execute.is_simulation = True
    catalog['dov_'+name+'.s'] = simu_cfg
    catalog[name+'.s'] = simu_cfg

    kin_cfg = cfg._deepcopy()
    kin_cfg.classname = 'dovecot.KinEnvironment'
    kin_cfg.execute.is_simulation = True
    catalog['dov_'+name+'.k'] = kin_cfg
    catalog[name+'.k'] = kin_cfg

    kb_cfg = cfg._deepcopy()
    kb_cfg.classname = 'dovecot.KinEnvironment'
    kb_cfg.sprims.names = ['push_collision']
    kb_cfg.execute.is_simulation = True
    catalog['dov_'+name+'.kb'] = kb_cfg


    ## Adding environments in the catalog ##

push_cfg = def_cfg._deepcopy()
push_cfg.sprims.names = ['push']

obj0 = objdesc._deepcopy()
obj0.pos     = (-60.0, 0.0, None)
obj0.mass    = 0.050
obj0.tracked = True

obj1 = obj0._deepcopy()
obj1.pos = (-180.0, -60.0, None)

obj2 = obj0._deepcopy()
obj2.pos = (-120.0, -90.0, None)

obj4 = obj0._deepcopy()
obj4.pos = (-180.0, -120.0, None)

obj3 = obj0._deepcopy()
obj3.pos = (-120.0, +90.0, None)

noobj = obj0._deepcopy()
noobj.pos = (-1000.0, -1000.0, None)
noobj_cfg = push_cfg._deepcopy()
noobj_cfg.execute.scene.objects.ball45 = noobj._deepcopy()
add(noobj_cfg, 'noobj')

# balls
ball45_0_cfg = push_cfg._deepcopy()
ball45_0_cfg.execute.scene.objects.ball45 = obj0._deepcopy()
add(ball45_0_cfg, 'ball45_0')

ball90_0_cfg = push_cfg._deepcopy()
ball90_0_cfg.execute.scene.objects.ball90 = obj0._deepcopy()
add(ball90_0_cfg, 'ball90_0')

ball15_0_cfg = push_cfg._deepcopy()
ball15_0_cfg.execute.scene.objects.ball15 = obj0._deepcopy()
add(ball15_0_cfg, 'ball15_0')

ball45_0_a20_cfg = ball45_0_cfg._deepcopy()
ball45_0_a20_cfg.execute.scene.arena.name  = 'arena20x20x10'
add(ball45_0_a20_cfg, 'ball45_0_a20')

ball45_1_cfg = push_cfg._deepcopy()
ball45_1_cfg.execute.scene.objects.ball45 = obj1._deepcopy()
add(ball45_1_cfg, 'ball45_1')

ball45_4_cfg = push_cfg._deepcopy()
ball45_4_cfg.execute.scene.objects.ball45 = obj4._deepcopy()
add(ball45_4_cfg, 'ball45_4')


ball45_1_a20_cfg = ball45_1_cfg._deepcopy()
ball45_1_a20_cfg.execute.scene.arena.name  = 'arena20x20x10'
add(ball45_1_a20_cfg, 'ball45_1_a20')

ball45_2_cfg = push_cfg._deepcopy()
ball45_2_cfg.execute.scene.objects.ball45 = obj2._deepcopy()
add(ball45_2_cfg, 'ball45_2')

ball45_3_cfg = push_cfg._deepcopy()
ball45_3_cfg.execute.scene.objects.ball45 = obj3._deepcopy()
add(ball45_3_cfg, 'ball45_3')

ball25_0_cfg = push_cfg._deepcopy()
ball25_0_cfg.execute.scene.objects.ball25 = obj0._deepcopy()
add(ball25_0_cfg, 'ball25_0')

ball60_0_cfg = push_cfg._deepcopy()
ball60_0_cfg.execute.scene.objects.ball60 = obj0._deepcopy()
add(ball60_0_cfg, 'ball60_0')

# tubes
tube40_80_0_cfg = push_cfg._deepcopy()
tube40_80_0_cfg.execute.scene.objects.tube40_80 = obj0._deepcopy()
add(tube40_80_0_cfg, 'tube40_80_0')

tube40_80_0_a20_cfg = tube40_80_0_cfg._deepcopy()
tube40_80_0_a20_cfg.execute.scene.arena.name  = 'arena20x20x10'
add(tube40_80_0_a20_cfg, 'tube40_80_0_a20')



# rollspin objects
rs_cfg = def_cfg._deepcopy()
rs_cfg.sprims.names = ['rollspin']

tube40_80_0_rs_cfg = rs_cfg._deepcopy()
tube40_80_0_rs_cfg.execute.scene.objects.tube40_80 = obj0._deepcopy()
add(tube40_80_0_rs_cfg, 'tube40_80_0_rs')

tube40_80_0_rs_a20_cfg = tube40_80_0_rs_cfg._deepcopy()
tube40_80_0_rs_a20_cfg.execute.scene.arena.name  = 'arena20x20x10'
add(tube40_80_0_rs_a20_cfg, 'tube40_80_0_rs_a20')

ball45_0_rs_cfg = rs_cfg._deepcopy()
ball45_0_rs_cfg.execute.scene.objects.ball45 = obj0._deepcopy()
add(ball45_0_rs_cfg, 'ball45_0_rs')

ball45_0_rs_a20_cfg = ball45_0_rs_cfg._deepcopy()
ball45_0_rs_a20_cfg.execute.scene.arena.name  = 'arena20x20x10'
add(ball45_0_rs_a20_cfg, 'ball45_0_rs_a20')

cube45_0_rs_cfg = rs_cfg._deepcopy()
cube45_0_rs_cfg.execute.scene.objects.cube45 = obj0._deepcopy()
add(cube45_0_rs_cfg, 'cube45_0_rs')

cube45_0_rs_a20_cfg = cube45_0_rs_cfg._deepcopy()
cube45_0_rs_a20_cfg.execute.scene.arena.name  = 'arena20x20x10'
add(cube45_0_rs_a20_cfg, 'cube45_0_rs_a20')


# cubes
cube25_0_cfg = push_cfg._deepcopy()
cube25_0_cfg.execute.scene.objects.cube25 = obj0._deepcopy()
add(cube25_0_cfg, 'cube25_0')

cube45_0_cfg = push_cfg._deepcopy()
cube45_0_cfg.execute.scene.objects.cube45 = obj0._deepcopy()
add(cube45_0_cfg, 'cube45_0')

cube45_0_a20_cfg = cube45_0_cfg._deepcopy()
cube45_0_a20_cfg.execute.scene.arena.name  = 'arena20x20x10'
add(cube45_0_a20_cfg, 'cube45_0_a20')




pool_cfg = push_cfg._deepcopy()

pool_cfg.execute.scene.arena.name  = 'arena20x20x10'
pool_cfg.execute.scene.arena.pos   = (400.0, 600.0, None)
pool_cfg.mprims.sim_end            = 1500

pool_cfg.execute.prefilter = False
pool_cfg.execute.scene.objects.ball         = obj0._deepcopy()
pool_cfg.execute.scene.objects.ball.tracked = True
pool_cfg.execute.scene.objects.ball.pos     = (180.0, 350.0, None)
pool_cfg.execute.scene.objects.ball.mass    = 0.010
pool_cfg.execute.scene.objects.blueball         = obj0._deepcopy()
pool_cfg.execute.scene.objects.blueball.pos     = ( -60.0, 0.0, None)
pool_cfg.execute.scene.objects.blueball.tracked = False
pool_cfg.execute.scene.objects.blueball.mass    = 0.050
add(pool_cfg, 'dov_pool')


# # pool config
# pool_cfg = push_cfg._deepcopy()
# pool_cfg.execute.scene.arena.name  = 'arena20x20x10'
# pool_cfg.execute.scene.arena.pos   = (400.0, 600.0, None)
# pool_cfg.mprims.sim_end            = 1000
# pool_cfg.execute.prefilter = False
# pool_cfg.execute.scene.objects.ball45         = obj0._deepcopy()
# pool_cfg.execute.scene.objects.ball45.tracked = True
# pool_cfg.execute.scene.objects.ball45.pos     = (180.0, 350.0, None)
# pool_cfg.execute.scene.objects.ball45.mass    = 0.0025
# pool_cfg.execute.scene.objects.ball45_2         = obj0._deepcopy()
# pool_cfg.execute.scene.objects.ball45_2.pos     = ( -60.0, 0.0, None)
# pool_cfg.execute.scene.objects.ball45_2.tracked = False
# pool_cfg.execute.scene.objects.ball45_2.mass    = 0.050
# add(pool_cfg, 'dov_pool')

# # pool 1500 config
# pool_1500_cfg = pool_cfg._deepcopy()
# pool_1500_cfg.mprims.sim_end            = 1500
# pool_1500_cfg.execute.scene.objects.ball45.mass    = 0.010
# add(pool_1500_cfg, 'dov_pool_1500')
