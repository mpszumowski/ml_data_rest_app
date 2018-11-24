import os

import connexion
from cheroot.wsgi import Server

from info import __version__, __title__

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
    bind_address = os.environ.get('APP_ADDRESS')
    port = int(os.environ.get('PORT'))
    server = Server((bind_address, port), app)
    server.start()
