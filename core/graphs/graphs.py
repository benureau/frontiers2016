from __future__ import division, print_function

import os
import bisect
import struct
import numbers
import math
import random
import collections

import numpy as np
import bokeh
from bokeh import plotting
from bokeh.core.properties import value
from bokeh.models import FixedTicker

try:
    import shapely
    import shapely.ops
    import shapely.geometry
except ImportError:
    pass

from environments import tools

import factored


PLOT_WIDTH  = 900
PLOT_HEIGHT = 450
PLOT_SIZE   = 450

    ## color

BLUE  = '#2577B2' # light blue
PINK  = '#E84A5F'
GREEN = '#5AB953'

MB_COLOR = BLUE
GB_COLOR = PINK

NOREUSE_COLOR   = BLUE
REUSE_COLOR     = PINK
RANDREUSE_COLOR = '#408000' # green

E_COLOR = '#2779B3' # blue
G_COLOR = '#FF030D' # red

TOOLS = "pan,reset,save"


white   = (255, 255, 255)

def rgbu2rgb255(rgb):
    return (int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2]))

def rgb2hex(rgb):
    return '#{0:02x}{1:02x}{2:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def hex2rgb(hexstr):
    return struct.unpack('BBB', hexstr[1:].decode('hex'))

def rgba2rgb(rgb, rgba):
    r,g,b,a = rgba;
    return ((1-a)*rgb[0] + a * r,
            (1-a)*rgb[1] + a * g,
            (1-a)*rgb[2] + a * b)

C_COLOR   = rgb2hex((21, 152, 71))
#C_COLOR_H = rgb2hex(rgba2rgb(white, (21, 152, 71, 0.5)))
C_COLOR_H = rgb2hex((200, 200, 200))

MUTED = [(0.282, 0.470, 0.811), (0.415, 0.8, 0.396), (0.839, 0.372, 0.372), (0.705, 0.486, 0.780), (0.768, 0.678, 0.4), (0.466, 0.745, 0.858)]
MUTED = [rgb2hex(rgbu2rgb255(rgb)) for rgb in MUTED]


def hexa(hex, alpha):
    rgb = hex2rgb(hex)
    return rgb2hex(rgba2rgb((255, 255, 255), rgb+(alpha,)))

def colorscale(timescale, rgb, alpha_step=0.15):
    color_n = len(timescale)
    colors = [rgba2rgb((255, 255, 255), rgb+(1.0-alpha_step*i,)) for i in range(color_n)]
    return [rgb2hex(c) for c in colors]

def ranges(s_channels, x_range=None, y_range=None):
    if x_range is None:
        x_range = s_channels[0].bounds
    if y_range is None:
        y_range = s_channels[1].bounds
    epsilon = 0.0000001 # HACK
    x_range = (x_range[0] - epsilon, x_range[1] + epsilon)
    y_range = (y_range[0] - epsilon, y_range[1] + epsilon)
    return x_range, y_range


    ## bokeh wrapping

results_dir = os.path.abspath(os.path.join(__file__, '../../../results'))
def output_file(filepath):
    return bokeh.io.output_file(os.path.join(results_dir, filepath))

def output_notebook():
    from IPython.display import display, Javascript
    disable_js = """
    IPython.OutputArea.auto_scroll_threshold = 9999;
    IPython.OutputArea.prototype._should_scroll = function(lines) {
        return false;
    }
    """
    display(Javascript(disable_js))
    return bokeh.io.output_notebook(hide_banner=True)

def show(figs):
    if isinstance(figs, collections.Iterable):
        if isinstance(figs[0], collections.Iterable):
            bokeh.io.show(bokeh.io.gridplot(figs))
        else:
            bokeh.io.show(bokeh.io.gridplot([figs]))
    else:
        bokeh.io.show(figs)

def gridplot(figs):
    return bokeh.io.gridplot(figs)

def hplot(figs):
    return bokeh.io.hplot(*figs)

def vplot(figs):
    return bokeh.io.vplot(*figs)


    ## figure defaults

def prepare_fig(fig, grid=False, tight=True, clean=True, **kwargs):
    if fig is None:
        if 'tools' not in kwargs:
            kwargs['tools'] = TOOLS
        if 'title_text_font_size' not in kwargs:
            kwargs['title_text_font_size'] = value('6pt')

        fig = plotting.figure(**kwargs)
        if clean:
            three_ticks(fig)
            disable_minor_ticks(fig)
        if tight:
            tight_layout(fig)
        if not grid:
            disable_grid(fig)

    return fig

def tight_layout(fig):
    fig.min_border_top    = 35
    fig.min_border_bottom = 35
    fig.min_border_right  = 35
    fig.min_border_left   = 35

def three_ticks(fig):
    x_min, x_max = fig.x_range.start, fig.x_range.end
    y_min, y_max = fig.y_range.start, fig.y_range.end
    x_ticks = [x_min, (x_min + x_max)/2.0, x_max]
    if x_min < 0 < x_max and 0.0 not in x_ticks:
        x_ticks.append(0)
        x_ticks.sort()
    y_ticks = [y_min, (y_min + y_max)/2.0, y_max]
    if y_min < 0 < y_max and 0.0 not in y_ticks:
        y_ticks.append(0)
        y_ticks.sort()

    fig.xaxis[0].ticker=FixedTicker(ticks=x_ticks)
    fig.yaxis[0].ticker=FixedTicker(ticks=y_ticks)

def disable_minor_ticks(fig):
    fig.axis.major_label_text_font_size = value('8pt')
    fig.axis.minor_tick_line_color = None
    fig.axis.major_tick_in = 0

def disable_grid(fig):
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None




    ## displaying kinematic 2D arm postures

def posture_vectors(env, m_vectors, **kwargs):
    m_signals = [tools.to_signal(m_vector, env.m_channels) for m_vector in m_vectors]
    return posture_signals(env, m_signals, **kwargs)

def posture_extrema(env, explorations, thetas=tuple(i*math.pi/4 for i in range(8)), **kwargs):
    s_vectors = [tools.to_vector(e[1]['s_signal'], env.s_channels) for e in explorations]
    idxs = factored.spread_extrema(s_vectors, dirs=thetas)
    m_signals = [explorations[idx][0]['m_signal'] for idx in idxs]
    return posture_signals(env, m_signals, **kwargs)

def posture_quadrans(env, explorations, **kwargs):
    s_vectors = [tools.to_vector(e[1]['s_signal'], env.s_channels) for e in explorations]
    pp, pn, nn, np = [], [], [], []
    for idx, (x, y) in enumerate(s_vectors):
        if x < 0:
            if y < 0:
                nn.append(idx)
            else:
                np.append(idx)
        else:
            if y < 0:
                pn.append(idx)
            else:
                pp.append(idx)
    idxs = [random.choice(pp), random.choice(np), random.choice(pn), random.choice(nn)]
    m_signals = [explorations[idx][0]['m_signal'] for idx in idxs]
    posture_signals(env, m_signals, **kwargs)


def posture_idxs(env, explorations, idxs=None, **kwargs):
    if idxs is None:
        idxs=[int(len(explorations)*i/5.0) for i in range(5)]
    posture_signals(env, [explorations[i][0]['m_signal'] for i in idxs], **kwargs)

def posture_random(env, explorations, n=5, **kwargs):
    m_display = choose_m_vectors(env.m_channels, explorations, n=n)
    posture_vectors(env, m_display, **kwargs)

def choose_m_vectors(m_channels, explorations, n=5):
    """FIXME: no replacements"""
    m_vectors = []
    for _ in range(n):
        explo = random.choice(explorations)
        m_vector = tools.to_vector(explo[0]['m_signal'], m_channels)
        m_vectors.append(m_vector)

    return m_vectors




#'#91C46C'
def posture_explorations(kin_env, explorations, **kwargs):
    return posture_signals(kin_env, [e[0]['m_signal'] for e in explorations], **kwargs)


def posture_signals(kin_env, m_signals, fig=None, plot_height=PLOT_SIZE, plot_width=PLOT_SIZE,
                    swap_xy=True, x_T=0.0, y_T=0.0, tools=TOOLS,
                    title='posture graphs', grid=False,
                    color='#666666', alpha=1.0, radius_factor=1.0, line_factor=1.0,
                    x_range=[-1.0, 1.0], y_range=[-1.0, 1.0], **kwargs):

    fig = prepare_fig(fig, x_range=x_range, y_range=y_range, tools=tools,
                      plot_width=plot_width, plot_height=plot_height, **kwargs)

    for m_signal in m_signals:
        m_vector = kin_env.flatten_synergies(m_signal)
        posture(kin_env, m_vector, fig=fig, swap_xy=swap_xy, x_T=x_T, y_T=y_T,
                color=color, alpha=alpha, radius_factor=radius_factor, line_factor=line_factor)

    return fig




def display_grid(fig, div_x, div_y, x_range=[0.0, 1.0], y_range=[0.0, 1.0],
                 color='#DDDDDD', alpha=0.25):
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_color = None
    xa, xb = x_range
    ya, yb = y_range

    x0s, y0s, x1s, y1s = [], [], [], []
    for i in range(div_x+1):
        x0s.append(xa+i*(xb-xa)/div_x)
        x1s.append(xa+i*(xb-xa)/div_x)
        y0s.append(ya)
        y1s.append(yb)
    for i in range(div_y+1):
        x0s.append(xa)
        x1s.append(xb)
        y0s.append(ya+i*(yb-ya)/div_y)
        y1s.append(ya+i*(yb-ya)/div_y)

    fig.segment(x0s, y0s, x1s, y1s, line_color=color, line_alpha=alpha)


def posture(kin_env, m_vector, fig=None, swap_xy=True, x_T=0.0, y_T=0.0,
            color='#666666', alpha=0.5, radius_factor=1.0, line_factor=1.0, **kwargs):

    assert fig is not None
    kwargs.update({'line_color'  : color,
                   'line_alpha'  : alpha,
                   'fill_color'  : color,
                   'fill_alpha'  : alpha,
                  })

    s_signal = kin_env._multiarm.forward_kin(m_vector)

    xs, ys = [0.0], [0.0]
    for i in range(kin_env.cfg.dim):
        xs.append(s_signal['x{}'.format(i+1)])
        ys.append(s_signal['y{}'.format(i+1)])

    if swap_xy:
        ys, xs = xs, ys

    xs, ys = np.array(xs), np.array(ys)
    fig.line(xs+x_T, ys+y_T, line_width=line_factor*radius_factor, line_color=color, line_alpha=alpha)
    fig.circle(xs[  : 1]+x_T, ys[  : 1]+y_T, radius=radius_factor*0.015, **kwargs)
    fig.circle(xs[ 1:-1]+x_T, ys[ 1:-1]+y_T, radius=radius_factor*0.008, **kwargs)
    fig.circle(xs[-1:  ]+x_T, ys[-1:  ]+y_T, radius=radius_factor*0.01, color='red', alpha=alpha)




    ## wrapping plots

def line(x_range, avg, std, color='#E84A5F', dashes=(4, 2), alpha=1.0):
    plotting.line(x_range, [avg, avg], line_color=color, line_dash=list(dashes), line_alpha=alpha)
    plotting.hold(True)
    plotting.rect([(x_range[0]+x_range[1])/2.0], [avg], [x_range[1]-x_range[0]], [2*std],
                  fill_color=color, line_color=None, fill_alpha=0.1*alpha)
    plotting.hold(False)

def spread(s_channels, s_vectors=(), s_goals=(), fig=None,
           title='no title', plot_height=PLOT_SIZE, plot_width=PLOT_SIZE, tools=TOOLS,
           swap_xy=True, x_range=None, y_range=None,
           e_radius=1.0, e_color=E_COLOR, e_alpha=0.75,
           g_radius=1.0, g_color=G_COLOR, g_alpha=0.75,
           grid=False, radius_units='screen', font_size='11pt', **kwargs):

    x_range, y_range = ranges(s_channels, x_range=x_range, y_range=y_range)
    fig = prepare_fig(fig, x_range=x_range, y_range=y_range, tools=tools,
                      plot_width=plot_width, plot_height=plot_height, **kwargs)

    # effects
    try:
        xv, yv = zip(*(s[:2] for s in s_vectors))
    except ValueError:
        xv, yv = [], []
    if swap_xy:
        x_range, y_range = y_range, x_range
        xv, yv = yv, xv
    fig.scatter(xv, yv,
                fill_color=e_color, fill_alpha=e_alpha, line_color=None,
                radius=e_radius, radius_units=radius_units)
#                title_text_font_size=font_size, **kwargs)

    # goals
    try:
        xg, yg = zip(*s_goals)
    except ValueError:
        xg, yg = [], []
    if swap_xy:
        xg, yg = yg, xg
    fig.scatter(xg, yg, radius=g_radius, radius_units="screen",
                fill_color=g_color, fill_alpha=g_alpha, line_color=None)

    return fig


def coverage(s_channels, threshold, s_vectors=(), fig=None, plot_height=PLOT_SIZE, plot_width=PLOT_SIZE,
             title='no title', swap_xy=True, x_range=None, y_range=None, grid=False,
             color=C_COLOR, c_alpha=1.0, alpha=0.5, **kwargs):

    x_range, y_range = ranges(s_channels, x_range=x_range, y_range=y_range)
    try:
        xv, yv = zip(*(s[:2] for s in s_vectors))
    except ValueError:
        xv, yv = [], []
    if swap_xy:
        x_range, y_range = y_range, x_range
        xv, yv = yv, xv

    fig = prepare_fig(fig, x_range=x_range, y_range=y_range, tools=TOOLS,
                      plot_width=plot_width, plot_height=plot_height, **kwargs)

    fig.circle(xv, yv, radius=threshold,
               fill_color=hexa(color, 0.35), fill_alpha=c_alpha, line_color=None)

    if len(s_vectors) > 0:
        union = shapely.ops.unary_union([shapely.geometry.Point(*sv_i).buffer(threshold)
                                         for sv_i in s_vectors])
        boundary = union.boundary
        if isinstance(boundary, shapely.geometry.LineString):
            boundary = [boundary]

        for b in boundary:
            x, y = b.xy
            x, y = list(x), list(y)
            if swap_xy:
                x, y = y, x
            fig.patch(x, y, fill_color=None, line_color=hexa(color, 0.75))

    disable_minor_ticks(fig)
    return fig


def bokeh_nn(s_channels, testset, errors,
             title='no title', swap_xy=True, x_range=None, y_range=None,
             radius=3.0, alpha=0.75):

    x_range, y_range = ranges(s_channels, x_range=x_range, y_range=y_range)
    xv, yv = zip(*testset)
    if swap_xy:
        x_range, y_range = y_range, x_range
        xv, yv = yv, xv

    scale = [0, max(errors)]
    colorbar = ColorBar(scale, ['#0000FF', '#FF0000'], continuous=True)
    colors = [colorbar.color(e) for e in errors]

    plotting.scatter(xv, yv, title=title,
                     x_range=x_range, y_range=y_range,
                     fill_color=colors, fill_alpha=alpha, line_color=None,
                     radius=radius, radius_units="screen")
    plotting.hold(True)
    plotting.grid().grid_line_color='white'
    plotting.hold(False)

def mesh(meshgrid, s_vectors=(), s_goals=(),
         mesh_timescale=(1000000,), mesh_colors=(C_COLOR_H,), title='no title',
         e_radius=1.0, e_color=E_COLOR, e_alpha=0.75,
         g_radius=1.0, g_color=G_COLOR, g_alpha=0.75, swap_xy=True, tile_ratio=0.97,
         x_range=None, y_range=None):

    x_range, y_range = ranges(meshgrid.s_channels, x_range=x_range, y_range=y_range)
    xm = zip(*[b.bounds[0] for b in meshgrid.nonempty_bins])
    ym = zip(*[b.bounds[1] for b in meshgrid.nonempty_bins])
    if swap_xy:
        x_range, y_range = y_range, x_range
        xm, ym = ym, xm

    color = []
    for b in meshgrid.nonempty_bins:
        t = b.elements[0][0]
        color.append(mesh_colors[bisect.bisect_left(mesh_timescale, t)])

    plotting.rect((np.array(xm[1])+np.array(xm[0]))/2         , (np.array(ym[1])+np.array(ym[0]))/2,
                  (np.array(xm[1])-np.array(xm[0]))*tile_ratio, (np.array(ym[1])-np.array(ym[0]))*tile_ratio,
                  x_range=x_range, y_range=y_range,
                  fill_color=color, fill_alpha=0.5,
                  line_color='#444444', line_alpha=0.0, title=title)
    plotting.hold(True)
    plotting.grid().grid_line_color='white'

    spread(meshgrid.s_channels, s_vectors=s_vectors, s_goals=s_goals, swap_xy=swap_xy,
           e_radius=e_radius, e_color=e_color, e_alpha=e_alpha,
           g_radius=g_radius, g_color=g_color, g_alpha=g_alpha)
    plotting.hold(False)


def bokeh_highlights(s_vectors, n=1, color='#DF4949', swap_xy=True, radius=2.5, alpha=0.5):
    """n is the number of effect per cell to pick"""
    xv, yv = zip(*s_vectors)
    if swap_xy:
        xv, yv = yv, xv
    plotting.circle(xv, yv, fill_color = None, line_color=color, line_alpha=alpha, line_width=0.5, radius=radius, radius_units='screen')

class ColorBar(object):

    def __init__(self, scale, colorscale, continuous=True):
        self.scale = scale
        self.continuous = continuous

        self.colorscale = list(colorscale)
        for i, c in enumerate(self.colorscale):
            if isinstance(c, str):
                self.colorscale[i] = hex2rgb(c)
            self.colorscale[i] = np.array(self.colorscale[i])
        self.colorscale = tuple(self.colorscale)
        print(self.scale)

    def color(self, x):
        if self.continuous:
            if x <= self.scale[0]:
                return rgb2hex(self.colorscale[0])
            if x >= self.scale[-1]:
                return rgb2hex(self.colorscale[-1])
            index = bisect.bisect_left(self.scale, x) - 1
            c_a = self.colorscale[index]
            c_b = self.colorscale[index+1]
            c = ((x-self.scale[index])*c_b + (self.scale[index+1]-x)*c_a)/(self.scale[index+1]-self.scale[index])
            return rgb2hex(c)
        else:
            raise NotImplementedError


def perf_std(ticks, avgs, stds, **kwargs):
    if stds is not None:
        stds = [(s, s) for s in stds]
    return perf_astd(ticks, avgs, stds, **kwargs)



def perf_astd(ticks, avgs, astds, color=BLUE, fig=None, alpha=1.0, sem=1.0,
              plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT, legend=None, **kwargs):

    fig = prepare_fig(fig, plot_width=plot_width, plot_height=plot_height, **kwargs)

    fig.legend.orientation = "bottom_right"
    fig.line(ticks, avgs, color=color, line_alpha=alpha, legend=legend)

    if astds is not None:
        x_std = list(ticks) + list(reversed(ticks))
        y_std = (             [a - s_min/math.sqrt(sem) for a, (s_min, s_max) in zip(avgs, astds)] +
                list(reversed([a + s_max/math.sqrt(sem) for a, (s_min, s_max) in zip(avgs, astds)])))
        fig.patch(x_std, y_std, fill_color=color, fill_alpha=alpha*0.25, line_color=None)
    fig.grid.grid_line_color=None
    #fig.grid().grid_line_color = 'white'
    #plotting_axis(fig)

    return fig
    #plotting.hold(False)


def perf_quantiles(results, color=BLUE, fig=None, alpha=1.0, extremes=(0, 100),
                   plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT, legend=None, max_line=True, **kwargs):
    ticks = results['ticks']
    quantiles = {}
    for q in (25, 50, 75) + tuple(extremes):
        quantiles[q] = [np.percentile(avgs, q) for avgs in results['tick_avgs']]

    fig = prepare_fig(fig, plot_width=plot_width, plot_height=plot_height,
                      clean=False, tight=False, **kwargs)

    fig.line(ticks, quantiles[50], color=color, line_alpha=alpha, legend=legend)

    xs_patch = list(ticks) + list(reversed(ticks))
    ys_patch = (quantiles[25] + list(reversed(quantiles[75])))
    fig.patch(xs_patch, ys_patch, fill_color=color, fill_alpha=alpha*0.25, line_color=None)

    for q in extremes:
        fig.line(ticks, quantiles[q],   color=color, line_alpha=alpha, line_dash=[3, 3])
#    fig.line(ticks, quantiles[100], color=color, line_alpha=alpha, line_dash=[3, 3])

    fig.grid.grid_line_color=None
    fig.legend.orientation = "bottom_right"

    return fig

def perf_lines(results, color=BLUE, fig=None, alpha=0.75,
               plot_width=PLOT_WIDTH, plot_height=PLOT_HEIGHT, legend=None, max_line=True, **kwargs):
    ticks = results['ticks']
    lines = [[] for _ in results['tick_avgs'][0]]
    for avgs in results['tick_avgs']:
        for line, avg in zip(lines, avgs):
            line.append(avg)

    fig = prepare_fig(fig, plot_width=plot_width, plot_height=plot_height, **kwargs)

    for line in results['rep_avgs']:
        fig.line(ticks, line, color=color, line_alpha=alpha, legend=legend)#, line_dash=[3, 3])

    fig.grid.grid_line_color=None
    fig.legend.orientation = "bottom_right"

    return fig


def perf_std_discrete(ticks, avgs, stds, legend=None,
                      std_width=0.3, plot_width=1000, plot_height=300,
                      color=BLUE, alpha=1.0, **kwargs):
    plotting.rect(ticks, avgs, [std_width for _ in stds], 2*np.array(stds),
                  line_color=None, fill_color=color, fill_alpha=alpha*0.5,
                  plot_width=plot_width, plot_height=plot_height, **kwargs)
    plotting.hold(True)
    plotting.line(ticks, avgs, line_color=color, line_alpha=alpha, legend=legend)
    plotting.circle(ticks, avgs, line_color=None, fill_color=color, fill_alpha=alpha)
    plotting.grid().grid_line_color = 'white'
    plotting_axis()

    plotting.hold(False)


if __name__ == '__main__':
    print(rgb2hex((37, 119, 178)))
    print(hex2rgb(rgb2hex((37, 119, 178))))
    import numpy as np
    print(np.array(rgba2rgb((255, 255, 255), (166, 48, 28, 0.50)))/255.0)
