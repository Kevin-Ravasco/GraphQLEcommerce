# Django Ecommerce API
### Summary
This project is an ecommerce API built using the following
technologies:
- Python 3.9.10
- Django 3.2.9
- GraphQL

### Features
###### Authentication 
- Register
- Login
- Password Reset
- Email Verification on Sign Up
- Password Reset
- Password Change
- Archive Account
- Delete Account
- Secondary Emails
- Secondary Email Verification
- Swap Emails (Primary and Secondary)
- Remove Secondary Email

###### Products
- Product Categories 
- Add Product Categories
- List Product Categories
- Add Products
- List Products
- Multipe images for products
- Delete Product

###### Orders
- Create user order
- Add / Remove to Cart
- Delete to order
- Order status (Pending, Out for Delivery, Delivered)
- Shipping information


### How to Run
- Clone the project
- Create a virtual environment
- Install requirement `pip install -r requirements.txt`
- Create A Postgres Database.
- Create a `.env` file and copy contents of `example.env` into it
- Update the contents of the local DB settings in the `.env` file
  to match your local postgres db credentials
- Run server:
```shell
python manage.py runserver
```
- Go to `/grahpql`

