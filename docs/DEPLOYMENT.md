# Deployment Guide

## Pre-Deployment Checklist

- [ ] Update SECRET_KEY in .env
- [ ] Set DEBUG=False
- [ ] Configure production DATABASE_URL
- [ ] Update CORS origins in backend/main.py
- [ ] Set up SSL/TLS certificates
- [ ] Configure backup strategy
- [ ] Set up monitoring and logging
- [ ] Test all endpoints

## Docker Deployment

### Build Production Images
```bash
docker-compose build
```

### Push to Registry
```bash
docker tag ticketing_backend your-registry/ticketing-backend:1.0.0
docker tag ticketing_frontend your-registry/ticketing-frontend:1.0.0

docker push your-registry/ticketing-backend:1.0.0
docker push your-registry/ticketing-frontend:1.0.0
```

### Deploy on Production Server

1. **SSH into server**:
   ```bash
   ssh user@production-server.com
   ```

2. **Clone repository**:
   ```bash
   git clone <repository-url>
   cd QR_Code_Event_Ticketing_System
   ```

3. **Create production .env**:
   ```bash
   cp backend/.env.example backend/.env
   # Edit with production values
   nano backend/.env
   ```

4. **Start services**:
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

5. **Verify deployment**:
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:3000
   ```

## Kubernetes Deployment

### Prerequisites
- kubectl configured
- Docker images pushed to registry

### Create Deployment Files

**deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ticketing-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ticketing-backend
  template:
    metadata:
      labels:
        app: ticketing-backend
    spec:
      containers:
      - name: backend
        image: your-registry/ticketing-backend:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: key
```

### Deploy to Kubernetes
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

## SSL/TLS Setup with Nginx

Update `nginx.conf`:
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # ... rest of configuration
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

## Database Backups

### Automated Backup Script

Create `backup.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/backups/database"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

mkdir -p $BACKUP_DIR

docker-compose exec -T postgres pg_dump -U user ticketing_system | \
    gzip > $BACKUP_DIR/ticketing_system_$TIMESTAMP.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -mtime +30 -delete
```

Schedule with cron:
```
0 2 * * * /path/to/backup.sh
```

## Monitoring & Logging

### Application Logs
```bash
# View backend logs
docker-compose logs -f backend

# View frontend logs
docker-compose logs -f frontend

# View database logs
docker-compose logs -f postgres
```

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Database connectivity
docker-compose exec postgres psql -U user -d ticketing_system -c "SELECT 1"
```

## Scaling

### Horizontal Scaling with Load Balancer

Update `docker-compose.yml` to run multiple backend instances:
```yaml
backend-1:
  # ... backend configuration
backend-2:
  # ... backend configuration
backend-3:
  # ... backend configuration
```

Configure Nginx upstream:
```nginx
upstream backend {
    server backend-1:8000;
    server backend-2:8000;
    server backend-3:8000;
}

location /api/ {
    proxy_pass http://backend;
}
```

## Maintenance

### Database Maintenance

```bash
# Vacuum database
docker-compose exec postgres psql -U user -d ticketing_system \
    -c "VACUUM ANALYZE"

# Check database size
docker-compose exec postgres psql -U user -d ticketing_system \
    -c "SELECT pg_size_pretty(pg_database_size('ticketing_system'))"
```

### Update Application

1. Pull latest changes
2. Rebuild images
3. Deploy without downtime using rolling updates
4. Verify all services are running

## Troubleshooting Deployment

### Container won't start
```bash
docker-compose logs backend
docker-compose exec backend bash
```

### Database connection error
```bash
docker-compose exec postgres psql -U user -c "SELECT version()"
```

### Out of disk space
```bash
docker system prune -a
docker volume prune
```

## Security Best Practices

- [ ] Use environment variables for sensitive data
- [ ] Implement rate limiting
- [ ] Use HTTPS/TLS
- [ ] Keep images updated
- [ ] Run containers as non-root user
- [ ] Use network policies
- [ ] Enable audit logging
- [ ] Regular security scans
- [ ] Implement WAF rules

## Performance Optimization

- Use connection pooling for database
- Implement caching (Redis)
- Compress API responses
- Optimize database queries
- Use CDN for static files
- Enable compression in Nginx

## Support & Monitoring

For production monitoring consider:
- Prometheus + Grafana
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Sentry for error tracking
- PagerDuty for alerts
