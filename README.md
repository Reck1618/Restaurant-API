# Little Lemon API
The Little Lemon API is an API for the Little Lemon restaurant. Little Lemon's management wants to have an online-based order management system and mobile application. The LittleLemonAPI is the back-end API that allows customers to browse food items, view the item of the day and place orders. Managers are able to update the item of the day and monitor orders and assign deliveries. The delivery crew are able to check the orders assigned to them and update an order once it is delivered.

# Features
User groups, It contains two user groups (Manager and delivery crew) and some random users assigned to these groups from the Django admin panel.

Manager

Delivery crew

Users not assigned to a group will be considered customers.

This API makes it possible for end-users to perform certain tasks. It has the following functionalities.

The admin can assign users to the manager group

You can access the manager group with an admin token

The admin can add menu items

The admin can add categories

Managers can log in

Managers can update the item of the day

Managers can assign users to the delivery crew

Managers can assign orders to the delivery crew

The delivery crew can access orders assigned to them

The delivery crew can update an order as delivered

Customers can register

Customers can log in using their username and password and get access tokens

Customers can browse all categories

Customers can browse all the menu items at once

Customers can browse menu items by category

Customers can paginate menu items

Customers can sort menu items by price

Customers can add menu items to the cart

Customers can access previously added items in the cart

Customers can place orders

Customers can browse their own orders
