//Gestisce la visualizzazione di un Alert Bootstrap per notificare un messaggio
//salvato nel sessionStorage presumibilmente prima di un redirect

const alertMessage = sessionStorage.getItem("alertMessage");
const alertType = sessionStorage.getItem("alertType");

if(alertMessage){
    const sessionStorageAlert = document.getElementById("sessionStorageAlert");
    alertBody = document.getElementById("alertMessage");

    alertBody.textContent = alertMessage;
    sessionStorageAlert.classList.add(`alert-${alertType}`);
    sessionStorageAlert.classList.remove("d-none");


    sessionStorage.removeItem("alertMessage");
    sessionStorage.removeItem("alertType");

}

