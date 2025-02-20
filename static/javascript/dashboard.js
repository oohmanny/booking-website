//Lo script fa il fetch dell'api /admin/prenotazioni
const table = document.getElementById("bookingsTableBody");

fetchBookings()

async function fetchBookings() {
  await fetch("/admin/prenotazioni")
    .then(response => response.json())
    .then(lista => {
      if (Array.isArray(lista) && lista.length > 0) {
        lista.forEach(element => {
          createBookingCard(element);
        });
      } else {
        const bookingsContainer = document.getElementById("bookingsContainer");
        h5 = document.createElement("h5");
        h5.classList.add("mx-1")
        h5.textContent = "Al momento non ci sono prenotazioni disponibili.";
        bookingsContainer.appendChild(h5);
        console.log("La lista è vuota.");
      }
    })
    .catch(error => console.error("Errore nel recupero delle prenotazioni:", error));
}

function createBookingCard(prenotazione) {
  const bookingInfo = document.createElement("tr");
  bookingInfo.classList.add("bookingInfo", "border", "border-bottom-0");
  bookingInfo.appendChild(creaBookingInfoContent(prenotazione))

  const bookingDescriptionRow = document.createElement("tr");
  bookingDescriptionRow.classList.add("bookingDescription", "d-none", "border", "border-top-0");
  bookingDescriptionRow.appendChild(creaBookingDescriptionCell(prenotazione));
  table.appendChild(bookingInfo);
  table.appendChild(bookingDescriptionRow);

  bookingInfo.addEventListener("click", function () {
    bookingDescriptionRow.classList.toggle("d-none");
    bookingInfo.classList.toggle("active");
  });
}

function creaBookingInfoContent(prenotazione) {
  var documentFragment = document.createDocumentFragment();

  const nomeCliente = document.createElement("td");
  const dataPrenotazione = document.createElement("td");
  const dataInvio = document.createElement("td");
  const stato = document.createElement("td");

  stato.textContent = prenotazione.stato_prenotazione;
  nomeCliente.textContent = prenotazione.nome_cliente;
  dataPrenotazione.textContent = formattaData(prenotazione.dataora_prenotazione);
  dataInvio.textContent = formattaData(prenotazione.data_invio);


  documentFragment.appendChild(stato);
  documentFragment.appendChild(nomeCliente);
  documentFragment.appendChild(dataPrenotazione);
  documentFragment.appendChild(dataInvio);


  return documentFragment;
}


function creaButtonDelete(codice) {
  const button = document.createElement("button");
  button.classList.add("btn", "btn-danger", "mx-2", "my-2");
  button.textContent = "CANCELLA";
  button.addEventListener("click", async function () {
    try {
      const response = await fetch(`/api/prenotazioni/${codice}`, { method: 'DELETE' });
      if (response.ok) {
        location.reload();
      }
    } catch (error) {
      alert("Errore di connessione, riprova tra un attimo.");
    }
  });

  return button;
}

function creaButtonComplete(codice) {
  const button = document.createElement("button");
  button.classList.add("btn", "btn-success", "mx-2", "my-2");
  button.textContent = "COMPLETATA";
  button.addEventListener("click", async function () {
    try {
      const response = await fetch(`/admin/prenotazioni/complete/${codice}`, { method: 'PATCH', credentials: 'include' });
      if (response.ok) {
        location.reload();
      }
    } catch (error) {
      alert("Errore di connessione, riprova tra un attimo." + error);
    }
  });

  return button;
}

function creaButtonFixAppointment(prenotazione, outerElement) {
  var documentFragment = document.createDocumentFragment();
  const inputDate = document.createElement("input");
  inputDate.setAttribute("id", "dateInput");
  const button = document.createElement("button");
  button.classList.add("btn", "btn-info", "mx-2", "my-2");
  button.textContent = "FISSA APPUNTAMENTO";

  //Crea il bottone conferma per il calendario
  const buttonConferma = document.createElement("button");
  buttonConferma.textContent = "CONFERMA";
  buttonConferma.classList.add("btn", "btn-dark", "my-2");
  buttonConferma.addEventListener("click", async function () {
    try {
      const response = await fetch(`/admin/prenotazioni/fix_appointment/${prenotazione.codice_prenotazione}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: `{"fixAppointment":"${inputDate.value}"}`,
        credentials: 'include'
      })
      if (response.ok)
        location.reload();
    } catch (error) { alert("Errore di connessione, riprova tra un attimo.") }
  });


  button.addEventListener("click", function () {
    // Inizializza il calendario alla pressione del tasto FISSA APPUNTAMENTO
    flatpickr.localize(flatpickr.l10ns.it);
    calendarioInterattivo = flatpickr(inputDate, {
      dateFormat: "Y-m-d H:i", // Formato standard ISO 8601
      altInput: true, // Mostra una versione formattata visivamente
      altFormat: "d M Y, H:i", // Formato alternativo visualizzato
      inline: true,
      minDate: "today",
      enableTime: true,
      minTime: "08:00",
      maxTime: "19:00",
      defaultDate: prenotazione.dataora_prenotazione,
      enable: [function (date) {
        return (date.getDay(date.getDay() === 7)) // Esclude le domeniche
      }]
    });
    outerElement.appendChild(buttonConferma);
  });

  documentFragment.appendChild(button);
  inputDate.classList.add("d-none");
  outerElement.appendChild(inputDate);

  return documentFragment;
}


function creaBookingDescriptionCell(prenotazione) {
  var documentFragment = document.createDocumentFragment();

  const bookingDescriptionCell = document.createElement("td");
  bookingDescriptionCell.classList.add("px-4", "my-1");
  bookingDescriptionCell.setAttribute("colspan", "5");
  bookingDescriptionCell.innerHTML = `
  <ul>
  <li><strong>Stato Prenotazione:</strong> ${prenotazione.stato_prenotazione}</li>
  <li><strong>Codice Prenotazione:</strong> ${prenotazione.codice_prenotazione}</li>
  <li><strong>Nome e Cognome:</strong> ${prenotazione.nome_cliente}</li>
  <li><strong>Email:</strong> ${prenotazione.email_cliente}</li>
  <li><strong>Numero di Telefono:</strong> ${prenotazione.numero_telefono}</li>
  <li><strong>Data Invio:</strong> ${formattaData(prenotazione.data_invio)}</li>
  <li><strong>Prenotato per:</strong> ${formattaData(prenotazione.dataora_prenotazione)}</li>
  <li><strong>Veicolo:</strong> ${prenotazione.veicolo}</li>
  <li><strong>Dettagli:</strong><br>${prenotazione.problema_descrizione}</li>

  </ul>`
  const innerDiv = document.createElement("div");
  innerDiv.classList.add("my-2", "d-flex", "flex-wrap");
  bookingDescriptionCell.appendChild(innerDiv);
  innerDiv.appendChild(creaButtonComplete(prenotazione.codice_prenotazione))
  innerDiv.appendChild(creaButtonDelete(prenotazione.codice_prenotazione))
  innerDiv.appendChild(creaButtonFixAppointment(prenotazione, bookingDescriptionCell))
  documentFragment.appendChild(bookingDescriptionCell);

  return documentFragment;
}







// Formatta la data nel formato dd/mm/YYYY per renderla più leggibile all'interno del riepilogo
function formattaData(data) {
  const [date, orario] = data.split(" ");
  const [ora, minuto, secondo] = orario.split(":")
  const [anno, mese, giorno] = date.split("-");
  return `${giorno}/${mese}/${anno}, ${ora}:${minuto}`;
}