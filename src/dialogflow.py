import os
import uuid
from google.cloud import dialogflow_v2


class PaulDialog(object):
  def __init__(self, project_id, language_code):
    self._sessions = {}
    self.project_id = project_id
    self.language_code = language_code
    self.session_client = dialogflow_v2.SessionsClient()

  def create_session(self, session_id=None):
    if session_id is None:
      session_id = uuid.uuid1()
    self._sessions[session_id] = self.session_client.session_path(self.project_id, session_id)
    return session_id

  def handle_input(self, session_id, input_text):
    text_input = dialogflow_v2.TextInput(text=input_text, language_code=self.language_code)
    query_input = dialogflow_v2.QueryInput(text=text_input)
    response_dialogflow = self.session_client.detect_intent(session=self._sessions[session_id], query_input=query_input)
    print(response_dialogflow)
    return response_dialogflow


if __name__ == "__main__":
  paul_dialog = PaulDialog(
      project_id = 'paul-fmma',
      language_code = "en"
    )
  session_id = paul_dialog.create_session()
  asdf = paul_dialog.handle_input(session_id, "hello!")

  qwer = asdf.query_result.fulfillment_text


  print(type(qwer))