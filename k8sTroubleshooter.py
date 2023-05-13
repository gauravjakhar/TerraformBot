from datetime import datetime, timedelta
import time
from functools import partial

import openai
import kubernetes
from kubernetes import client, config, watch

# Initialize OpenAI API client
openai.api_key = "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"

# Initialize Kubernetes API client
config.load_kube_config(config_file="kube-config.yaml")
v1 = client.CoreV1Api()
timeout_seconds = 10

# Define function to generate response from OpenAI API
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Define function to check pod status and fix issues using OpenAI
def check_and_fix_pod(pod):
    # check pod status
    status = pod.status.phase
    print(f"Pod name: {pod.metadata.name}, status: {status}")
    if status != "Running":
        # generate response from OpenAI API
        response = generate_response(
            "Troubleshoot and fix Kubernetes pod\nPod name: " + pod.metadata.name + "\nProblem: " + status)
        print("Possible fix suggestion: ", response)
        # fix pod based on response
        if "restart" in response:
            v1.delete_namespaced_pod(name=pod.metadata.name, namespace="default")
            print("Pod deleted. Waiting for pod to restart...")
            while True:
                try:
                    v1.read_namespaced_pod(name=pod.metadata.name, namespace="default")
                except kubernetes.client.rest.ApiException:
                    print("Pod restarted successfully.")
                    break
        else:
            print("Cannot fix pod. Manual intervention required.")


# Define function to check all pods and fix issues
def check_and_fix_all_pods():
    # retrieve all pods in default namespace
    pods = v1.list_namespaced_pod(namespace="default")
    # check each pod and fix issues
    for pod in pods.items:
        check_and_fix_pod(pod)

def check_cluster_events():
    now = datetime.utcnow()
    one_minute_ago = now - timedelta(minutes=10)
    one_minute_ago_ts = int(time.mktime(one_minute_ago.timetuple()))  # convert to Unix timestamp
    label_selector = f"lastTimestamp<{one_minute_ago_ts}"  # "last_timestamp" #
    events = v1.list_namespaced_event(namespace='default')#, label_selector=label_selector)

    # Check each event and send a notification for any event with type not equal to "Normal"
    for event in events.items:
        if "failed" in event.reason.lower() or "backoff" in event.reason.lower():
            message = f"Event type: {event.type}\nMessage: {event.message}\nReason: {event.reason}"
            print(message)

def check_cluster_events_stream():
    count = 10
    w = watch.Watch()
    for event in w.stream(partial(v1.list_namespaced_event, namespace="default"), timeout_seconds=10):
        if event.type != "Normal":
            print(f"Event - Message: {event['object']['message']} at {event['object']['metadata']['creationTimestamp']}")
            count -= 1
            if not count:
                w.stop()
    print("Finished namespace stream.")

if __name__ == "__main__":
    while True:
        check_cluster_events()
        time.sleep(10)
