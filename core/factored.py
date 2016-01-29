from __future__ import division

import math

import numpy as np
import shapely

from environments import tools
import learners
from clusterjobs import datafile

import paths
import gfx

from random_seeds import src_seeds, tgt_seeds
seeds = src_seeds


def dist(p1, p2):
    return math.sqrt(sum((p1i-p2i)**2 for p1i, p2i in zip(p1, p2)))

_testset = None
def testset():
    global _testset
    if _testset is None:
        ts = datafile.load_file(paths.testset_filepath)
        _testset = tuple(tools.to_vector(s_signal, ts['s_channels']) for s_signal in ts['s_signals'])
    return _testset

def run_exploration(env, ex, N, mesh=None, verbose=False, prefix=''):
    explorations, s_vectors, s_goals = [], [], []

    for i in range(N):
        if verbose and i % 100 == 0:
            gfx.print_progress(i, N, prefix=prefix)
        exploration = ex.explore()
        feedback = env.execute(exploration['m_signal'])
        ex.receive(exploration, feedback)
        s_vectors.append(tools.to_vector(feedback['s_signal'], env.s_channels))
        if 's_goal' in exploration:
            s_goals.append(tools.to_vector(exploration['s_goal'], env.s_channels))
        if mesh is not None:
            mesh.add(feedback['s_signal'], m_signal=exploration['m_signal'])
        explorations.append((exploration, feedback))
    if verbose:
        gfx.print_progress(N, N, prefix=prefix)

    return explorations, s_vectors, s_goals


def run_nn(testset, s_vectors):

    nnset = learners.NNSet()
    for s_vector in s_vectors:
        nnset.add((), s_vector)

    errors = []
    for s_vector_goal in testset:
        distances, idx = nnset.nn_y(s_vector_goal, k=1)
        s_vector = nnset.ys[idx[0]]
        errors.append(dist(s_vector_goal, s_vector))

    return errors

def run_nns(testset, s_vectors, ticks=None, verbose=True):
    if ticks is None:
        ticks = range(len(s_vectors))
    ticks, N = set(ticks), len(ticks)


    avgs, stds = [], []
    nnset = learners.NNSet()
    for t, s_vector in enumerate(s_vectors):

        nnset.add((), s_vector)

        if t in ticks:
            if verbose:
                gfx.print_progress(len(avgs) , N)
            errors = []
            for s_vector_goal in testset:
                distances, idx = nnset.nn_y(s_vector_goal, k=1)
                s_vector = nnset.ys[idx[0]]
                errors.append(dist(s_vector_goal, s_vector))
            avgs.append(np.mean(errors))
            stds.append(np.std(errors))

    if verbose:
        gfx.print_progress(N, N)

    return avgs, stds


def run_coverage(threshold, s_vectors):
    union = shapely.ops.unary_union([shapely.geometry.Point(*sv_i).buffer(threshold)
                                     for sv_i in s_vectors])
    return union.area

def run_coverages(threshold, s_vectors, ticks=None):
    if ticks is None:
        ticks = range(len(s_vectors))
    ticks = set(ticks)

    union = shapely.geometry.MultiPolygon([])
    areas = [0.0]
    for t, s_vector in enumerate(s_vectors):
        union = union.union(shapely.geometry.Point(*s_vector).buffer(threshold))
        if t in ticks:
            areas.append(union.area)

    return areas

def percentile_mean(error_avgs, p=0.10):
    ms = []
    for errors in error_avgs:
        errors = sorted(errors)
        errors = errors[:int(len(errors)*p)]
        ms.append(np.average(errors))

    return ms

def compass_extrema(s_vectors):
    min_x, min_x_idx = float('+inf'), -1
    max_x, max_x_idx = float('-inf'), -1
    min_y, min_y_idx = float('+inf'), -1
    max_y, max_y_idx = float('-inf'), -1

    for i, (x, y) in enumerate(s_vectors):
        if x < min_x:
            min_x     = x
            min_x_idx = i

        if x > max_x:
            max_x     = x
            max_x_idx = i

        if y < min_y:
            min_y     = y
            min_y_idx = i

        if y > max_y:
            max_y     = y
            max_y_idx = i

    return {'min_x': min_x_idx, 'max_x': max_x_idx,
            'min_y': min_y_idx, 'max_y': max_y_idx}



thetas = tuple(i*math.pi/4 for i in range(8))

def spread_extrema(s_vectors, dirs=thetas):
    def proj(x, y, theta):
        return (  x*math.cos(theta)
                + y*math.sin(theta))

    records = [(float('-inf'), -1) for d in thetas]
    for i, (x, y) in enumerate(s_vectors):
        for j, theta in enumerate(thetas):
            d = proj(x, y, theta)
            if records[j][0] < d:
                records[j] = d, i

    return [idx for d, idx in records]
