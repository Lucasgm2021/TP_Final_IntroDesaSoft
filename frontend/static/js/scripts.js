function comprar_porsche() {
    alert("100 virus detectados!!!");
}

function editarPlato(id){

    window.location.href =
        `/dashboard/menu?edit=${id}`
}

function eliminarPlato(id){

    window.location.href =
        `/dashboard/menu?eliminar=${id}`
}

function editarReserva(id) {
    window.location.href = `/dashboard/reservas?edit=${id}`;
}

function eliminarReserva(id) {
    window.location.href = `/dashboard/reservas?eliminar=${id}`;
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
        console.log(`/dashboard/reseñas?desaprobar=${id}`)
    } else {
        window.location.href = `/dashboard/reseñas?aprobar=${id}`;
        console.log(`/dashboard/reseñas?desaprobar=${id}`)
    }
}