// alert('ok');

const rowLotti = document.querySelector('#row-produttori');


// Fa fetch di un file JSON e lo stampa in console
  fetch("../static/data/dati_produttori.json")
  .then(response => response.json())
  .then(data => {
      for (produttore of data){
          //console.log(lotto);

        //   let displayButton = '';
          
        //   if(lotto.sospeso) {
        //     // button rosso
        //     displayButton = '<button class="btn btn-danger w-100" disabled>Sospeso</button>';
        //   }
        //   else if (lotto.get_qta_disponibile == 0) {
        //       displayButton = '<button class="btn btn-warning w-100" disabled>Esaurito</button>';  
        //     }
        //   else {
        //      displayButton = '<button class="btn btn-primary w-100">Prenota</button>';  
             
        //   }
        
        

          rowLotti.innerHTML += `
          
          <div class="col-lg-3 my-2">
                <div class="card h-100">
                    <div class="card-header">
                        <h4 class="card-title">${produttore.nome}</h4>
                        <p class="text-end"><small>(cod. lotto: ${produttore.id})</small></p>
                    </div>
                    <div class="card-body">
                        <p>Descrizione: <b>${produttore.descrizione}</b></p>
                        <p>Indirizzo: <b>${produttore.indirizzo}</b></p>
                        <p>Email: <b>${produttore.email}</b></p>
                        <p>Telefono: <b>${produttore.telefono}</b></p>
                        <button class="btn btn-primary w-100">Prodotti</button>
                    </div>
                </div>          
          </div>
          
          `;
      }

  
  });
