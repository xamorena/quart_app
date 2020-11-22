from .application import application


if __name__ == "__main__":
    application.run('0.0.0.0', port=5000, debug=True)
