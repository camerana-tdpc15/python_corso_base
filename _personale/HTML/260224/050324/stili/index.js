

console.log('questo e un file esterno');

let firstName='pippo';

//concatenazione di stringhe:
console.log('nome utente: ' + firstName + '!'); //nome utente: poppi


const lastName = 'Rossi'

//backtick(digita alt+96  ``) 
//template string:
console.log(`cognomer utente: ${lastName}!`)


console.log(`nome: ${firstName}, cognome:${lastName}`)


let age = 60;
console.log(age);

console.log(1+1);  //2
console.log(42 + age); //102

let city ='';

console.log(`citta: ${city}`);
city= 'Torino'
console.log(`&{city}`)

let mediaVoti = [5, 3, 2, 4, 7];

console.log(mediaVoti)

let perdona= {
    fName: 'Walter',
    lName:'White',
    isAlive: false,
    age: 60,
    work: ['inisegnante di chimica', 'cuoco']
}
const book= {
    id: 1,
    titolo: 'il miglio verde',
    autore: {
        nome:'222',
        cognome: '333'},

        numeroPagina: 656,  
        generi:['giallo', 'thriller']
    }

    const auto= {
        id: 42,
        brand: 'FIAT',
        modello: 'panda',
        colore: 'giallo',
        targa: 'FX770NE'
    }
    console.log(auto);
    console.log(auto.targa);
    