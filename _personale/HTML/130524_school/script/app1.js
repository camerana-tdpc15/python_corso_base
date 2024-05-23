console.log('Starting file')

//const req = new XMLHttpRequest();
//req.open("GET", "data/book.json");
//req.send();
//req.responseType = "json";
//req.onload = function() {
//    const b = req.response;
//    console.log(b)
//}




//fetch('data/book.json')
//    .then(res=> res.json())
//    .then(data=>{
//        console.log(data);
//    });

fetch('data/books.json')
    .then(res=> res.json())
    .then(data=>{
       // console.log(data);   //data e un ARAY
       console.log(data);
       for(b of data) {
        console.log(b.title);
       }
    });


