let num = 1;
let $add = document.getElementsByClassName('add')[0];
let $form = document.getElementsByClassName('formm')[0];
$add.addEventListener('click', function (event) {
    let $input = document.createElement('input');
    $input.type = 'file';
    $input.placeholder = `Фото ${num}`;
    $input.name = `img${num}`
    $input.classList.add('form-group');
    $input.style = "width: 100%;!important"
    $input.accept = ".jpg"
    $form.insertBefore($input, $add);
    document.getElementById("quality").value = num;
    num = num + 1;
});

function chekProduct() {
    let productTitle = document.getElementById("product-title").value;
    let productDescription = document.getElementById("product-description").value;
    let productPrice = document.getElementById("product-price").value;
    let imageProducts = parseInt(document.getElementById("quality").value);
    let form = document.getElementById('create-product-form');
    if (productTitle === "") {
        alert("Не добавленно название товара")
    } else if (productDescription === "") {
        alert("Не добавленно описание товара")
    } else if (productPrice === "") {
        alert("Не добавленна цена товара")
    } else if (imageProducts < 1) {
        alert("Не добавленно ни одно фото")
    } else {
        form.submit()
    }
}