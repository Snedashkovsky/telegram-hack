# from fluence.fluence_client import FluenceClient
import requests
import base64
import json


FLUENCE_PATH = "http://localhost:30000/apps/0/tx"

GLOBAL = {'session_id': 0, 'data_ids': []}


class FluenceClient():
    def __init__(self):
        print(GLOBAL)

    def _get_requests_data(self, body, action):
        body["action"] = action
        requests_data = '{session_id}\n{body}'.format(
            session_id=self._get_session_id(),
            body=json.dumps(body),
            action=action
        )
        print(requests_data)
        return requests_data

    def _get_session_id(self):
        return "sessionId/{id}".format(id=GLOBAL["session_id"])

    def _send_request(self, url, data):
        response = requests.post(url, data=data)
        response = response.json()
        GLOBAL["session_id"] += 1
        return base64.b64decode(response['result']['data']).decode("utf-8")

    def send_low_level_post(self, author, title, body, parent_link):
        body = {"data": body.replace('"', "'")}
        requests_data = self._get_requests_data(body, "AddData")
        response = self._send_request(FLUENCE_PATH, requests_data)
        response_json = json.loads(response)
        GLOBAL["data_ids"].append(response_json["data_id"])

    def get_posts(self, permlink_collection):
        messages = []
        votes = []
        for data_id in GLOBAL["data_ids"]:
            request_data = self._get_requests_data({"data_id": data_id}, "GetData")
            response = self._send_request(FLUENCE_PATH, request_data)
            response = json.loads(response)["data"].replace("'", '"')
            if 'voter' in response:
                votes.append(response)
            else:
                messages.append(response)

        print(messages)
        print(votes)

        return messages, votes