console.log('inizio file');


const btnUno = document.getElementById('btnUno');
const p = document.getElementById('primoPar');

const urlImg = 'https://img.freepik.com/free-photo/closeup-shot-adorable-kitten-sitting-couch_181624-46615.jpg?w=826&t=st=1661376842~exp=1661377442~hmac=ddbc90a80a7179ac4ac0b6017327562157a57933c95d475b80c7e24b869c114a';

btnUno.onclick = function () {
    // p.innerText = 'paragrafo <b>modificato</b> via js...';
    p.innerHTML = `
        paragrafo
        <b>modificato</b> 
        via js...
        <img src="${urlImg}" />
        <p>
            ciao
        </p>
        <h2>titolino</h2>
        `;

    p.style.color = 'red';
    p.style.backgroundColor = 'yellow';
    p.style.marginTop = '50px';

    btnUno.style.backgroundColor = 'black';
    btnUno.style.color = 'red';
    btnUno.style.width = '200px';
    btnUno.style.height = '100px';

    document.body.style.backgroundColor = 'gray';
}

console.log(p); 