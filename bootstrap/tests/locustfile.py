import time
from locust import HttpUser, task, between
import random

import yaml

with open("questions.yaml") as f:
    data = yaml.safe_load(f)
    QUESTIONS = data["questions"]

class AdaUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def test_ada_workflow(self):
        """
        POST to /v1/ada, extract task_id, then poll GET /v1/ada/{task_id} every 2s until done. Measure total time.
        """
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        question = random.choice(QUESTIONS)
        payload = {
            "query": question,
            "tenant_id": "920a2f73-c7db-405f-98ea-f768c6da864f",
            "region": "eu",
            "session_id": "1243j0123jr0",
            "preferred_currency": "EUR",
            "category": "Bearings",
            "language": "English"
        }
        workflow_start = time.perf_counter()
        post_start = time.perf_counter()
        try:
            response = self.client.post(
                "/v1/ada",
                json=payload,
                headers=headers,
                name="POST /v1/ada"
            )
            post_duration = (time.perf_counter() - post_start) * 1000
            if response.status_code == 200:
                self.environment.events.request.fire(
                    request_type="POST",
                    name="POST /v1/ada",
                    response_time=post_duration,
                    response_length=len(response.content),
                    context={},
                    exception=None
                )
                try:
                    task_id = response.json().get("task_id")
                    if task_id:
                        self.poll_until_complete(task_id, workflow_start)
                except Exception:
                    pass
            else:
                self.environment.events.request.fire(
                    request_type="POST",
                    name="POST /v1/ada",
                    response_time=post_duration,
                    response_length=len(response.content),
                    context={},
                    exception=Exception(f"Unexpected status: {response.status_code}")
                )
        except Exception as e:
            post_duration = (time.perf_counter() - post_start) * 1000
            self.environment.events.request.fire(
                request_type="POST",
                name="POST /v1/ada",
                response_time=post_duration,
                response_length=0,
                context={},
                exception=e
            )

    def poll_until_complete(self, task_id, workflow_start):
        """
        Poll GET /v1/ada/{task_id} every 2s until status is not pending/started. Report total workflow time.
        """
        headers = {"accept": "application/json"}
        url = f"/v1/ada/{task_id}"
        max_polls = 30  # avoid infinite loop, e.g. 1 minute max
        for _ in range(max_polls):
            poll_start = time.perf_counter()
            try:
                response = self.client.get(
                    url,
                    headers=headers,
                    name="GET /v1/ada/{task_id}"
                )
                poll_duration = (time.perf_counter() - poll_start) * 1000
                status = None
                if response.status_code == 200:
                    try:
                        status = response.json().get("status")
                    except Exception:
                        pass
                    self.environment.events.request.fire(
                        request_type="GET",
                        name="GET /v1/ada/{task_id}",
                        response_time=poll_duration,
                        response_length=len(response.content),
                        context={},
                        exception=None
                    )
                    if status and status.lower() not in ["pending", "started"]:
                        # Terminal state reached, report total workflow time
                        total_duration = (time.perf_counter() - workflow_start) * 1000
                        self.environment.events.request.fire(
                            request_type="WORKFLOW",
                            name="POST+GET /v1/ada",
                            response_time=total_duration,
                            response_length=len(response.content),
                            context={"final_status": status},
                            exception=None
                        )
                        break
                else:
                    self.environment.events.request.fire(
                        request_type="GET",
                        name="GET /v1/ada/{task_id}",
                        response_time=poll_duration,
                        response_length=len(response.content),
                        context={},
                        exception=Exception(f"Unexpected status: {response.status_code}")
                    )
            except Exception as e:
                poll_duration = (time.perf_counter() - poll_start) * 1000
                self.environment.events.request.fire(
                    request_type="GET",
                    name="GET /v1/ada/{task_id}",
                    response_time=poll_duration,
                    response_length=0,
                    context={},
                    exception=e
                )
            time.sleep(2)

# poetry run locust -f chat-service/tests/locustfile.py --host=http://localhost:8086 --headless -u 10 -r 2 --run-time 1m