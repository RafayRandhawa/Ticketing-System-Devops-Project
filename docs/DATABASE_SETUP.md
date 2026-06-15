# Database Setup & Configuration Guide

## 📊 Database Overview

The system uses **PostgreSQL 15** as the relational database. It includes 4 main tables and indexes for optimal performance.

### Database Schema

```
┌─────────────────────────────────────────┐
│              USERS TABLE                │
├─────────────────────────────────────────┤
│ id (INT, PK)                           │
│ username (VARCHAR(50), UNIQUE)         │
│ email (VARCHAR(100), UNIQUE)           │
│ hashed_password (VARCHAR(255))         │
│ full_name (VARCHAR(100))               │
│ is_active (BOOLEAN)                    │
│ created_at (TIMESTAMP)                 │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│             EVENTS TABLE                │
├─────────────────────────────────────────┤
│ id (INT, PK)                           │
│ title (VARCHAR(200))                   │
│ description (TEXT)                     │
│ organizer_id (INT, FK → users)         │
│ location (VARCHAR(255))                │
│ event_date (TIMESTAMP)                 │
│ capacity (INT)                         │
│ ticket_price (FLOAT)                   │
│ is_active (BOOLEAN)                    │
│ created_at (TIMESTAMP)                 │
│ updated_at (TIMESTAMP)                 │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│            TICKETS TABLE                │
├─────────────────────────────────────────┤
│ id (INT, PK)                           │
│ event_id (INT, FK → events)            │
│ ticket_number (VARCHAR(50), UNIQUE)    │
│ qr_code (TEXT)                         │
│ attendee_name (VARCHAR(100))           │
│ attendee_email (VARCHAR(100))          │
│ is_used (BOOLEAN)                      │
│ used_at (TIMESTAMP)                    │
│ created_at (TIMESTAMP)                 │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│           QR_CODES TABLE                │
├─────────────────────────────────────────┤
│ id (INT, PK)                           │
│ ticket_id (INT, FK → tickets, UNIQUE)  │
│ qr_data (VARCHAR(500))                 │
│ image_path (VARCHAR(255))              │
│ generated_at (TIMESTAMP)               │
└─────────────────────────────────────────┘
```

---

## 🐳 Database Setup with Docker (Recommended)

### Option 1: Docker Compose (Easiest)

The `docker-compose.yml` file automatically sets up PostgreSQL with the correct configuration.

```bash
# Start all services including database
docker-compose up -d

# Verify database is running
docker-compose ps

# Access database shell
docker-compose exec postgres psql -U user -d ticketing_system

# View database logs
docker-compose logs postgres
```

**Environment Variables** (in `.env`):
```
DATABASE_URL=postgresql://user:password@postgres:5432/ticketing_system
```

When using Docker Compose, these are automatically set:
- **Host**: `postgres` (internal Docker network)
- **Port**: `5432`
- **Username**: `user`
- **Password**: `password`
- **Database**: `ticketing_system`

---

## 🖥️ Local Database Setup (Without Docker)

### Prerequisites
- PostgreSQL 15+ installed
- psql command-line tool
- Administrator access

### Step 1: Install PostgreSQL

**Windows**:
```
Download from: https://www.postgresql.org/download/windows/
Run installer and remember the password you set for 'postgres' user
```

**Mac (using Homebrew)**:
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
```

### Step 2: Create Database and User

Open PostgreSQL command line:

**Windows (PowerShell)**:
```powershell
psql -U postgres
```

**Mac/Linux**:
```bash
sudo -u postgres psql
```

Then execute:

```sql
-- Create user for the application
CREATE USER ticketing_user WITH PASSWORD 'ticketing_password';

-- Create database
CREATE DATABASE ticketing_system OWNER ticketing_user;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE ticketing_system TO ticketing_user;

-- Connect to the database
\c ticketing_system

-- Grant schema privileges
GRANT ALL PRIVILEGES ON SCHEMA public TO ticketing_user;

-- Exit
\q
```

### Step 3: Initialize Schema

Option A - Using the SQL file:
```bash
# From project root
psql -U ticketing_user -d ticketing_system -h localhost -f database/init.sql
```

Option B - Using psql directly:
```bash
psql -U ticketing_user -d ticketing_system -h localhost
```

Then copy-paste the contents of [database/init.sql](../database/init.sql)

### Step 4: Update Connection String

Edit `backend/.env`:

```env
DATABASE_URL=postgresql://ticketing_user:ticketing_password@localhost:5432/ticketing_system
```

### Step 5: Start Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🔧 Database Configuration Options

### Connection String Format

```
postgresql://[username]:[password]@[host]:[port]/[database]
```

### Common Configurations

**Local Development**:
```
postgresql://ticketing_user:ticketing_password@localhost:5432/ticketing_system
```

**Docker Compose**:
```
postgresql://user:password@postgres:5432/ticketing_system
```

**Remote Server**:
```
postgresql://user:password@db.example.com:5432/ticketing_system
```

**With SSL (Production)**:
```
postgresql://user:password@db.example.com:5432/ticketing_system?sslmode=require
```

### Environment Variables

Create `backend/.env`:

```env
# Database connection
DATABASE_URL=postgresql://user:password@localhost:5432/ticketing_system

# Connection pool settings (optional)
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10

# Security
SECRET_KEY=your-secret-key-change-in-production
```

---

## 📊 Database Management

### Connect to Database

**With Docker**:
```bash
docker-compose exec postgres psql -U user -d ticketing_system
```

**Local**:
```bash
psql -U ticketing_user -d ticketing_system -h localhost
```

### Common Commands

```sql
-- List all tables
\dt

-- Describe a table
\d users

-- List all databases
\l

-- Switch database
\c ticketing_system

-- View users
SELECT * FROM users;

-- View events
SELECT * FROM events;

-- View tickets
SELECT * FROM tickets;

-- Count tickets for an event
SELECT COUNT(*) FROM tickets WHERE event_id = 1;

-- Find unused tickets
SELECT * FROM tickets WHERE is_used = false;

-- View database size
SELECT pg_size_pretty(pg_database_size('ticketing_system'));

-- Exit
\q
```

### Backup Database

**Docker**:
```bash
docker-compose exec -T postgres pg_dump -U user ticketing_system > backup.sql
```

**Local**:
```bash
pg_dump -U ticketing_user ticketing_system > backup.sql
```

### Restore Database

**Docker**:
```bash
cat backup.sql | docker-compose exec -T postgres psql -U user ticketing_system
```

**Local**:
```bash
psql -U ticketing_user ticketing_system < backup.sql
```

### Reset Database

**⚠️ WARNING: This will delete all data!**

```sql
-- Drop and recreate
DROP DATABASE ticketing_system;
CREATE DATABASE ticketing_system OWNER ticketing_user;
```

Then reinitialize with `init.sql`.

---

## 🔐 Security Best Practices

### Development

```env
DATABASE_URL=postgresql://dev_user:dev_password@localhost:5432/ticketing_dev
```

### Production

```env
# Use strong password
DATABASE_URL=postgresql://user:random_strong_password@prod-db.example.com:5432/ticketing_system

# Enable SSL
DATABASE_URL=postgresql://user:password@prod-db.example.com:5432/ticketing_system?sslmode=require

# Consider managed database services:
# - AWS RDS PostgreSQL
# - Azure Database for PostgreSQL
# - Google Cloud SQL
# - Heroku Postgres
```

### Database User Permissions

For least privilege, create a limited user:

```sql
CREATE USER app_user WITH PASSWORD 'app_password';
GRANT CONNECT ON DATABASE ticketing_system TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;
```

---

## ⚡ Performance Optimization

### Indexes

The schema includes indexes on:
- `users.username` - Fast user lookups
- `users.email` - Unique email checking
- `events.organizer_id` - Organizer events
- `events.is_active` - Event filtering
- `tickets.event_id` - Event tickets
- `tickets.ticket_number` - Ticket lookup
- `tickets.is_used` - Usage filtering
- `qr_codes.ticket_id` - QR code lookup

### Connection Pooling

For production, use PgBouncer or similar:

```
[databases]
ticketing_system = host=db.example.com port=5432 dbname=ticketing_system

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
```

### Maintenance

Regular maintenance tasks:

```sql
-- Vacuum and analyze
VACUUM ANALYZE;

-- Reindex tables
REINDEX DATABASE ticketing_system;

-- Check for unused indexes
SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;
```

---

## 🚨 Troubleshooting

### Connection Refused

```bash
# Check if PostgreSQL is running
# Docker
docker-compose ps postgres

# Local
pg_isready -h localhost -p 5432
```

### Authentication Failed

```
psql: error: FATAL: Ident authentication failed
```

**Solution**: 
- Check username/password in `.env`
- Verify user exists: `SELECT * FROM pg_user;`
- Reset password: `ALTER USER user_name WITH PASSWORD 'new_password';`

### Database Does Not Exist

```
psql: error: FATAL: database "ticketing_system" does not exist
```

**Solution**:
```bash
# Create database
createdb -U postgres ticketing_system

# Or via psql
psql -U postgres
CREATE DATABASE ticketing_system;
```

### Out of Disk Space

```sql
-- Check database size
SELECT pg_size_pretty(pg_database_size('ticketing_system'));

-- Check table sizes
SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) 
FROM pg_catalog.pg_statio_user_tables 
ORDER BY pg_total_relation_size(relid) DESC;
```

### Slow Queries

```sql
-- Enable query logging
ALTER SYSTEM SET log_min_duration_statement = 1000;
SELECT pg_reload_conf();

-- View query stats
SELECT query, calls, total_time, mean_time 
FROM pg_stat_statements 
ORDER BY total_time DESC LIMIT 10;
```

---

## 📚 Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Database Design Best Practices](https://www.postgresql.org/docs/current/ddl.html)
- [Connection Pool Configuration](https://www.postgresql.org/docs/current/runtime-config-connection.html)

---

## Quick Reference

| Task | Docker | Local |
|------|--------|-------|
| Connect | `docker-compose exec postgres psql` | `psql -U user` |
| Backup | `docker-compose exec postgres pg_dump` | `pg_dump` |
| Restore | `cat backup.sql \| docker-compose exec postgres psql` | `psql < backup.sql` |
| Check Size | `docker-compose exec postgres psql -c "SELECT pg_size_pretty..."` | `psql -c "SELECT..."` |
| Restart | `docker-compose restart postgres` | `service postgresql restart` |

