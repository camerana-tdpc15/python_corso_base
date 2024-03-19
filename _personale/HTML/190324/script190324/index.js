console.log('inizio file...');

const generi= ['classico', 'rock', 'pop'];

//for(let i =0; i< WebGLRenderingContext.length; i++)
//{
//    console.log(generi[i])
//
//}
for(g of generi){console.log(g)};


//creare le variabili che contengono botton e paragrafo

const btnColora = document.getElementById('btnColora');
//const- crea variabile
//btnColora- e il id a  quale voliamo dare la variabile
//document-carica body html
//getElem...-da dove rendere
//(il id del elem  da modificare)

const p= document.getElementById('primoPar');

const btnReset = document.getElementById('btnReset')

console.groupCollapsed(p);

//gestire l'evento click sul botton
//questa e una funzione anonima, senza nome

// btnColora.onclick = function () {
//     p.style.color = 'red';
//     p.style.backgroundColor = 'yellow'
//     p.style.fontSize = '30px'
// }

btnColora.onclick = colora;
btnReset.onclick = reset;

// btnReset.onclick = function () {
//     p.style.backgroundColor = '';
//     p.style.color = 'black';
//     p.style.fontSize = ''
// }

function colora(){
    p.style.color = 'red';
    p.style.backgroundColor = 'yellow'
    p.style.fontSize = '30px'
}
function reset(){
    p.style.backgroundColor = '';
    p.style.color = 'black';
    p.style.fontSize = ''
}





//questa e una funzione  con nome...

//function saluta(){console.log('ciao')}


