from flask import Blueprint, make_response, redirect, request, jsonify, session, render_template, url_for
from models.Prenotazione import Prenotazione
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.DatabaseManager import DatabaseManager
import hashlib
db = DatabaseManager()
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/prenotazioni', methods=['GET'])
@jwt_required(locations=["cookies"])
def get_prenotazioni():
    prenotazioni = Prenotazione.get_all()

    if prenotazioni is None:
        return jsonify({"message":"Nessuna prenotazione.", "messageType":"warning"}), 200
    
    prenotazioniDict = [dict(prenotazione.__dict__) for prenotazione in prenotazioni]
    return jsonify(prenotazioniDict), 200

@admin_bp.route('/prenotazioni/complete/<string:codice_prenotazione>', methods=['PATCH'])
@jwt_required(locations=["cookies"])
def complete_prenotazione(codice_prenotazione):
    prenotazione = Prenotazione.get_by_code(codice_prenotazione)

    if prenotazione is None:
        return jsonify({"message":"Nessuna prenotazione.", "messageType":"warning"}), 404

    prenotazione.complete()
    return jsonify("Prenotazione completata. Potrai ora consultarla nello storico."), 200

@admin_bp.route('/prenotazioni/fix_appointment/<string:codice_prenotazione>', methods=['PUT'])
@jwt_required(locations=["cookies"])
def fix_appointment(codice_prenotazione):
    prenotazione = Prenotazione.get_by_code(codice_prenotazione)

    if prenotazione is None:
        return jsonify({"message":"Nessuna prenotazione.", "messageType":"warning"}), 200
    
    data = request.json
    appuntamento = data.get("fixAppointment")
    if prenotazione.stato_prenotazione == "In attesa":
        prenotazione.propose_appointment(appuntamento)
        return jsonify("Proposta di appuntamento inviata, attendi una conferma."), 200
    else:
        return jsonify("La prenotazione non è più modificabile."), 400


@admin_bp.route('/prenotazioni/history')
@jwt_required(locations=["cookies"])
def get_bookings_history():
    storico = Prenotazione.get_history()

    if storico is None:
        return jsonify({"message":"Storico vuoto", "messageType":"warning"}), 200
    
    else:
        return storico
    
@admin_bp.route('/prenotazioni/history', methods=['DELETE'])
@jwt_required(locations=["cookies"])
def clear_bookings_history():
    storico = Prenotazione.get_history()

    if storico is None:
        return jsonify({"message":"Storico vuoto", "messageType":"warning"}), 404
    
    else:
        Prenotazione.clear_history()
        return jsonify({"message":"Hai cancellato lo storico.", "messageType":"warning"}), 200


@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required(locations=["cookies"])
def get_dashboard():
    return render_template('admindashboard.html')

@admin_bp.route('/history', methods=['GET'])
@jwt_required(locations=["cookies"])
def get_bookingshistory():
    return render_template('bookingshistory.html')

@admin_bp.route('/login', methods=['GET'])
def get_login():
    return render_template('adminlogin.html')

@admin_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("adminUsername")
    password = data.get("adminPassword")

    query = """SELECT * FROM admin WHERE username=?"""
    row = db.execute_query(query, (username,), fetchone=True)

    if row:
        admin = dict(**row)
        if admin.get('password') == hashlib.sha256(password.encode()).hexdigest():
            access_token = create_access_token(identity=username)
            # return jsonify(access_token=access_token)
            response = jsonify({"message": "Login effettuato con successo!"})
            response.set_cookie("access_token_cookie", access_token, httponly=True, secure=False, samesite="Lax")
            return response, 200

    return jsonify({"error": "Credenziali non valide"}), 401


@admin_bp.route('/logout')
def logout():
    response = make_response(redirect("/"))
    response.set_cookie("access_token_cookie", '', expires=0, httponly=True)

    return response