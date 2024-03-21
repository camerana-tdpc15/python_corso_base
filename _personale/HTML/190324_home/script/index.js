console.log('inizio file js...');

const btnDati = document.getElementById ('btnDati');
const tbody01 =document.getElementById ('tbody01');

btnDati.onclick = function(){
    tbody01.innerHTML =`
    <tr>
        <td>Cristian</td>
        <td>Dretcanu</td>
        <td>011 011 011</td>
    </tr>`
}