document.getElementById("profileForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const data = {
        name: document.getElementById("name").value,
        phone: document.getElementById("phone").value,
        password: document.getElementById("password").value
    };
    fetch("/profile", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error("Error al actualizar perfil:", error));
});