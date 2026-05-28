function comprar_porsche() {
    alert("100 virus detectados!!!");
}

function mostrarMesasDisponibles(){
    let fecha = document.querySelector("input[name='fecha']").value;
    let hora = document.querySelector("input[name='hora']").value;
    let ubicacion = document.querySelector("input[name='ubicacion']:checked").value;
    let nro_comensales = document.querySelector("input[name='comensales']").value;
    
    let formData = {
        fecha: fecha,
        hora: hora,
        ubicacion: ubicacion,
        nro_comensales: nro_comensales
    }
    sessionStorage.setItem('savedFormDataReserva', JSON.stringify(formData));
    window.location.href = window.location.pathname + "?mesas=true&fecha=" + fecha + "&hora=" + hora + "&ubicacion=" + ubicacion + "&comensales=" + nro_comensales
}

window.addEventListener('DOMContentLoaded', () => {
    const savedData = sessionStorage.getItem('savedFormDataReserva');
    
    if (savedData) {
        const formData = JSON.parse(savedData);
        document.querySelector('input[name="fecha"]').value = formData.fecha;
        document.querySelector('input[name="hora"]').value = formData.hora;
        console.log("Data retrieved from locker:", formData);
        const radioToCheck = document.querySelector(`input[name="ubicacion"][value="${formData.ubicacion}"]`);
        console.log("Radio to check:", radioToCheck);
        if (radioToCheck) {
            radioToCheck.checked = true;
        }

        document.querySelector('input[name="comensales"]').value = formData.nro_comensales;
        sessionStorage.removeItem('savedFormDataReserva');
    }
});