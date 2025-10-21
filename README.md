# Disease Report Dashboard - Deployment Guide

## Overview
This is a Streamlit-based disease surveillance dashboard for measles case reporting in Uganda. It connects to a PostgreSQL database and provides interactive visualizations including choropleth maps, epicurves, and summary statistics.

## System Requirements
- Ubuntu Server (18.04+ recommended)
- Python 3.8 or higher
- PostgreSQL database access
- At least 2GB RAM
- Internet connection for initial setup

## Deployment Steps

### 1. Copy Project to Server
```bash
# On your local machine, create a zip file
cd /Projects
zip -r disease-report.zip Disease-Report/ -x "Disease-Report/streamlit_env/*" "Disease-Report/__pycache__/*" "Disease-Report/*.pyc"

# Copy to server
scp disease-report.zip user@your-server:/home/user/

# On server, create hisp directory and extract
ssh user@your-server
cd /home/user/
mkdir -p hisp
cd hisp
unzip ../disease-report.zip
mv Disease-Report/* .
rm -rf Disease-Report
```

### 2. Install System Dependencies
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install PostgreSQL client (if needed for testing connection)
sudo apt install postgresql-client -y
```

### 3. Create Python Virtual Environment
```bash
cd /home/user/hisp
python3 -m venv streamlit_env
source streamlit_env/bin/activate
```

### 4. Install Python Dependencies
```bash
# Install required packages
pip install --upgrade pip
pip install streamlit==1.28.0
pip install pandas==2.0.3
pip install plotly==5.17.0
pip install sqlalchemy==2.0.21
pip install psycopg2-binary==2.9.7
pip install python-dotenv==1.0.0
pip install geopandas==0.14.0
pip install folium==0.15.0
pip install streamlit-folium==0.15.0
```

### 5. Configure Database Connection
```bash
# Edit the .env file with your database credentials
nano .env
```

Update the .env file with your server's database details:
```bash
# Database Configuration
DB_HOST=your-database-host
DB_PORT=5432
DB_NAME=uganda_dwh
DB_USER=your-username
DB_PASSWORD=your-password
```

### 6. Test Database Connection
```bash
# Test connection
python3 -c "from config import test_connection; test_connection()"
```

### 7. Run the Application

#### Development Mode (for testing):
```bash
source streamlit_env/bin/activate
streamlit run main_report.py --server.port 8501
```

#### Production Mode (recommended):
```bash
# Create systemd service file
sudo nano /etc/systemd/system/disease-dashboard.service
```

Add the following content:
```ini
[Unit]
Description=Disease Report Dashboard
After=network.target

[Service]
Type=simple
User=user
WorkingDirectory=/home/user/hisp
Environment=PATH=/home/user/hisp/streamlit_env/bin
ExecStart=/home/user/hisp/streamlit_env/bin/streamlit run main_report.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable disease-dashboard.service
sudo systemctl start disease-dashboard.service
```

### 8. Configure Firewall (if needed)
```bash
# Allow port 8501 through firewall
sudo ufw allow 8501
```

### 9. Access the Application
Open your browser and navigate to:
```
http://your-server-ip:8501
```

#### URL Parameters
You can customize the dashboard view using URL parameters:
```
http://localhost:8502/?year=2024&month=all&orgunit=national
```

Available parameters:
- `year`: Year for data filtering (default: 2025)
- `month`: Month filter (default: all)
- `orgunit`: Organization unit level - national, regional, or district (default: national)

Examples:
```
# View 2023 data for all months at national level
http://localhost:8502/?year=2023&month=all&orgunit=national

# View January 2024 data at regional level
http://localhost:8502/?year=2024&month=january&orgunit=regional

# View specific district data for March 2025
http://localhost:8502/?year=2025&month=march&orgunit=district
```

## File Structure
```
hisp/
├── main_report.py          # Main Streamlit application
├── data_fetcher.py         # Database query functions
├── choropleth_data.py      # Map data functions
├── config.py              # Database configuration
├── .env                   # Environment variables (database credentials)
├── uganda_districts.geojson # Geographic boundaries
├── streamlit_env/         # Python virtual environment
└── README.md             # This file
```

## Troubleshooting

### Database Connection Issues
```bash
# Test database connectivity
python3 -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='your-host',
        port='5432', 
        database='uganda_dwh',
        user='your-user',
        password='your-password'
    )
    print('Database connection successful')
    conn.close()
except Exception as e:
    print(f'Connection failed: {e}')
"
```

### Service Status Check
```bash
# Check service status
sudo systemctl status disease-dashboard.service

# View logs
sudo journalctl -u disease-dashboard.service -f
```

### Performance Issues
- Ensure adequate RAM (2GB+ recommended)
- Monitor database query performance
- Adjust Streamlit caching settings if needed

### Port Already in Use
```bash
# Find process using port 8501
sudo netstat -tlnp | grep :8501

# Kill process if needed
sudo kill -9 <process-id>
```

## Maintenance

### Update Application
```bash
cd /home/user/hisp
source streamlit_env/bin/activate

# Pull updates (if using git) or replace files
# Then restart service
sudo systemctl restart disease-dashboard.service
```

### Monitor Logs
```bash
# View application logs
sudo journalctl -u disease-dashboard.service --since "1 hour ago"
```

### Backup Configuration
```bash
# Backup important files
cp .env .env.backup
cp config.py config.py.backup
```

## Security Notes
- Keep .env file permissions restricted: `chmod 600 .env`
- Use strong database passwords
- Consider using SSL for database connections
- Regularly update system packages
- Consider setting up a reverse proxy (nginx) for production

## Support
- Check database connectivity first for any data loading issues
- Verify all environment variables are correctly set
- Monitor system resources (RAM, disk space)
- Review application logs for specific error messages