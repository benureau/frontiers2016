# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import os, sys
import importlib
import copy

import dotdot
import graphs

def reuse_quantiles(results_trios, y_max=360000, extremes=(0, 100), show=True):
    figs = []

    for nor_results, src_results, tgt_results in results_trios:
        nor_cfg = nor_results.expcfg
        tgt_cfg = tgt_results.expcfg

        f = graphs.perf_quantiles(nor_results, extremes=extremes,
                                  color=graphs.NOREUSE_COLOR, plot_width=1000, plot_height=500,
                                  x_range=(0, tgt_cfg.exploration.steps), y_range=(0, y_max),#3.268),
                                  title='{}'.format(tgt_results.job.key))
        graphs.perf_quantiles(tgt_results, fig=f, extremes=extremes, color=graphs.REUSE_COLOR)
        figs.append(f)

    fig = graphs.vplot(figs)
    if show:
        graphs.show(fig)
    else:
        return fig


def reuse_perflines(results_trios, y_max=360000, extremes=(0, 100), show=True):
    figs = []
    for nor_results, src_results, tgt_results in results_trios:
        nor_cfg = nor_results.expcfg
        tgt_cfg = tgt_results.expcfg

        f = graphs.perf_lines(nor_results,
                              color=graphs.NOREUSE_COLOR, plot_width=1000, plot_height=500,
                              x_range=(0, tgt_cfg.exploration.steps), y_range=(0, y_max),
                              title='{}'.format(tgt_results.key))

        graphs.perf_lines(tgt_results, fig=f,
                           color=graphs.REUSE_COLOR)
        figs.append(f)

    fig = graphs.vplot(figs)
    if show:
        print('show')
        graphs.show(fig)
    return fig
