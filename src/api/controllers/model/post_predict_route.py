from typing import Union
import cv2
from flask import request
import numpy as np
from api.routes import ApiRouteInterface
from model.gcp import GCPVertexAI
from model.task import TaskQueueManager


class PostPredictRoute(ApiRouteInterface):
    __vertex_ai: GCPVertexAI
    __queue_manager: TaskQueueManager

    def __init__(
        self,
        vertex_ai: Union[None, GCPVertexAI],
        queue_manager: Union[None, TaskQueueManager],
    ):
        if vertex_ai is None:
            raise ValueError("vertex_ai is required")
        if queue_manager is None:
            raise ValueError("queue_manager is required")
        self.__vertex_ai = vertex_ai
        self.__queue_manager = queue_manager

    def register(self, app):
        @app.post("/model/predict")
        def predict():
            self.__vertex_ai.init_aiplatform()
            uploaded_file = request.files["img"]
            nparr = np.frombuffer(uploaded_file.stream.read(), np.uint8)
            image_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            image = self.__queue_manager.load_image(image_np)
            answer = self.__vertex_ai.vertex_ai_predict(image.tolist())
            return {"answer": answer}, 200
