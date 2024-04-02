const btn = document.getElementById('btn1');
const btnRemove = document.getElementById('btn2');
const par = document.getElementById('par1');

const testoParagrafo =par.innerText;

btn.onclick = function(){ //console.log(par.classList);
    par.classList.add('rosso');
    par.innerText = 'questo è testo che arriva da js...';
}
btnRemove.onclick = function() {
  par.classList.remove('rosso');
  par.innerText = testoParagrafo;
}

/*
elemento.innerHTML
elemento.style. nome proprietà css
elemento.classList.add('nome classe da aggiungere')
elemento.classList.remove('nome classe da rimuovere')
*/


const btnPopolaTabella = document.getElementById('btnPopolaTabella')
const bodyTabella =document.getAnimations('bodyTabella');
const nome = 'Pino';
btnPopolaTabella.onclick = function() {
    //prendere il body della tabella e inserire HTML una row con 
    //dentro i dati presenti nella variabile JS nome
    bodyTabella.innerHTML =`
    <tr>
    <td>011</td>
    <td>${nome}</td>
    </tr>
    `;

}