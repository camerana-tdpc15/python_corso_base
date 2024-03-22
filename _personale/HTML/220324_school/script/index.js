console.log('Starting...');

const paragrafi = document.getElementsByTagName('p');
const paragrafiSpeciali = document.getElementsByClassName('speciale');

console.log(paragrafi);

// paragrafi.style.color = 'red';----errore 
//perche tratiamo una array(colezione di elementi)

//paragrafi[2].style.color = 'red'-----OK, valido per singolo elemento


    for(p of paragrafi) {

        p.style.color = 'red';

     }
     
     //----colora tutti paragrafi


for(let i = 0; i < paragrafi.length; i++) {
    paragrafi[i].style.color = 'blue';

};

for(let i = 0; i< paragrafiSpeciali.length; i++ ) {

paragrafiSpeciali[i].style.backgroundColor = 'yellow';
paragrafiSpeciali[i].classList.add('evidenzia');

}


const btn = getElementsByTagName('button');
const inputnomeUtente = document.getElementById('nomeUtente');

btn[0].onclick = function(){

    console.log(inputnomeUtente.value);
}
    
    