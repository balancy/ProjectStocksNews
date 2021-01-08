from datetime import datetime
from math import pi
import matplotlib
import matplotlib.pyplot as plt
import pathlib
from flaskr.tickers.calculate_diagram_coefficients import get_coefficients
matplotlib.use('Agg')

RED = 'red'
ORANGE = 'orange'
YELLOW = 'yellow'
GREEN = 'green'

FILEPATH = "flaskr/graphs/"
FILENAME = "_chart_perspective.png"


def is_graph_exists(complete_filename):
    """Verifies if graph on this date exists already
    """

    fname = pathlib.Path(complete_filename)
    if fname.exists():
        file_mtime = datetime.fromtimestamp(fname.stat().st_mtime)
        now = datetime.now()
        if file_mtime.day == now.day:
            return True
    return False


def get_color(score_):
    """Get color according to score
    """

    if score_ < 10:
        return RED
    elif score_ < 16:
        return ORANGE
    elif score_ < 23:
        return YELLOW
    else:
        return GREEN


def create_and_save_plot(ticker):
    """Create spider plot according to coefficients calculated on the basis of ticker fundamentals
    """

    # Set data
    df = get_coefficients(ticker)

    # categories
    categories = df.keys()
    N = len(categories)

    values = list(df.values())
    score = sum(values)
    color = get_color(score)
    values += values[:1]

    # angles for chart
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += [2*pi]

    # Initialise the spider plot
    plt.polar(angles, values, color=color, linewidth=1)

    # Draw one axe per variable + add labels labels
    plt.xticks(angles[:-1], categories, color='grey', size=10)
    plt.tick_params(axis='x', which='major', pad=10)

    # Draw y-labels
    plt.yticks([1, 2, 3, 4, 5], color="lightgrey", size=7)
    plt.ylim(0, 6)

    # Fill area
    plt.fill(angles, values, color=color, alpha=0.5)

    # Saving picture
    complete_filename = f"{FILEPATH}{ticker}{FILENAME}"
    plt.savefig(complete_filename)
    plt.clf()


def create_chart_perspective(ticker):
    """If chart doesn't exist, we create and save it
    """

    complete_filename = f"{FILEPATH}{ticker}{FILENAME}"
    if not is_graph_exists(complete_filename):
        create_and_save_plot(ticker)

