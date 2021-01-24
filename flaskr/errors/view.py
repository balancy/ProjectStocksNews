from flask import Blueprint, render_template

blueprint = Blueprint('/errors', __name__)


@blueprint.app_errorhandler(404)
def page_not_found(e):
    """
    Handling page not found link.
    """
    return render_template('error.html', parameter=404), 404


@blueprint.app_errorhandler(408)
def page_timeout(e):
    """
    Handling page timeout error.
    """
    return render_template('error.html', parameter='timeout'), 408


@blueprint.app_errorhandler(ConnectionError)
def page_timeout(e):
    """
    Handling page connection error.
    """
    return render_template('error.html', parameter='connection')
