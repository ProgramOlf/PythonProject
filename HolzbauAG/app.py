from __init__ import create_app

# Create a flask instance from the __init__.py
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)