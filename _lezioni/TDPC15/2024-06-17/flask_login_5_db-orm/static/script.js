// Per precauzione, attivo il toast solo dopo che la pagina è stata caricata completamente
document.addEventListener('DOMContentLoaded', () => {

    // Il seguente codice l'ho preso da:
    // https://getbootstrap.com/docs/5.3/components/toasts/#usage
    // Questo serve per far funzionare il toast Bootstrap.

    const toastElList = document.querySelectorAll('.toast')
    const toastList = [...toastElList].map(toastEl => new bootstrap.Toast(toastEl, {
        autohide: true,  // Si nasconde automaticamente dopo 'delay' tempo
        delay: 5000      // in millisecondi ( == 5 secondi )
    }).show());

});


