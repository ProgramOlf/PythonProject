from __init__ import create_app

app = create_app()
app.config['SECRET_KEY'] = 'Holzbau'

if __name__ == '__main__':
    app.run(debug=True)