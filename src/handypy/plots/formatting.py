"""
Helps setup matplotlib for pretty plots.
"""
import os
import re
from termcolor import cprint
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.transforms import ScaledTranslation
from ..cli.cli_input import cli_input

FIGURES_PATH = "FIGURES_PATH"


def get_figures_path(short_filename : str):
    """
    This returns the full path to a figure to be saved.
    """

    if FIGURES_PATH in os.environ:
        return os.path.join(f"{os.environ[FIGURES_PATH]}", short_filename)

    # otherwise, return home
    if os.name == "posix":
        return os.path.join(f"{os.environ['HOME']}", short_filename)

    if os.name == "nt":
        return os.path.join(f"{os.environ['HOMEDRIVE']}{os.environ['HOMEPATH']}", short_filename)

    raise Exception("No clue how to figure out the FIGURES_PATH!")


def save_pdf(short_filename=None, default_filename="temp.pdf"):
    """
    Saves a pdf
    """

    if short_filename is not None:
        filename = get_figures_path(short_filename)
        cprint(f"Saving to {filename}.", color="yellow")
        plt.savefig(filename)

    if default_filename is not None:
        filename = get_figures_path(default_filename)
        cprint(f"Saving to {filename}.", color="yellow")
        plt.savefig(filename)


def setup_generic_plots(fontsize=18, usetex=True, figsize=None, layout=None):
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
    mpl.rc('text', usetex=usetex)
    mpl.rc("text.latex", preamble=r"\usepackage{amsmath}")
    mpl.rc('savefig', dpi=300)
    mpl.rc('figure', dpi=100)
    cprint("LaTeX set up for generic single-page style, CM font.", "yellow", attrs=["bold"])
    cprint(f"Font size {fontsize} gives 9pt at scale = {9.0/fontsize}", "yellow", attrs=["bold"])

    return plt.figure(figsize=figsize, layout=layout)


def setup_jpp_pgf_plots(fontsize=9, dpi=600, majorwidth=0.6, minorwidth=0.5, linewidth=0.8, figsize=(5, 3), layout=None, times_font=True):
    """
    Sets up matplotlib for JPP plots
    using the pgf backend.
    """
    font = {'family' : 'serif',
            'weight' : 'normal',
            'size'   : fontsize}

    mpl.use("pgf")
    mpl.rcParams["figure.titlesize"] = fontsize
    mpl.rcParams["axes.titlesize"] = fontsize
    mpl.rcParams["figure.labelsize"] = fontsize
    mpl.rcParams["axes.labelsize"] = fontsize

    mpl.rcParams["lines.linewidth"] = linewidth

    mpl.rcParams["axes.linewidth"] = majorwidth
    mpl.rcParams["xtick.major.width"] = majorwidth
    mpl.rcParams["ytick.major.width"] = majorwidth

    mpl.rcParams["xtick.minor.width"] = minorwidth
    mpl.rcParams["ytick.minor.width"] = minorwidth

    mpl.rc('font', **font)
    mpl.rc('text', usetex=True)
    mpl.rc("pgf", texsystem="pdflatex")
    if times_font:
        mpl.rc("pgf", preamble=r"\usepackage{amsmath}\usepackage{newtxtext}\usepackage{newtxmath}")
    else:
        mpl.rc("pgf", preamble=r"\usepackage{amsmath}")
    mpl.rc('savefig', dpi=dpi)
    mpl.rc('figure', dpi=dpi)
    cprint("LaTeX set up for JPP with the pgf backend.", "yellow", attrs=["bold"])
    cprint(f"Font size is {fontsize}", "yellow", attrs=["bold"])

    return plt.figure(figsize=figsize, layout=layout)


def setup_aps_pgf_plots(fontsize=8, dpi=600, majorwidth=0.6, minorwidth=0.5, linewidth=0.8, figsize=(3.4, 2.1), layout=None):
    """
    Sets up matplotlib for APS plots
    using the pdf backend.
    """
    font = {'family' : 'serif',
            'weight' : 'normal',
            'size'   : fontsize}

    mpl.use("pgf")
    mpl.rcParams["axes.titlesize"] = fontsize
    mpl.rcParams["axes.labelsize"] = fontsize
    mpl.rcParams["figure.titlesize"] = fontsize
    mpl.rcParams["figure.labelsize"] = fontsize

    # Slighly smaller ticks to save space
    mpl.rcParams["xtick.labelsize"] = fontsize - 1
    mpl.rcParams["ytick.labelsize"] = fontsize - 1
    mpl.rcParams["legend.fontsize"] = fontsize - 1


    mpl.rcParams["lines.linewidth"] = linewidth

    mpl.rcParams["axes.linewidth"] = majorwidth
    mpl.rcParams["xtick.major.width"] = majorwidth
    mpl.rcParams["ytick.major.width"] = majorwidth

    mpl.rcParams["xtick.minor.width"] = minorwidth
    mpl.rcParams["ytick.minor.width"] = minorwidth

    mpl.rc('font', **font)
    mpl.rc('text', usetex=True)
    mpl.rc("pgf", texsystem="pdflatex")
    mpl.rc('text.latex', preamble=r"\usepackage{amsmath}\usepackage{amssymb}")
    mpl.rc('pgf', preamble=r"\usepackage{amsmath}\usepackage{amssymb}")
    mpl.rc('savefig', dpi=dpi)
    mpl.rc('figure', dpi=dpi)
    cprint("LaTeX set up for APS with the PDF backend.", "yellow", attrs=["bold"])
    cprint(f"Font size is {fontsize}", "yellow", attrs=["bold"])

    return plt.figure(figsize=figsize, layout=layout)

def save_pgf(short_filename, clean_fontsize=True):
    """
    Saves a pgf and optionally clean fontsize calls inside it.
    """
    filename = get_figures_path(short_filename)

    plt.savefig(filename)
    cprint(f"Saved {filename}.", "yellow")

    if clean_fontsize:
        clean_pgf_fontsize(filename)


def clean_pgf_fontsize(filename):
    """
    Removes all \fontsize{}{} calls inside a pgf file.
    """
    with open(filename, encoding="utf-8") as file:
        filestr = file.read()

    filestr = re.sub(r"\\fontsize\{([+-]?\d*\.?\d*)\}\{([+-]?\d*\.?\d*)\}", "", filestr)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(filestr)

    cprint(f"Cleaned {filename}.", "yellow", attrs=["bold"])


def annotate_axes(fig, ax, label, loc="upper left", xoffset=-2, yoffset=1, **kwargs):
    """
    Used for subplot annotation

    Args:
        fig: The figure that owns the Axes.
        ax: The Axes that will be annotated.
        label: The annotation label. Typically, something like (a), (b), etc.
        loc: Location. Must be one of "upper left", "upper right", "lower left", "lower right".
        xoffset: Additional horizontal offset. Given in units of mpl.rcParams["font.size"].
        yoffset: Additional vertical offset. Given in units of mpl.rcParams["font.size"].
        **kwargs: All other names arguments are passed to pyplot's Axes.text function.
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

    if "fontsize" not in kwargs:
        fontsize = mpl.rcParams["font.size"]
    else: fontsize = kwargs["fontsize"]

    xoffset *= fontsize
    yoffset *= fontsize

    ax.text(x, y, label,
            transform=ax.transAxes + ScaledTranslation(xoffset/72, yoffset/72, fig.dpi_scale_trans), **kwargs)

def adjust_axes_properties_cli(ax, ax_name):
    print(f"Adjusting properties of axes {ax_name}")
    
    # Axes scale
    print(f"Current axes (x, y) scale is ({ax.get_xscale()}, {ax.get_yscale})")
    ax.set_xscale(cli_input("x scale = ", dtype=str, default=ax.get_xscale()))
    ax.set_yscale(cli_input("y scale = ", dtype=str, default=ax.get_yscale()))

    # x lim
    lim = np.zeros(2)
    lim[:] = ax.get_xlim()[:]

    print(f"xlim is {lim}")
    lim[0] = cli_input("xlim left = ", dtype=str, default=lim[0])
    lim[1] = cli_input("xlim right = ", dtype=str, default=lim[1])

    ax.set_xlim(lim)
    
    # y lim
    lim = np.zeros(2)
    lim[:] = ax.get_ylim()[:]

    print(f"ylim is {lim}")
    lim[0] = cli_input("ylim left = ", dtype=str, default=lim[0])
    lim[1] = cli_input("ylim right = ", dtype=str, default=lim[1])

    ax.set_ylim(lim)
