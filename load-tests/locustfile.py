from locust import HttpUser, task, between
import base64


# you can find your API key at https://k8s.uzmankaza.com/#settings/account-and-privacy
class ZulipUser(HttpUser):
    wait_time = between(5, 15)
    email = "lamikaan@gmail.com"
    api_key = "EtWkfyX8BH3nbCubqm8KPPTO9tDZTpi3"  # replace with your user's API key

    @task(1)
    def send_message(self):
        # https://zulip.com/api/send-message for more info
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(f"{self.email}:{self.api_key}".encode()).decode()
        }

        data = {
            'type': 'private',
            'to': 'user8@k8s.uzmankaza.com', # change this to the email of the user you want to send a message to, email format is user<id>@<domain>
            'content': 'With mirth and laughter let old wrinkles come.'
        }
        self.client.post("/api/v1/messages", headers=headers, data=data)

    @task(1)
    def upload_file_and_send_message(self):
        # https://zulip.com/api/upload-file for more info
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(f"{self.email}:{self.api_key}".encode()).decode()
        }

        files = {'file': open('boun.jpg', 'rb')}
        result = self.client.post("/api/v1/user_uploads", headers=headers, files=files)

        data = {
            'type': 'private',
            'to': 'user8@k8s.uzmankaza.com',
            'content': "Check out [this picture]({}) of my castle!".format(result.json()['uri'])
        }

        self.client.post("/api/v1/messages", headers=headers, data=data)

    @task(5)
    def view_index_page(self):
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(f"{self.email}:{self.api_key}".encode()).decode()
    }
        self.client.get("/", headers=headers)

    @task(4)
    def view_streams_page(self):
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(f"{self.email}:{self.api_key}".encode()).decode()
        }
        self.client.get("/api/v1/streams", headers=headers)

    @task(3)
    def send_message_to_stream_1(self):
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(f"{self.email}:{self.api_key}".encode()).decode()
        }
        data = {"type": "stream",
                "to": "general",
                "content": "test message sent using locust",
                "topic": "test_1"}
        self.client.post("/api/v1/messages", data=data, headers=headers)

    @task(2)
    def send_message_to_stream_2(self):
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(f"{self.email}:{self.api_key}".encode()).decode()
        }
        data = {"type": "stream",
                "to": "general",
                "content": "@**Ali Kenan** sa using locust",
                "topic": "test_2"}
        self.client.post("/api/v1/messages", data=data, headers=headers)

    @task(1)
    def send_private_message_to_user(self):
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(f"{self.email}:{self.api_key}".encode()).decode()
        }
        data = {"type": "private",
                "to": "user8@k8s.uzmankaza.com",
                "content": "private test message sent using locust"}
        self.client.post("/api/v1/messages", data=data, headers=headers)