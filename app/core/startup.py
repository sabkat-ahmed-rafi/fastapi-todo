from core.exceptions.handlers import register_exception_handler

def setup_app(app):
    register_exception_handler(app)