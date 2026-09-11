# Fashion Store

A full-stack fashion e-commerce web application built with Django, Python, HTML, CSS, JavaScript, and MySQL.

## Project Overview

Fashion Store is an online shopping platform designed to provide a simple and user-friendly fashion shopping experience.

Users can browse products, search and filter products, view product details, add items to their cart, manage quantities, enter delivery addresses, place orders, and view their previous orders.

The project also includes a Django Admin panel for managing products, categories, stock, and orders.

## Features

### User Features

- User registration and login
- User profile
- Browse fashion products
- Shop by category
- Product search
- Product filtering
- Product sorting
- Product detail pages
- Sale products section
- Add products to cart
- Increase or decrease cart quantity
- Remove products from cart
- Stock availability validation
- Checkout
- Save delivery addresses
- Place orders
- Order confirmation
- View previous orders
- View individual order details
- Contact page

### Admin Features

- Manage products
- Manage product categories
- Manage product prices
- Manage sale prices
- Manage product stock
- Manage customer orders
- Manage users and addresses

## Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- Django

### Database

- MySQL

### Other Tools

- Git
- GitHub
- Django Admin
- VS Code

## Product Categories

The application includes:

- Women
- Men
- Children
- Bags
- Shoes

## Project Structure

```text
FashionStore/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── media/
│   ├── categories/
│   ├── hero/
│   ├── products/
│   └── trends/
│
├── store/
│   ├── migrations/
│   ├── templates/
│   │   └── store/
│   ├── static/
│   │   └── store/
│   │       ├── css/
│   │       └── js/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md