from main import make_app

# start server
app = make_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8789')
