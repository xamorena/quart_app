from .application import application


if __name__ == "__main__":
    application.run('localhost', port=5000, debug=True)
