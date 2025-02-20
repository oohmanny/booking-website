const loginButton = document.getElementById("loginButton");

loginButton.addEventListener("click", function(e) {
    e.preventDefault()
    fetch("/admin/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            adminUsername: document.getElementById('adminUsername').value,
            adminPassword: document.getElementById('adminPassword').value
        }),
        credentials: "include"
    })
    .then(response => 
        {
            if(response.ok)
                window.location.href = '/admin/dashboard';
        })
    })