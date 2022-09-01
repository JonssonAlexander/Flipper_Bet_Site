from app import app, db

from app.models import User
# export FLASK_APP=flipper_betting.py

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User}

#if __name__ == '__main__':  app.run(debug=True, host='127.0.0.1', port='5000')
