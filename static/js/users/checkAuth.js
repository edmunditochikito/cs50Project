import {getCookie} from "../utils.js"


document.addEventListener("DOMContentLoaded", function () {
    const reservationsLink = document.getElementById("reservations-link");
    
    reservationsLink.addEventListener("click", function (event) {
        // Evita la acción predeterminada del enlace
        event.preventDefault();

        // Lógica para verificar si el usuario está autenticado
        
        let isAuthenticated= getCookie("csrf_access_token")
        
        if (!isAuthenticated) {
            // Muestra un mensaje de alerta
            Swal.fire({
                icon: 'warning',
                title: 'No has iniciado sesión',
                text: 'Por favor, inicia sesión para continuar.',
                showConfirmButton: true,
                confirmButtonText:"Iniciar sesion"
                 
            }).then((confirm) => {
                // Redirige a la página de inicio de sesión
                if(confirm){
                    window.location.href = '/Login';
                }
            });
        } else {
            // Si está autenticado, permite la navegación normal
            window.location.href = '/reservations';
        }
    });
});
