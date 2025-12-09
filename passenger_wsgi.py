"""
cPanel Python App Configuration for o2switch
=============================================

Configuration fields in cPanel:
- Python version: 3.12.11
- Application root: /home/YOUR_USER/crosswords-analytics-api (or your path)
- Application URL: https://your-subdomain.your-domain.com
- Application startup file: passenger_wsgi.py
- Application Entry point: application
- Environment variables: Set DATABASE_URL and other vars in cPanel interface
"""

import os
import sys

# Add application directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables from .env file (backup if not set in cPanel)
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Import the FastAPI app
from app.main import app

# Entry point for cPanel Python App
# This is what cPanel's Passenger will call
application = app
