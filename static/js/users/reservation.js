document.addEventListener("DOMContentLoaded", () => {
  const reservationForm = document.getElementById("reservationForm");

  reservationForm.addEventListener("submit", async (event) => {
      event.preventDefault(); // Evita el envío del formulario por defecto

      // Obtiene los valores de los campos del formulario
      const reservationDate = document.getElementById("reservation_date").value;
      const reservationTime = document.getElementById("reservation_time").value;
      const numPeople = document.getElementById("number_of_people").value;
      const tableType = document.getElementById("table_type").value;
      const specialRequests = document.getElementById("special_requests").value;
      const termsAccepted = document.getElementById("terms_and_conditions").checked;
      const emailConfirmation = document.getElementById("email_confirmation").checked;
      const tableNumber = document.getElementById("table_number").value;

      // Valida los campos
      let isValid = true;
      let errorMessage = '';

      // Validación de la fecha y hora de la reservación
      if (!reservationDate) {
          errorMessage += "La fecha de la reservación es requerida.\n";
          isValid = false;
      }
      if (!reservationTime) {
          errorMessage += "La hora de la reservación es requerida.\n";
          isValid = false;
      }

      // Validación del número de personas
      if (numPeople < 1) {
          errorMessage += "El número de personas debe ser al menos 1.\n";
          isValid = false;
      }

      // Validación del tipo de mesa
      if (!tableType) {
          errorMessage += "El tipo de mesa es requerido.\n";
          isValid = false;
      }

      // Validación de aceptación de términos y condiciones
      if (!termsAccepted) {
          errorMessage += "Debes aceptar los términos y condiciones.\n";
          isValid = false;
      }

      // Mostrar mensajes de error si hay validaciones fallidas
      if (!isValid) {
          alert(errorMessage);
          return; // Detiene el envío del formulario
      }

      // Si todos los campos son válidos, procede a enviar el formulario como JSON
      const reservationData = {
          reservation_date: reservationDate,
          reservation_time: reservationTime,
          num_people: numPeople,
          table_type: tableType,
          special_requests: specialRequests,
          terms_and_conditions_accepted: termsAccepted,
          email_confirmation: emailConfirmation,
          table_number: tableNumber // Asegúrate de tener este campo en tu HTML
      };

      try {
          const response = await fetch('/reservations', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json' // Especifica que se envían datos JSON
              },
              body: JSON.stringify(reservationData) // Convierte el objeto a JSON
          });

          if (!response.ok) {
              const errorResponse = await response.json();
              throw new Error(errorResponse.message);
          }

          const data = await response.json();
          alert('Reserva creada con éxito: ' + data.message); // Manejo de la respuesta
          reservationForm.reset(); // Opcional: reinicia el formulario
      } catch (error) {
          alert('Error al crear reserva: ' + error.message);
      }
  });
});
