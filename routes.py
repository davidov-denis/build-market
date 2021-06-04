import hashlib
import os

from flask import Flask, render_template, request, session, redirect, abort
from db import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"


def is_auth_admin():
    if "is_auth_admin" in session:
        if session["is_auth_admin"] == "true":
            return True
        else:
            return False
    else:
        return False


def category_list():
    categorys = []
    for category in select_all_categorys():
        categorys.append(category[1])
    return categorys


@app.route('/')
def index():
    products = select_all_products()
    categorys = select_all_categorys()
    print(categorys)
    return render_template("index.html", products=products, categorys=categorys)


@app.route("/add-to-cart/<product_id>")
def add_to_cart(product_id):
    if "cart" not in session:
        session["cart"] = {}
    cart_dict = session["cart"]
    if product_id in cart_dict:
        cart_dict[product_id] += 1
    else:
        cart_dict[product_id] = 1
    session["cart"] = cart_dict
    return "<script>window.history.back();</script>"


@app.route("/cart/", methods=["POST", "GET"])
def cart_view():
    if request.method == "POST":
        cart_products = select_all_cart_products(session["cart"])
        cart_products_quality = list(session["cart"].values())
        user_email = request.form.get("email")
        user_name = request.form.get("userName")
        user_surname = request.form.get("userSurname")
        price = request.form.get("price")
        order_id = create_order(user_email, user_name, user_surname, "Не подтверждён", price)
        print(int(order_id[0]))
        for cart_product_and_cart_product_quality in zip(cart_products, cart_products_quality):
            product_id, product_quality = cart_product_and_cart_product_quality[0][0], \
                                          cart_product_and_cart_product_quality[1]
            print(order_id[0], product_id, product_quality)
            add_product_to_order(order_id[0], product_id, product_quality)
            print(product_id, product_quality)
        session["cart"] = {}
    if "cart" in session:
        if len(session["cart"]) > 0:
            cart_products = select_all_cart_products(session["cart"])
            cart_products_quality = list(session["cart"].values())
            a = 0
            itog = 0
            for i in cart_products:
                itog += float(i[3]) * cart_products_quality[a]
                a += 1
            return render_template("cart.html", itog=itog, cart_products=cart_products,
                                   cart_products_quality=cart_products_quality, categorys=select_all_categorys())
        else:
            return render_template("cart.html", categorys=select_all_categorys())
    else:
        return render_template("cart.html", categorys=select_all_categorys())


@app.route("/<category_name>/")
def view_category(category_name):
    if category_name in category_list():
        products = select_all_category_by_name(category_name)
        return render_template("category.html", categorys=select_all_categorys(), products=products)
    else:
        return abort(404)


@app.route("/<category_name>/<product_id>")
def view_product(category_name, product_id):
    if category_name in category_list():
        product = select_product(category_name, product_id)[0]
        print(product)
        images = len(os.listdir(f"D:\\build-market\\static\\productImages\\{str(product[0])}"))
        return render_template("product.html", images=images, categorys=select_all_categorys(), product=product)
    else:
        return abort(404)


@app.route("/admin/update-status/<order_id>/<order_status>/")
def admin_update_status(order_id, order_status):
    if is_auth_admin():
        update_status(order_id, order_status)
        print(order_id, order_status)
        return redirect("/admin/orders/")
    else:
        return redirect("/admin/login/")


@app.route("/admin/delete-category/<category>/")
def admin_delete_category(category):
    print("category")
    if is_auth_admin():
        delete_category(category)
        return redirect("/admin/categorys/")
    else:
        return redirect('/admin/login/')


@app.route("/admin/categorys/")
def admin_categorys():
    if is_auth_admin():
        categorys = select_all_categorys()
        return render_template("admin/categorys.html", categorys=categorys)
    else:
        return redirect("/admin/login/")


@app.route("/admin/orders/<order_id>/")
def view_order(order_id):
    if is_auth_admin():
        order = select_order_by_id(order_id)
        if len(order) > 0:
            return render_template("admin/view_order.html", categorys=select_all_categorys(), order=order)
        else:
            abort(404, "<h2>Такого заказа нет</h2>")
    else:
        return redirect("/admin/login")


@app.route("/admin/logout/")
def admin_logout():
    session.pop("is_auth_admin", None)
    session.pop("role", None)
    session.pop("login", None)
    return redirect("/admin/login/")


@app.route("/admin/add-category/", methods=["POST", "GET"])
def admin_add_category():
    if is_auth_admin():
        if request.method == "POST":
            category = request.form.get("category")
            add_category(category)
        return render_template("admin/add-category.html", categorys=select_all_categorys())
    else:
        return redirect("/admin/login/")


@app.route("/admin/create-product/", methods=["POST", "GET"])
def admin_create_product_view():
    if is_auth_admin():
        categorys = select_all_categorys()
        if request.method == "POST":
            title = request.form.get("product-title")
            description = request.form.get("product-description")
            price = request.form.get("product-price")
            category = request.form.get("product-category")
            product_id = create_product(title, description, price, category)[0]
            os.mkdir("D:\\build-market\\static\\productImages" + f'\\{product_id}')
            for i in range(1, int(request.form.get("quality")) + 1):
                number = "img" + str(i)
                file = request.files[number]
                extension = file.filename.split(".")[-1]
                filename = str(i) + "." + extension
                file.save(os.path.join("static\\productImages" + f"\\{product_id}", filename))
        return render_template("admin/create-product.html", categorys=categorys)
    else:
        return redirect("/admin/login/")


@app.route("/admin/login/", methods=["POST", "GET"])
def admin_login_view():
    if not is_auth_admin():
        if request.method == "POST":
            login = request.form.get("email")
            password = request.form.get("password")
            password = hashlib.md5(password.encode()).hexdigest()
            user_data = select_password_with_login(login)
            if user_data:
                print(user_data)
                if user_data[2] == password and user_data[3] == "admin":
                    session["login"] = user_data[1]
                    session["is_auth_admin"] = "true"
                    session["role"] = "admin"
                    return redirect("/")
        return render_template("admin/login.html", categorys=select_all_categorys())
    else:
        return redirect("/")


@app.route("/admin/orders/")
def admin_orders():
    if is_auth_admin():
        orders = select_orders()
        return render_template("admin/orders.html", orders=orders)
    else:
        return redirect("/admin/login/")


if __name__ == '__main__':
    app.run(debug=True)
