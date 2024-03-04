from flask import render_template
from api.routes import PageRouteInterface


class GetPredictPageRoute(PageRouteInterface):
    def register(self, app):
        @app.get("/model/predict")
        def predict_page():
            return render_template("index.html")
