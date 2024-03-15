const automobile2 = {
    brand: 'AUDI',
    model:'TT',
    alimentaz: ['diesel'],
    velocita:0,
    accendi: function() {
        console.log('wrooooooom');

    },
    accelera: function () {
        this.velocita += 1;
        console.log(this.velocita);
    },
};

console.log(automobile);
automobile.accendi();


// const persona = {
//     nome: 'John'
// };

let nomeUtente = 'John';
let nomeUtente2 = 'Anthony';
let nomeUtente3 = 'Chad';

saluta(nomeUtente);
saluta(nomeUtente2);

console.log('ciao');
function salutaGenerico () {
    console.log('ciao io sono un utente');
}
function saluta(nome) {
    console.log(`ciao io sono ${nome}`)
}