#!/usr/bin/env python3

import subprocess
import requests
import time
import sys

def test_backend():
    """Test if the backend is working correctly by checking if it responds to requests"""
    
    # Start the backend in the background
    try:
        # Start the backend server
        process = subprocess.Popen([
            sys.executable, "-m", "flask", "--app", "app", "run", 
            "--debug", "--host=0.0.0.0", "--port=5000"
        ], cwd="/var/home/peter/Repos/Personal/hf-cli-web-ui/backend")
        
        # Give it a moment to start
        time.sleep(3)
        
        # Check if it's responding
        try:
            response = requests.get("http://localhost:5000/api/cache/stats", timeout=5)
            if response.status_code == 200:
                print("✅ Backend is running and accessible")
                data = response.json()
                print(f"Cache size: {data.get('size_formatted', 'Unknown')}")
                process.terminate()
                return True
            else:
                print(f"❌ Backend responded with status code: {response.status_code}")
                process.terminate()
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Backend is not responding - connection refused")
            process.terminate()
            return False
        except Exception as e:
            print(f"❌ Error connecting to backend: {e}")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False

if __name__ == "__main__":
    success = test_backend()
    if success:
        print("🎉 Backend is working correctly!")
    else:
        print("💥 Backend has issues.")