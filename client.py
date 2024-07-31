import typing as T
import requests
import uuid


class Client:
    def __init__(self, service: str) -> None:
        self.user_id = str(uuid.uuid4())
        self.service = service
        self.uri = "http://0.0.0.0:1432"

    def recv(self) -> T.Optional[dict]:
        r = requests.get(self.uri + "/inbox/" + self.user_id)
        message = r.json()
        print(message)

    def send(self, d: dict, to_user_id: str = "", to_service: str = "", **kwargs):
        d["from_user_id"] = self.user_id
        d["from_service"] = self.service
        d["to_user_id"] = to_user_id
        d["to_service"] = to_service
        r = requests.post(
            "http://0.0.0.0:1432/message",
            headers={"Content-Type": "application/json"},
            json=d,
        )
