// Lo script serve per mostrare, nei form di prenotazione o di modifica
// della prenotazione, una barra di progresso e una scritta che indicano
// i caratteri rimanenti per arrivare alla maxLength

const textarea = document.getElementById("descriptionInput");
const progressBar = document.getElementById("progress-bar");
const remChars = document.getElementById("remaining-chars");

function charCounter(inputField){
    const maxLength = inputField.getAttribute("maxlength");
    const currentLength = inputField.value.length;
    const progressWidth = (currentLength / maxLength) * 100
    progressBar.style.width = `${progressWidth}%`;
    remChars.innerHTML = `${currentLength}` + "/" +  `${maxLength}`;
    if (progressWidth <= 60) {
        progressBar.style.backgroundColor = "rgb(19, 160, 19)";
      } else if (progressWidth > 60 && progressWidth < 85) {
        progressBar.style.backgroundColor = "rgb(236, 157, 8)";
      } else {
        progressBar.style.backgroundColor = "rgb(241, 9, 9)";
      }    
}

textarea.oninput = () => charCounter(textarea);
