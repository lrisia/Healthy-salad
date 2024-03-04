import os
from click import option
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
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
import firebase_admin


class PlaygroundCommand(CommandInterface):

    def execute(self):
        print("Welcome to playground!")

        config = get_config()

        # url = "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
        # headers = {"Metadata-Flavor": "Google"}
        # response = requests.get(url, headers=headers).json()
        # credentials = GCPAuthToken(**response)

        # print(response)

        # cred = Credentials(
        #     "ya29.c.c0AY_VpZj1GEdvvhv3VYl3oehjWJzNRz1Lqxy3qY_k-A0de7eM1IfRJvErxk2S7fh7cfQ8TnKHEhIGIW11bXXJ1Sw7PZf_Ac_KrBd7xXGsuNGRFcG_IM9jaoTHK9uWidsWhQIWDw1yorRQmi5nViLaV3WVknNpJcRyTsl-rofYNVSVYZx-K6qv04Nxq4OpIo6RQ4m_LBbyLIQprsyio1IFKNARSBfxVipczoHyn4rKzlfDZ1UQ_redDBo0PXgtfdW6K3LJCj1gCoNtTTL0ElNGscl1p6BqQ_Yx6CMGoNYmQwTVFNPxw29Ko4tmPWMdk6871jhn3XBlZpivEOVIhahmUt-Rlb8XDZmC5m2keCgWbSYJ0iB6ptgA_DiqNRBzc88_wXitu0vbRIqSxpcPVBnX4R3GYBlFvw8EVZ9sqV9vws5oMvAuC_z2or22QYYib9vuOy5BBIwSXNSUFkkHvua1N477PraB9qaibJJ0ledqXS2rxrIxYo3yfqBlus4waaU24hgWy_VjxqpURFaZOS_g3v-dSmwYykOvWMwSJRslo-B6p6aSzBmpjUfVfOZWbRhm2Q53rf8QigIdXqxOVs1pdlntcwxsk7c_JOyjQpdrhcZ9zhByFu_gvFcdq1blbintF4lX3jB-5Q_ZdsSnj9fOZcvsFu038Xr4jim2hhlh8RaFwB-dsJFJy4JjOfXl0urWacti2mUpmS3jY7ZqWQ2QQ0bWw6jSmYSeSqJ4t-FdptuveuiY5Xj2mnVF1kaRvxWk7FkWc16zS2Mz3Yye62fgiaciuUtjwtXldM6xcrUJ9Zu3f2cqqRhzQeR83UV2n6x9kjyifuVzgFkdZs_O-Bm0cfuaR691RI-tUkXW31lv9yyInx_I5jbXc7uofwR_pxy7i4lQa4qbMQgiMpUI82V3itFzf2Uf_8rhjf6utax8hxktpF6uB-Sp0pl143W34tB8s8adakb0RzZV_ovJlOsgpcaJ9oJzJIz8w6atRModZq4r9mbQ8p9M3ob"
        # ) # Expired
        cred = Credentials(
            "ya29.c.c0AY_VpZhYkC82YAkjAWF8P0Xfq--ARNcOPKWsuFnC4WeIk9uhT6Lyygek1lWW-VxX0Rb3WlXakEaEeWO_w9-L2dVEA1HI5o20d9fcrSaEahc6u_0zko_SPqyKkLz-ahYHo9Xva6WCgU-ZEa8UESlG3AM28xf67z2c973eo8JyYLs3Qy0QQBRuuPUzPNssTOTyllYiKtx9V8Q2aA6wy_UFlXCURC8xTlx-aD6AS4Ef-R2ymWLQ6al_qI9bvD2onv4r7L5FmboWhma1ThtH_RxEkFRjr1FJrUz6_tkdrJFzoi9ihWK-qLSfiq8SOpXlnMYlb0ExArJjmf86IolXByHRiODIlDquJW62G2GgiXKqNjOZVJSaZRaQ43iVw6ivqR80tpfuZ14L595usNKql7VsN_QeBRawlosSc2RPDn102qE6Zl3Z1SylelE-IvN6hPkiX56NtjE4VNE9UTcycFD_T477AUIUfxIoM2R38voot0x46u4cxhXn59br9kxvSq9s4hge6Vy18wS1lYjheFytlpwWiIhIduYtie91y1cs5gxY7VzrZxx44kdjpcnnn3-bpwcsi-9xOw8bxYJb7kVX_zJ0sR5it2Zfzp4Y8b3wgbymg2d7vfBxiM7rq1FYuZ3VZr9wrfztnIXvY92zdky68btyk1O40xmdx7Zwgi30a-lSufnfw7x9W9XrY139rROyo99a-vwRbjkIo0pUotwz-yjUMQiMUtmYij0sJiZv5a-U-9582Yqkr8ti4U88OUUurh-9nxy4jVqoYOOgR601S1ox7Jfeo4kgOFaOtWVfaqrUg52WOpQB4QRpY3xgZkq7ZMlmMSBQQcSy437Yq534Z5seayoFrVl3r8syW414vIuXU9SrfweIxths8J_dtnwsFg5BarrZdf0IkrajyWi3rRbxvQ69x5VUfXb4uBq_pqpXlineB9Yzdosog82jVwfftqhm-jYwv--3Uzfpmbul9cRk8XylWFZ8stUiQQjJIUrObcMBViq0pkh"
        )

        # aiplatform.init(
        #     location="asia-southeast1", credentials=cred
        # )

        firebase_admin.initialize_app(options={
            "serviceAccountId": "deployer-service@healthy-salad-414811.iam.gserviceaccount.com"
        })

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

        predict_img_path = os.path.join(config.ROOT_DIR, "example_image.jpg")
        predict_img = import_image(predict_img_path)

        # Make predictions using the custom trained model
        prediction_result = predict_custom_trained_model(
            instances=predict_img.tolist(),
            project_number=config.GCP_PROJECT_NUMBER,
            endpoint_id=config.GCP_ENDPOINT_ID,
        )

        # Print the predicted class
        print(prediction_result[0])
