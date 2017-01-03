from flask import render_template, redirect, request
from flask_login import login_required, logout_user

from social_flask.utils import load_strategy

from example import app


@app.route('/')
def main():
    return render_template('home.html')


@app.route('/done/')
@login_required
def done():
    return render_template('home.html')


@app.route('/email')
def require_email():
    strategy = load_strategy()
    partial_token = request.args.get('partial_token')
    partial = strategy.partial_load(partial_token)
    return render_template('home.html',
                           email_required=True,
                           partial_backend_name=partial.backend,
                           partial_token=partial_token)


@app.route('/logout/')
@login_required
def logout():
    """Logout view"""
    logout_user()
    return redirect('/')
