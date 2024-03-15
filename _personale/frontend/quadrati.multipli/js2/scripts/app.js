//console.log('inizio file app.js');
//const pi = 3,14;

//let firstName ='Pippo';
//let lastName ='Pallino';
//let isAlive = true;
//let favColors = ['rosso','verde', 'giallo'];
//let estrazione = [2, 45, 67, 21];

//console.log(firstNAme);
// il nome dell'utente è Pippo!

// 1. concatenazione di stringhe:
//console.log('il nome dell\' utente è ' + firstName + '!')

// 2. template string (alt+96) backtick



//let favColors = ['rosso','verde', 'giallo'];
//let estrazione = [2, 45, 67, 21];
//console.log(favColors);
//console.log(favColors[0]);

//il colore preferito dell'utente è il verde...
//console.log(`il colore preferito dell'utente è il ${}`);


let brand = 'FIAT';
let model = '500';


let automobile = {
    brand: 'FIAT',
    model: '500',
    alimentaz: ['benzina', 'gpl'],
    proprietario: {
        nome: 'Walter',
        cognome: 'white',
        età: 60,
        occupazione: ['insegnante di chimica', 'cuoco'],
        residenza: {
            città: 'Torino',
            cap: '10100'
        }
    }
};
let automobile2 = {}
console.log(automobile);
console.log(`il modello è:${automobile.model}`)
console.log(automobile.proprietario.residenza)




const libro = {
    titolo: 'il signore degli anelli',
    autore: {
        nome: 'J.R.R',
        cognome: 'Tolkien',
    },
    immagineCopertina: 'https://www.bing.com/images/search?view=detailV2&ccid=lN%2buB1JK&id=2F970CD62FE069A10788C524656FAEC10BC3DF60&thid=OIP.lN-uB1JKGs-fuxHJGHAkRwHaLH&mediaurl=https%3a%2f%2flordchannel.com%2fmedia%2fxvjOBWfm32skiwIAU2iocb6fyC8.jpg&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.94dfae07524a1acf9fbb11c918702447%3frik%3dYN%252fDC8Gub2UkxQ%26pid%3dImgRaw%26r%3d0&exph=3000&expw=2000&q=i+l+signore+degl+ianelli+copertina&simid=608009435252199015&FORM=IRPRST&ck=C655B5F8F771368D2E3883398C15D689&selectedIndex=2&itb=0&ajaxhist=0&ajaxserp=0',
    numeroPagine: 4034,
    generi: ['fantasy', 'avventura']
}