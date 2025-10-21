import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2

# Load environment variables from .env file
load_dotenv(override=True)

# Test connectivity to production server, fallback to localhost if not accessible
def test_network_connectivity(host, port, timeout=5):
    import socket
    try:
        sock = socket.create_connection((host, int(port)), timeout=timeout)
        sock.close()
        return True
    except (socket.error, socket.timeout):
        return False

# Get production settings from .env
PROD_HOST = os.getenv('DB_HOST')
PROD_USER = os.getenv('DB_USER')

# Test if production server is accessible
if PROD_HOST and test_network_connectivity(PROD_HOST, os.getenv('DB_PORT', '5432')):
    # Use production settings - you're on the network
    DB_HOST = PROD_HOST
    DB_USER = PROD_USER
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    print(f"Connected to production database at {DB_HOST}")
else:
    # Fallback to localhost - you're not on the intranet
    DB_HOST = 'localhost'
    DB_USER = 'postgres'
    DB_PASSWORD = ''
    print(f"Using localhost fallback database")

DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'uganda_dwh')

# PostgreSQL connection string with timeout parameters
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?connect_timeout=30&application_name=disease_report_app"

# SQLAlchemy engine with connection pooling and timeout settings
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,
    connect_args={
        "connect_timeout": 30,
        "options": "-c statement_timeout=60s",
        "application_name": "disease_report_app"
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_connection():
    """Get a direct psycopg2 connection with timeout settings"""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=30,
        application_name="disease_report_app",
        options="-c statement_timeout=60s"
    )

def get_db_session():
    """Get SQLAlchemy session"""
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        raise e

def test_connection():
    """Test database connection"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Connected to PostgreSQL: {version[0]}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False