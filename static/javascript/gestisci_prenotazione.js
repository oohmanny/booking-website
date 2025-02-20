var codicePrenotazione;
var datiPrenotazione;

// Inizializza il calendario interattivo
flatpickr.localize(flatpickr.l10ns.it);
calendarioInterattivo = flatpickr("#dateInput", {
    dateFormat: "Y-m-d H:i", // Formato standard ISO 8601
    altInput: true, // Mostra una versione formattata visivamente
    altFormat: "d M Y, H:i", // Formato alternativo visualizzato
    minDate: "today",
    enableTime: true,
    minTime: "08:00",
    maxTime: "19:00",
    enable: [function (date) {
        return (date.getDay(date.getDay() === 7)) // Esclude le domeniche
    }]
});

// Cerca la prenotazione tramite codice prenotazione
document.getElementById("searchButton").addEventListener("click", async function (e) {
    e.preventDefault();

    codicePrenotazione = document.getElementById("bookingCode").value;
    if (codicePrenotazione == "") {
        showAlertNotification("Inserisci un codice di prenotazione", "warning");
        return;
    }

    try {
        let response = await fetch(`/api/prenotazioni/${codicePrenotazione}`)

        let data = await response.json();

        if (data.error) {
            //Se viene restituito un errore, mostra un Alert Bootstrap
            showAlertNotification(data.error, data.messageType);
            document.getElementById('riepilogoPrenotazione').classList.add('d-none');
            return;
        }

        //Disabilita l'input per evitare modifiche successive alla richiesta
        document.getElementById("bookingCode").disabled = true;
        datiPrenotazione = data;


        //Imposta il form di riepilogo con i dati della prenotazione
        document.getElementById('nameSpan').textContent = data.nome_cliente;
        document.getElementById('emailSpan').textContent = data.email_cliente;
        document.getElementById('vehicleSpan').textContent = data.veicolo;
        document.getElementById('numberSpan').textContent = data.numero_telefono;
        document.getElementById('descriptionSpan').textContent = data.problema_descrizione;
        document.getElementById('dateSpan').textContent = formattaData(data.dataora_prenotazione);


        //Mostra il form di riepilogo all'utente
        document.getElementById('riepilogoPrenotazione').classList.remove('d-none');
    }

    catch (error) {
        // showAlertNotification('Errore nella connessione al server. Riprova tra qualche minuto.', "danger");
        console.error("Errore:", error);
    }
});

//Formatta la data nel formato dd/mm/YYYY per renderla più leggibile all'interno del riepilogo
function formattaData(data) {
    const [date, orario] = data.split(" ");
    const [ora, minuto, secondo] = orario.split(":")
    const [anno, mese, giorno] = date.split("-");
    return `${giorno}/${mese}/${anno}, ${ora}:${minuto}`;
}

//Imposta il form di modifica
document.getElementById("editButton").addEventListener("click", function (e) {
    e.preventDefault();

    if (datiPrenotazione != null) {
        try {
            //Inizializza i vari campi del form ai rispettivi valori inseriti in fase di prenotazione
            document.getElementById('nameInput').value = datiPrenotazione.nome_cliente;
            document.getElementById('numberInput').value = datiPrenotazione.numero_telefono;
            document.getElementById('emailInput').value = datiPrenotazione.email_cliente;
            document.getElementById('vehicleInput').value = datiPrenotazione.veicolo;
            document.getElementById('descriptionInput').value = datiPrenotazione.problema_descrizione;
            calendarioInterattivo.setDate(datiPrenotazione.dataora_prenotazione, true, "Y-m-d H:i");

            //Mostra il form per la modifica all'utente
            document.getElementById('containerModifica').style.display = 'block';
        } catch (exception) {
            alert(exception);
        }
    }
});


//Invia la modifica al server
document.getElementById("interactiveForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    // Salva i dati inseriti nel form di modifica in un oggetto prenotazioneModificata
    const prenotazioneModificata = {
        nome_cliente: document.getElementById('nameInput').value,
        numero_telefono: document.getElementById('numberInput').value,
        veicolo: document.getElementById('vehicleInput').value,
        email_cliente: document.getElementById('emailInput').value,
        dataora_prenotazione: document.getElementById('dateInput').value,
        problema_descrizione: document.getElementById('descriptionInput').value
    };

    // Invia al server i dati di prenotazioneModificata in formato JSON
    await fetch(`/api/prenotazioni/${codicePrenotazione}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(prenotazioneModificata)
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                // Mostra il messaggio di risposta dal server in un Alert Bootstrap
                showAlertNotification(data.message, data.messageType);
                document.getElementById("searchButton").click();
                document.getElementById("containerModifica").style.display = 'none';
            }
        })
});


//Gestisce la logica della cancellazione
document.getElementById("deleteButton").addEventListener("click", async function (e) {
    e.preventDefault();

    await fetch(`/api/prenotazioni/${codicePrenotazione}`, {
        method: 'DELETE'
    })
        .then(response => response.json())
        .then(message => {
            if (message.message) {
                //Imposta gli item nel sessionStorage per visualizzare l'Alert Bootstrap dopo il redirect
                sessionStorage.setItem("alertMessage", message.message);
                sessionStorage.setItem("alertType", "success");
                window.location.replace('/');
            }
        })
        .catch(error => {
            alert('Errore durante la connessione al server. Riprova tra qualche minuto.' + error);
        })
});


//Imposta il tipo di Alert Bootstrap, il corpo dello stesso e lo mostra
function showAlertNotification(message, type) {
    const alertNotification = document.getElementById("alertNotification");
    const alertMessage = document.getElementById("alertMessage");

    alertNotification.classList.remove("alert-success");
    alertNotification.classList.remove("alert-danger");
    alertNotification.classList.add(`alert-${type}`);
    alertMessage.textContent = message;
    alertNotification.classList.remove('d-none');
}