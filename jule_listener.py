"""
Provenance header: keep this block in every generated artifact.
"""
import json
import time
import requests

class JuleListener:
    """
    Jule Containers Listener.
    קולט פקודות מה-Interaction Bridge דרך ה-API ומבצע אותן.
    """
    def __init__(self, api_url):
        self.api_url = api_url
        self.running = True

    def process_command(self, command):
        print(f"--- Jule Listener: Processing Command ---")
        print(f"Instruction: {command.get('instruction')}")
        print(f"Target SDK: {command.get('target_sdk')}")
        print(f"Priority: {command.get('priority')}")

        # Simulate execution
        time.sleep(1)

        # Specific logic for simulated Google Drive mapping
        if "Map Google Drive" in command.get('instruction'):
            print("Mapping folders to 64GB Partition...")

        report = {
            "action_id": f"ACT_{int(time.time())}",
            "status": "SUCCESS",
            "instruction": command.get('instruction')
        }

        try:
            resp = requests.post(f"{self.api_url}/bridge/report", json=report)
            if resp.status_code == 200:
                bridge_response = resp.json().get("bridge_response")
                print(f"Bridge Response: {bridge_response}")
            else:
                print(f"Error reporting to bridge: {resp.status_code}")
        except Exception as e:
            print(f"Exception during report: {e}")

    def run(self, once=False):
        print(f"Jule Listener is active and listening to {self.api_url}...")
        while self.running:
            try:
                resp = requests.post(f"{self.api_url}/bridge/pop_command")
                if resp.status_code == 200:
                    command = resp.json()
                    self.process_command(command)
                elif resp.status_code == 204:
                    # No commands
                    pass
                else:
                    print(f"Error fetching command: {resp.status_code}")
            except Exception as e:
                print(f"Exception during poll: {e}")

            if once:
                break
            time.sleep(2)

if __name__ == "__main__":
    # Default local Master Bundle URL
    API_URL = "http://127.0.0.1:8080"
    listener = JuleListener(API_URL)
    # Start the listener. In this demo, it will poll once and then exit.
    listener.run(once=True)
