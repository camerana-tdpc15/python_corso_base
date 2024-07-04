// alert("ok")
const rowLotti = document.querySelector('#row-lotti');

  // Fa fetch di un file JSON e lo stampa in console
  fetch("../static/data/dati_lotti.json")
  .then(response => response.json())
  .then(data => {
      for(lotto of data) {
          // console.log(lotto);

          let displayButton= '';
          if (lotto.sospeso) {
              //button rosso
            
            displayButton='<button class= "btn btn-danger w-100" disabled>Sospeso</button>'
          }

        else if(lotto.get_qta_disponibile == 0){

          displayButton= '<button class = ""btn btn-warning w-100" disable> Esaurito</button>';
        }

        else{
          displayButton='<button class="btn btn-primary w-100">Prenota</button>'

        }
        rowLotti.innerHTML += `
          <div class="col-lg-3 my-2">
              <div class="card h-100">
                  <div class="card-header">
                  <h4 class="card-title">${lotto.prodotto.nome}</h4>
                  <p class="text-end"><small>(cod. lotto:${lotto.id})</small></p>
                  </div>
                  <div class="card-body">
                  <p>produttore: <b>${lotto.prodotto.produttore.nome}</b></p>
                  <p>data consegna: <b>${lotto.get_date}</b></p>
                  <p>QTA Tot: <b>${lotto.qta_lotto} ${lotto.qta_unita_misura}</b></p>
                  <p>QTA Disp: <b>${lotto.get_qta_disponibile} ${lotto.qta_unita_misura}</b></p>
                  <p>Prezzo: <b>${lotto.get_prezzo} </b></p>
                  ${displayButton}
                  </div>
  
            </div>
          
          `
      }
 
});