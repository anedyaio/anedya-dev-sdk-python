import json


def _response_callback(self, client, userdata, message):
    # This callback is called when a message is received on response topic.
    payload_data = json.loads(message.payload)
    # Find the transaction and mark that transaction as complete.
    # Fetch the ID
    transaction_id = payload_data['reqId']
    # Mark the transaction as complete
    self._transactions.mark_complete(id=transaction_id, data=payload_data)
    return


def _error_callback(self, client, userdata, message):
    payload_data = json.loads(message.payload)
    # This callback is called when an error occurs.
    transaction_id = payload_data["reqId"]
    self._transactions.mark_complete(id=transaction_id, data=payload_data)
    return
