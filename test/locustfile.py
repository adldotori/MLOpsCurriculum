from locust import HttpUser, task
import json
import random


class PerformanceTest(HttpUser):
    @task
    def get_all_users(self):
        self.client.get("/users")

    @task
    def create_user(self):
        self.client.post(
            "/users",
            json={"name": str(random.randint(0, 100000000)), "age": 21},
        )
