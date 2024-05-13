const urlUsers = 'https://jsonplaceholder.typicode.com/users';
const urlComments = 'https://jsonplaceholder.typicode.com/comments'

fetch(urlComments)
    .then(res=> res.json())
    .then(data=>{
       //console.log(data);

       for(c of data){
       console.log(c.email)
       }
       });

       