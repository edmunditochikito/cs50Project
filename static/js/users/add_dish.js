import { toastMessage, showAlert } from "../utils.js";

// Función para inicializar el formulario
export function initializeAddDishForm() {
  document.addEventListener("DOMContentLoaded", async (e) => {
    let select = document.querySelector("select");
    let response = await axios.post("/categories");
    let data = response.data;
    data.forEach((category) => {
      let option = document.createElement("option");
      option.value = category.id;
      option.text = category.name;
      select.appendChild(option);
    });

    let form = document.querySelector("form");
    let textarea = document.querySelector("textarea");

    let inputs = document.querySelectorAll("input");
    inputs.forEach((input) => {
      input.addEventListener("blur", valid);
    });
    textarea.addEventListener("blur", valid);

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      let invalidFields = form.querySelectorAll(".is-invalid");
      if (invalidFields.length > 0) {
        invalidFields[0].focus();
        return;
      }

      let formData = new FormData();

      inputs.forEach((input) => {
        if (input.type === "file") {
          formData.append(input.id, input.files[0]);
        } else {
          formData.append(input.id, input.value);
        }
      });

      formData.append(textarea.id, textarea.value);
      formData.append("categories_id", select.value);

      try {
        let response = await axios.post("/admin/add_dish", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        let data = response.data;
        toastMessage(data.status, data.message);
        if (data.status == "success") {
          e.target.reset();
          let form_inputs_ = form.querySelectorAll(".is-valid");
          form_inputs_.forEach((input) => {
            input.classList.remove("is-valid");
            if (input.id == "name") input.focus();
          });
        }
      } catch (err) {
        console.error(err);
      }
    });
  });
}

// Función de validación exportada
export function valid(e) {
  if (e.target.id == "price") {
    let message = "";
    if (!/^\d{1,4}$/.test(e.target.value)) {
      
      message = "Cantidad invalida";
    }
    showAlert(e.target, message);
  }

  if (e.target.id == "name") {
    let message = "";
    if (!/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s.,;!?'"-]{1,40}$/.test(e.target.value)) {
      message = "Nombre no valido";
    }
    showAlert(e.target, message);
  }

  if (e.target.id == "description") {
    let message = "";
    if (!/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s.,;!?'"-]{1,160}$/.test(e.target.value)) {
      message = "Descripcion no valida";
    }
    showAlert(e.target, message);
  }
  if (e.target.id == "image") {
    let message = "";
    if (e.target.value.trim() == "") {
      message = "Debe seleccionar una imagen";
    }
    showAlert(e.target, message);
  }
}

if (window.location.href=="http://127.0.0.1:3000/admin/add_dish") {
  initializeAddDishForm();
}
