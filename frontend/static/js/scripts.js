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


function editarPlato(id){

    window.location.href =
        `/dashboard/menu?edit=${id}`
}

function eliminarPlato(id){

    window.location.href =
        `/dashboard/menu?eliminar=${id}`
}

function volverAlInicio() {
    window.location.href = '/';
}


function editarReserva(id){

    window.location.href =
        `/dashboard/reservas?edit=${id}`
}

function editarUsuario(id) {
    window.location.href = `/dashboard/usuarios?edit=${id}`;
}

function eliminarUsuario(id) {
    window.location.href = `/dashboard/usuarios?eliminar=${id}`;
}

function editarInfo(clave) {
    window.location.href = `/dashboard/configuracion/?edit=${clave}`;
}

function eliminarInfo(clave) {
    window.location.href = `/dashboard/configuracion/?eliminar=${clave}`;
}

function toggleResenia(id, aprobada) {
    if (aprobada) {
        window.location.href = `/dashboard/reseñas?desaprobar=${id}`;
    } else {
        window.location.href = `/dashboard/reseñas?aprobar=${id}`;
    }
}