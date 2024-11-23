import { updateDatatable, createDatatable, getCookie } from "../utils.js";
import { valid } from "./add_table.js";
document.addEventListener("DOMContentLoaded", async (e) => {
  createDatatable({
    id: "Tabla",
    ajaxUrl: {
      url: "/admin/getTables",
      type: "GET",
    },
    searchBuilder: true,
    buttons: true,
    columns: [
      { data: "code", className: "text-center" },
      { data: "capacity", className: "text-center" },
      { data: "type", className: "text-center" },
      {
        data: "availabillity",
        className: "text-center",
        render: function (data, type, row, meta) {
            console.log(data)
          if (data) {
            return "disponible";
          } else {
            return "fuera de servicio";
          }
        },
      },
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
  let inputs = document.querySelectorAll("input");
  inputs.forEach((input) => {
    input.addEventListener("blur", valid);
  });
});

window.openModal = async (data) => {
  let modalElement = document.querySelector(".modal");
  let modal = new bootstrap.Modal(modalElement);
  let form = modalElement.querySelector("form");
  console.log(data);

  modalElement.removeEventListener("hidden.bs.modal", handleModalClose);

  modalElement.addEventListener("hidden.bs.modal", handleModalClose);

  // Obtén los datos y muestra el modal
  let response = await axios.get("/admin/getTable/" + data);
  let responseData = response.data;
  populateModal(form, responseData);

  //   form.removeEventListener("submit", sweetConfirmUpdate);
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    let invalidFields = form.querySelectorAll(".is-invalid");

    if (invalidFields.length > 0) {
      invalidFields[0].focus();
      return;
    }
     sweetConfirmUpdate(data);
    modal.hide();
  });

  modal.show();
};

function populateModal(form, data) {
  let inputs = form.querySelectorAll("input");
  let type = form.querySelector("#type");
  let availabillity = form.querySelector("#availabillity");
  console.log(availabillity.value)
  inputs.forEach((input) => {
    input.value = data[input.id];
  });
  type.value = data[type.id];
  availabillity.value = data[availabillity.id];
  console.log(availabillity.value)
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
      title: "¿Estas seguro de que deseas actualizar esta mesa",
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
            updateTable(id);
          },
        });
      }
    });
  };
  async function updateTable (id)  {

    try {
      const formData = new FormData(document.querySelector("form"));
      const response = await axios.post("/admin/updateTable/"+id,formData);
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
        updateDatatable("/admin/getTables");
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
      title: "¿Estas seguro de que deseas desactivar esta mesa?",
      showCancelButton: true,
      cancelButtonText: "Cancelar",
      confirmButtonText: "Desactivar",
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
      let response=await axios.post("/admin/deactivate-table/"+id)
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
        updateDatatable("/admin/getTables");
      } else {
        console.error("Error al Eliminar el producto:", data.message);
      }
    } catch (error) {
      console.error("Error al Eliminar el Producto:", error);
    }
  };