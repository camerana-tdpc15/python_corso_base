console.log('Starting file');
function first_function() {
    
    document.getElementById('demo01').innerHTML = 'This script is from Js';

}


//      IN W3 CE QUESTA NOTA DA QUALE CAPISCO CHE 
//      LA PAROLA CHIAVE VAR DEVE ESSERE UTILISATO SOLO PER BROWSER NEMO RECENTI (vedi commento a piu righe)


//      GIUSTO??  


//      PERO LE PAROLE CHIAVE LET E CONST NON SONO PER DICHIARARE VARIABILI DI BLOCCO?


/*Nota
La varparola chiave è stata utilizzata in tutto il codice JavaScript dal 1995 al 2015.

Le parole chiave lete constsono state aggiunte a JavaScript nel 2015.

La varparola chiave deve essere utilizzata solo nel codice scritto per i browser meno recenti.
*/

let carName = "Volvo";
document.getElementById('demo02').innerHTML = let carName;

