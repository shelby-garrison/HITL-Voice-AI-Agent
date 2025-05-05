import requests
import time

BASE_URL = "http://localhost:5000"

class HumanFallbackSystem:
    def create_request(self, question):
        try:
            res = requests.post(f"{BASE_URL}/api/requests", json={"question": question})
            if res.status_code == 200:
                request_id = res.json().get("request_id")
                print(f"Successfully created request ID: {request_id}")
                return request_id
            else:
                print(f"❌ Failed to create request: {res.status_code} - {res.text}")
                return None
        except Exception as e:
            print(f"❌ Exception when creating request: {e}")
            return None
    
    def wait_for_response(self, request_id):
        if not request_id:
            return {"answer": "Could not create a request for human assistance."}
            
        print(f"⌛ Python waiting for human response to request {request_id}")
        
        
        max_wait_time = 120  # seconds
        polling_interval = 3  # seconds
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            try:
                
                res = requests.get(f"{BASE_URL}/api/requests/{request_id}", timeout=5)
                
                if res.status_code == 200:
                    data = res.json()
                    if data.get("resolved") and data.get("answer"):
                        print(f"✅ Received human answer: {data['answer']}")
                        return {"answer": data['answer']}
                
                # Waiting before trying again
                time.sleep(polling_interval)
                
            except Exception as e:
                print(f"❌ Error checking for human response: {e}")
                time.sleep(polling_interval)
        
        print("Timeout: No human response received within time limit")
        return {"answer": "I haven't received a response from the salon staff yet. Could I help you with something else in the meantime?"}