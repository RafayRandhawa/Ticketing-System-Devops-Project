# Quick Start Guide

## 🚀 Getting Started (5 minutes)

### Prerequisites
- Docker & Docker Compose installed
- 4GB RAM minimum
- 2GB disk space

### Step 1: Start the Application

**Windows**:
```bash
startup.bat
```

**Linux/Mac**:
```bash
chmod +x startup.sh
./startup.sh
```

### Step 2: Access the Application

Open your browser and visit:
- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

### Step 3: Create Your First Event

1. Register or login
2. Click "Create Event" button
3. Fill in event details
4. Generate tickets and share QR codes

## 📝 Sample Credentials (Pre-loaded)

```
Username: admin
Password: (Check the database initialization)
```

## 🛠️ Common Commands

### View Logs
```bash
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f postgres
```

### Stop Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Access Database
```bash
docker-compose exec postgres psql -U user -d ticketing_system
```

### Access Backend Shell
```bash
docker-compose exec backend bash
```

### Run Tests
```bash
docker-compose exec backend pytest
```

## 📱 API Examples

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "password123",
    "full_name": "John Doe"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "password123"
  }'
```

### 3. Create Event
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

## 🐛 Troubleshooting

### Port Already in Use
**Problem**: `Error starting UserWarning: bind: Port already in use`

**Solution**: 
- Change port in docker-compose.yml
- Or stop the service using that port

### Database Connection Error
**Problem**: `Can't connect to database`

**Solution**:
```bash
# Check if postgres is running
docker-compose ps

# View postgres logs
docker-compose logs postgres

# Restart postgres
docker-compose restart postgres
```

### Frontend Not Loading
**Problem**: Blank page on http://localhost:3000

**Solution**:
```bash
# Check Nginx logs
docker-compose logs frontend

# Verify API connection works
curl http://localhost:8000/health
```

## 📚 Documentation

- **Full README**: [README.md](README.md)
- **API Documentation**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Contributing Guide**: [CONTRIBUTING.md](CONTRIBUTING.md)

## 🔧 Next Steps

1. Customize the frontend
2. Add more features
3. Set up monitoring
4. Deploy to production
5. Scale the application

## ❓ FAQ

**Q: Can I use this without Docker?**
A: Yes, see the "Local Development" section in README.md

**Q: How do I add more features?**
A: See CONTRIBUTING.md for development guidelines

**Q: How do I deploy to production?**
A: See DEPLOYMENT.md for production deployment guide

**Q: Where are my files stored?**
A: Database: PostgreSQL container volume
   QR Codes: `qr_codes/` directory
   Uploads: `uploads/` directory (create if needed)

**Q: How do I backup my database?**
A: See DEPLOYMENT.md for backup strategies

## 📞 Support

For issues or questions:
1. Check existing documentation
2. Review error logs: `docker-compose logs`
3. Check API documentation: http://localhost:8000/docs
4. Create an issue on the repository

## ✨ Features

- ✅ User authentication with JWT
- ✅ Event management
- ✅ QR code generation
- ✅ Ticket verification
- ✅ Attendee management
- ✅ Responsive design
- ✅ REST API
- ✅ Docker support
- ✅ Database backups
- ✅ API documentation

## 🎯 Performance Tips

- Use indexes on frequently queried columns
- Implement caching for events list
- Use pagination for large datasets
- Enable database connection pooling
- Compress API responses
- Use CDN for static files

## 🔒 Security Notes

- Change SECRET_KEY in production
- Use HTTPS in production
- Validate all user inputs
- Implement rate limiting
- Regular security updates
- Use strong passwords
- Enable audit logging

Enjoy building! 🎉
