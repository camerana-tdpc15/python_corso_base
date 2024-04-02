//dichiarazioni variabili, elementi ecc

const nomi = ['Pino','Lino','Mino'];
const righeTabella = document.getElementById('righe');
const btnInserisciDati = document.getElementById('btn');
let isClcked = false;


//gestione eventi
btnInserisciDati.onclick = function() {
  //  righeTabella.innerHTML = `
   // <tr>
   // <td>${nome}</td>
   // </tr>
   // `;

   // esempio di ciclo su array e stampa su piu' righe
   /*
   1. ciclare la lista
   2. per ogni elemento della stessa: 
    2a creare una riga  nella tabella
    2b inserire il nome prendendolo dall'elemento
    N.B. NON SOVRASCRIVERE I DATI 
    */

    btnInserisciDati.classList.remove('btn-success');
    btnInserisciDati.classList.add('btn-danger');

   if(isClcked == false) {

    for (let i = 0; i <nomi.length; i++) {
        //console.log(nomi[i]);
        righeTabella.innerHTML += `
        <tr>
        <td> ${nomi[i]}</td>
        </tr>
        `;

    }
}
    isClcked = true;
}

//PER CASA: riscrivere ciclo for tradizionale


let testo = 'ciao';
testo = 'pippo';
testo = 'hello';
testo = 'ciaone';