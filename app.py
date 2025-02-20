from flask import Flask, redirect, render_template, url_for, request
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message
from mail import mail
import os
import config
import runpy

app = Flask(__name__)

app.secret_key = os.urandom(24)

# FLASK-MAIL
app.config['MAIL_SERVER'] = 'smtp.libero.it'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'email@email.it'
app.config['MAIL_PASSWORD'] = 'password'
mail.init_app(app)

# JWT
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = "progettotesi2025"
jwt = JWTManager(app)

@jwt.expired_token_loader
def expired_token_callback(expired_token, second=''):
    return redirect("/admin/login")

@jwt.unauthorized_loader
def unauthorized_token_callback(error):
    return redirect("/admin/login")

#Blueprint registration
from routes.prenotazioni import prenotazioni_bp
from routes.admin import admin_bp
app.register_blueprint(prenotazioni_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/admin")

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/gestisci-prenotazione')
def cancellaprenotazione():
    return render_template('gestisciprenotazione.html')
@app.route('/prenota')
def prenota():
    return render_template('prenota.html')
@app.route('/servizi')
def mostraservizi():
    return render_template('services.html')
@app.route('/location')
def locationview():
    return  redirect(url_for('home') + '#location')

if __name__ == "__main__":
    runpy.run_path("config.py")
    app.run(debug=True, host='0.0.0.0', port=80)