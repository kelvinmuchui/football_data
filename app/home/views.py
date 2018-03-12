from flask import abort, render_template

from flask_login import current_user ,login_required

from . import home
from ..models import Record
from forms import RecordForm


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """

    return render_template('index.html', title = "Welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """

    return render_template('home/dashboard.html', title = "Dashboard")
##--------------------------------------------------------------------------------
#### Records route
##--------------------------------------------------------------------------------
@home.route('/record', methods=['GET', 'POST'])
@login_required
def add_record():

    add_department = True

    form = RecordForm()
    if form.validate_on_submit():
        record = Record(name=form.name.data,
                            day = form.day.data,
                            production= form.production.data,
                            opening = form.opening.data,
                            closing = form.closing.data
                            )
        try:
            # add department to the database
            db.session.add(record)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('home/record.html', action="Add",
                           add_record=add_record, form=form,
                           title="Add Record")




@home.route('/records',  methods=['GET', 'POST'])
@login_required
def records():
    """
    List all departments
    """

    records = Record.query.all()

    return render_template('home/records.html',
                           records=records, title="Records")

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    #prevent non_admins from accessing the page
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html')
