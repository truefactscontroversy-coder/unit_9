const login_btn = document.getElementById("login_button");
const register_btn = document.getElementById("register_button");



login_btn.addEventListener("click", () => {
    window.location.href = "/templates/login.html";
});

register_btn.addEventListener("click", () => {
    window.location.href = "/templates/register.html";
});