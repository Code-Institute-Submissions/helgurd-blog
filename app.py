from blog import app
import eventlet.wsgi

port = 9000
if __name__ == "__main__":
    app.run()
    # eventlet.wsgi.server(eventlet.listen(('', port)), app)



