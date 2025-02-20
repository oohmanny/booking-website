from flask import Blueprint, request, jsonify
from .randomid import generatecode
from .sanitizer import *
import datetime
from models.Prenotazione import Prenotazione

prenotazioni_bp = Blueprint('prenotazioni', __name__)

#Lista la prenotazione in base al codice prenotazione
@prenotazioni_bp.route('/prenotazioni/<string:codice_prenotazione>', methods=['GET'])
def get_prenotazione(codice_prenotazione):
    prenotazione = Prenotazione.get_by_code(codice_prenotazione)
    if prenotazione is None:
        return jsonify({'error': 'Prenotazione non trovata. Controlla il codice prenotazione e riprova.',\
                        'messageType' : 'danger'}), 404

    # Se la prenotazione esiste, restituiscila
    return jsonify(dict(prenotazione.__dict__))



#Gestisce la creazione della prenotazione
@prenotazioni_bp.route('/prenotazioni', methods=["POST"])
def crea_prenotazione():
    data = request.json

    campiPrenotazione = {
        "nome_cliente": nameFormat(data.get('nome_cliente')),
        "email_cliente": emailFormat(data.get('email_cliente')),
        "numero_telefono": phoneFormat(data.get('numero_telefono')),
        "veicolo": vehicleFormat(data.get('veicolo')),
        "dataora_prenotazione": dateFormat(data.get('dataora_prenotazione')),
        "problema_descrizione": data.get('problema_descrizione')
    }
    
    #Se la prenotazione è incompleta o alcuni campi non rispettano le RegEx definite in Sanitizer, restituisce error
    for value in campiPrenotazione.values():
        if (value is None or value == ""):
            return jsonify({'error': 'Controlla i tuoi dati e riprova', 'messageType': 'danger'}), 400
    
    #Se la prenotazione è compilata in tutti i suoi campi, che rispettano le RegEx definite in Sanitizer, salva in DB
    prenotazione = Prenotazione(**campiPrenotazione)
    prenotazione.save()
    return jsonify({'message': 'Hai prenotato il tuo appuntamento con successo',
                    'messageType': 'success',
                    'bookingCode':prenotazione.codice_prenotazione}), 201



#Gestisce la cancellazione della prenotazione
@prenotazioni_bp.route('/prenotazioni/<string:codice_prenotazione>', methods=['DELETE'])
def delete_prenotazione(codice_prenotazione):

    prenotazione = Prenotazione.get_by_code(codice_prenotazione)

    # Verifica se esiste una prenotazione con quel codice e, in caso contrario, restituisce un errore
    if prenotazione is None:
        return jsonify({'error': 'Prenotazione non trovata. Controlla il codice prenotazione e riprova.',\
                        'messageType' : 'danger'}), 404

    # Se la prenotazione esiste
    else: 
        prenotazione.delete()
        return jsonify({'message': 'Prenotazione cancellata con successo.'}), 200


#Gestisce la modifica di una prenotazione in base al codice prenotazione
@prenotazioni_bp.route('/prenotazioni/<string:codice_prenotazione>', methods=['PUT'])
def modifica_prenotazione(codice_prenotazione):
    data = request.json
    prenotazione = Prenotazione.get_by_code(codice_prenotazione)

    #Se la prenotazione non esiste, restituisce error
    if prenotazione is None:
        return jsonify({'error': 'Prenotazione non trovata. Controlla il codice prenotazione e riprova.',
                'messageType': 'danger'}), 404

    campiPrenotazione = {
        "nome_cliente": nameFormat(data.get('nome_cliente')),
        "email_cliente": emailFormat(data.get('email_cliente')),
        "numero_telefono": phoneFormat(data.get('numero_telefono')),
        "veicolo": vehicleFormat(data.get('veicolo')),
        "dataora_prenotazione": dateFormat(data.get('dataora_prenotazione')),
        "problema_descrizione": data.get('problema_descrizione')
    }
    
    #Se la prenotazione è incompleta o i dati non rispettano le RegEx definite in Sanitizer, error
    for value in campiPrenotazione.values():
        if (value is None or value == ""):
            return jsonify({'error': 'Controlla i tuoi dati e riprova', 'messageType': 'danger'}), 400

    #Se la prenotazione è valida, salva in db 
    if prenotazione.stato_prenotazione != "Confermata":   
        prenotazione.update(**campiPrenotazione)
        return jsonify({'message': 'Hai modificato la tua prenotazione con successo',
                        'messageType': 'success'}), 201
    else:
        return jsonify({'message': 'Non puoi modificare una prenotazione confermata.',
                        'messageType': 'success'}), 201


@prenotazioni_bp.route('/prenotazioni/conferma/<string:codice_prenotazione>-<hash_value>')
def conferma_prenotazione(codice_prenotazione, hash_value):
    prenotazione = Prenotazione.get_by_code(codice_prenotazione)
    if prenotazione is None:
        return jsonify({'error': 'Prenotazione non trovata. Controlla il codice prenotazione e riprova.',
                'messageType': 'danger'}), 404
    else:
        if hash_value == Prenotazione.generate_hash(prenotazione.codice_prenotazione):
            if prenotazione.stato_prenotazione == "Da confermare":
                prenotazione.accept_appointment()
                return jsonify({'message': 'Hai confermato la tua prenotazione con successo.',
                            'messageType': 'success'}), 201
            else:
                return jsonify({'message': 'La tua prenotazione non e\' in attesa di conferma.',
                            'messageType': 'warning'}), 400
                
        else:
            return jsonify({'message': 'Il link utilizzato non e\' corretto.',
                        'messageType': 'danger',
                        'correctHash' : Prenotazione.generate_hash(prenotazione.codice_prenotazione)}), 400



