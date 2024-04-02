console.log('inizio file js');

const generi = ['classico', 'rock', 'pop'];

//for(let i = 0; i< generi.length; i++) {
 //   console.log(generi [i]);
//}

for(g of generi) {
    console.log(g);
}
//cicla tutti gli elementi di una collezione indipendentemente da cosa sono


const btnColora = document.getElementById('btnColora');
const btnReset = document.getElementById('btnReset');

const p = document.getElementById('primoPar');


//creare le variabili che contengono button e paragrafo




//btnColora.onclick = function(){
   // p.style.color = 'red';
   // p.style.backgroundColor ='yellow';
   // p.style.fontSize = '30px';

//}
btnColora.onclick = colora;
btnReset.onclick =sbianca;

//btnReset.onclick = function(){
 //   p.style.color = 'black';
 //   p.style.backgroundColor ='';
 //   p.style.fontSize = '';
//}
//gestire l'evento di click sul button


function colora() { p.style.color = 'red';
p.style.backgroundColor ='yellow';
p.style.fontSize = '30px';

}
function sbianca() {
    p.style.color = 'black';
    p.style.backgroundColor ='';
    p.style.fontSize = '';

}

//console.log(p);
 