//alert('ok')


const rowLotti = document.querySelector("#row-lotti");


  // Fa fetch di un file JSON e lo stampa in console
  fetch("../static/data/dati_lotti.json")
  .then(response => response.json())
  .then(data => {
      for (lotto of data){
          //console.log(lotto.prodotto.produttore.nome);
          rowLotti.innerHTML += `
          <div class="col-lg-3 my-2">

          <div class="card">
  <div class="card-header"><h4 class="card-title">${lotto.prodotto.nome}</h4>
  <p class= "text-end"><small>(cod. lotto ${lotto.id}</small></p>
  </div>
  <div class="card-body"><b>Produttore:${lotto.prodotto.produttore}</b><p>Data Consegna</p></div>
  </div>
</div>
          </div>
          `;
      }

  });



  