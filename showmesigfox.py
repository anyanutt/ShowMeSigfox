from sms_app import create_app
#from sms_app.models import User, Device, Dashboard, Variable, Message

app = create_app()

'''
@app.shell_context_processor
def make_shell_context():
    return {'User': User, 'Device': Device, 'Dashboard': Dashboard, 'Variable': Variable, 'Message': Message}
    '''