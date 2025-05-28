function confirmarEliminacion(id){
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
          confirmButton: 'btn btn-success',
          cancelButton: 'btn btn-danger'
        },
        buttonsStyling: false
      })
      
      swalWithBootstrapButtons.fire({
        title: '¿Está seguro?',
        text: "¡No podrás revertir esto!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '¡Sí, bórralo!',
        cancelButtonText: '¡No, Cancela!',
        reverseButtons: true
      }).then((result) => {
        if (result.isConfirmed) {
             //redirigir al usuario a la ruta de eliminar

           window.location.href ="/eliminar_Producto/"+id+"/";
           
          swalWithBootstrapButtons.fire(
             
            '¡Eliminado!',
            'Su archivo ha sido eliminado.',
            'success'
          )
          
        } else if (
          /* Read more about handling dismissals below */
          result.dismiss === Swal.DismissReason.cancel
        ) {
          swalWithBootstrapButtons.fire(
            'Cancelado',
            'Tu archivo imaginario está a salvo :)',
            'error'
          )
        }
      })

}