from datetime import datetime
import logging
from math import pi
import matplotlib
import matplotlib.pyplot as plt
import pathlib
from config import CHART_FILENAME, CHART_FILEPATH
matplotlib.use('Agg')


class Diagram:
    """
    Class for operations with perspective diagram.
    """

    def __init__(self, ticker):
        self.ticker = ticker
        self.checks = dict()

    def set_checks(self, checks):
        self.checks = checks

    @staticmethod
    def _get_color(score_):
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

    def exists(self):
        """
        Verifies if graph on this date exists already.
        :return: does this graph exist or not
        """

        fname = pathlib.Path(f"{CHART_FILEPATH}{self.ticker}{CHART_FILENAME}")
        if fname.exists():
            file_mtime = datetime.fromtimestamp(fname.stat().st_mtime)
            if file_mtime.day == datetime.now().day:
                return True
        return False

    def create_and_save_plot(self):
        """
        Create spider plot according to the company perspective checks.
        """

        fname = pathlib.Path(f"{CHART_FILEPATH}{self.ticker}{CHART_FILENAME}")
        # categories
        categories = self.checks.keys()
        axes_number = len(categories)

        values = [sum(dict_.values()) for dict_ in self.checks.values()]
        score = sum(values)
        color = self._get_color(score)
        values += values[:1]

        # angles for chart
        angles = [n / float(axes_number) * 2 * pi for n in range(axes_number)]
        angles += [2 * pi]

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
        plt.savefig(fname)
        logging.info(f"Graph {fname} created.")
        plt.clf()
