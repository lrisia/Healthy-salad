from typing import Union
import cv2
import numpy as np
from pydantic import BaseModel


class Task(BaseModel):
    image_path: str

    # For Line user
    reply_token: str


class TaskQueueManager:
    queue: list[Task]

    def __init__(self):
        self.queue = []

    def add(self, task: Task) -> None:
        self.queue.append(task)

    def get(self) -> Task:
        return self.queue.pop(0)

    def is_empty(self) -> bool:
        return len(self.queue) == 0

    # Process with task
    def load_image(
        self, source: Union[np.ndarray, str], image_size: int = 224
    ) -> np.ndarray:
        image: np.ndarray
        if isinstance(source, str):
            image = cv2.imread(source)
        else:
            image = source
        resized_img = cv2.resize(image, (image_size, image_size))
        img_gray_scale = np.expand_dims(cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY), axis=-1)
        return img_gray_scale
