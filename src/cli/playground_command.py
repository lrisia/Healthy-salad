import os
import cv2
import numpy as np
import requests
from cli.command_interface import CommandInterface
from google.cloud import aiplatform
from config import get_config
from model.gcp import GCPAuthToken
import google.auth
import google.auth.transport.requests
from google.auth import compute_engine


class PlaygroundCommand(CommandInterface):

    def execute(self):
        print("Welcome to playground!")

        cred = compute_engine.Credentials()
        aiplatform.init(location="asia-southeast1",
                        credentials=cred)
        
        # url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
        # headers = {"Metadata-Flavor": "Google"}
        # gcp_response: GCPAuthToken = requests.get(url, headers=headers).json()
        

        def import_image(path: str, image_size: int = 224):
            img = cv2.resize(cv2.imread(path), (image_size, image_size))
            img_gray_scale = np.expand_dims(
                cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), axis=-1
            )
            return img_gray_scale

        def predict_custom_trained_model(instances, project_number, endpoint_id):
            endpoint = aiplatform.Endpoint(
                endpoint_name=f"projects/{project_number}/locations/asia-southeast1/endpoints/{endpoint_id}"
            )
            result = endpoint.predict(instances=[instances])
            return result.predictions

        config = get_config()
        predict_img_path = (
            os.path.join(config.ROOT_DIR, "example_image.jpg")
        )
        predict_img = import_image(predict_img_path)

        # Make predictions using the custom trained model
        prediction_result = predict_custom_trained_model(
            instances=predict_img.tolist(),
            project_number=config.GCP_PROJECT_NUMBER,
            endpoint_id=config.GCP_ENDPOINT_ID,
        )

        # Print the predicted class
        print(prediction_result[0])
