import connexion
from cheroot.wsgi import Server

from ml_data.config import rest_cfg
from ml_data.info import __version__, __title__

connexion_app = connexion.FlaskApp(
    __name__,
    specification_dir='.',
    options={
        "swagger_ui": True
    },
    arguments={
        'title': __title__,
        'version': __version__
    }
)
connexion_app.add_api('swagger.yaml')
app = connexion_app.app

if __name__ == "__main__":
    bind_address = (rest_cfg['address'], int(rest_cfg['port']))
    server = Server(bind_address, app)
    print('starting server...')
    server.start()
