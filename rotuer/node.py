from flask import Flask, request
import queue
import dataclasses as dc
import typing as T
import uuid

USER_ID = str(uuid.uuid4())
SERVICE = "node"

app = Flask(__name__)

inboxes = {}


@dc.dataclass
class RoutingInfo:
    from_user_id: str
    from_service: str
    to_user_id: str
    to_service: str

    @staticmethod
    def parse(d: T.Any) -> T.Optional["RoutingInfo"]:
        try:
            return RoutingInfo(
                d["from_user_id"],
                d["from_service"],
                d["to_user_id"],
                d["to_service"],
            )
        except KeyError:
            return None


@app.route("/")
def home():
    return ""


@app.route("/inbox/<user_id>", methods=["GET"])
def inbox(user_id):
    if user_id not in inboxes:
        inboxes[user_id] = queue.Queue()
    try:
        data = inboxes[user_id].get(block=False)
        return data, 200
    except queue.Empty:
        return {
            "from_user_id": USER_ID,
            "from_service": SERVICE,
            "to_user_id": user_id,
            "to_service": "",
            "message": "EMPTY INBOX",
        }, 200


@app.route("/message", methods=["POST"])
def message():
    data = request.json
    info = RoutingInfo.parse(data)
    if info is None:
        return "Error while parsing routing info", 400

    if info.to_user_id == "":
        for inbox in inboxes.values():
            inbox.put(data)
    else:
        if info.to_user_id in inboxes:
            inboxes[info.to_user_id].put(data)
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1432)
