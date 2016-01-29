import os, sys

from environments import tools
from bokeh.models import FixedTicker

import dotdot
import graphs


red = '#DF6464'


def reuse_coverage(data, milestones=(200, 1000), nor=True, src=True, tgt=True, testname='tcov'):
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
                                      s_vectors=s_vectors[:t],
                                      swap_xy=False, grid=True,
                                      plot_width=400, plot_height=400,
                                      title='{} {}'.format(d.key, t))
                graphs.spread(d['s_channels'], s_vectors=s_vectors[:K_boot], fig=fig,
                              swap_xy=False, e_radius=3.0, e_alpha=1.0, e_color=red)
                graphs.spread(d['s_channels'], s_vectors=s_vectors[K_boot:t], fig=fig,
                              swap_xy=False, e_radius=3.0, e_alpha=1.0)

                figs[-1].append(fig)

    return graphs.show(figs)
