from app import create_app

newApp = create_app()

if __name__ == "__main__":
    newApp.run(debug=True)