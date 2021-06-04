function checkOrder(){
    let reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    let email = document.getElementById("userEmail").value;
    let name = document.getElementById("userName").value;
    let surname = document.getElementById("userSurname").value;
    let form = document.getElementById("orderForm");
    if (email === "" && name === "" && surname === "") {
        alert("Данные не введены")
    } else if (email === ""){
        alert("Не введён email");
    } else if (name === ""){
        alert("Не введёно имя");
    } else if (surname === ""){
        alert("Не введена фамилия")
    } else if (reg.test(email) === false){
        alert("Не верный email");
    } else {
        form.submit()
        alert("Спасибо за заказ. Мы свяжемся с вами по указанной почте")
    }
}