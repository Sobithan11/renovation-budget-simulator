from flask import Flask

from database import initialise_database
from routes.simulation import simulation_bp
from routes.projects import projects_bp


app = Flask(__name__)

initialise_database()

app.register_blueprint(simulation_bp)
app.register_blueprint(projects_bp)


if __name__ == "__main__":
    app.run(debug=True)