CREATE TABLE `products`(
    `id` integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    `title` varchar(250),
    `description` text,
    `price` text,
    `category` text
);

CREATE TABLE `users`(
    `id` integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    `email` varchar(250) unique,
    `password` text,
    `role` text
);

CREATE TABLE `categorys`(
    `id` integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    `category` varchar(250) unique
);


CREATE TABLE `orders`(
    `id` integer PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    `userEmail` text,
    `userName` text,
    `userSurname` text,
    `orderStatus` text
);

CREATE TABLE `orderIdProductId`(
    `id` integer primary key autoincrement not null unique,
    `orderId` integer,
    `productId` integer,
    `quality` integer,
    FOREIGN KEY (orderId) REFERENCES orders(id),
    FOREIGN KEY (productId) REFERENCES products(id)
);