# Vendor Management System

## 1. Installation Requirements

To run the Vendor Management System application, make sure you have the following installed:

- Python 3.11
- Django
- Django REST Framework

You can install Django and Django REST Framework using pip:

```bash
pip install -r requirements.txt
```

## 2. Running Tests

To run the unit tests for the Vendor Management System, navigate to the root directory of the project and execute the following command:

```bash
python manage.py test
```

## 3. Vendor Management System API Documentation

This document provides an overview of the API endpoints available in the Vendor Management System (VMS) application.

### Authentication

All API endpoints in the Vendor and Purchase Order apps are secured with token-based authentication. To access these endpoints, clients must include a valid token in the Authorization header of their HTTP requests.

To obtain a token, clients should authenticate by sending a POST request to the `/api/accounts/login/` endpoint with valid credentials. Upon successful authentication, the server will respond with a token that can be used for subsequent requests.

### Authentication Endpoints

- `POST /api/accounts/signup/`: Create a new user account.
  - Request Body:
    ```json
    {
        "username": "example_user",
        "password": "example_password",
        "email": "example@example.com"
    }
    ```
- `POST /api/accounts/login/`: Authenticate and obtain a token.
  - Request Body:
    ```json
    {
        "username": "example_user",
        "password": "example_password"
    }
    ```
  - Response:
    ```json
    {
        "token": "your_access_token_here"
    }
    ```

## Vendor Management

### Vendor Endpoints

- `POST /api/vendors/`: Create a new vendor profile.
  - Request Body:
    ```json
    {
        "name": "New Vendor",
        "contact_details": "Contact Details",
        "address": "Vendor Address",
        "vendor_code": "V001"
    }
    ```
- `GET /api/vendors/`: List all vendors.
- `GET /api/vendors/{vendor_id}/`: Retrieve details of a specific vendor.
- `PUT /api/vendors/{vendor_id}/`: Update details of a specific vendor.
  - Request Body:
    ```json
    {
        "name": "Updated Vendor Name",
        "contact_details": "Updated Contact Details",
        "address": "Updated Address",
        "vendor_code": "V001"
    }
    ```
- `DELETE /api/vendors/{vendor_id}/`: Delete a specific vendor.

### Vendor Performance Endpoints

- `GET /api/vendors/{vendor_id}/performance/`: Retrieve performance metrics for a specific vendor.

## Purchase Order Tracking

### Purchase Order Endpoints

- `POST /api/purchase_orders/`: Create a new purchase order.
  - Request Body:
    ```json
    {
        "po_number": "PO001",
        "vendor": 1,
        "order_date": "2024-05-10T10:00:00Z",
        "delivery_date": "2024-05-15T10:00:00Z",
        "items": {"item1": "Description1"},
        "quantity": 10,
        "status": "pending",
        "quality_rating": 4.5,
        "issue_date": "2024-05-10T10:00:00Z",
        "acknowledgment_date": "2024-05-11T10:00:00Z"
    }
    ```
- `GET /api/purchase_orders/`: List all purchase orders with optional filtering by vendor.
- `GET /api/purchase_orders/{po_id}/`: Retrieve details of a specific purchase order.
- `PUT /api/purchase_orders/{po_id}/`: Update details of a specific purchase order.
  - Request Body:
    ```json
    {
        "status": "completed",
        "acknowledgment_date": "2024-05-12T10:00:00Z"
    }
    ```
- `DELETE /api/purchase_orders/{po_id}/`: Delete a specific purchase order.
- `POST /api/purchase_orders/{po_id}/acknowledge/`: Acknowledge a purchase order.

## Usage

To use the API endpoints, clients should authenticate using token-based authentication. Include the obtained token in the Authorization header of all requests to secure endpoints.

Example:

```http
GET /api/vendors/ HTTP/1.1
Host: example.com
Authorization: Token <your_token_here>
