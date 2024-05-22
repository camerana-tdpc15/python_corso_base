const url_cocktails = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?s=';
const contenitore = document.getElementById('cards-cocktails')
// fetch(url_cocktails)
//     .then(res => res.json())
//     .then(data => {
//         console.log(data.drinks)
//     });



//per ogni cocktails

fetch(url_cocktails)
    .then(res => res.json())
    .then(data => {
        // console.log(data)  //data qui è un array
        for (drink of data.drinks) {
            // 1. creare un div (card)
            contenitore.innerHTML += `
            <div>
                <h1>${drink.strDrink}</h1>
                <h2>${drink.strCategory}</h2>
                <p>${drink.strInstructionsIT}</p>
                <img src="${drink.strDrinkThumb}">
            </div>
            `;
            // 2. creare i vari sotto elementi html contenenti:
                // nome
                // categoria
                // istruzioni
                // immagine
        }
    });

    