
const username_text_login = document.getElementById("username_text_login");

const username_bar_login = document.getElementById("username_bar_login");

const username_text_register = document.getElementById("username_text_register");

const username_bar_register = document.getElementById("username_bar_register");

const nav_link_login = document.getElementById("nav_link_login");

const nav_link_acccount = document.getElementById("nav_link_account");

const form_data_login = document.getElementById("form_data_login");

const form_data_register = document.getElementById("form_data_register");



if (form_data_login) {
    form_data_login.addEventListener("submit", function(e) {
        e.preventDefault();

        if (!username_bar_login.value) {
            username_text_login.innerText = "Please enter a username";
            username_text_login.style.border = "solid red";
            return;
        }

        fetch("/login_page", { 
            method: "POST",
            body: new FormData(form_data_login)
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                window.location.href = data.redirect;
            } else {
                username_text_login.innerText = "Invalid username";
                username_text_login.style.border = "solid red";
            }
        });
    });
}


if (username_bar_login) {
    username_bar_login.addEventListener("input", function() {
        username_text_login.innerText = "username";
        username_text_login.style.border = "none";
    });
}



if (form_data_register) {
    form_data_register.addEventListener("submit", function(e) {
        e.preventDefault();

        if (!username_bar_register.value) {
            username_text_register.innerText = "Please enter a username";
            username_text_register.style.border = "solid red";
            return;
        }

        fetch("/register_page", { 
            method: "POST",
            body: new FormData(form_data_register)
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === "success") {
                window.location.href = data.redirect;
            } else if (data.status === "empty"){
                username_text_register.innerText = "Please enter a username";
                username_text_register.style.border = "solid red";
            } else {
                username_text_register.innerText = "Username is already taken, please enter a new username";
                username_text_register.style.border = "solid red";
            }
        });
    });
}

if (username_bar_register) {
    username_bar_register.addEventListener("input", function() {
        username_text_register.innerText = "username";
        username_text_register.style.border = "none";
    });
}
        