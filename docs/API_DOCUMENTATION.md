# QR Code Event Ticketing System - API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Authentication Endpoints

### Register User
```
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "full_name": "John Doe"
}

Response (201):
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2026-06-14T10:00:00"
}
```

### Login
```
POST /auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}

Response (200):
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Get Current User
```
GET /auth/me
Authorization: Bearer <access_token>

Response (200):
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2026-06-14T10:00:00"
}
```

## Events Endpoints

### Create Event
```
POST /events/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Tech Conference 2026",
  "description": "Annual technology conference",
  "location": "Convention Center, New York",
  "event_date": "2026-07-15T09:00:00",
  "capacity": 500,
  "ticket_price": 99.99,
  "organizer_id": 1
}

Response (200):
{
  "id": 1,
  "title": "Tech Conference 2026",
  "description": "Annual technology conference",
  "location": "Convention Center, New York",
  "event_date": "2026-07-15T09:00:00",
  "capacity": 500,
  "ticket_price": 99.99,
  "organizer_id": 1,
  "is_active": true,
  "created_at": "2026-06-14T10:00:00",
  "updated_at": "2026-06-14T10:00:00"
}
```

### List Events
```
GET /events/?skip=0&limit=10
Authorization: Bearer <access_token>

Response (200):
[
  {
    "id": 1,
    "title": "Tech Conference 2026",
    "description": "Annual technology conference",
    "location": "Convention Center, New York",
    "event_date": "2026-07-15T09:00:00",
    "capacity": 500,
    "ticket_price": 99.99,
    "organizer_id": 1,
    "is_active": true,
    "created_at": "2026-06-14T10:00:00",
    "updated_at": "2026-06-14T10:00:00"
  }
]
```

### Get Event Details
```
GET /events/{event_id}
Authorization: Bearer <access_token>

Response (200):
{
  "id": 1,
  "title": "Tech Conference 2026",
  "description": "Annual technology conference",
  "location": "Convention Center, New York",
  "event_date": "2026-07-15T09:00:00",
  "capacity": 500,
  "ticket_price": 99.99,
  "organizer_id": 1,
  "is_active": true,
  "created_at": "2026-06-14T10:00:00",
  "updated_at": "2026-06-14T10:00:00",
  "tickets": [
    {
      "id": 1,
      "ticket_number": "ABC12345",
      "attendee_name": "John Doe",
      "attendee_email": "john@example.com",
      "is_used": false,
      "created_at": "2026-06-14T10:30:00"
    }
  ]
}
```

### Update Event
```
PUT /events/{event_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Tech Conference 2026 - Updated",
  "capacity": 600,
  "ticket_price": 89.99
}

Response (200):
{
  "id": 1,
  "title": "Tech Conference 2026 - Updated",
  "capacity": 600,
  "ticket_price": 89.99,
  ...
}
```

### Delete Event
```
DELETE /events/{event_id}
Authorization: Bearer <access_token>

Response (204): No Content
```

## Tickets Endpoints

### Create Ticket (Buy Ticket)
```
POST /tickets/{event_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "attendee_name": "John Doe",
  "attendee_email": "john@example.com"
}

Response (200):
{
  "id": 1,
  "event_id": 1,
  "ticket_number": "ABC12345",
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANS...",
  "attendee_name": "John Doe",
  "attendee_email": "john@example.com",
  "is_used": false,
  "created_at": "2026-06-14T10:30:00"
}
```

### List Event Tickets
```
GET /tickets/{event_id}
Authorization: Bearer <access_token>

Response (200):
[
  {
    "id": 1,
    "event_id": 1,
    "ticket_number": "ABC12345",
    "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANS...",
    "attendee_name": "John Doe",
    "attendee_email": "john@example.com",
    "is_used": false,
    "created_at": "2026-06-14T10:30:00"
  }
]
```

### Get Ticket Details
```
GET /tickets/ticket/{ticket_id}
Authorization: Bearer <access_token>

Response (200):
{
  "id": 1,
  "event_id": 1,
  "ticket_number": "ABC12345",
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANS...",
  "attendee_name": "John Doe",
  "attendee_email": "john@example.com",
  "is_used": false,
  "created_at": "2026-06-14T10:30:00"
}
```

### Verify Ticket
```
POST /tickets/verify/{ticket_number}
Authorization: Bearer <access_token>

Response (200):
{
  "message": "Ticket verified successfully",
  "ticket": {
    "id": 1,
    "event_id": 1,
    "ticket_number": "ABC12345",
    "attendee_name": "John Doe",
    "attendee_email": "john@example.com",
    "is_used": true,
    "used_at": "2026-06-14T15:45:00"
  }
}
```

## QR Code Endpoints

### Get QR Code for Ticket
```
GET /qr/ticket/{ticket_id}
Authorization: Bearer <access_token>

Response (200):
{
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANS..."
}
```

### Scan QR Code
```
POST /qr/scan/{ticket_number}
Authorization: Bearer <access_token>

Response (200):
{
  "valid": true,
  "ticket_number": "ABC12345",
  "attendee_name": "John Doe",
  "event_id": 1,
  "is_used": false
}

Error Response (404):
{
  "detail": "Invalid QR code"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Event capacity reached"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Event not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Response Status Codes

- `200 OK` - Successful GET/POST/PUT request
- `201 Created` - Resource created successfully
- `204 No Content` - Successful DELETE request
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Missing or invalid authentication
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Testing with cURL

### Example 1: Register and Login
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "password123",
    "full_name": "John Doe"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "password123"
  }'

# Save token as TOKEN variable
TOKEN="eyJhbGciOiJIUzI1NiIs..."
```

### Example 2: Create Event
```bash
curl -X POST http://localhost:8000/api/events/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tech Conference",
    "location": "New York",
    "event_date": "2026-07-15T09:00:00",
    "capacity": 500,
    "ticket_price": 99.99,
    "organizer_id": 1
  }'
```

### Example 3: Buy Ticket
```bash
curl -X POST http://localhost:8000/api/tickets/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "attendee_name": "Jane Doe",
    "attendee_email": "jane@example.com"
  }'
```
