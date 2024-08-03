# Little Lemon Restaurant API
This API provides various endpoints to manage the Little Lemon Restaurant's menu, categories, cart, orders, and user groups. It is built using Django and Django REST Framework and includes authentication and authorization features.

## Endpoints

### Categories
- GET /api/categories/: Retrieve a list of all categories.
- POST /api/categories/: Create a new category.
- GET /api/categories/<pk>/: Retrieve a specific category by its primary key.
- PUT /api/categories/<pk>/: Update a specific category by its primary key.
- PATCH /api/categories/<pk>/: Partially update a specific category by its primary key.
- DELETE /api/categories/<pk>/: Delete a specific category by its primary key.

### Menu Items
- GET /api/menu-item/: Retrieve a list of all menu items.
- POST /api/menu-item/: Create a new menu item.
- GET /api/menu-item/<pk>/: Retrieve a specific menu item by its primary key.
- PUT /api/menu-item/<pk>/: Update a specific menu item by its primary key.
- PATCH /api/menu-item/<pk>/: Partially update a specific menu item by its primary key.
- DELETE /api/menu-item/<pk>/: Delete a specific menu item by its primary key.

### Cart
- GET /api/cart/menu-item/: Retrieve the cart items for the authenticated user.
- POST /api/cart/menu-item/: Add an item to the cart.
- DELETE /api/cart/menu-item/: Remove an item from the cart or clear the cart.

### Orders
- GET /api/orders/: Retrieve a list of orders for the authenticated user or all orders for admin and manager users.
- POST /api/orders/: Place a new order.
- GET /api/orders/<pk>/: Retrieve a specific order by its primary key.
- PATCH /api/orders/<pk>/: Update the status of a specific order by its primary key.
- PUT /api/orders/<pk>/: Assign a delivery crew to a specific order.
- DELETE /api/orders/<pk>/: Delete a specific order by its primary key.

### User Groups
- Manager Group: Manage manager group members.
    - GET /api/groups/manager/users: List users in the manager group.
    - POST /api/groups/manager/users: Add a user to the manager group.
    - DELETE /api/groups/manager/users: Remove a user from the manager group.

- Delivery Crew Group: Manage delivery crew group members.
    - GET /api/groups/delivery-crew/users: List users in the delivery crew group.
    - POST /api/groups/delivery-crew/users: Add a user to the delivery crew group.
    - DELETE /api/groups/delivery-crew/users: Remove a user from the delivery crew group.

## Querying Menu Items
- You can filter menu items by category, title, price, and featured status using query parameters:
    - Example: GET /api/menu-item/?category=Appetizers&featured=true

## Authentication and Authorization
The API uses JWT for authentication. Users can obtain, refresh, and verify tokens using endpoints provided by djoser.

## Permissions
- Categories & Menu Items: Authenticated users can retrieve, but only managers and admins can create, update, or delete.
- Cart: Only customers can manage their cart items.
- Orders: Orders can be placed by customers. Admins, managers, and delivery crew members have specific permissions for order management.
- User Groups: Only admins and managers can manage user groups.

## Swagger Documentation
You can explore the API documentation using Swagger UI:

URL: 'http://localhost:8000/swagger/'
Description: Swagger UI provides interactive documentation for exploring the endpoints and testing the API directly from your browser.

## Request and Response Formats
- Requests should be in JSON format.
- Responses will be in JSON format.

### Sample Objects

#### Category Object
```json
{
  "id": 1,
  "title": "Appetizers",
  "slug": "appetizers"
}
```

#### Menu Item Object
```json
{
  "id": 1,
  "title": "Caesar Salad",
  "price": "10.00",
  "featured": true,
  "category": 1
}
```

#### Cart Object
```json
{
  "id": 1,
  "user": 1,
  "menu_item": 1,
  "quantity": 2,
  "unit_price": "10.00",
  "price": "20.00"
}
```

#### Order Object
```json
{
  "id": 1,
  "user": 1,
  "delivery_crew": 2,
  "status": false,
  "total": "30.00",
  "date": "2024-08-03"
}
```