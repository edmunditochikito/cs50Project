import {getCookie} from "../utils.js"
document.addEventListener("DOMContentLoaded", () => {

    const logoutButton = document.querySelector("#logout");
    if(logoutButton){
        logoutButton.addEventListener("click", async (event) => {
            event.preventDefault();
    
            try {
                // Obtener el token CSRF de la cookie
                const csrfToken = getCookie("csrf_access_token")
    
                // Enviar la solicitud POST a /logout con el token CSRF
                const response = await axios.post("/logout", {}, {
                    headers: {
                        "X-CSRF-TOKEN": csrfToken,
                    }
                });
    
                if (response.data.status === "success") {
                    // Mostrar mensaje de despedida
                    Swal.fire({
                        icon: 'success',
                        title: 'Sesión cerrada',
                        text: '¡Hasta luego!',
                        timer: 3000, // Se cierra automáticamente después de 3 segundos
                        showConfirmButton: false
                    }).then(() => {
                        // Redirigir a la página de inicio después de que se cierra el mensaje
                        window.location.href = "/";
                    });
                } else {
                    console.error("Error al cerrar sesión:", response.data.message);
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: response.data.message || 'No se pudo cerrar sesión. Intenta nuevamente.'
                    });
                }
            } catch (error) {
                console.error("Error en la solicitud de cierre de sesión:", error);
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Hubo un problema al cerrar la sesión. Intenta nuevamente.'
                });
            }
        });
    }

});
