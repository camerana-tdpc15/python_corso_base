console.log('starting file...')


const btn01 = document.getElementById('btn01');
const thead01 = document.getElementById('thead01');
const nome = 'Pino';
const nomi = ['Pino', 'Lino', 'Mino']

btn01.onclick = function() {
   // prendere il body della tabella e inserire HTML una row con 
   // dentro i dati presenti nella variabile js nome
   thead01.innerHTML = `
   <ol type="I" class=" border border-5">
   <li>Un Italiano</li>
   <li>Un Francese</li>
   <li>Un Tedesco</li>
</ol>
   `;

   // ESERCIZIO 2: al click del button,
   // popolare la tabella con n righe quanti sono i personaggi 
   // dentro la variabile array nomi
   // USANDO IL FOR!!!
}
document.getElementById('p01').innerHTML = 'Esercizio 01 W3School!'