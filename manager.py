import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from src import api, db, ma, create_app, configs, bp

config = os.environ.get('PYTH_SRVR')

config = configs.get(config, 'default')

extensions = [api, db, ma]
bps = [bp]

app = create_app(__name__, config, extensions=extensions, blueprints=bps)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.shell
def _shell_context():
    return dict(
        app=app,
        db=db,
        ma=ma,
        config=config
        )

if __name__ == "__main__":
    manager.run()
