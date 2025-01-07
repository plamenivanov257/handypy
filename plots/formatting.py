"""
Helps setup matplotlib for pretty plots.
"""
from termcolor import cprint
import matplotlib as mpl


def setup_generic_plots(fontsize=18, dpi=300):
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
    mpl.rc('savefig', dpi=dpi)
    mpl.rc('figure', dpi=dpi)
    cprint("LaTeX set up for generic single-page style, CM font.", "yellow", attrs=["bold"])
    cprint(f"Font size {fontsize} gives 9pt at scale = {9.0/fontsize}", "yellow", attrs=["bold"])


def setup_jpp_pgf_plots(fontsize=10, dpi=600):
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
    mpl.rc('font', **font)
    mpl.rc('text', usetex=True)
    mpl.rc("pgf", texsystem="pdflatex")
    mpl.rc("pgf", preamble=r"\usepackage{amsmath}\usepackage{newtxtext}\usepackage{newtxmath}")
    mpl.rc('savefig', dpi=dpi)
    mpl.rc('figure', dpi=dpi)
    cprint("LaTeX set up for JPP with the pgf backend.", "yellow", attrs=["bold"])
    cprint(f"Font size is {fontsize}", "yellow", attrs=["bold"])
