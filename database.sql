create database reservaya;
use reservaya;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password TEXT,
    phone VARCHAR(20),
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    role ENUM('administrator', 'buyer') DEFAULT 'buyer'
);

CREATE TABLE login_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,  -- Relaciona con el user_id del usuario
    login_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

create table tables (
id INTEGER PRIMARY KEY auto_increment,
code INTEGER not null unique,
capacity INTEGER not null,
type ENUM('interior', 'exterior'),
availabillity boolean
);

CREATE TABLE  categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE dishes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    image VARCHAR(200),
    categories_id INT NOT NULL,
    FOREIGN KEY (categories_id) REFERENCES categories(id) 
);


create table orders(
id int primary key auto_increment,
special_request text
);

create table order_dish_join (
id int primary key auto_increment,
order_id int not null,
dish_id int not null,
quantity int not null,
foreign key (order_id) references orders (id),
foreign key (dish_id) references dishes (id)
);

CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    table_id INTEGER not null,
    reservation_date DATETIME NOT NULL,
    num_people INTEGER NOT NULL,
    special_requests TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    terms_and_conditions_accepted BOOLEAN DEFAULT FALSE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (table_id) REFERENCES tables(id)
);