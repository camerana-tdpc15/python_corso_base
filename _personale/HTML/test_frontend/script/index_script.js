console.log('Starting at 11.30pm Finish at 2am');

const btnColora = document.getElementById('btnColora');
const btnReset = document.getElementById('btnReset');
const par = document.getElementById('par1');

const testoParagrafo = par.innerText;

btnColora.onclick = function() {
   
    par.classList.add('rosso');
    par.innerHTML = testoParagrafo;
}

btnReset.onclick = function() {
    par.classList.remove('rosso');
    par.innerText = testoParagrafo;
}