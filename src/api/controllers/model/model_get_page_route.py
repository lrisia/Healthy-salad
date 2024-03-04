from flask import render_template
from api.routes import PageRouteInterface


class ModelGetPageRoute(PageRouteInterface):
    def register(self, app):
        @app.get("/model/predict")
        def model_get_page():
            return render_template("index.html")
