# Authentication & Database Setup - Complete Guide

## ✅ What Was Fixed

### 1. Frontend Authentication
- ✅ Added **Login Page** - Users can now login
- ✅ Added **Register Page** - Users can create new accounts
- ✅ Navbar visibility - Only shows after login
- ✅ Logout functionality - Properly removes token and redirects to login
- ✅ Auto-redirect - Checks token on page load, redirects to login if not authenticated

### 2. Backend Authentication
- ✅ Updated `/api/auth/login` endpoint to accept JSON body with username/password
- ✅ Updated `/api/auth/me` endpoint to read Bearer token from Authorization header
- ✅ Proper JWT token validation and user verification

### 3. Database Configuration
- ✅ Full database setup guide with Docker and local options
- ✅ Complete schema documentation
- ✅ Connection string examples for different environments

---

## 🚀 Getting Started

### Option 1: Docker Compose (Recommended - Easiest)

```bash
cd d:\Uni\Devops\Project

# Windows
startup.bat

# Linux/Mac
./startup.sh
```

The database will be automatically set up with:
- **Host**: `postgres` (Docker internal network)
- **Database**: `ticketing_system`
- **User**: `user`
- **Password**: `password`

### Option 2: Manual Local Setup

See [DATABASE_SETUP.md](DATABASE_SETUP.md) for detailed instructions.

---

## 🔑 Authentication Flow

### 1. Register New User

**Frontend**:
1. Click "Register here" on login page
2. Fill in: Full Name, Email, Username, Password
3. Click "Register"

**Backend**:
```
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "full_name": "John Doe"
}
```

Response (201):
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2026-06-14T10:00:00"
}
```

### 2. Login

**Frontend**:
1. Enter Username and Password on login page
2. Click "Login"
3. Token is saved to browser localStorage
4. Redirected to Home page

**Backend**:
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}
```

Response (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Use API Endpoints

All subsequent requests must include the Bearer token:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Example:
```bash
curl -X GET http://localhost:8000/api/events/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 4. Logout

**Frontend**:
1. Click "Logout" in navbar
2. Token is removed from localStorage
3. Redirected back to login page

---

## 📊 Database Schema Required

The system automatically creates these tables on first run:

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Events Table
```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    organizer_id INTEGER NOT NULL,
    location VARCHAR(255),
    event_date TIMESTAMP NOT NULL,
    capacity INTEGER NOT NULL,
    ticket_price FLOAT DEFAULT 0.0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organizer_id) REFERENCES users(id)
);
```

### Tickets Table
```sql
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL,
    ticket_number VARCHAR(50) UNIQUE NOT NULL,
    qr_code TEXT,
    attendee_name VARCHAR(100) NOT NULL,
    attendee_email VARCHAR(100) NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);
```

### QR Codes Table
```sql
CREATE TABLE qr_codes (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER NOT NULL UNIQUE,
    qr_data VARCHAR(500) NOT NULL,
    image_path VARCHAR(255),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id)
);
```

All these are **automatically created** by the `database/init.sql` file!

---

## 🌐 API Endpoints Reference

### Authentication
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user (returns token) |
| GET | `/api/auth/me` | Get current user info |

### Events
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/events/` | Create event |
| GET | `/api/events/` | List all events |
| GET | `/api/events/{id}` | Get event details |
| PUT | `/api/events/{id}` | Update event |
| DELETE | `/api/events/{id}` | Delete event |

### Tickets
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/tickets/{event_id}` | Buy ticket |
| GET | `/api/tickets/` | List all tickets |
| GET | `/api/tickets/{event_id}` | List event tickets |
| GET | `/api/tickets/ticket/{id}` | Get ticket details |
| POST | `/api/tickets/verify/{number}` | Verify ticket |

### QR Codes
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/qr/ticket/{id}` | Get QR code |
| POST | `/api/qr/scan/{number}` | Scan QR code |

---

## 🔐 Database Connection Options

### Docker Compose (Default)
```
DATABASE_URL=postgresql://user:password@postgres:5432/ticketing_system
```

### Local PostgreSQL
```
DATABASE_URL=postgresql://ticketing_user:ticketing_password@localhost:5432/ticketing_system
```

### Remote Server
```
DATABASE_URL=postgresql://user:password@db.example.com:5432/ticketing_system
```

### With SSL (Production)
```
DATABASE_URL=postgresql://user:password@db.example.com:5432/ticketing_system?sslmode=require
```

To change connection, edit `backend/.env`:
```env
DATABASE_URL=your_connection_string_here
SECRET_KEY=your_secret_key_here
```

---

## 🧪 Testing the System

### 1. Start Services
```bash
startup.bat  # Windows
./startup.sh # Linux/Mac
```

### 2. Register User
- Open http://localhost:3000
- Click "Register here"
- Fill in details and register

### 3. Login
- Enter credentials
- Click Login

### 4. Create Event
- Click "Events" → Try to find "Create Event" option
- Or use API: 
```bash
curl -X POST http://localhost:8000/api/events/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tech Conference",
    "description": "Annual tech event",
    "location": "Convention Center",
    "event_date": "2026-07-15T09:00:00",
    "capacity": 500,
    "ticket_price": 99.99,
    "organizer_id": 1
  }'
```

### 5. Buy Ticket
- View event details
- Click "Buy Ticket"
- Enter attendee name and email
- Get QR code with ticket

### 6. Verify Ticket
- Go to "Scan Ticket"
- Enter ticket number
- See verification result

---

## 🔍 Database Inspection

### Via Docker
```bash
# Connect to database
docker-compose exec postgres psql -U user -d ticketing_system

# Common queries
\dt              # List tables
SELECT * FROM users;
SELECT * FROM events;
SELECT * FROM tickets;
\q              # Exit
```

### Via Local psql
```bash
psql -U ticketing_user -d ticketing_system -h localhost

# Same commands as above
```

---

## 🚨 Common Issues & Solutions

### "Invalid credentials" on login
- Check username spelling
- Verify password is correct
- User must be registered first

### "Bearer token required" error
- Make sure you're logged in
- Token is stored in browser localStorage
- Check browser developer console

### Database connection error
- Verify Docker is running: `docker-compose ps`
- Check DATABASE_URL in `.env`
- For local setup, verify PostgreSQL is running

### "Event capacity reached"
- Event has maximum tickets sold
- Can't buy more tickets for that event

### QR Code not showing
- JavaScript might be blocked
- Check browser console for errors
- Verify backend is running

---

## 📝 Environment Variables

Edit `backend/.env`:

```env
# Database (required)
DATABASE_URL=postgresql://user:password@postgres:5432/ticketing_system

# JWT (required)
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server (optional)
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### Generating SECRET_KEY

```bash
# Python
python -c "import secrets; print(secrets.token_hex(32))"

# OpenSSL
openssl rand -hex 32
```

---

## 🎓 Next Steps

1. ✅ Start the project (startup.bat / startup.sh)
2. ✅ Register a new account
3. ✅ Login with your credentials
4. ✅ Explore all features
5. ✅ Read [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed API info
6. ✅ Check [DATABASE_SETUP.md](DATABASE_SETUP.md) for database details
7. ✅ Read [DEPLOYMENT.md](DEPLOYMENT.md) to deploy to production

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| [INDEX.md](INDEX.md) | Navigation guide |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup |
| [README.md](README.md) | Full documentation |
| [DATABASE_SETUP.md](DATABASE_SETUP.md) | Database configuration |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | API reference |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Development guide |
| **This file** | Authentication & DB setup |

---

**Status**: ✅ Complete and Ready to Use
**Last Updated**: 2026-06-14

