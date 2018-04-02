from locust import HttpLocust, TaskSet, task

class MyTaskSet(TaskSet):
    @task(100)
    def index(self):
        self.client.get("/")

    @task(10)
    def about(self):
        self.client.get("/about/")

class MyLocust(HttpLocust):
    task_set = MyTaskSet
    min_wait = 5000
    max_wait = 15000