# Supabase Migration Setup Guide

## Overview
Your QR Code Event Ticketing System has been migrated from local PostgreSQL to Supabase, a cloud-hosted PostgreSQL database. This eliminates the need to run PostgreSQL locally via Docker.

## Prerequisites
1. A free Supabase account (sign up at https://supabase.com)
2. Docker and Docker Compose installed
3. The latest `.env.example` configuration

## Step-by-Step Setup

### 1. Create a Supabase Project
1. Go to [https://supabase.com](https://supabase.com) and sign in/sign up
2. Click "New Project" 
3. Fill in project details:
   - Name: `qr-ticketing-system` (or your preferred name)
   - Database Password: Create a strong password (save this!)
   - Region: Choose closest to your location
4. Wait for the project to initialize (usually 1-2 minutes)

### 2. Get Your Connection Credentials
1. In your Supabase project, go to **Settings → Database**
2. Under "Connection String", select **PostgreSQL** (or **Connection pooling** for production)
3. Copy the connection string - it should look like:
   ```
   postgresql://postgres:[YOUR_PASSWORD]@aws-0-[region].pooler.supabase.com:5432/postgres
   ```

### 3. Get Supabase API Keys (Optional - for direct Supabase SDK usage)
1. Go to **Settings → API** in your Supabase project
2. Note:
   - **Project URL** (SUPABASE_URL): `https://[project-id].supabase.co`
   - **Anon Key** (SUPABASE_ANON_KEY): The public key
   - **Service Role Key** (SUPABASE_SERVICE_ROLE_KEY): The secret key

### 4. Update Your .env File
Edit `backend/.env` and update these variables:

```env
# Replace with your actual Supabase credentials
DATABASE_URL=postgresql://postgres:[YOUR_PASSWORD]@aws-0-[region].pooler.supabase.com:5432/postgres
SUPABASE_URL=https://[project-id].supabase.com
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# Keep existing configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
HOST=0.0.0.0
PORT=8000
DEBUG=True
QR_CODE_SIZE=10
QR_CODE_BORDER=4
```

### 5. Initialize Database Schema
1. In Supabase, go to **SQL Editor**
2. Create a new query and run your database initialization script
3. Or use the Supabase Query editor to run:
   ```bash
   # Read the content from database/init.sql and execute it
   ```

### 6. Start Your Application
Run the startup script:

**On Linux/Mac:**
```bash
chmod +x startup.sh
./startup.sh
```

**On Windows:**
```cmd
startup.bat
```

The backend will now connect to your Supabase database instead of local PostgreSQL.

### 7. Verify the Connection
1. Check that the backend container started successfully:
   ```bash
   docker logs ticketing_backend
   ```
2. Visit http://localhost:8000/docs to access the API documentation
3. Try creating a new user or event to verify database operations work

## Key Changes Made

### Files Modified:
- **docker-compose.yml**: Removed PostgreSQL service (no longer needed)
- **backend/.env.example**: Added Supabase connection variables
- **backend/config.py**: Added Supabase configuration support
- **startup.sh & startup.bat**: Updated with Supabase setup instructions

### What Stayed the Same:
- FastAPI backend code (no changes to routes or models)
- Database models (SQLAlchemy ORM works with Supabase PostgreSQL)
- Frontend remains unchanged
- API endpoints remain the same

## Troubleshooting

### "Connection refused" errors
- Verify DATABASE_URL is correct from Supabase
- Ensure your Supabase project is active (not paused)
- Check that Supabase allows connections from your IP

### Database not initialized
- Run your `database/init.sql` script in Supabase SQL Editor
- Ensure tables are created before running the application

### Slow connections
- Use **Connection pooling** in Supabase settings for better performance
- Select the pooler endpoint instead of direct connection in production

### Need to revert to local PostgreSQL?
1. Restore the original docker-compose.yml (with postgres service)
2. Update DATABASE_URL to: `postgresql://user:password@postgres:5432/ticketing_system`
3. Uncomment the database initialization in startup.sh/startup.bat

## Production Recommendations

1. **Use Connection Pooling**: Set max connections appropriately
2. **Enable SSL**: Always use SSL in production (Supabase enables this by default)
3. **Backup**: Enable automated backups in Supabase settings
4. **Monitor**: Check Supabase dashboard for performance metrics
5. **Scale**: Supabase auto-scales, but monitor costs
6. **Security**: Use Service Role Key only on backend (never expose to frontend)

## Next Steps

1. Ensure all environment variables are properly set
2. Test the authentication and ticket creation workflows
3. Verify QR code generation works end-to-end
4. Set up monitoring and logging for production

For more information, visit [Supabase Documentation](https://supabase.com/docs)
