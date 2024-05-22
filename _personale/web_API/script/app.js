const url = 'http://jsonplaceholder.typicode.com/users'
const url_comments = 'https://jsonplaceholder.typicode.com/comments'

// fetch(url)
//     .then(res => res.json())
//     .then(data => {
        
//             console.log(data);
//         }
//     );

    // fetch(url)
    // .then(res => res.json())
    // .then(data => {
    //     // console.log(data)  //data qui è un array
    //     for (u of data) {
    //         console.log(u.email);
    //     }
    // });

    // fetch(url_comments)
    // .then(res => res.json())
    // .then(data => {
    //     console.log(data)
    // });

    fetch(url_comments)
    .then(res => res.json())
    .then(data => {
        // console.log(data)  //data qui è un array
        for (c of data) {
            console.log(c.email);
        }
    });