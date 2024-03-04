from http import HTTPStatus

from flask import make_response
from api.routes import ApiRouteInterface


class PostPredictQueueRoute(ApiRouteInterface):
    def register(self, app):
        @app.post(
            "/model/predict",
            tags=[],
            description="Add a new prediction task to the queue.",
            responses={
                # 200: DefaultResponse,
                # 500: ErrorResponse,
            }
        )
        def add_predict_queue():
            return make_response({"message": "Healthy"}, HTTPStatus.OK)