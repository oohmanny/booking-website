from flask import url_for
from .DatabaseManager import DatabaseManager
import random, string
import datetime
import hmac, hashlib, base64
from flask_mail import Message, Mail
from mail import invia_mail


db = DatabaseManager()
SECRET_KEY = "prenotazioni2025"

class Prenotazione:

    
    def __init__(self, id=None, stato_prenotazione="", nome_cliente="", email_cliente="", numero_telefono="", veicolo="", dataora_prenotazione="",
                 problema_descrizione="", codice_prenotazione="", data_invio=""):
        self.id = id
        self.stato_prenotazione = stato_prenotazione
        self.nome_cliente = nome_cliente
        self.email_cliente = email_cliente
        self.numero_telefono= numero_telefono
        self.veicolo = veicolo
        self.dataora_prenotazione = dataora_prenotazione
        self.problema_descrizione = problema_descrizione
        self.codice_prenotazione = codice_prenotazione
        self.data_invio = data_invio


    @staticmethod
    def get_by_code(codice_prenotazione):
        #Recupera la prenotazione dal DB
        query = "SELECT * FROM prenotazioni WHERE codice_prenotazione = ?"
        row = db.execute_query(query, (codice_prenotazione,), fetchone=True)
        if not row:
            return None
        return Prenotazione(**row)
    
    
    @staticmethod
    def get_all():
        #Recupera tutte le prenotazioni dal DB
        query = "SELECT * FROM prenotazioni"
        rows = db.execute_query(query)
        if not rows:
            return None
        return [Prenotazione(**row) for row in rows]

    
    def save(self):
        #Salva una nuova prenotazione o ne aggiorna una già esistente
        if self.id:
            query = """UPDATE prenotazioni SET stato_prenotazione=?, nome_cliente=?, email_cliente=?, numero_telefono=?, veicolo=?, dataora_prenotazione=?,
                        problema_descrizione=? WHERE id=?"""
            params= ("In Attesa", self.nome_cliente, self.email_cliente, self.numero_telefono, self.veicolo, self.dataora_prenotazione,
                     self.problema_descrizione, self.id)
            invia_mail("Prenotazione Modificata", self.email_cliente, "mail_modificaprenotazione.html", self.__dict__)
            
            
        else:
            dataInvio = datetime.datetime.now()
            dataInvio = datetime.datetime.strftime(dataInvio, "%Y-%m-%d %H:%M")
            self.codice_prenotazione = Prenotazione.__generatecode()
            query = """INSERT INTO prenotazioni (stato_prenotazione, nome_cliente, numero_telefono, email_cliente, veicolo, dataora_prenotazione,
                        problema_descrizione, data_invio, codice_prenotazione) VALUES (?,?,?,?,?,?,?,?,?)"""
            params = ("In attesa", self.nome_cliente, self.numero_telefono, self.email_cliente, self.veicolo, self.dataora_prenotazione,
                      self.problema_descrizione, dataInvio, self.codice_prenotazione)
            invia_mail("Riepilogo Prenotazione", self.email_cliente, "mail_invioprenotazione.html", self.__dict__)
        
        db.execute_query(query, params, commit=True)



    def update(self, nome_cliente="", email_cliente="", numero_telefono="", veicolo="", dataora_prenotazione="",
                problema_descrizione=""):
        self.nome_cliente = nome_cliente
        self.email_cliente = email_cliente
        self.numero_telefono= numero_telefono
        self.veicolo = veicolo
        self.dataora_prenotazione = dataora_prenotazione
        self.problema_descrizione = problema_descrizione
        self.save()

    def delete(self):
        #Cancella la prenotazione dal database
        if self.id:
            datacompletamento = datetime.datetime.now()
            datacompletamento = datetime.datetime.strftime(datacompletamento, "%Y-%m-%d %H:%M")
            query = "DELETE FROM prenotazioni WHERE id = ?"
            db.execute_query(query, (self.id,), commit=True)

            query = """INSERT INTO storico (nome_cliente, email_cliente, numero_telefono, veicolo,
                        problema_descrizione, stato_prenotazione, dataora_prenotazione, data_completamento) VALUES (?,?,?,?,?,?,?,?)"""
            params = (self.nome_cliente, self.email_cliente, self.numero_telefono, self.veicolo,
                      self.problema_descrizione, "Cancellato", self.dataora_prenotazione, datacompletamento)
            db.execute_query(query, params, commit=True)

            invia_mail("Prenotazione Cancellata", self.email_cliente, "mail_cancellaprenotazione.html", self.__dict__)

    def complete(self):
        if self.id:
            datacompletamento = datetime.datetime.now()
            datacompletamento = datetime.datetime.strftime(datacompletamento, "%Y-%m-%d %H:%M")
            query = "DELETE FROM prenotazioni WHERE id = ?"
            db.execute_query(query, (self.id,), commit=True)

            query = """INSERT INTO storico (nome_cliente, email_cliente, numero_telefono, veicolo,
                        problema_descrizione, stato_prenotazione, dataora_prenotazione, data_completamento) VALUES (?,?,?,?,?,?,?,?)"""
            params = (self.nome_cliente, self.email_cliente, self.numero_telefono, self.veicolo,
                      self.problema_descrizione, "Completato", self.dataora_prenotazione, datacompletamento)
            db.execute_query(query, params, commit=True)
            invia_mail("Prenotazione Completata", self.email_cliente, "mail_completaprenotazione.html", self.__dict__)

    def propose_appointment(self, dataora_appuntamento=""):
        if self.stato_prenotazione == "In attesa":
            if dataora_appuntamento == self.dataora_prenotazione:
                query = "UPDATE prenotazioni SET stato_prenotazione=? WHERE id=?"
                params = ("Confermato", self.id)
                db.execute_query(query, params, commit=True)
                invia_mail("Prenotazione Confermata", self.email_cliente, "mail_prenotazioneconfermata.html", self.__dict__)

            else:
                query = "UPDATE prenotazioni SET stato_prenotazione=?, dataora_prenotazione=? WHERE id=?"
                params = ("Da confermare", dataora_appuntamento, self.id)
                db.execute_query(query, params, commit=True)
                self.dataora_prenotazione = dataora_appuntamento
                invia_mail("PROPOSTA APPUNTAMENTO", self.email_cliente, "mail_propostaprenotazione.html", self.__dict__, link="localhost/api/prenotazioni/conferma/"+self.codice_prenotazione+"-"+ Prenotazione.generate_hash(self.codice_prenotazione))

    def accept_appointment(self):
        if self.stato_prenotazione == "Da confermare":
            query = "UPDATE prenotazioni SET stato_prenotazione=? WHERE id=?"
            params = ("Confermato", self.id)
            db.execute_query(query, params, commit=True)
            invia_mail("["+self.codice_prenotazione + "] CONFERMATO", "mannybrr@libero.it", "mail_proposta_accettata.html", self.__dict__)

    
    
    @staticmethod
    def get_history():
        query = "SELECT * FROM storico ORDER BY data_completamento DESC"
        rows = db.execute_query(query)
        if not rows:
            return None
        else:
            return[dict(row) for row in rows]
            


    @staticmethod
    def clear_history():
        query = "DELETE FROM storico"
        db.execute_query(query, commit=True)



    @staticmethod
    def __generatecode(length=8):
        characters = string.ascii_letters + string.digits
        randomcode = ''.join(random.choices(characters, k=length))
        return randomcode.upper()
    
    @staticmethod
    def generate_hash(codice_prenotazione):
        return hmac.new(SECRET_KEY.encode(), codice_prenotazione.encode(), hashlib.sha256).hexdigest()