// Variable para rastrear la tarjeta actualmente abierta
let openCard = null;

// Seleccionar todas las tarjetas
document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('click', () => {
        // Si hay una tarjeta abierta y no es la misma que se hizo clic, ciérrala
        if (openCard && openCard !== card) {
            openCard.classList.remove('show');
        }

        // Alternar la clase 'show' en la tarjeta actual
        card.classList.toggle('show');

        // Actualizar la tarjeta abierta o dejarla en null si se cerró
        openCard = card.classList.contains('show') ? card : null;
    });
});
