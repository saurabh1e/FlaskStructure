from flask import Flask


def create_app(package_name, config, blueprints=None, extensions=None):
    app = Flask(package_name)
    app.config.from_object(config)
    config.init_app(app)

    if blueprints:
        for bp in blueprints:
            app.register_blueprint(bp)
    print(blueprints, app.blueprints.values())
    if extensions:
        for extension in extensions:
            extension.init_app(app)

    return app