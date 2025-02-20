//Lo script fa il fetch dell'api /admin/prenotazioni
const table = document.getElementById("bookingsTableBody");

fetchHistory()
async function fetchHistory() {
  await fetch("/admin/prenotazioni/history")
    .then(response => response.json())
    .then(lista => {
      // Check if 'lista' is not empty
      if (Array.isArray(lista) && lista.length > 0) {
        lista.forEach(element => {
          createBookingCard(element);
        });
      } else {
        const bookingsContainer = document.getElementById("bookingsContainer");
        h5 = document.createElement("h5");
        h5.classList.add("mx-1")
        h5.textContent = "Al momento non ci sono prenotazioni nello storico.";
        bookingsContainer.appendChild(h5);
      }
    })
    .catch(error => console.error("Errore nel recupero dello storico:", error));
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
  dataInvio.textContent = formattaData(prenotazione.data_completamento);


  documentFragment.appendChild(stato);
  documentFragment.appendChild(nomeCliente);
  documentFragment.appendChild(dataPrenotazione);
  documentFragment.appendChild(dataInvio);


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
  <li><strong>Nome e Cognome:</strong> ${prenotazione.nome_cliente}</li>
  <li><strong>Email:</strong> ${prenotazione.email_cliente}</li>
  <li><strong>Numero di Telefono:</strong> ${prenotazione.numero_telefono}</li>
  <li><strong>Prenotato per:</strong> ${formattaData(prenotazione.dataora_prenotazione)}</li>
  <li><strong>Data Completamento:</strong> ${formattaData(prenotazione.data_completamento)}</li>
  <li><strong>Veicolo:</strong> ${prenotazione.veicolo}</li>
  <li><strong>Dettagli:</strong><br>${prenotazione.problema_descrizione}</li>

  </ul>`

  documentFragment.appendChild(bookingDescriptionCell);
  return documentFragment;
}

const cleanHistory = document.getElementById("cleanHistory");
cleanHistory.addEventListener("click", async function (e) {
  e.preventDefault();
  await fetch("/admin/prenotazioni/history", {
    method: 'DELETE',
    credentials: 'include'
  }).then(response => {
    if(response.ok){
      console.log("Storico cancellato");
      location.reload();
    }
  }).catch(error => alert("Errore: " + error))
});






// Formatta la data nel formato dd/mm/YYYY per renderla più leggibile all'interno del riepilogo
function formattaData(data) {
  const [date, orario] = data.split(" ");
  const [ora, minuto, secondo] = orario.split(":")
  const [anno, mese, giorno] = date.split("-");
  return `${giorno}/${mese}/${anno}, ${ora}:${minuto}`;
}