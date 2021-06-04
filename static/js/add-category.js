function checkCategory(){
    let category = document.getElementById("category").value;
    let form = document.getElementById("categotyForm");
    if (category === ""){
        alert("Не заполнена категория товара")
    } else{
        form.submit()
    }
}