//dichiarazioni variabili, elementi, etc
console.log('strating...');


//const nome = 'Papperino'
const nomi = ['Pino', 'Lino', 'Mimo'];

const righeTabella = document.getElementById('righe');

const btnInserisciDati = document.getElementById('btn01');

let isClicked = false;

//gestione eventi

btnInserisciDati.onclick = function(){
    //  1  esempio con un solo nome
    // righeTabella.innerHTML = `
    
    // <tr>
    //     <td> ${nome} </tr>
    // </tr>  
    
    // `;


    //  2  esempio di ciclo su array e stampa su piu righe

/*
    1. ciclare la lista
    2. x igni elem della stessa
        2a. creare una righa nella tabella
        2b. inserire una riga nella tabella

    nb. non sottoscrivi i dati
    nb. non ciclare piu di un a volta
 */

    btnInserisciDati.classList.remove('btn-succes');
    btnInserisciDati.classList.add('btn-danger')

    if  (isClicked == false) {

        for(let i = 0; i < nomi.length; i++) {
        //  console.log(nomi[i]);--verifica se e corretto il ciclo 
        righeTabella.innerHTML += `
        <tr>
        
            <td>${nomi[i]}</td>
        
        </tr>
                
        `;

        

        }
    }

    isClicked = true;

}

//riscrivere tutto il ciclo FOR tradizionale e sistituitelo con il for..of