from app import create_app
# from werkzeug.contrib.fixers import ProxyFix

app = create_app('development')
# app.wsgi_app = ProxyFix(app.wsgi_app)
application = app

if __name__ == '__main__':
    application.run()
