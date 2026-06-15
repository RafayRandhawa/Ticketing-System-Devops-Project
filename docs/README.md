# QR Code Event Ticketing System

A modern event ticketing system that generates QR codes for ticket verification and management.

> 📚 **This system now uses Supabase for database hosting!** See [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for detailed setup instructions.

## Features

- 🎟️ Event creation and management
- 🔐 User authentication with JWT
- 📱 QR code generation for tickets
- ✅ Ticket verification and scanning
- 👥 Attendee management
- 💰 Ticket pricing
- ☁️ Cloud database with Supabase
- 🏗️ Containerized deployment with Docker

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML/CSS/JavaScript (Vanilla)
- **Database**: Supabase (PostgreSQL)
- **Server**: Uvicorn
- **Web Server**: Nginx
- **Containerization**: Docker & Docker Compose

## Project Structure

```
QR_Code_Event_Ticketing_System/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile              # Backend container image
│   ├── models/                 # SQLAlchemy models
│   ├── routes/                 # API endpoints
│   ├── schemas/                # Pydantic schemas
│   └── utils/                  # Utility functions
├── frontend/
│   ├── index.html              # Main HTML file
│   ├── styles.css              # Styling
│   └── script.js               # Frontend logic
├── database/
│   └── init.sql                # Database initialization
├── docker-compose.yml          # Docker Compose configuration
├── nginx.conf                  # Nginx configuration
└── README.md                   # This file
```

## Prerequisites

- Docker & Docker Compose (for containerized deployment)
- Supabase account (free at https://supabase.com)
- OR
- Python 3.11+
- Node.js (for frontend development, optional)

## Quick Start

### 1. Set Up Supabase (Required)
Before running the application, you need a Supabase database:
1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project
3. Get your connection string from Settings → Database
4. See [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for detailed instructions

### 2. Docker Compose (Recommended)

1. **Navigate to the project**:
   ```bash
   cd d:\Uni\Devops\Project
   ```

2. **Create .env file**:
   ```bash
   cp backend\.env.example backend\.env
   ```

3. **Update environment variables with Supabase credentials**:
   ```
   DATABASE_URL=postgresql://postgres:[PASSWORD]@[SUPABASE_HOST]:5432/postgres
   SUPABASE_URL=https://[PROJECT-ID].supabase.co
   SUPABASE_ANON_KEY=your-key
   SUPABASE_SERVICE_ROLE_KEY=your-key
   SECRET_KEY=your-secret-key-here
   ```

4. **Start services**:
   ```bash
   docker-compose up -d
   ```

5. **Access the application**:
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs
   - API: http://localhost:8000

### Option 2: Local Development

1. **Install PostgreSQL** and create a database:
   ```sql
   CREATE DATABASE ticketing_system;
   ```

2. **Setup backend**:
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

3. **Create .env file**:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/ticketing_system
   SECRET_KEY=dev-secret-key
   DEBUG=True
   ```

4. **Initialize database**:
   ```bash
   psql -U user -d ticketing_system -f ../database/init.sql
   ```

5. **Run backend**:
   ```bash
   uvicorn main:app --reload
   ```

6. **Serve frontend** (in another terminal):
   ```bash
   cd frontend
   python -m http.server 3000
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Events
- `POST /api/events/` - Create event
- `GET /api/events/` - List events
- `GET /api/events/{event_id}` - Get event details
- `PUT /api/events/{event_id}` - Update event
- `DELETE /api/events/{event_id}` - Delete event

### Tickets
- `POST /api/tickets/{event_id}` - Create ticket
- `GET /api/tickets/{event_id}` - List event tickets
- `GET /api/tickets/ticket/{ticket_id}` - Get ticket details
- `POST /api/tickets/verify/{ticket_number}` - Verify ticket

### QR Codes
- `GET /api/qr/ticket/{ticket_id}` - Get QR code for ticket
- `POST /api/qr/scan/{ticket_number}` - Scan and verify QR code

## Usage Examples

### Create an Event
```bash
curl -X POST http://localhost:8000/api/events/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "title": "Tech Conference",
    "description": "Annual tech conference",
    "location": "Convention Center",
    "event_date": "2026-07-15T09:00:00",
    "capacity": 500,
    "ticket_price": 99.99
  }'
```

### Buy a Ticket
```bash
curl -X POST http://localhost:8000/api/tickets/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "attendee_name": "John Doe",
    "attendee_email": "john@example.com"
  }'
```

### Verify a Ticket
```bash
curl -X POST http://localhost:8000/api/tickets/verify/ABC12345 \
  -H "Authorization: Bearer {token}"
```

## Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ticketing_system

# JWT Configuration
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# QR Code
QR_CODE_SIZE=10
QR_CODE_BORDER=4
```

## Database Schema

The system uses the following tables:
- **users**: User accounts and authentication
- **events**: Event information
- **tickets**: Ticket details for attendees
- **qr_codes**: QR code data and generation info

See `database/init.sql` for full schema.

## Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild images
docker-compose build

# Access database
docker-compose exec postgres psql -U user -d ticketing_system

# Backend shell
docker-compose exec backend bash
```

## Development

### Adding New Features

1. **Backend**: Add routes in `routes/`, models in `models/`, schemas in `schemas/`
2. **Frontend**: Update `frontend/index.html`, `styles.css`, `script.js`
3. **Database**: Update schema in `database/init.sql` if needed

### Running Tests

```bash
cd backend
pytest
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env file
- Verify credentials match

### Port Already in Use
- Change ports in docker-compose.yml or local configuration
- Example: Change port `3000:80` to `3001:80`

### API CORS Issues
- Update CORS origins in `backend/main.py`
- Add your frontend URL to the `origins` list

## Production Deployment

1. **Set secure SECRET_KEY**
2. **Use environment-specific .env files**
3. **Enable HTTPS**
4. **Configure proper database backups**
5. **Set DEBUG=False**
6. **Use production-grade server (Gunicorn instead of Uvicorn)**

## License

This project is for educational purposes.

## Support

For issues or questions, please check the documentation or create an issue in the repository.
