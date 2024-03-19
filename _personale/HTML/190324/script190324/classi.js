console.log('inizio file...');

const btn01 = document.getElementById('btn01');
const par01 = document.getElementById('par01');
const btnReset01 = document.getElementById('btnReset01');

const testoParagrafo = par01.innerText;

//  btn.onclick = function () {
//      p.style.color = 'green';
//      p.style.backgroundColor = 'blue'
//      p.style.fontSize = '40px'
//  }


btn01.onclick = function () {
      //console.log(par01.classList);

      par01.classList.add('rosso');
    
//innerText modifica il testo
      par01.innerHTML = 'Questo testo arriva da <b>js</b>...';
  }

  btnReset01.onclick = function() {

    par01.classList.remove('rosso');
    par01.innerText =testoParagrafo;

  }

const btnCompila =document.getElementById('btnCompila');
const bodyTb = document.getElementById('bodyTb')
const nome = 'Pippo';

btnCompila.onclick =function () {
    bodyTb.innerHTML = 
<tr>
    <td>011</td>
    <td>${nome}</td>
</tr>


//prendere il body della tabella e inserisci una row con
//dentro  i dati  presenti nella variabile js nome



//sol02 al click del btn, popolare la tabela con n° righe 
//quante sono i personaggi dentro la variabile arrei
}

