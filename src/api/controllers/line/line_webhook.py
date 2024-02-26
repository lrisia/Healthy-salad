import sys
from flask import Flask, request, abort
from api.controllers.api_route_interface import ApiRoute
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)


class LineWebhookPostRoute(ApiRoute):
    def register(self, server: Flask, conf: tuple[Configuration, WebhookHandler]):
        configuration, handler = conf
      
        @server.route("/callback", methods=['POST'])
        def callback():
            # get X-Line-Signature header value
            signature = request.headers['X-Line-Signature']

            # get request body as text
            body = request.get_data(as_text=True)
            print("Request body: " + body, file=sys.stderr)

            # handle webhook body
            try:
                handler.handle(body, signature)
            except InvalidSignatureError:
                server.logger.info("Invalid signature. Please check your channel access token/channel secret.")
                abort(400)

            return 'OK', 200
        
        @handler.add(MessageEvent, message=TextMessageContent)
        def handle_message(event):
            with ApiClient(configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=event.message.text)] # type: ignore
                    )
                )
