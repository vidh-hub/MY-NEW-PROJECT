"""Generic WSGI entry point for cloud hosts (Render, Railway, etc.)."""

from app import app

application = app

if __name__ == "__main__":
    app.run()
