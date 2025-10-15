from flask import Flask, render_template, request, jsonify, session
import pg8000
import logging
import json
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-to-something-random'

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Config file path
CONFIG_FILE = 'db_config.json'

# Default database settings
DEFAULT_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'snaily-cadv41',
    'user': 'postgres',
    'password': 'admin1'
}

def load_db_config():
    """Load database config from file or return default"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return DEFAULT_CONFIG.copy()

def save_db_config(config):
    """Save database config to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def get_db_connection():
    """Get database connection using current config"""
    config = load_db_config()
    try:
        conn = pg8000.connect(
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=int(config['port']),
            database=config['database']
        )
        return conn
    except Exception as e:
        app.logger.error(f"Database connection error: {e}")
        raise

@app.route("/")
def citizens():
    return render_template("citizens.html")

@app.route("/api/db-config", methods=["GET"])
def get_config():
    """Get current database configuration (without password)"""
    config = load_db_config()
    # Don't send password to frontend
    safe_config = config.copy()
    safe_config['password'] = '••••••••' if config['password'] else ''
    return jsonify(safe_config)

@app.route("/api/db-config", methods=["POST"])
def update_config():
    """Update database configuration"""
    try:
        data = request.json
        config = {
            'host': data.get('host', 'localhost'),
            'port': int(data.get('port', 5432)),
            'database': data.get('database', ''),
            'user': data.get('user', ''),
            'password': data.get('password', '')
        }
        
        # Save the new config
        save_db_config(config)
        app.logger.info(f"Database config updated: {config['host']}:{config['port']}/{config['database']}")
        
        return jsonify({'success': True, 'message': 'Configuration saved successfully'})
    except Exception as e:
        app.logger.error(f"Error updating config: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route("/api/test-connection", methods=["POST"])
def test_connection():
    """Test database connection with provided credentials"""
    try:
        data = request.json
        
        # Try to connect with provided credentials
        conn = pg8000.connect(
            user=data.get('user'),
            password=data.get('password'),
            host=data.get('host'),
            port=int(data.get('port', 5432)),
            database=data.get('database')
        )
        
        # Test query
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM public."Citizen"')
        count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': f'Connection successful! Found {count} citizens in database.'
        })
    except Exception as e:
        app.logger.error(f"Connection test failed: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route("/api/citizens", methods=["GET"])
def get_citizens():
    """API endpoint for live data fetching with search"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get search and filter parameters
        search_query = request.args.get('search', '').strip()
        status_filter = request.args.get('status', 'all')
        
        # Build the SQL query
        sql = 'SELECT id, name, surname, arrested, "phoneNumber" FROM public."Citizen"'
        params = []
        where_clauses = []
        
        # Add search filter
        if search_query:
            search_pattern = f'%{search_query}%'
            where_clauses.append(
                '(LOWER(name) LIKE LOWER(%s) OR LOWER(surname) LIKE LOWER(%s) OR LOWER("phoneNumber") LIKE LOWER(%s))'
            )
            params.extend([search_pattern, search_pattern, search_pattern])
            app.logger.info(f"Searching database for: {search_query}")
        
        # Add status filter
        if status_filter == 'arrested':
            where_clauses.append('arrested = TRUE')
        elif status_filter == 'free':
            where_clauses.append('arrested = FALSE')
        
        # Combine WHERE clauses
        if where_clauses:
            sql += ' WHERE ' + ' AND '.join(where_clauses)
        
        sql += ' ORDER BY surname, name LIMIT 200'
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        
        app.logger.info(f"Found {len(rows)} citizens")
        
        # Convert to JSON-friendly format
        citizens = []
        for row in rows:
            citizens.append({
                'id': str(row[0]),
                'name': row[1],
                'surname': row[2],
                'arrested': bool(row[3]),
                'phoneNumber': row[4]
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({'citizens': citizens, 'count': len(citizens)})
    
    except Exception as e:
        app.logger.error(f"Error fetching citizens: {e}")
        return jsonify({'error': str(e), 'citizens': [], 'count': 0}), 500

@app.route("/update", methods=["POST"])
def update_citizen():
    """Handle instant citizen updates - sets arrested to TRUE or FALSE"""
    try:
        citizen_id = request.form.get("citizen_id")
        arrested_value = request.form.get("arrested") == "on"
        
        app.logger.info(f"Updating citizen {citizen_id}: Setting arrested = {arrested_value}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Update the arrested column to TRUE or FALSE
        if arrested_value:
            cursor.execute(
                'UPDATE public."Citizen" SET arrested = TRUE WHERE id = %s',
                (citizen_id,)
            )
        else:
            cursor.execute(
                'UPDATE public."Citizen" SET arrested = FALSE WHERE id = %s',
                (citizen_id,)
            )
        
        conn.commit()
        
        # Verify the update
        cursor.execute(
            'SELECT arrested FROM public."Citizen" WHERE id = %s',
            (citizen_id,)
        )
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True, 
            'arrested': arrested_value,
            'verified': result[0] if result else None
        })
    
    except Exception as e:
        app.logger.error(f"Error updating citizen: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
