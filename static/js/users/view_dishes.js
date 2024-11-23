import { createDatatable,updateDatatable,getCookie } from "../utils.js";
import { valid } from "./add_dish.js";
const csrfToken = getCookie("csrf_access_token")
document.addEventListener("DOMContentLoaded", async (e) => {
  let select = document.querySelector("select");
  let response = await axios.post("/categories",{},{ headers: {
    "X-CSRF-TOKEN":csrfToken
  }},);
  let data = response.data;
  data.forEach((category) => {
    let option = document.createElement("option");
    option.value = category.id;
    option.text = category.name;
    select.appendChild(option);
  });

  createDatatable({
    id: "Tabla",
    ajaxUrl: {
      url: "/admin/getDishes",
      type: "GET",
      
    },
    searchBuilder: true,
    buttons: true,
    columns: [
      { data: "name", className: "text-center" },
      { data: "description", className: "text-center" },
      { data: "price", className: "text-center" },
      {
        title: "Acciones",
        className: "text-center",
        orderable: false,
        searchable: false,
      },
    ],
    buttonsEvents: {
      targets: -1,
      data: null,
      render: function (data, type, row, meta) {
        return `<button class="btn btn-sm btn-danger remove-btn" onclick="sweetConfirmDelete('${data.id}')"><i class="bi bi-trash"></i></button>
            <button class="btn btn-sm btn-primary edit-btn" onclick="openModal('${data.id}')"><i class="bi bi-pencil"></i></button>`;
      },
    },
    columnsExport: [0, 1, 2, 3, 4],
    columnsPrint: [0, 1, 2, 3, 4],
  });
  let textarea = document.querySelector("textarea");
  let inputs = document.querySelectorAll("input");
  inputs.forEach((input) => {
    input.addEventListener("blur", valid);
  });
  textarea.addEventListener("blur", valid);
});

window.openModal = async (data) => {
  let modalElement = document.querySelector(".modal");
  let modal = new bootstrap.Modal(modalElement);
  let form = modalElement.querySelector("form");

  modalElement.removeEventListener("hidden.bs.modal", handleModalClose);

  modalElement.addEventListener("hidden.bs.modal", handleModalClose);

  // Obtén los datos y muestra el modal
  let response = await axios.post("/admin/getDish",{ "id": data },
   { headers: {
      "X-CSRF-TOKEN":csrfToken
    }},);
  let responseData = response.data;
  populateModal(form, responseData);

  form.removeEventListener("submit",sweetConfirmUpdate)
  form.addEventListener("submit",(e)=>{
    e.preventDefault()
    let invalidFields = form.querySelectorAll(".is-invalid");

    if (invalidFields.length > 0) {
      invalidFields[0].focus();
      return;
    }
    sweetConfirmUpdate(data)
    modal.hide();
  })


  modal.show();
};

function populateModal(form, data) {
  let inputs = form.querySelectorAll("input");
  let textArea = form.querySelector("textarea");
  let select = form.querySelector("select");

  inputs.forEach((input) => {
    input.value = data[0][input.id];
  });
  textArea.value = data[0].description;
  select.value = data[0].category;
 
}

function handleModalClose(e) {
  let invalidelements = e.target.querySelectorAll(".is-invalid");
  let validelements = e.target.querySelectorAll(".is-valid");
  invalidelements.forEach((element) => {
    element.classList.remove("is-invalid");
  });
  validelements.forEach((element) => {
    element.classList.remove("is-valid");
  });
}

async function sweetConfirmUpdate (id) {
  Swal.fire({
    icon: "question",
    title: "¿Estas seguro de que deseas actualizar este platillo?",
    showCancelButton: true,
    cancelButtonText: "Cancelar",
    confirmButtonText: "Actualizar",
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: `<h4 class="fw-bold m-0">Actualizando...</h4>`,
        allowOutsideClick: false,
        timerProgressBar: true,
        didOpen: () => {
          Swal.showLoading();
          updateDish(id);
        },
      });
    }
  });
};

async function updateDish (id)  {

  try {
    const formData = new FormData(document.querySelector("form"));
    const response = await axios.post("/admin/updateDish/"+id,formData,{ headers: {
      "X-CSRF-TOKEN":csrfToken
    }},);
    const data=response.data
    console.log(data)

    if (response) {
      Swal.fire({
        position: "center",
        icon: data.status,
        title: data.title,
        text: data.message,
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
      });
      updateDatatable("/admin/getDishes");
    } else {
      console.error("Error al actualizar el proveedor:", data.message);
    }
  } catch (error) {
    console.error("Error al actualizar el proveedor:", error);
  }
};

window.sweetConfirmDelete = async (id) => {
  Swal.fire({
    icon: "warning",
    title: "¿Estas seguro de que deseas eliminar este Platillo?",
    showCancelButton: true,
    cancelButtonText: "Cancelar",
    confirmButtonText: "Eliminar",
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: `<h4 class="fw-bold m-0">Eliminando...</h4>`,
        allowOutsideClick: false,
        timerProgressBar: true,
        didOpen: () => {
          Swal.showLoading();
          deleteDish(id);
        },
      });
    }
  });
};

async function deleteDish(id){
  try {
    let response=await axios.post("/admin/deleteDish/"+id,{},{ headers: {
      "X-CSRF-TOKEN":csrfToken
    }},)
    let data=response.data
    console.log(response)
    
    if (response) {
      Swal.fire({
        position: "center",
        icon: data.status,
        title: data.title,
        text: data.message,
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
      });
      updateDatatable("/admin/getDishes");
    } else {
      console.error("Error al Eliminar el producto:", data.message);
    }
  } catch (error) {
    console.error("Error al Eliminar el Producto:", error);
  }
};