from .auth_controller import auth_bp
from .chatroom_controller import chatroom_bp
from .message_controller import message_bp
from .user_controller import user_bp

def register_all_blueprints(app):
    app.register_blueprint(auth_bp,  url_prefix="/api/Auth")
    app.register_blueprint(chatroom_bp, url_prefix="/api/Chatroom")
    app.register_blueprint(message_bp, url_prefix="/api/Message")
    app.register_blueprint(user_bp, url_prefix="/api/User")