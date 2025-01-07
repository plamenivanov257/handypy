"""
Helps setup matplotlib for pretty plots.
"""
import os
from termcolor import cprint
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.transforms import ScaledTranslation

PGF_PDF_LOCATION = "PGF_PDF_LOCATION"


def get_pgf_pdf_location():
    """
    When using pgf, we can save to a pdf somewhere
    to see what the pgf actually contains.
    """
    if PGF_PDF_LOCATION in os.environ:
        return os.environ[PGF_PDF_LOCATION]

    # otherwise, return generic file in home
    if os.name == "posix":
        return f"{os.environ['HOME']}/temp.pdf"

    if os.name == "nt":
        return f"{os.environ['HOMEDRIVE']}{os.environ['HOMEPATH']}\\temp.pdf"

    raise Exception("No clue where to save temp.pdf!")


def save_pdf():
    """
    Saves a debug pdf when using pgf.
    """
    plt.savefig(get_pgf_pdf_location())


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


def setup_jpp_pgf_plots(fontsize=9, dpi=600, majorwidth=0.6, minorwidth=0.5, figsize=(5, 3), layout=None):
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

    mpl.rcParams["axes.linewidth"] = majorwidth
    mpl.rcParams["xtick.major.width"] = majorwidth
    mpl.rcParams["ytick.major.width"] = majorwidth

    mpl.rcParams["xtick.minor.width"] = minorwidth
    mpl.rcParams["ytick.minor.width"] = minorwidth

    mpl.rc('font', **font)
    mpl.rc('text', usetex=True)
    mpl.rc("pgf", texsystem="pdflatex")
    mpl.rc("pgf", preamble=r"\usepackage{amsmath}\usepackage{newtxtext}\usepackage{newtxmath}")
    mpl.rc('savefig', dpi=dpi)
    mpl.rc('figure', dpi=dpi)
    cprint("LaTeX set up for JPP with the pgf backend.", "yellow", attrs=["bold"])
    cprint(f"Font size is {fontsize}", "yellow", attrs=["bold"])

    return plt.figure(figsize=figsize, layout=layout)


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
