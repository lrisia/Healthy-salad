from typing import Union
import cv2
import numpy as np
from pydantic import BaseModel


class Task(BaseModel):
    image_id: str

    # For Line user
    user_id: str


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
