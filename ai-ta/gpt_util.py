import openai
import os
from good_prompt import SYSTEM_PROMPT, get_prompt

# Set openai.api_key to the OPENAI environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]
OPENAI_MAX_TOKEN = 2048


def gpt_grade(hw_desc, student_code, stdout, stderr, call_back=None):
    content = get_prompt(hw_desc, student_code, stdout, stderr)
    content = content[:OPENAI_MAX_TOKEN]
    msgs = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": content},
    ]

    stream = True if call_back else False
    result = ""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=msgs, stream=stream
    )
    if stream and call_back:
        for resp in response:
            if "content" in resp.choices[0].delta and resp.choices[0].delta.get(
                "content"
            ):
                result += resp.choices[0].delta.get("content")
                call_back(result)

        return result
    else:
        status_code = response["choices"][0]["finish_reason"]
        assert status_code == "stop", f"The status code was {status_code}."
        return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    hw_desc = """
Write code to print out the followings:
*
**
***
****
***
**
*
"""

    student_code = """  
for i in range(1, 5):
    print("*" * i)
for i in range(5, 0, -1):
    print("*" * i)
"""
    stdout = """            
*   
**

***
****

***
**

*
"""
    stderr = ""
    print(gpt_grade(hw_desc, student_code, stdout, stderr))
