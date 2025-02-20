import random
import string


#Genera il codice di prenotazione e lo restituisce al chiamante
def generatecode(length=8):
    characters = string.ascii_letters + string.digits
    randomcode = ''.join(random.choices(characters, k=length))
    return randomcode.upper()