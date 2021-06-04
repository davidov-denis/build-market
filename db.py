import sqlite3


def update_status(order_id, order_status):
    conn = sqlite3.connect("D:\\build-market\\db.sqlite")
    cur = conn.cursor()
    cur.execute(f"UPDATE orders SET orderStatus='{order_status}' WHERE id={order_id}")
    cur.close()
    conn.commit()
    conn.close()


def delete_category(category):
    conn = sqlite3.connect("D:\\build-market\\db.sqlite")
    cur = conn.cursor()
    cur.execute(f"DELETE FROM categorys WHERE category='{category}'")
    cur.execute(f"DELETE FROM products WHERE category='{category}'")
    cur.close()
    conn.commit()
    conn.close()


def select_order_by_id(id):
    conn = sqlite3.connect("D:\\build-market\\db.sqlite")
    cur = conn.cursor()
    order = cur.execute(
        f"SELECT * FROM orderIdProductId INNER JOIN products p on p.id = orderIdProductID.productId WHERE orderId={id}").fetchall()
    cur.close()
    conn.close()
    return order


def select_orders():
    conn = sqlite3.connect("D:\\build-market\\db.sqlite")
    cur = conn.cursor()
    orders = cur.execute("SELECT * FROM orders").fetchall()
    cur.close()
    conn.close()
    return orders


def add_product_to_order(order_id, product_id, product_quality):
    conn = sqlite3.connect("D:\\build-market\\db.sqlite")
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO orderIdProductId(orderId, productId, quality) VALUES({int(order_id)}, {int(product_id)}, {int(product_quality)})")
    cur.close()
    conn.commit()
    conn.close()


def create_order(user_email, user_name, user_surname, orderStatus, price):
    conn = sqlite3.connect("D:\\build-market\\db.sqlite")
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO orders(userEmail, userName, userSurname, orderStatus, price) VALUES('{user_email}', '{user_name}', '{user_surname}', '{orderStatus}', '{price}')")
    cur.close()
    conn.commit()
    cur = conn.cursor()
    id = cur.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 1").fetchall()
    cur.close()
    conn.close()
    return id[0]


def select_product(category_name, product_id):
    conn = sqlite3.connect("D:\\build-market\\db.sqlite")
    cur = conn.cursor()
    product = cur.execute(f"SELECT * FROM products WHERE category='{category_name}' AND id='{product_id}'").fetchall()
    cur.close()
    conn.close()
    return product


def select_all_category_by_name(category_name):
    conn = sqlite3.connect("D:\\build-market\\db.sqlite")
    cur = conn.cursor()
    products = cur.execute(f"SELECT * FROM products WHERE category='{category_name}'").fetchall()
    cur.close()
    conn.close()
    return products


def select_all_categorys():
    conn = sqlite3.connect("D:\\build-market\\db.sqlite")
    cur = conn.cursor()
    categorys = cur.execute("SELECT * FROM categorys").fetchall()
    cur.close()
    conn.close()
    return categorys


def add_category(category):
    conn = sqlite3.connect("D:\\build-market\\db.sqlite")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO categorys(category) VALUES('{category}')")
    cur.close()
    conn.commit()
    conn.close()


def select_all_cart_products(cart_dict):
    conn = sqlite3.connect("D:\\build-market\\db.sqlite")
    cur = conn.cursor()
    ids = tuple(cart_dict.keys())
    if len(ids) > 1:
        cart_products = cur.execute(f"SELECT * FROM products WHERE id IN {ids}").fetchall()
    else:
        cart_products = cur.execute(f"SELECT * FROM products WHERE id={ids[0]}").fetchall()
    cur.close()
    conn.close()
    return cart_products


def select_all_products():
    conn = sqlite3.connect("D:\\build-market\\db.sqlite")
    cur = conn.cursor()
    products = cur.execute("SELECT * FROM products").fetchall()
    cur.close()
    conn.close()
    return products


def select_password_with_login(email):
    conn = sqlite3.connect("D:\\build-market\\db.sqlite")
    cur = conn.cursor()
    data = cur.execute(f'''SELECT * FROM users WHERE email="{email}" AND role="admin"''').fetchall()
    cur.close()
    conn.close()
    if len(data) >= 1:
        return data[0]
    else:
        return False


def create_user(email, password, role):
    conn = sqlite3.connect("D:\\build-market\\db.sqlite")
    cur = conn.cursor()
    try:
        cur.execute(f"INSERT INTO users(email, password, role) VALUES('{email}', '{password}', '{role}')")
    except sqlite3.IntegrityError:
        return False
    cur.close()
    conn.commit()
    conn.close()
    return True


def create_product(title, description, price, category):
    conn = sqlite3.connect("D:\\build-market\\db.sqlite")
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO products(title, description, price, category) VALUES('{title}', '{description}', '{price}', '{category}')")
    cur.close()
    conn.commit()
    cur = conn.cursor()
    id = cur.execute("SELECT * FROM products ORDER BY id DESC LIMIT 1").fetchall()
    cur.close()
    conn.close()
    return id[0]
