//alert('Ciao');
console.log ('Starting...');

/*
variabili per input, button,ul,
array per lista (aggiunge voce lista spessa)
 */


/*
let nome = '42'
if(nome == '42'){
        alert('OK')

        !!! TRIPLO =   === VERIFICA IL CINTENUTO E IL TIPO DI DATO
}
*/ 


const inputListaSpessa =document.getElementById('Input-voce-lista');
const btnInserisci=document.getElementsByClassName('btnInserisci')[0];
const ulSpessa=document.getElementsByTagName('ul')[0];
/* 
con [0] li dico di prendere solo il primi elemento con class btn... e ul
li altri non li prende in considerazione
*/ 

// let listaSpessa = []; //array da utilisare dopo

//ci serve la gestione degli eventi
btnInserisci.onclick =function() {
// console.log('con il eventi');
const item =inputListaSpessa.value;
if(item==''){
alert('non hai iniserito nulla');
}
else{
    
    console.log(item);
    //prendi da input il suo valore
    
    ulSpessa.innerHTML += `
    <li>${item}</li>
    
    `;
    inputListaSpessa.value = '';
    //dopo che ai inserito il input lui ritorna con al valore null, vuoto
}

}