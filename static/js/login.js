function check() {
    let reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    let email = document.getElementById("userEmail").value;
    let password = document.getElementById("password").value;
    let form = document.getElementById("loginForm");
    if (email === "" && password === "") {
        alert("Не введён пароль и email")
    } else if (password === ""){
        alert("Не введён пароль");
    } else if (email === ""){
        alert("Не введён email");
    } else if (reg.test(email) === false){
        alert("Не верный email");
    } else {
        form.submit()
    }
}