const par1 = document.getElementById('uno');
const paragrafi = document.getElementsByTagName('p');
console.log(paragrafi);
const paragrafiSpeciali = document.getElementsByClassName('speciale')

//paragrafi.style.color='red'
//errore! non possiamo perchè stiamo trattando una
//collezione di elementi 

//paragrafi[2].style.color ='red';

for(p of paragrafi) {
p.style.color = 'red';
}


for(let i = 0; i <paragrafi.length; i++) {
    paragrafi[i].style.color = 'blue';
}

for(let i = 0; i < paragrafiSpeciali.length; i++){
    paragrafiSpeciali[i].style.backgroundColor = 'yellow';
}



//////////////////////
const btn = document.getElementsByTagName('button');
const nomeUtente = document.getElementById('nomeUtente');
btn [0].onclick = function () {
console.log(nomeUtente);
}


