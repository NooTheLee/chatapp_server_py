from app import create_app

_app = create_app()

if __name__ == "__main__":
    _app.run(debug=True, port=5057)
