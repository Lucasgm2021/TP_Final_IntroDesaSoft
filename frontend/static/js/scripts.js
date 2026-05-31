function comprar_porsche() {
    alert("100 virus detectados!!!");
}

function mostrarMesasDisponibles(){
    let fecha = document.querySelector("input[name='fecha']").value;
    let hora = document.getElementById("horarios-select").value;
    let ubicacion = document.querySelector("input[name='ubicacion']:checked").value;
    let nro_comensales = document.querySelector("input[name='comensales']").value;
    
    let formData = {
        fecha: fecha,
        hora: hora,
        ubicacion: ubicacion,
        nro_comensales: nro_comensales
    }
    sessionStorage.setItem('savedFormDataReserva', JSON.stringify(formData));
    window.location.href = window.location.pathname + "?fecha=" + fecha + "&hora=" + hora + "&ubicacion=" + ubicacion + "&comensales=" + nro_comensales
}

window.addEventListener('DOMContentLoaded', () => {
    const savedData = sessionStorage.getItem('savedFormDataReserva');
    
    if (savedData) {
        const formData = JSON.parse(savedData);
        document.querySelector('input[name="fecha"]').value = formData.fecha;
        document.getElementById("horarios-select").value = formData.hora;
        const radioToCheck = document.querySelector(`input[name="ubicacion"][value="${formData.ubicacion}"]`);
        if (radioToCheck) {
            radioToCheck.checked = true;
        }

        document.querySelector('input[name="comensales"]').value = formData.nro_comensales;
        sessionStorage.removeItem('savedFormDataReserva');
    }
});

const selectFecha = document.getElementById('fechaReservaCreacion');
if (selectFecha) {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const formattedDate = `${year}-${month}-${day}`;
    selectFecha.setAttribute('min', formattedDate);
}
