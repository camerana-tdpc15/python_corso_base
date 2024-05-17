const urlCocktails = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?s=';
const sezioneCards =document.querySelector('#cards-drink'); //seleziono elemento che ha ID specifico


fetch(urlCocktails)
    .then(res=>res.json())
    .then(data=>{
        //console.log(data)       //otteniamo la lista con i cocktail ARAY (OGGETTO ) HA LE {}
        //console.log(data.drinks)  //ottengo solo  la proprieta dell ogetto DRINKS ha le []


        //console.log(data.drinks[0]);  //ottengo il elemento 0
        /* PROPRIETA CHE CI INTERESSA
        strDrink
        strAlcoholic
        strCategory
        strDrinkThumb
        strGlass
        strInstructions
        */
        //console.log(data.drinks[0].strDrink)
        //console.log(data.drinks[0].strAlcoholic)
        //console.log(data.drinks[0].strCategory)
        //console.log(data.drinks[0].strDrinkThumb)
        //console.log(data.drinks[0].strGlass)
        //console.log(data.drinks[0].strInstructions)  //Ho ottenuto tutte le propr desiderate



        
        
        //cicliamo l'array che contiene i drinks
        for(d of data.drinks)  {        
        
           // console.log(d.strDrink);         //ottengo la proprieta desiderata per ogni cocktail

           //per ogni drink...
            sezioneCards.innerHTML +=`
            <div class="col-lg-3 mt-5">
          
          
          <div class="card" style="width:100%">
            <img class="card-img-top" src="${d.strDrinkThumb}" alt="Card image">
            <div class="card-body">
              <h4 class="card-title">${d.strDrink}
              <span>(${d.strAlcoholic})</span>
              </h4>
              
              <p class="card-text">
              <b>Categoria: </b>${d.strCategory}
              </p>
              
              <button class="btn btn-primary" data-bs-toggle="collapse" data-bs-target="${d.idDrink}">Collapsible</button>

                 <div id="${d.idDrink}" class="collapse">
                   <p>${d.strInstructionsIT}</p>
                 </div>
              
            </div>
            `

        }

        //for(d of data.drinks)  {
        //    console.log(d);         //ottengo tutti gli elementi
        //}
    });

    /* 
    ciclare aray che contiene drinks
    per ogni drink
        - creare una col da 3 contenente una card
    */