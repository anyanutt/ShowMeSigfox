import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from sms_app.main import bp
from sms_app.main.forms import NewDashboardForm, NewDeviceForm, NewVariableForm, NewWidgetForm

from sms_app.models import User, Device, Message, Variable, Dashboard
from sms_app.functions import timeToStr, sortTimeAsc, sortTimeDec
from sms_app.decorators import check_confirmed

@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.devices'))
    return render_template('home.html')

@bp.route('/devices')
@login_required
@check_confirmed
def devices():
    uid = str(User.collection.find_one({ 'email' : current_user.email })['_id'])
    devices = Device.get_list_by_uid(uid)
    return render_template('devices.html', title='Devices', devices=devices)

@bp.route('/devices/new', methods=['GET', 'POST'])
@login_required
@check_confirmed
def add_device():
    uid = str(User.collection.find_one({ 'email' : current_user.email })['_id'])
    form = NewDeviceForm()
    if form.validate_on_submit():
        if Device.register(sigfox_id=form.sigfox_id.data.upper(), dev_name=form.dev_name.data, user_id=uid):
            flash('New device registered: {} ({})'.format(form.dev_name.data, form.sigfox_id.data.upper()), 'success')
            return redirect(url_for('main.devices'))
    return render_template('modals/newdev.html', title='New Device', form=form)

@bp.route('/devices/delete/<_id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def delete_device(_id):
    if Device.remove(_id):
        flash('Device deleted', 'success')
    return redirect(url_for('main.devices'))

@bp.route('/devices/<_id>')
@login_required
@check_confirmed
def device_idv(_id):
    device = Device.get_by_id(_id)
    messages = sortTimeDec(Message.get_list_by_id(device['sigfox_id']))
    fields = Message.get_fields(device['sigfox_id'])
    variables = Variable.get_list_by_oid(_id)
    return render_template('dev_idv.html', title=device['sigfox_id'], device=device, messages=messages, fields=fields, variables=variables)

@bp.route('/variables/new', methods=['GET', 'POST'])
@login_required
@check_confirmed
def add_variable():
    dev_id = request.args.get('dev_id')
    keys = Message.get_fields(dev_id)
    form = NewVariableForm()
    form.source.choices = list(zip(keys,keys))
    if form.validate_on_submit():
        if Variable.register(var_name=form.var_name.data, dev_id=dev_id):
            flash('New variable created: {}'.format(form.var_name.data), 'success')
            return redirect(url_for('main.device_idv', _id=dev_id))
    return render_template('modals/newvar.html', title='New Variable', form=form)

@bp.route('/variables/<_id>')
@login_required
@check_confirmed
def variable(_id):
    variable = Variable.get_by_id(_id)
    dev_name = Device.get_by_id(variable['dev_id'])['dev_name']
    return render_template('variable.html', title=variable['var_name'], dev_name=dev_name ,variable=variable)

@bp.route('/variables/delete/<_id>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def delete_variable(_id):
    Variable.delete_variable(_id)
    flash('Variable deleted', 'success')
    return redirect(url_for('main.devices'))

@bp.route('/dashboard')
@login_required
@check_confirmed
def dashboard():
    return render_template('dashboard.html', title='Dashboard', widgets="")

@bp.route('/dashboard/addwidget', methods=['GET', 'POST'])
@login_required
@check_confirmed
def add_widget():
    '''
    uid = str(User.collection.find_one({ 'email' : current_user.email })['_id'])
    form = NewDashboardForm()
    if form.validate_on_submit():
        if Dashboard.register(dash_name=form.dash_name.data, user_id=uid):
            flash('New Dashboard Created: {}'.format(form.dash_name.data), 'success')
            return redirect(url_for('main.dashboard'))
    '''
    return render_template('modals/addwidget.html', title='Add Widget', dashboard='My dashboard')

@bp.route('/dashboard/addwidgets', methods=['GET', 'POST'])
@login_required
@check_confirmed
def add_widget2():
    form = NewWidgetForm()
    if form.validate_on_submit():
        return redirect(url_for('main.dashboards'))
    return render_template('modals/addwidget2.html', title='Add Widget', dashboard='My dashboard', form=form)

@bp.route('/dashboards')
@login_required
@check_confirmed
def dashboards():
    device = Device.get_by_id('60d06784d52faa9b9ff9962d')
    messages = sortTimeDec(Message.get_list_by_id(device['sigfox_id']))
    values = []
    values2 = []
    dates = []
    count = 0
    for i in messages:
        data = i['data'][0:7]
        data2 = i['data'][16:23]
        values.append(int('0x' + data, 0) / 1000000)
        values2.append(int('0x' + data2, 0) / 1000000)
        dates.append(i['time'])
        count = count + 1
        if count > 10:
            break

    values.reverse()
    values2.reverse()
    dates.reverse()

    return render_template('dashboards.html', title='Dashboard', widgets="", values=values, values2=values2, dates=dates)

@bp.route('/dashboards/new', methods=['GET', 'POST'])
@login_required
@check_confirmed
def add_dashboard():
    uid = str(User.collection.find_one({ 'email' : current_user.email })['_id'])
    form = NewDashboardForm()
    if form.validate_on_submit():
        if Dashboard.register(dash_name=form.dash_name.data, user_id=uid):
            flash('New Dashboard Created: {}'.format(form.dash_name.data), 'success')
            return redirect(url_for('main.dashboard'))
    return render_template('modals/newdash.html', title='New Dashboard', form=form)

@bp.route('/account')
@login_required
def account():
    return render_template('account.html')

@bp.route('/account/delete')
@login_required
def delete_account():
    _id = User.collection.find_one({ 'email' : current_user.email })['_id']
    if User.remove(_id):
        flash('Account deleted', 'success')
    return redirect(url_for('auth.logout'))
