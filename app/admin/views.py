
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import TeamForm,PlayerForm, PlayerAssignForm
from .. import db
from ..models import Team, Player, User

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Department Views

@admin.route('/teams', methods=['GET', 'POST'])
@login_required
def list_teams():
    """
    List all teams
    """
    check_admin()

    teams = Team.query.all()

    return render_template('admin/teams/teams.html',
                           teams=teams, title="Teams")

@admin.route('/teams/add', methods=['GET', 'POST'])
@login_required
def add_team():
    """
    Add a team to the database
    """
    check_admin()

    add_team = True

    form = TeamForm()
    if form.validate_on_submit():
        team = Team(name=form.name.data,
                                history=form.history.data)
        try:
            # add department to the database
            db.session.add(team)
            db.session.commit()
            flash('You have successfully added a new team.')
        except:
            # in case department name already exists
            flash('Error: team name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_teams'))

    # load department template
    return render_template('admin/teams/team.html', action="Add",
                           add_team=add_team, form=form,
                           title="Add Team")

@admin.route('/teams/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_team(id):
    """
    Edit a team
    """
    check_admin()

    add_team = False

    team = Team.query.get_or_404(id)
    form = TeamForm(obj=team)
    if form.validate_on_submit():
        team.name = form.name.data
        team.history = form.history.data
        db.session.commit()
        flash('You have successfully edited the team.')

        # redirect to the departments page
        return redirect(url_for('admin.list_teams'))

    form.history.data = team.history
    form.name.data = team.name
    return render_template('admin/teams/team.html', action="Edit",
                           add_team=add_team, form=form,
                           team=team, title="Edit Team")




# @admin.route('/players')
# @login_required
# def list_players():
#     check_admin()
#     """
#     List all players
#     """
#     players = Player.query.all()
#     return render_template('admin/players/players.html',
#                            players=players, title='Players')

@admin.route('/players/add', methods=['GET', 'POST'])
@login_required
def add_player():
    """
    Add a player to the database
    """
    check_admin()

    add_player = True

    form = PlayerForm()
    if form.validate_on_submit():
        player = Player(email=form.email.data,
                        username=form.username.data,
                        last_name=form.last_name.data,
                        first_name=form.first_name.data)

        try:
            # add player to the database
            db.session.add(player)
            db.session.commit()
            flash('You have successfully added a new player.')
        except:
            # in case player name already exists
            flash('Error: role name already exists.')

        # redirect to the players page
        return redirect(url_for('admin.list_players'))

    # load player template
    return render_template('admin/players/player.html', add_player=add_player,
                           form=form, title='Add player')

@admin.route('/players/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_player(id):
    """
    Edit a player
    """
    check_admin()

    add_player = False

    player = Player.query.get_or_404(id)
    form = PrayerForm(obj=player)
    if form.validate_on_submit():
        player.email = form.email.data
        player.username = form.username.data
        player.first_name = form.first_name.data
        player.last_name = form.last_name.data
        db.session.add(player)
        db.session.commit()
        flash('You have successfully edited the player.')

        # redirect to the players page
        return redirect(url_for('admin.list_players'))

    form.email.data = player.email
    form.username.data = player.username
    form.first_name.data = player.first_name
    form.last_name.data = player.last_name
    return render_template('admin/players/player.html', add_player=add_player,
                           form=form, title="Edit Player")

@admin.route('/players/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_player(id):
    """
    Delete a player from the database
    """
    check_admin()

    player = Player.query.get_or_404(id)
    db.session.delete(player)
    db.session.commit()
    flash('You have successfully deleted the player.')

    # redirect to the roles page
    return redirect(url_for('admin.list_players'))

    return render_template(title="Delete player")

@admin.route('/teams/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_team(id):
    """
    Delete a team from the database
    """
    check_admin()

    team = Team.query.get_or_404(id)
    db.session.delete(team)
    db.session.commit()
    flash('You have successfully deleted the team.')

    # redirect to the departments page
    return redirect(url_for('admin.list_teams'))

    return render_template(title="Delete Team")
# players Views

@admin.route('/players')
@login_required
def list_players():
    """
    List all players
    """
    check_admin()

    players = Player.query.all()
    return render_template('admin/players/players.html',
                           players=players, title='Players')
@admin.route('/users')
@login_required
def users():
    '''
    list of all users
    '''

    check_admin()
    users = User.query.all()

    return render_template('admin/users/users.html',
                                users = users, title = 'User')
@admin.route('/players/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_player(id):
    """
    Assign a player  to a team
    """
    check_admin()

    player = Player.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    # if user.is_admin:
    #     abort(403)

    form = PlayerAssignForm(obj=player)
    if form.validate_on_submit():
        player.team = form.team.data
        db.session.add(player)
        db.session.commit()
        flash('You have successfully assigned a team')

        # redirect to the roles page
        return redirect(url_for('admin.list_players'))

    return render_template('admin/players/player.html',
                           player=player, form=form,
                           title='Assign Player')
