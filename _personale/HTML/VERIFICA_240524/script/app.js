console.log('Starting file')

const urlUser = "https://jsonplaceholder.typicode.com/users";

const sezioneUser = document.querySelector('#card-utente');
// const inputUser = document.querySelector('#input-user');
// const btnSearch = document.querySelector('#btn-search');

// let userSerch = '';


// btnSearch.addEventListener('click', function() {
//     console.log('btn search cliccato');
//     userSearched = inputUser.value;
//     console.log(userSerch);
    
//     const urlSearched = urlUser + userSerch;
    
//     cleanCards();
    
//     callAPI(urlSearched);
// });

callAPI(urlUser);

function callAPI(url) {

    fetch(url)
    .then(res => res.json())
    .then(data => {

      
        for (u of data) {
          //console.log(u.address.street)
           sezioneUser.innerHTML +=  `
           <div class="col-lg-3 mb-4">
                 <!-- singola card -->
                 <div class="card" style="width:100%" >
                    
                     <div class="card-body">
                         <h4 class="card-title">${u.name}
                             <span>(${u.email})</span>
                         </h4>                    
                         <p class="card-text">
                             <b>Street: </b>${u.address.street}
                         </p>
                         <p class="card-text">
                             <b>suite: </b>${u.address.suite}
                         </p>
                         <p class="card-text">
                             <b>city: </b>${u.address.city} (${u.address.zipcode})
                         </p>
                         <button class="btn btn-primary" data-bs-toggle="collapse"
                             data-bs-target="#D${u.id}">Dettagli</button>
                         <!-- per fare collassare solo 1 elemento, l'id
                             deve essere univoco.. e deve iniziare per lettera
                             usiamo la proprieta' univoca id del drink preceduta
                             da un qualsiasi carattere
                         -->
                         <div id="D${u.id}" class="collapse">
                             <p>${u.company.name}</p>
                             <p>${u.phone}</p>
                             <p>${u.website}</p>
                         </div>
                     </div>
                 </div>
             </div>
           `;
        }

    });

}


function cleanCards() {
    sezioneCards.innerHTML = '';
    inputUser.value = '';
}