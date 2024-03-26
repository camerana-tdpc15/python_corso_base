//console.log('Starting...');



//creazione card 

const arrayCities = [
    {
        id: 1,
        city: 'Turin',
        desctiption: 'Welcome to Turin',
        urlImg: 'https://images.pexels.com/photos/12739774/pexels-photo-12739774.jpeg?auto=compress&cs=tinysrgb&w=400'
    },
    {
        id: 2,
        city: 'Rome',
        descttiption: 'Welcome to Rome',
        urlImg: 'https://images.pexels.com/photos/16353919/pexels-photo-16353919/free-photo-of-citta-punto-di-riferimento-estate-italia.jpeg?auto=compress&cs=tinysrgb&w=400'
    },
    {
        id: 3,
        city: 'Venice',
        desctiption: 'Welcome to Venice',
        urlImg: 'https://images.pexels.com/photos/17407338/pexels-photo-17407338/free-photo-of-punto-di-riferimento-edifici-parete-muro.jpeg?auto=compress&cs=tinysrgb&w=400'
    },
    {
        id: 4,
        city: 'New York',
        desctiption: 'Welcome to Venice',
        urlImg: 'https://images.pexels.com/photos/8218/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=400'
    }

];

//variabili

let cont = 4;
const rowCities = document.getElementById('row-cities');
const inputCity = document.getElementById('City') ;
const inputDescriptio = document.getElementById('description') ;
const inputUrlImg = document.getElementById('url')  ;

const btnAdd = document.getElementById('btnAdd')  ;
btnAdd.onclick = handleClickAdd;
function printCityCards = handleClickAdd;


//logica onload/refresh

printCityCards()

/*
iniziamo a ciclare array sopra creato
*/
//utilisa alt96``


//questo for diventa function printCityCards

// for (c of arrayCities) {
//     // console.log(c)---per verificare se carica array
//     rowCities.innerHTML += `
//     <div class="col-lg-3">
//                     <div class="card" style="width:100%">
//                             <img class="card-img-top" src="${c.urlImg}" alt="Card image">
//                         <div class="card-body">
//                             <h4 class="card-title">${c.city}</h4>
//                             <p class="card-text">${c.descttiption}.</p>
//                             <a href="#" class="btn btn-primary">See ${c.city}</a>
//                         </div>
//                     </div>

//     </div>
//     `;
// }

// funzioni

function handleClickAdd () {
    //verifichiamo se l'utente ha inserito tutti i dati

    if(inputCity.value == '' || inputDescriptio.value == '' || 
    inputUrlImg.value ==''){
        alert('inserisci dati');
    }
    //utente ha inserito tutto
    else{
        cont +=1;   //incrementa di 1 la variabile per id
        const newCity = {
            id: 5,
            city:inputCity.value  ,
            desctiption:inputDescriptio .value ,
            urlImg:inputUrlImg.value ,
        };
        arrayCities.push(newCity);
        // console.log(arrayCities)
        rowCities.innerText = '';

        
    }

}

function printCityCards () {
    for (c of arrayCities) {
        // console.log(c)---per verificare se carica array
        rowCities.innerHTML += `
        <div class="col-lg-3">
                        <div class="card" style="width:100%">
                                <img class="card-img-top" src="${c.urlImg}" alt="Card image">
                            <div class="card-body">
                                <h4 class="card-title">${c.city}</h4>
                                <p class="card-text">${c.descttiption}.</p>
                                <a href="#" class="btn btn-primary">See ${c.city}</a>
                            </div>
                        </div>
    
        </div>
        `;
}
}
