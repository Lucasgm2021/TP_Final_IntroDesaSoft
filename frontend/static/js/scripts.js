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