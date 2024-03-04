from typing import Union
import cv2
from flask import make_response, request
import numpy as np
from api.controllers.model.model_schema import ModelResponse
from api.routes import ApiRouteInterface
from api.shema import ApiTag, ErrorResponse, HttpStatus
from model.gcp import GCPVertexAI
from model.task import TaskQueueManager


class ModelPredictPostRoute(ApiRouteInterface):
    __vertex_ai: GCPVertexAI
    __queue_manager: TaskQueueManager

    def __init__(
        self,
        vertex_ai: GCPVertexAI,
        queue_manager: TaskQueueManager,
    ):
        self.__vertex_ai = vertex_ai
        self.__queue_manager = queue_manager

    def register(self, app):
        @app.post(
            "/model/predict",
            tags=[ApiTag.Model],
            description="Get predicted answers by input image",
            responses={
                HttpStatus.OK: ModelResponse,
                HttpStatus.INTERNAL_SERVER_ERROR: ErrorResponse,
            },
        )
        def model_predict_post():
            try:
                self.__vertex_ai.init_aiplatform()
                uploaded_file = request.files["img"]
                nparr = np.frombuffer(uploaded_file.stream.read(), np.uint8)
                image_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                image = self.__queue_manager.load_image(image_np)
                answer = self.__vertex_ai.predict(image.tolist())
                return make_response(
                    ModelResponse(message=None, answers=answer).model_dump(), 200
                )
            except Exception as e:
                return make_response(
                    ErrorResponse(
                        message="Internal Server Error", stacktrace=e.__str__()
                    ).model_dump(),
                    500,
                )
