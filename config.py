import hashlib
from models.DatabaseManager import DatabaseManager

db = DatabaseManager()

def init_tablePrenotazioni():
    query = '''
        CREATE TABLE IF NOT EXISTS prenotazioni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stato_prenotazione TEXT CHECK (stato_prenotazione IN ('In attesa','Da confermare','Confermato')),
            nome_cliente TEXT NOT NULL,
            email_cliente TEXT NOT NULL,
            numero_telefono TEXT NOT NULL,
            veicolo TEXT NOT NULL,
            dataora_prenotazione TEXT NOT NULL,
            problema_descrizione TEXT NOT NULL,
            codice_prenotazione TEXT NOT NULL,
            data_invio TEXT NOT NULL
        )
    '''

    db.execute_query(query)

def init_tableAdmin():
    query = '''
            CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    '''
    
    db.execute_query(query)


def init_tableStorico():
    query = '''
            CREATE TABLE IF NOT EXISTS storico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cliente TEXT NOT NULL,
            email_cliente TEXT NOT NULL,
            numero_telefono TEXT NOT NULL,
            veicolo TEXT NOT NULL,
            dataora_prenotazione TEXT NOT NULL,
            problema_descrizione TEXT NOT NULL,
            stato_prenotazione TEXT CHECK (stato_prenotazione IN ('Completato', 'Cancellato')),
            data_completamento TEXT NOT NULL
            )
            '''
    
    db.execute_query(query)

def initializeCredentials():
    username = "prova"
    password = "nuoveapi"
    passwordHash = hashlib.sha256(password.encode()).hexdigest()

    exists = db.execute_query("SELECT * FROM admin WHERE username=?", (username,), fetchone=True)
    
    if not exists:
        query = "INSERT INTO admin (username, password) VALUES (?, ?)"
        db.execute_query(query, (username, passwordHash), commit=True)
    

init_tablePrenotazioni()
init_tableAdmin()
initializeCredentials()
init_tableStorico()