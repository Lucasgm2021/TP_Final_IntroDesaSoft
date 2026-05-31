function comprar_porsche() {
    alert("100 virus detectados!!!");
}

const selectFecha = document.getElementById('fechaReservaCreacion');
if (selectFecha) {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const formattedDate = `${year}-${month}-${day}`;
    selectFecha.setAttribute('min', formattedDate);
}
