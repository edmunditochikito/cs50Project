import {createDatatable} from '../utils.js'
document.addEventListener("DOMContentLoaded",async(e)=>{
    let response= await axios.get("/admin/getDishes");
    let data=response.data;
    console.log(data)
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
          { data: "price", className: "text-center" },
          { data: "description", className: "text-center" },
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
            return `<button class="btn btn-sm btn-danger remove-btn" onclick=""><i class="bi bi-trash"></i></button>
            <button class="btn btn-sm btn-primary edit-btn" onclick=""><i class="bi bi-pencil"></i></button>`;
          },
        },
        columnsExport: [0, 1, 2, 3, 4],
        columnsPrint: [0, 1, 2, 3, 4],
      });
})