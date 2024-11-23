import { showAlert,getCookie,toastMessage } from "../utils.js";
function initializeAddTableForm(){

  document.addEventListener("DOMContentLoaded", async (e) => {
    let form = document.querySelector("form");
    let inputs = form.querySelectorAll("input");
    let select = document.querySelector("select")
    inputs.forEach((input) => {
      input.addEventListener("blur", valid);
    });
  
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
  
      let invalidFields = form.querySelectorAll(".is-invalid");
      if (invalidFields.length > 0) {
        invalidFields[0].focus();
        return;
      }
      let inputData = {};
      inputs.forEach(input=>{
          inputData[input.id] = input.value;
      })
      inputData[select.id]=select.value;
      try{
          const csrfToken = getCookie("csrf_access_token");
          let response= await axios.post("/admin/add-table",inputData,{headers:{"X-CSRF-TOKEN":csrfToken}})
          let data=response.data
          toastMessage(data.status, data.message);
          if (data.status == "success") {
              e.target.reset();
              let form_inputs_ = form.querySelectorAll(".is-valid");
              form_inputs_.forEach((input) => {
                input.classList.remove("is-valid");
                if (input.id == "code") input.focus();
              });
            }
      }catch(e){
  
      }
    });
  
  });
}
export function valid(e) {
  if (e.target.id == "code") {
    let message = "";
    if (!/^\d{1,4}$/.test(e.target.value)) {
      message = "codigo invalido";
    }
    showAlert(e.target, message);
  }
  if (e.target.id == "capacity") {
    let message = "";
    if (!/^[2-8]$/.test(e.target.value)) {
      message = "Debe ser un numero entre 2 y 8";
    }
    showAlert(e.target, message);
  }
}
if (window.location.href=="http://127.0.0.1:3000/admin/add-table") {
  initializeAddTableForm();
}

