from flask import abort, render_template

from flask_login import current_user ,login_required

from . import home
from ..models import Team, Player
#............................................................
#home route
#............................................................
@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """

    return render_template('home/index.html', title = "Welcome")
#.......................................................................
#dashboard route
#...................................................................
@home.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
        # """
        # List all teams
        # """
        #
        # teams = Team.query.all()

        return render_template('home/dashboard.html')
#.................................................................
#teams route
#.................................................................

@home.route('/teams', methods = ['GET', 'POST'])
@login_required
def teams():
    """
    List all teams
    """

    teams = Team.query.all()

    return render_template('home/teams/teams.html',
                                teams = teams, titles = "Teams")
#.................................................................
#admin dashboard
#..................................................................
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    #prevent non_admins from accessing the page
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html')

#......................................................................
#team route
#.....................................................................
@home.route('/team/<int:id>', methods = ['GET', 'POST'])
@login_required
def team_details(id):
    """
    List details of a team
    """
    team = Team.query.get_or_404(id)

    return render_template ('home/teams/team.html', team = team)

@home.route('/player/<int:id>', methods = ['GET', 'POST'])
@login_required
def player_details(id):
    """
    List details of a player
    """
    player = Player.query.get_or_404(id)

    return render_template ('home/players/player.html', player = player)
