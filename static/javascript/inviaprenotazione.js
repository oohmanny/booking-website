//Inizializza il calendario interattivo
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


// Gestisce l'invio della prenotazione
document.getElementById("interactiveForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    //Crea un oggetto prenotazione sulla base dei dati inseriti nel form
    const nuovaPrenotazione = {
        nome_cliente: document.getElementById('nameInput').value,
        numero_telefono: document.getElementById('numberInput').value,
        veicolo: document.getElementById('vehicleInput').value,
        email_cliente: document.getElementById('emailInput').value,
        dataora_prenotazione: document.getElementById('dateInput').value,
        problema_descrizione: document.getElementById('descriptionInput').value
    };

    await fetch('/api/prenotazioni', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(nuovaPrenotazione)
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showAlertNotification(data.error, data.messageType);
            } else {
                //Se la prenotazione viene inviata correttamente, disabilita gli input e il tasto invia del form
                const inputs = document.querySelectorAll("input, textarea");
                inputs.forEach((input) => {
                    input.disabled = true;
                });
                document.getElementById("buttonInvia").disabled = true;

                //Mostra il codice prenotazione all'utente
                showAlertNotification(`${data.message}, conserva il tuo codice prenotazione:
                <strong>${data.bookingCode}</strong>`, data.messageType);
            }
        })

});

//Imposta il tipo di Alert Bootstrap, il corpo dello stesso e lo mostra
function showAlertNotification(message, type) {
    const alertNotification = document.getElementById("alertNotification");
    const alertMessage = document.getElementById("alertMessage");

    alertNotification.classList.remove("alert-success");
    alertNotification.classList.remove("alert-danger");
    alertNotification.classList.add(`alert-${type}`);
    alertMessage.innerHTML = message;
    alertNotification.classList.remove('d-none');
}