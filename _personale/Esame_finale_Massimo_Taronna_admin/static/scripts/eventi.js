// Carica gli eventi quando il DOM è completamente caricato
document.addEventListener("DOMContentLoaded", function () {
  // Fetch degli eventi con le relative repliche
  fetch("/api/eventi_con_repliche")
    .then((response) => response.json())
    .then((eventi) => {
      const container = document.getElementById("eventi-container");
      eventi.forEach((evento) => {
        // Crea una card per ogni evento
        const col = document.createElement("div");
        col.className = "col-md-3";
        col.innerHTML = `
          <div class="card h-100">
            <div class="d-flex flex-row justify-content-between align-items-center p-2">
              <img src="/static/imgs/${evento.immagine}" class="card-img-top" alt="${evento.nome}" style="max-width: 50px;">
              <div>
                <h5 class="mb-0"><b>${evento.nome_locale}</b></h5>
                <h6 class="mb-0">${evento.luogo}</h6>
              </div>
            </div>
            <div class="card-body d-flex flex-column">
              <h3 class="card-title text-center mt-0"><b>${evento.nome_evento}</b></h3>
              <ul class="list-group list-group-flush flex-grow-1">
                ${evento.repliche
                  .map(
                    (replica) => `
                      <li class="list-group-item ${replica.annullato ? "text-danger" : ""}">
                        ${replica.data_ora}
                        <p>Posti disponibili: ${replica.posti_disponibili}</p>
                        ${replica.annullato ? "<h4>EVENTO ANNULLATO!</h4>" : ""}
                      </li>`
                  )
                  .join("")}
              </ul>
              ${
                evento.repliche.some((replica) => !replica.annullato)
                  ? `<button class="btn btn-primary mt-2" onclick="apriModalPrenotazione(${evento.id}, ${JSON.stringify(
                      evento.repliche.filter((replica) => !replica.annullato)
                    ).replace(/"/g, "&quot;")})">Prenota</button>`
                  : ""
              }
            </div>
          </div>
        `;
        container.appendChild(col);
      });
    });
});

// Funzione per aprire il modal di prenotazione
function apriModalPrenotazione(eventoId, repliche) {
  const replicaSelect = document.getElementById("replicaSelect");
  replicaSelect.innerHTML = repliche
    .map(
      (replica) => `
        <option value="${replica.id}">${replica.data_ora} - Posti disponibili: ${replica.posti_disponibili}</option>
    `
    )
    .join("");
  const modal = new bootstrap.Modal(document.getElementById("prenotaModal"));
  modal.show();
  document.getElementById("prenotaForm").onsubmit = function (event) {
    event.preventDefault();
    const replicaId = replicaSelect.value;
    const quantita = document.getElementById("quantitaInput").value;
    prenotaReplica(replicaId, quantita, modal);
  };
}

// Funzione per effettuare una prenotazione
function prenotaReplica(replicaId, quantita, modal) {
  fetch(`/prenota/${replicaId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ quantita: quantita }),
  }).then((response) => {
    if (response.ok) {
      response.json().then((data) => {
        alert(data.message);
        modal.hide();
        window.location.href = "/prenotazioni";
      });
    } else {
      response.json().then((data) => {
        alert(data.error);
        if (
          data.error.includes("Hai già una prenotazione per questa replica")
        ) {
          modal.hide();
          window.location.href = "/prenotazioni";
        }
      });
    }
  });
}
