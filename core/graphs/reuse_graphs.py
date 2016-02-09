# Code for generating figures of the the PhD thesis:
# 'Self-Exploration of Sensorimotor Spaces in Robots' by Fabien C. Y. Benureau
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import os, sys
import importlib
import copy

import dotdot
import graphs


RED = '#DF6464'


def reuse_quantiles(results_trios, y_max=360000, show=True,
                    src_quantiles=(0, 100), tgt_quantiles=(0, 100)):
    figs = []

    for nor_results, src_results, tgt_results in results_trios:
        nor_cfg = nor_results.expcfg
        tgt_cfg = tgt_results.expcfg

        f = graphs.perf_quantiles(nor_results, dashed_quant=src_quantiles,
                                  color=graphs.NOREUSE_COLOR, plot_width=900, plot_height=450,
                                  x_range=(0, tgt_cfg.exploration.steps), y_range=(0, y_max),#3.268),
                                  title='{}'.format(tgt_results.job.key))
        graphs.perf_quantiles(tgt_results, fig=f, dashed_quant=tgt_quantiles, color=graphs.REUSE_COLOR)
        figs.append([f])

    if show:
        graphs.show(figs)
    else:
        return figs


def reuse_perflines(results_trios, y_max=360000, extremes=(0, 100), show=True):
    figs = []
    for nor_results, src_results, tgt_results in results_trios:
        nor_cfg = nor_results.expcfg
        tgt_cfg = tgt_results.expcfg

        f = graphs.perf_lines(nor_results,
                              color=graphs.NOREUSE_COLOR, plot_width=900, plot_height=450,
                              x_range=(0, tgt_cfg.exploration.steps), y_range=(0, y_max),
                              title='{}'.format(tgt_results.key), minimalist=False)

        graphs.perf_lines(tgt_results, fig=f,
                           color=graphs.REUSE_COLOR)
        figs.append(f)

    fig = graphs.vplot(figs)
    if show:
        graphs.show(fig)
    else:
        return fig


def reuse_coverage(data, milestones=(200, 1000), nor=True, src=True, tgt=True, testname='tcov', **kwargs):
    figs = []
    for d, flag in zip(data, (src, tgt, nor)):
        if flag and d is not None:
            figs.append([])
            try:
                K_boot = d['jobcfg'].exploration.explorer.eras[0]
            except KeyError:
                K_boot = 200
            s_vectors = d['s_vectors']

            for t in milestones:
                fig = graphs.coverage(d['s_channels'], d.expcfg.tests[testname].buffer_size,
                                      s_vectors=s_vectors[:t], swap_xy=False,
                                      plot_width=400, plot_height=400,
                                      title='{} {}'.format(d.key, t), **kwargs)
                graphs.spread(d['s_channels'], s_vectors=s_vectors[:K_boot], fig=fig,
                              swap_xy=False, e_radius=3.0, e_alpha=1.0, e_color=RED)
                graphs.spread(d['s_channels'], s_vectors=s_vectors[K_boot:t], fig=fig,
                              swap_xy=False, e_radius=3.0, e_alpha=1.0)

                figs[-1].append(fig)

    return graphs.show(figs)
