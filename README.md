# Little Lemon Restaurant API
This API provides various endpoints to manage the Little Lemon Restaurant's menu, categories, cart, orders, and user groups. It is built using Django and Django REST Framework and includes authentication and authorization features.

## Endpoints

### Categories
- `GET /api/v1/categories/`: Retrieve a list of all categories.
- `POST /api/v1/categories/`: Create a new category.
- `GET /api/v1/categories/<pk>/`: Retrieve a specific category by its primary key.
- `PUT /api/v1/categories/<pk>/`: Update a specific category by its primary key.
- `PATCH /api/v1/categories/<pk>/`: Partially update a specific category by its primary key.
- `DELETE /api/v1/categories/<pk>/`: Delete a specific category by its primary key.

### Menu Items
- `GET /api/v1/menu-item/`: Retrieve a list of all menu items.
- `POST /api/v1/menu-item/`: Create a new menu item.
- `GET /api/v1menu-item/<pk>/`: Retrieve a specific menu item by its primary key.
- `PUT /api/v1/menu-item/<pk>/`: Update a specific menu item by its primary key.
- `PATCH /api/v1/menu-item/<pk>/`: Partially update a specific menu item by its primary key.
- `DELETE /api/v1/menu-item/<pk>/`: Delete a specific menu item by its primary key.

### Cart
- `GET /api/v1/cart/menu-item/`: Retrieve the cart items for the authenticated user.
- `POST /api/v1/cart/menu-item/`: Add an item to the cart.
- `DELETE /api/v1/cart/menu-item/`: Remove an item from the cart or clear the cart.

### Orders
- `GET /api/v1/orders/`: Retrieve a list of orders for the authenticated user or all orders for admin and manager users.
- `POST /api/v1/orders/`: Place a new order.
- `GET /api/v1/orders/<pk>/`: Retrieve a specific order by its primary key.
- `PATCH /api/v1/orders/<pk>/`: Update the status of a specific order by its primary key.
- `PUT /api/v1/orders/<pk>/`: Assign a delivery crew to a specific order.
- `DELETE /api/v1/orders/<pk>/`: Delete a specific order by its primary key.

### User Groups
- Manager Group: Manage manager group members.
    - `GET /api/v1/groups/manager/users`: List users in the manager group.
    - `POST /api/v1/groups/manager/users`: Add a user to the manager group.
    - `DELETE /api/v1/groups/manager/users`: Remove a user from the manager group.

- Delivery Crew Group: Manage delivery crew group members.
    - `GET /api/v1/groups/delivery-crew/users`: List users in the delivery crew group.
    - `POST /api/v1/groups/delivery-crew/users`: Add a user to the delivery crew group.
    - `DELETE /api/v1/groups/delivery-crew/users`: Remove a user from the delivery crew group.

## Querying Menu Items
- You can filter menu items by category, title, price, and featured status using query parameters:
    - Example: `GET /api/v1/menu-item/?category=Appetizers&featured=true`

## Authentication and Authorization
The API uses JWT for authentication. Users can obtain, refresh, and verify tokens using endpoints provided by djoser.

## Permissions
- Categories & Menu Items: Authenticated users can retrieve, but only managers and admins can create, update, or delete.
- Cart: Only customers can manage their cart items.
- Orders: Orders can be placed by customers. Admins, managers, and delivery crew members have specific permissions for order management.
- User Groups: Only admins and managers can manage user groups.

## Swagger Documentation
You can explore the API documentation using Swagger UI:

- **URL**: `http://localhost:8000/swagger/`
- **Description**: Swagger UI provides interactive documentation for exploring the endpoints and testing the API directly from your browser.

## HTML Views
You can also explore the API using the HTML views:

- **URL**: `http://localhost:8000/api/v1/`
- **Description**: The HTML views provide a user-friendly interface to interact with the API endpoints directly from your browser.

## Request and Response Formats
- Requests should be in JSON format.
- Responses will be in JSON format.

### Category Object

```json
{
  "id": 1,
  "title": "Appetizers",
  "slug": "appetizers"
}
```

### Menu Item Object

```json
{
  "id": 1,
  "title": "Caesar Salad",
  "price": "10.00",
  "featured": true,
  "category": 1
}
```

### Cart Object

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

### Order Object

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
## Getting Started On Local

- Clone the repository.
- Create a Python virtual environment.
```
python -m venv env
```
- Activate the virtual environment
```
source env/bin/activate
```
- Install the Dependencies.
```
pip install -r requirements.txt
```
- Run Migrations
```
python manage.py migrate
```
- Run the Development Server
```
python manage.py runserver
```
- Access the API
  - you can now access the API at `http://localhost:8000/api/v1/`
  - if you access localhost:8000 it will redirect to - `http://localhost:8000/api/v1/`
  - you can also use swagger endpoints to try the api **effectly** - `http://localhost:8000/swagger/`

## Error Handling
- The API returns appropriate HTTP status codes for different types of errors.
- Error responses include a descriptive message in the JSON format.

## Testing
- Unit tests are included in the tests.py file.
- Run tests using the command:
```
python manage.py test
```

## Production Environment
- This API is not production-ready and is only suitable for the development environment.
- You can configure the production environment according to your needs - [SET UP PRODUCTION ENVIRONMENT](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment)

## Deployment
- Choose your preferred deployment method (e.g., Heroku, AWS, etc.).
- Configure your deployment environment.
- Deploy your Django project according to the platform-specific instructions.
- Make sure to set up necessary environment variables, database configurations, and any other settings required for deployment.
- For more help - [Deploy Django](https://docs.djangoproject.com/en/5.0/howto/deployment/)

## Additional Information
- Authentication: This API requires authentication.
- User Management: This API supports user management.
