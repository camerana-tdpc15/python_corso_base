const urlCocktails='https://www.thecocktaildb.com/api/json/v1/1/search.php?s=';
const contenitore = document.getElementById('cards-cocktails');

fetch(urlCocktails)
    .then(res=> res.json())
    .then(data=>{
        console.log(data.drinks);       //  ARRAY

        //PER OGHI COCKTAIL 
            for (drink of data.drinks){
                //CREARE UN DIV (CARD)
                contenitore.innerHTML += '
                    <div>
                         <h1>${drink.strDrink}</h1>
                         <h2>${drink.strCategory}</h2>
                         <p>${drink.strInstructionsIT</p>
                         <img src></img>
                     </div>
                ';
                //CREARE I VARI SOTTO ELEMENTI HTML CONTENENTI
                //NOME
                //CATEGORIA
                //ISTRUZIONI
                //IMMAGINI
                
            }

       });