from flask import abort, render_template

from flask_login import current_user ,login_required

from . import home
from ..models import Team, Player

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """

    return render_template('home/index.html', title = "Welcome")

@home.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
        """
        List all teams
        """

        teams = Team.query.all()

        return render_template('home/dashboard.html',
                               teams=teams, title="Teams")

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """"
    Rendert the admin dashdoard
    """
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html', title = "Dashboard")
@home.route('/teams', methods=['GET', 'POST'])
@login_required
def list_teams():
    """
    List all teams
    """

    teams = Team.query.all()

    return render_template('home/dashdoard.html',
                           teams=teams, title="Teams")
