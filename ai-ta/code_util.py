import requests

PISTON_URL = "https://emkc.org/api/v2/piston/execute"
PASS_CODE = "1234"


# Function to execute code using Piston API
def execute_code(code):
    # Prepare the payload for the Piston API
    payload = {
        "language": "py3",
        "version": "3.10.0",
        "files": [
            {
                "name": "my_cool_code.py",  # You can change the filename if needed
                "content": code,  # Pass the code as content
            }
        ],
        "compile_timeout": 10000,
        "run_timeout": 3000,
        "compile_memory_limit": -1,
        "run_memory_limit": -1,
    }

    # Make a POST request to the Piston API
    piston_api_url = (
        "https://emkc.org/api/v2/piston/execute"  # Replace with the actual API URL
    )
    response = requests.post(piston_api_url, json=payload)

    if response.status_code == 200:
        data = response.json()
        stdout_output = data.get("run", {}).get("stdout", "").strip()
        stderr_output = data.get("run", {}).get("stderr", "").strip()

        if stderr_output:
            return None, stderr_output  # If there's stderr output, return it as error
        else:
            return (
                stdout_output,
                None,
            )  # If no stderr output, return stdout output and None as error
    else:
        return None, None
