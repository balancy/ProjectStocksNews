from datetime import datetime
import logging
from math import pi
import matplotlib
import matplotlib.pyplot as plt
import pathlib
from config import CHART_FILENAME, CHART_FILEPATH
matplotlib.use('Agg')


def is_graph_exists(complete_filename):
    """
    Verifies if graph on this date exists already.
    :param complete_filename: path to the graph
    :return: does this graph exist or not
    """

    fname = pathlib.Path(complete_filename)
    if fname.exists():
        file_mtime = datetime.fromtimestamp(fname.stat().st_mtime)
        now = datetime.now()
        if file_mtime.day == now.day:
            return True
    return False


def get_color(score_):
    """
    Get color according to score.
    :param score_: company perspective score
    :return: color
    """

    if score_ < 5:
        return 'red'
    elif score_ < 10:
        return '#FF4500'
    elif score_ < 15:
        return 'orange'
    elif score_ < 20:
        return 'yellow'
    elif score_ < 25:
        return '#ADFF2F'
    else:
        return 'green'


def create_and_save_plot(coefficients, complete_filename) -> None:
    """
    Create spider plot according to the company perspective checks.
    :param coefficients: perspective checks
    :param complete_filename: path to the graph
    """

    # categories
    categories = coefficients.keys()
    axes_number = len(categories)

    values = [sum(dict_.values()) for dict_ in coefficients.values()]
    score = sum(values)
    color = get_color(score)
    values += values[:1]

    # angles for chart
    angles = [n / float(axes_number) * 2 * pi for n in range(axes_number)]
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
    plt.savefig(complete_filename)
    logging.info(f"Graph {complete_filename} created.")
    plt.clf()


def check_perspective_chart(ticker, coefficients) -> None:
    """
    If chart doesn't exist, we create and save it.
    :param ticker: stocks ticker
    :param coefficients: company perspective checks
    """

    complete_filename = f"{CHART_FILEPATH}{ticker}{CHART_FILENAME}"
    if not is_graph_exists(complete_filename):
        create_and_save_plot(coefficients, complete_filename)

