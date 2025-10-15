# Citizens Management System

A modern web application for managing citizen records with live PostgreSQL database integration. Features real-time search, arrest status management, and configurable database connections.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 📋 Features

- ✅ **Live Database Search** - Search citizens by name, surname, or phone number in real-time
- ✅ **Instant Updates** - Toggle arrest status with immediate database updates
- ✅ **Configurable Connection** - Change database settings through the web interface
- ✅ **Auto-Refresh** - Live sync with database every 5 seconds
- ✅ **Status Filtering** - Filter by arrested/free status
- ✅ **Dark Modern UI** - Clean, professional interface
- ✅ **Statistics Dashboard** - Real-time count of total, arrested, and free citizens

## 🖥️ System Requirements

- Python 3.7 or higher
- PostgreSQL database with a "Citizen" table
- Modern web browser (Chrome, Firefox, Edge, Safari)

## 📦 Installation

### Windows

#### Step 1: Install Python
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer and **check "Add Python to PATH"**
3. Verify installation:
```cmd
python --version
```

#### Step 2: Clone or Download the Project
```cmd
cd C:\Users\YourName\Desktop
mkdir citizens-management
cd citizens-management
```

#### Step 3: Create Project Structure
Create the following files and folders:
```
citizens-management/
├── app.py
├── requirements.txt
├── README.md
└── templates/
    └── citizens.html
```

#### Step 4: Install Dependencies
```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 5: Run the Application
```cmd
python app.py
```

#### Step 6: Open in Browser
Open your browser and go to: `http://localhost:5000`

---

### Linux (Ubuntu/Debian)

#### Step 1: Update System
```bash
sudo apt update
sudo apt upgrade -y
```

#### Step 2: Install Python and pip
```bash
sudo apt install python3 python3-pip python3-venv -y
python3 --version
```

#### Step 3: Clone or Download the Project
```bash
cd ~
mkdir citizens-management
cd citizens-management
```

#### Step 4: Create Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 5: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 6: Run the Application
```bash
python3 app.py
```

#### Step 7: Open in Browser
Open your browser and go to: `http://localhost:5000`

To access from other devices on your network: `http://YOUR_IP_ADDRESS:5000`

---

### Linux (CentOS/RHEL/Fedora)

#### Step 1: Update System
```bash
sudo dnf update -y
# or for older systems
sudo yum update -y
```

#### Step 2: Install Python
```bash
sudo dnf install python3 python3-pip -y
# or
sudo yum install python3 python3-pip -y
```

#### Step 3: Follow the same steps as Ubuntu from Step 3 onwards

---

## ⚙️ Database Configuration

### Initial Setup

The application comes with default PostgreSQL settings:
- **Host:** localhost
- **Port:** 5432
- **Database:** snaily-cadv41
- **User:** postgres
- **Password:** admin1

### Change Database Settings

**Option 1: Via Web Interface (Recommended)**
1. Open the application in your browser
2. Click "⚙️ Database Settings" button
3. Enter your database credentials:
   - Host (e.g., localhost, 192.168.1.100, db.example.com)
   - Port (default: 5432)
   - Database name
   - Username
   - Password
4. Click "🔍 Test Connection" to verify
5. Click "💾 Save & Apply" to save settings

**Option 2: Edit db_config.json**

The application creates a `db_config.json` file on first run. You can edit it manually:
```json
{
  "host": "localhost",
  "port": 5432,
  "database": "your_database_name",
  "user": "your_username",
  "password": "your_password"
}
```

### Database Requirements

Your PostgreSQL database must have a table named `Citizen` with at least these columns:
- `id` (UUID or text) - Primary key
- `name` (text) - Citizen's first name
- `surname` (text) - Citizen's last name
- `arrested` (boolean) - Arrest status
- `phoneNumber` (text, optional) - Phone number

Example SQL to create the table:
```sql
CREATE TABLE public."Citizen" (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    arrested BOOLEAN DEFAULT FALSE,
    "phoneNumber" VARCHAR(50)
);
```

---

## 🚀 Usage Guide

### Starting the Application

**Windows:**
```cmd
cd C:\path\to\citizens-management
python app.py
```

**Linux:**
```bash
cd /path/to/citizens-management
source venv/bin/activate  # If using virtual environment
python3 app.py
```

### Accessing the Application

- **Local:** http://localhost:5000
- **Network:** http://YOUR_IP_ADDRESS:5000

### Using the Interface

1. **Search Citizens**
   - Type in the search box to filter by name, surname, or phone number
   - Results update in real-time from the database

2. **Filter by Status**
   - Use the dropdown to show "All Status", "Free Only", or "Arrested Only"

3. **Update Arrest Status**
   - Toggle switch LEFT (Green) = Free
   - Toggle switch RIGHT (Red) = Arrested
   - Changes save immediately to the database
   - Status indicator shows "✓ Saved to DB" when successful

4. **View Statistics**
   - Top cards show Total Citizens, Arrested, and Free counts
   - Updates automatically

5. **Manual Refresh**
   - Click "↻ Refresh Now" to force a data refresh
   - Auto-refresh runs every 5 seconds

---

## 🛑 Stopping the Application

Press `CTRL + C` in the terminal/command prompt where the app is running.

---

## 🔧 Troubleshooting

### Connection Errors

**Error: "Connection refused"**
- Check if PostgreSQL is running
- Verify host and port are correct
- Check firewall settings

**Error: "Authentication failed"**
- Verify username and password
- Check PostgreSQL pg_hba.conf for authentication method

**Error: "Database does not exist"**
- Verify database name is correct
- Create the database if it doesn't exist

### Port Already in Use

If port 5000 is already in use, change it in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001 or any free port
```

### Permission Issues (Linux)

If you get permission errors, try:
```bash
sudo python3 app.py
```

Or run on a higher port (> 1024):
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

---

## 🌐 Running as a Service (Production)

### Linux (systemd)

Create a service file:
```bash
sudo nano /etc/systemd/system/citizens-management.service
```

Add this content:
```ini
[Unit]
Description=Citizens Management System
After=network.target postgresql.service

[Service]
User=youruser
WorkingDirectory=/path/to/citizens-management
Environment="PATH=/path/to/citizens-management/venv/bin"
ExecStart=/path/to/citizens-management/venv/bin/python app.py

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable citizens-management
sudo systemctl start citizens-management
sudo systemctl status citizens-management
```

### Windows (NSSM - Non-Sucking Service Manager)

1. Download NSSM from [nssm.cc](https://nssm.cc/)
2. Install the service:
```cmd
nssm install CitizensManagement "C:\Python39\python.exe" "C:\path\to\app.py"
nssm start CitizensManagement
```

---

## 📊 Database Schema

The application expects a PostgreSQL table with this structure:
```sql
CREATE TABLE public."Citizen" (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    arrested BOOLEAN DEFAULT FALSE,
    "phoneNumber" VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Create indexes for better performance
CREATE INDEX idx_citizen_name ON public."Citizen"(LOWER(name));
CREATE INDEX idx_citizen_surname ON public."Citizen"(LOWER(surname));
CREATE INDEX idx_citizen_arrested ON public."Citizen"(arrested);
```

---

## 🔐 Security Notes

⚠️ **Important Security Considerations:**

1. **Change the Secret Key** - Edit `app.py` and change:
```python
   app.secret_key = 'your-secret-key-change-this-to-something-random'
```

2. **Don't Expose Publicly** - This application has no authentication. Only run it on trusted networks.

3. **Use HTTPS in Production** - Use a reverse proxy like nginx with SSL certificates.

4. **Database Credentials** - Keep `db_config.json` secure and don't commit it to version control.

5. **Firewall** - Configure firewall to restrict access:
```bash
   # Linux
   sudo ufw allow from 192.168.1.0/24 to any port 5000
```

---

## 📝 License

MIT License - Feel free to use and modify as needed.

---

## 🐛 Known Issues

- Limited to 200 citizens per query (configurable in code)
- No user authentication/authorization
- No backup/restore functionality
- No audit logging

---

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review console logs for error messages
3. Check PostgreSQL logs

---

## 🎯 Future Enhancements

- [ ] User authentication
- [ ] Audit logging
- [ ] Export to CSV/Excel
- [ ] Bulk operations
- [ ] Advanced filtering
- [ ] Mobile responsive improvements
- [ ] Dark/Light theme toggle

---

**Made with ❤️ for SnailyCAD**
