import json
import cv2
from flask import current_app, request, abort
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, ImageMessageContent

from api.routes import ApiRouteInterface
from model.gcp import GCPVertexAI
from model.line_connection import LineConnection
from utils.image import preprocess_image


class LineWebhookPostRoute(ApiRouteInterface):
    __line_connection: LineConnection
    __gcp_vertex_ai: GCPVertexAI

    def __init__(
        self, line_connection: LineConnection, gcp_vertex_ai: GCPVertexAI
    ) -> None:
        self.__line_connection = line_connection
        self.__vertex_ai = gcp_vertex_ai

    def register(self, app):
        @app.post("/webhook")
        def line_webhook_post():
            # get X-Line-Signature header value
            signature = request.headers["X-Line-Signature"]
            # get request body as text
            body = request.get_data(as_text=True)
            print("Request body: " + body)
            body_json = json.loads(body)
            # handle webhook body
            try:
                if (
                    len(body_json["events"]) > 0
                    and body_json["events"][0]["message"]["type"] == "image"
                ):
                    if (
                        body_json["events"][0]["deliveryContext"]["isRedelivery"]
                        == True
                    ):
                        return "OK", 200
                    image_id = body_json["events"][0]["message"]["id"]
                    user_id = body_json["events"][0]["source"]["userId"]
                    self.__line_connection.handler.handle(body, signature)

                    # Preprocess image
                    data = self.__line_connection.get_content(image_id)
                    image_np = cv2.imdecode(data, cv2.IMREAD_COLOR)
                    image = preprocess_image(image_np)

                    # Predict
                    self.__vertex_ai.init_aiplatform()
                    answer = self.__vertex_ai.predict(image.tolist())

                    self.__line_connection.send_message(user_id, answer)
                else:
                    self.__line_connection.handler.handle(body, signature)
            except InvalidSignatureError as e:
                current_app.logger.info(
                    "Invalid signature. Please check your channel access token/channel secret."
                )
                self.__line_connection.send_message(
                    user_id, "ประเมินผลล้มเหลวเนื่องจากมีข้อผิดพลาดเกี่ยวกับไลน์"
                )
                print(e.message)
                return "OK", 200
            except Exception as e:
                self.__line_connection.send_message(
                    user_id, "ประเมินผลล้มเหลวเนื่องจากมีข้อผิดพลาดบางอย่าง กรุณาลองใหม่ภายหลัง"
                )
                print(e)
                return "OK", 200

            return "OK", 200

        @self.__line_connection.handler.add(MessageEvent, message=TextMessageContent)
        def handle_message(event):
            with ApiClient(self.__line_connection.configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(self.__line_connection.handle_image(text=event.message.text))],  # type: ignore
                    )
                )

        @self.__line_connection.handler.add(MessageEvent, message=ImageMessageContent)
        def handle_image(event):
            with ApiClient(self.__line_connection.configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text="กำลังประมวลผล")],  # type: ignore
                    )
                )
