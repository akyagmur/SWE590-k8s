from locust import HttpUser, task, between
import base64


# you can find your API key at https://k8s.uzmankaza.com/#settings/account-and-privacy
class ZulipUser(HttpUser):
    wait_time = between(5, 15)

    @task
    def send_message(self):
        # https://zulip.com/api/send-message for more info
        headers = {
            'Authorization': 'Basic ' + base64.b64encode('<your-login-email>:<your-api-key>'.encode()).decode()
        }

        data = {
            'type': 'private',
            'to': 'user9@k8s.uzmankaza.com', # change this to the email of the user you want to send a message to, email format is user<id>@<domain>
            'content': 'With mirth and laughter let old wrinkles come.'
        }
        self.client.post("/api/v1/messages", headers=headers, data=data)

    @task
    def upload_file_and_send_message(self):
        # https://zulip.com/api/upload-file for more info
        headers = {
            'Authorization': 'Basic ' + base64.b64encode('<your-login-email>:<your-api-key>'.encode()).decode()
        }

        files = {'file': open('boun.jpg', 'rb')}
        result = self.client.post("/api/v1/user_uploads", headers=headers, files=files)

        data = {
            'type': 'private',
            'to': 'user9@k8s.uzmankaza.com',
            'content': "Check out [this picture]({}) of my castle!".format(result.json()['uri'])
        }

        self.client.post("/api/v1/messages", headers=headers, data=data)