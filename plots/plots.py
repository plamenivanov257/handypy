"""
Contains some useful plotting functions.
"""
import numpy as np
from termcolor import cprint
import matplotlib as mpl
from matplotlib.colors import hsv_to_rgb
from matplotlib.transforms import ScaledTranslation
from warnings import warn


def domaincol_c(w, s=1, abs_norm=1, abs_pow=0.2):  # Classical domain coloring
    # w is the  array of values f(z)
    # s is the constant saturation

    abs2 = lambda z : z.real**2 + z.imag**2

    H = Hcomplex(w)
    S = s * np.ones(H.shape)
    #modul = np.absolute(w)

    if abs_norm is not None:
        V = (1.0-1.0/(1+abs2(w)/abs_norm))**abs_pow
    else:
        V = 1 * np.ones(H.shape)
    # the points mapped to infinity are colored with white; hsv_to_rgb(0, 0, 1)=(1, 1, 1)=white

    HSV = np.dstack((H, S, V))
    RGB = hsv_to_rgb(HSV)
    return RGB

def plot_domain(color_func=domaincol_c, func=None, re=[-2,2], im=[-2,2], title='', 
                s=1, abs_norm=1, N=200, daxis=None, cax=None, cax_orientation="vertical", cax_size_ratio=10, cax_abs_limit=1, abs_pow=0.4):
    x = np.linspace(re[0], re[1], N)
    y = np.linspace(im[0], im[1], N)
    x, y = np.meshgrid(x, y)
    z = x + 1j*y

    data = func(z)
    # print(np.max(np.abs(data)))

    daxis.set_xlim(re)
    daxis.set_ylim(im)
    domc = color_func(data, s, abs_norm, abs_pow)
    daxis.imshow(domc, origin="lower", extent=(re[0], re[1], im[0], im[1]))


    if cax is None:
        return

    # Make a pwetty colourbar
    if type(cax) is not tuple or len(cax) != 2:
        warn("Colorbar axes (cax) should be a tuple of two matplotlib Axes!")
        return

    cax_abs = cax[0]
    cax_phase = cax[1]
    cax_N = N

    cax_abs_limit = 5  # a big number to make the colour fully saturated
    if cax_orientation == "vertical":
        cbf_phase = lambda z : np.exp(2j * np.pi* (np.imag(z) - im[0]) / (im[1] - im[0])) * np.exp(-1j * np.pi)
        cbf_abs = lambda z : cax_abs_limit*(np.imag(z) - im[0]) / (im[1] - im[0])
         
        # axes labels
        cax_abs.set_xlim(np.array(re)*cax_size_ratio)
        cax_abs.set_xlabel("")
        cax_abs.set_xticks([])
        cax_abs.set_xticklabels([])
        cax_abs.set_ylabel(r"Absolute value")
        cax_abs.set_ylim(im)
        cax_abs.set_yticks([im[0], im[1]])
        #cax_abs.set_yticklabels([0, cax_abs_limit])
        cax_abs.set_yticklabels([0, r"$+\infty$"])
        cax_abs.yaxis.set_label_position("right")
        cax_abs.yaxis.tick_right()

        cax_phase.set_xlim(np.array(re)*cax_size_ratio)
        cax_phase.set_xlabel("")
        cax_phase.set_xticks([])
        cax_phase.set_xticklabels([])
        cax_phase.set_ylabel("Phase")
        cax_phase.set_ylim(im)
        cax_phase.set_yticks([im[0], im[1]])
        cax_phase.set_yticklabels([r"$-\pi$", r"$\pi$"])
        cax_phase.yaxis.set_label_position("right")
        cax_phase.yaxis.tick_right()


        data = cbf_phase(z)
        domc = color_func(data, s, None, abs_pow)
        cax_phase.imshow(domc, origin="lower", extent=(re[0], re[1], im[0], im[1]))

        data = cbf_abs(z)
        domc = color_func(data, s=0, abs_norm=abs_norm, abs_pow=abs_pow)
        cax_abs.imshow(domc, origin="lower", extent=(re[0], re[1], im[0], im[1]))
        
    else:
        cbf_phase = lambda z : np.exp(2j * np.pi* (np.real(z) - re[0]) / (re[1] - re[0])) * np.exp(-1j * np.pi)
        cbf_abs = lambda z : cax_abs_limit*(np.real(z) - re[0]) / (re[1] - re[0])

        # axes labels
        cax_abs.set_ylim(np.array(im)*cax_size_ratio)
        cax_abs.set_ylabel("")
        cax_abs.set_yticks([])
        cax_abs.set_yticklabels([])
        cax_abs.set_xlabel("Absolute value")
        cax_abs.set_xlim(re)
        cax_abs.set_xticks([re[0], re[1]])
        cax_abs.set_xticklabels([0, r"$+\infty$"])
        #cax_abs.set_xticklabels([0, cax_abs_limit])
        cax_abs.get_xticklabels()[0].set_horizontalalignment("left")
        cax_abs.get_xticklabels()[1].set_horizontalalignment("right")

        cax_phase.set_ylim(np.array(im)*cax_size_ratio)
        cax_phase.set_ylabel("")
        cax_phase.set_yticks([])
        cax_phase.set_yticklabels([])
        cax_phase.set_xlabel("Phase")
        cax_phase.set_xlim(re)
        cax_phase.set_xticks([re[0], re[1]])
        cax_phase.set_xticklabels([r"$-\pi$", r"$\pi$"])
        cax_phase.get_xticklabels()[0].set_horizontalalignment("left")
        cax_phase.get_xticklabels()[1].set_horizontalalignment("right")

        data = cbf_phase(z)
        #print(np.angle(data[0, :]))
        domc = color_func(data, s, None, abs_pow)
        cax_phase.imshow(domc, origin="lower", extent=(re[0], re[1], im[0], im[1]))

        data = cbf_abs(z)
        domc = color_func(data, s=0, abs_norm=abs_norm, abs_pow=abs_pow)
        cax_abs.imshow(domc, origin="lower", extent=(re[0], re[1], im[0], im[1]))


def Hcomplex(z):  # computes the hue corresponding to the complex number z
    H = np.angle(z) / (2*np.pi) + 1
    return np.mod(H, 1)


def contourf_plot_diverging(ax, plot_xrange, plot_yrange, plot_data, n_levels=100, levels=None, cmap='seismic', rasterized=True):
    try:
        if levels is None:
            plot_data_maxabs = np.max(np.abs(plot_data))
            print("Plot data in range ", np.min(plot_data), " to ", np.max(plot_data))
            levels = np.linspace(-plot_data_maxabs, plot_data_maxabs, n_levels)

        cf = ax.contourf(plot_xrange, plot_yrange, np.transpose(plot_data[:, :]), levels=levels, cmap=cmap)
        if rasterized:
            for c in cf.collections:
                c.set_rasterized(True)
        return cf
    except Exception as ex:
        cprint("Couldn't plot!", "red")
        cprint(ex, "red")
        return None


def setup_generic_plots(fontsize=18):
    """
    Sets up matplotlib for LaTeX-enabled plots.
    """
    font = {'family' : 'serif',
            'serif'  : ['Computer Modern Roman'],
            # 'weight' : 'bold',
            'size'   : fontsize}

    mpl.rcParams["figure.titlesize"] = fontsize
    mpl.rcParams["axes.titlesize"] = fontsize
    mpl.rcParams["figure.labelsize"] = fontsize
    mpl.rcParams["axes.labelsize"] = fontsize
    mpl.rc('font', **font)
    mpl.rc('text', usetex=True)
    mpl.rc("text.latex", preamble=r"\usepackage{amsmath}")
    mpl.rc('savefig', dpi=300)
    mpl.rc('figure', dpi=100)
    cprint("LaTeX set up for generic single-page style, CM font.", "yellow", attrs=["bold"])
    cprint(f"Font size {fontsize} gives 9pt at scale = {9.0/fontsize}", "yellow", attrs=["bold"])


def annotate_axes(fig, ax, label, loc="upper left", xoffset=-2.5, yoffset=0.5):
    """
    Used for subplot annotation

    Args:
        fig: The figure that owns the Axes.
        ax: The Axes that will be annotated.
        label: The annotation label. Typically, something like (a), (b), etc.
        loc: Location. Must be one of "upper left", "upper right", "lower left", "lower right".
        xoffset: Additional horizontal offset. Given in units of mpl.rcParams["font.size"].
        yoffset: Additional vertical offset. Given in units of mpl.rcParams["font.size"].
    """

    # Parse location
    loc_split = loc.split(" ")
    invalid_loc_exception = ValueError('Location must be one of "upper left", "upper right", "lower left", "lower right"!')

    if len(loc_split) != 2:
        raise invalid_loc_exception

    if loc_split[0] == "upper":
        y = 1.0
    elif loc_split[0] == "lower":
        y = 0.0
    else:
        raise invalid_loc_exception

    if loc_split[1] == "left":
        x = 0.0
    elif loc_split[1] == "right":
        x = 1.0
    else:
        raise invalid_loc_exception

    xoffset *= mpl.rcParams["font.size"]
    yoffset *= mpl.rcParams["font.size"]

    ax.text(x, y, label,
            transform=ax.transAxes + ScaledTranslation(xoffset/72, yoffset/72, fig.dpi_scale_trans))
