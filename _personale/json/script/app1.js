// const b = {
//     id: 1,
//     titolo: 'Il vecchio e il mare',
//     autore: {
//         firstName: 'Ernesto',
//         lastName: 'Eminguaio'
//     },
//     cover: 'copertina_libro.jpg',
//     pages: 5623,
//     genres: ['thriller', 'adventures']
// }

// console.log(b.autore.firstName);
// for (g of b.genres) {
//     console.log(g)
// }
//-----------------------------------------------------------------------------

//CHIAMATA VECCHIO STILE CON XMLHTTPREQUEST con ajax
// const req = new XMLHttpRequest();
// req.open("GET", "data/book.json");
// req.send();
// req.responseType = "json";
// req.onload = function() {
//     const b = req.response;
//     console.log(b);
// }

//------------------------------------------------------------------------------
// COME FARE LE REQUEST CON JAVASCRIPT VANILLA

// fetch('data/book.json')
//     .then(res => res.json())
//     .then(data => {
//         console.log(data);   //data qui è un oggetto
//     });

fetch('data/books.json')
    .then(res => res.json())
    .then(data => {
        // console.log(data)  //data qui è un array
        for (b of data) {
            console.log(b.titolo);
        }
    });

