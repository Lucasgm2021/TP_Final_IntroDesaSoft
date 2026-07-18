const selectFecha = document.getElementById('fechaReservaCreacion');
if (selectFecha) {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const formattedDate = `${year}-${month}-${day}`;
    selectFecha.setAttribute('min', formattedDate);
}

function togglePopup(id_reserva) {
    const popup = document.getElementById('my-popup-overlay');
    if (id_reserva) {
        const hidden_reseña = document.getElementById(`hidden-reseña-${id_reserva}`)
        const fecha = hidden_reseña.getElementsByClassName("fecha")[0].textContent
        const comentario = hidden_reseña.getElementsByClassName("comentario")[0].textContent
        const calificacion = hidden_reseña.getElementsByClassName("calificacion")[0].textContent
        popup.getElementsByTagName("strong")[0].textContent = `${calificacion}/5`
        popup.getElementsByClassName("reseña-fecha")[0].textContent = `Fecha: ${fecha}`
        popup.getElementsByClassName("reseña-comentario")[0].textContent = comentario
        const porcentaje = calificacion * 20
        popup.getElementsByClassName("estrellas-progreso")[0].style.width = `${porcentaje}%` 
    }
    popup.hidden = !popup.hidden;
}