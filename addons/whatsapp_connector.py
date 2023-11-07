import logging
import inspect
import httpx
import json
from sanic import Sanic, Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from typing import Text, Callable, Awaitable, Optional, Dict, Any

from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    UserMessage,
    OutputChannel,
)

logger = logging.getLogger(__name__)
client = httpx.AsyncClient()


class WhatsAppIO(InputChannel):
    def name(self) -> Text:
        """Name of your custom channel."""
        return "whatsappio"

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> InputChannel:
        if not credentials:
            cls.raise_missing_credentials_exception()

        return cls(
            credentials.get("api_url"),
            credentials.get("api_key"),
            credentials.get("whatsapp_number"),
        )

    def __init__(self, api_url, api_key, whatsapp_number) -> None:
        self.api_url = api_url
        self.api_key = api_key
        self.whatsapp_number = whatsapp_number

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        custom_webhook = Blueprint(
            "custom_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request) -> HTTPResponse:
            sender_id = request.json.get("sender")  # method to get sender_id
            text = request.json.get("message")  # method to fetch text
            input_channel = self.name()  # method to fetch input channel
            metadata = self.get_metadata(request)  # method to get metadata

            collector = CollectingOutputChannel()

            # include exception handling

            await on_new_message(
                UserMessage(
                    text,
                    collector,
                    sender_id,
                    input_channel=input_channel,
                    metadata=metadata,
                )
            )

            logger.info(len(collector.messages))

            if len(collector.messages) > 1:
                for message in collector.messages:
                    payload_message = {
                        "number": f"{sender_id}",
                        "options": {
                            "delay": 1200,
                            "presence": "composing",
                            "linkPreview": False,
                        },
                        "textMessage": message,
                    }

                    await client.post(
                        url=f"{self.api_url}/message/sendText/aguiardev",
                        headers={
                            "Content-Type": "application/json",
                            "apikey": self.api_key,
                        },
                        json=payload_message,
                    )

            return response.json(collector.messages)

        return custom_webhook

    # def get_output_channel(self, remoteJid) -> OutputChannel:
    #     return WhatsAppOutput(self.whatsapp_number, self.api_key, remoteJid)
