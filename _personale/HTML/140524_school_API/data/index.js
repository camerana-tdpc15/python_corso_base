const urlBBQuote = 'https://api.breakingbadquotes.xyz/v1/quotes';

const btnRandomQuote = document.querySelector('button');

const quoteContainer = document.querySelector('#quote');
//  btnRandomQuote.onclick = function(){
//  console.log('perche funzioni???')
//  }


btnRandomQuote.addEventListener('click',function(){
//    console.log('perche funzioni?')

//      fetch(urlBBQuote)
//      .then(res=>res.json())
//      .then(data=>{
//      console.log(data);
//  });

callAPI(urlBBQuote, printQuote);



});

function callAPI(url,callback) {
    fetch(url)
    .then(res=>res.json())
    .then(data=>{
//    console.log(data);
    clbk(data)
});
}


//function callback(bbQuote){
//    console.log(data);

function printQuote(quote){
    quoteContainer.innerHTML = ` 
    <p>
    <b>Citazione:</b>
    ${quote[0].quote}
    </p>

    <p>
    <b></b>
    ${quote[0].author}
    </p>
    
    `
}