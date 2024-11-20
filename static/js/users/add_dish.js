import { toastMessage,showAlert,} from "../utils.js";


document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("addDishForm");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Capturar los valores de los campos
    const name = document.getElementById("name");
    const price = document.getElementById("price");
    const description = document.getElementById("description");
    const category = document.getElementById("category");
    const image = document.getElementById("image");

    let valid = true;

    // Validar cada campo
    if (!name.value.trim()) {
      showAlert(name, "El nombre es obligatorio.");
      valid = false;
    } else {
      showAlert(name, "");
    }

    if (!price.value || isNaN(price.value) || price.value <= 0) {
      showAlert(price, "El precio debe ser un número positivo.");
      valid = false;
    } else {
      showAlert(price, "");
    }

    if (!description.value.trim()) {
      showAlert(description, "La descripción es obligatoria.");
      valid = false;
    } else {
      showAlert(description, "");
    }

    if (!category.value.trim()) {
      showAlert(category, "La categoría es obligatoria.");
      valid = false;
    } else {
      showAlert(category, "");
    }

    if (!valid) {
      toastMessage("error", "Por favor, corrige los errores antes de enviar.");
      return;
    }

    // Enviar datos al servidor
    const formData = new FormData(form);
    try {
      const response = await fetch("/dishes/add", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      if (response.ok) {
        toastMessage("success", "Platillo agregado exitosamente.");
        form.reset();
      } else {
        toastMessage("error", result.message || "Ocurrió un error.");
      }
    } catch (error) {
      toastMessage("error", "Error al enviar los datos.");
    }
  });
});
