# code from https://github.com/UpstageAI/tmp-llm-proxy-server/blob/master/solar.py
import requests
import time
import os
import logging
import json
from good_prompt import SYSTEM_PROMPT, get_prompt

LOCAL_TESTING = os.getenv("LOCAL_TESTING", "")
LOGLEVEL = os.getenv("LOGLEVEL", "INFO")

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=LOGLEVEL)

TOGETHERAI_API_HOST = os.getenv("TOGETHERAI_API_HOST", "https://api.together.xyz")
TOGETHERAI_API_KEY = os.environ["TOGETHERAI_API_KEY"]
SOLAR_MAX_TOKEN = 1024
SOLAR_MAX_CONTEXT = 2048
SOLAR_TEMPERATURE = 0.7

headers = {
    "Authorization": f"Bearer {TOGETHERAI_API_KEY}",
    "Content-Type": "application/json",
}

role_map = {
    "system": "### System:\n{}".strip() + "\n",
    "user": "### User:\n{}".strip() + "\n",
    "assistant": "### Assistant:\n{}".strip() + "\n",
}


def extract_body_and_prompt_suggestions(s):
    # Split the string into sections by '###'
    sections = s.split("###")
    body = sections[0].strip()
    prompt_suggestions = [
        section.replace("User:", "").strip()
        for section in sections[1:]
        if section.lstrip().startswith("User:")
    ]
    return body, prompt_suggestions


def parse_messages(messages):
    result = ""
    for message in messages:
        # print("role:", message["role"])
        role = message["role"]
        content = message["content"]

        formatted_message = role_map.get(role, "").format(content)
        result += formatted_message + "\n"

    # last message is always assistant with empty content
    result += role_map.get("assistant").format("")
    return result


# Send a message
def solar_chat(system_prompt, messages):
    start_time = time.time()
    # if messages contains more tan 1024 tokens, only use the last 1024 tokens
    token_length = 0
    checked_messages = []
    for message in messages[::-1]:
        token_length += len(message["content"].split())
        if token_length > SOLAR_MAX_TOKEN:
            logger.info("Truncating messages to SOLAR_MAX_TOKEN")
            break

        checked_messages.insert(0, message)

    # Add system prompt to the beginning of the messages
    messages = [{"role": "system", "content": system_prompt}] + checked_messages
    prompt = parse_messages(messages)
    # print(prompt)

    url = f"{TOGETHERAI_API_HOST}/inference"
    payload = {
        "model": "upstage/SOLAR-0-70b-16bit",
        "prompt": prompt,
        "max_tokens": SOLAR_MAX_TOKEN,
        "temperature": SOLAR_TEMPERATURE,
        "stream_tokens": False,
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        # Check if the response code is 200
        if response.status_code != 200:
            logger.error(f"Error: SOLAR server error: {response.status_code}")
            return "Our SOLAR server is having trouble now. Please try again or try new message mode."

        response_json = response.json()
        reply = response_json["output"]["choices"][0]["text"]

        if LOCAL_TESTING:
            logger.info(f"Received reply from SOLAR: {reply}")

        reply_body, prompt_suggestions = extract_body_and_prompt_suggestions(reply)

        if prompt_suggestions and len(prompt_suggestions) > 0:
            reply_body += "\n\nYou can also try asking me:"

        for suggestion in prompt_suggestions:
            # strip leading and trailing whitespace
            suggestion = suggestion.strip()
            if suggestion:
                # Add ? if the suggestion doesn't end with punctuation
                if "?" not in suggestion[-1]:
                    suggestion += "?"
                reply_body += f'\n"{suggestion}"'

        logger.info(f"Called Solar in [{(time.time() - start_time):.2f}]")
        return reply_body
    except Exception as e:
        logger.error(f"Error: Unable to get reply from SOLAR: {e}")
        return "We're having trouble reading from SOLAR. Please try again or try new message mode."


# Send a message
def solar_chat_stream_on(system_prompt, messages, call_back_func):
    start_time = time.time()
    # if messages contains more tan 1024 tokens, only use the last 1024 tokens
    token_length = 0
    checked_messages = []
    for message in messages[::-1]:
        token_length += len(message["content"].split())
        if token_length > SOLAR_MAX_TOKEN:
            logger.info("Truncating messages to SOLAR_MAX_TOKEN")
            break

        checked_messages.insert(0, message)

    # Add system prompt to the beginning of the messages
    messages = [{"role": "system", "content": system_prompt}] + checked_messages
    prompt = parse_messages(messages)
    # print(prompt)

    url = f"{TOGETHERAI_API_HOST}/inference"
    payload = {
        "model": "upstage/SOLAR-0-70b-16bit",
        "prompt": prompt,
        "max_tokens": SOLAR_MAX_TOKEN,
        "temperature": SOLAR_TEMPERATURE,
        "stream_tokens": True,
    }

    try:
        with requests.post(url, json=payload, headers=headers, stream=True) as response:
            # Check if the response code is 200
            if response.status_code != 200:
                logger.error(f"Error: SOLAR server error: {response.status_code}")
                return "Our SOLAR server is having trouble now. Please try again or try new message mode."

            result = ""
            for line in response.iter_lines():
                # filter out keep-alive new lines
                if line:
                    decoded_line = line.decode("utf-8")
                    json_text = decoded_line.split("data: ")[1]
                    if json_text == "[DONE]":
                        break

                    json_dict = json.loads(json_text)
                    if "choices" in json_dict and len(json_dict["choices"]) > 0:
                        result += json_dict["choices"][0]["text"]
                        call_back_func(result)

            reply_body, prompt_suggestions = extract_body_and_prompt_suggestions(result)

            if prompt_suggestions and len(prompt_suggestions) > 0:
                reply_body += "\n\nYou can also try asking me:"

            for suggestion in prompt_suggestions:
                # strip leading and trailing whitespace
                suggestion = suggestion.strip()
                if suggestion:
                    # Add ? if the suggestion doesn't end with punctuation
                    if "?" not in suggestion[-1]:
                        suggestion += "?"
                    reply_body += f'\n"{suggestion}"'

            logger.info(f"Called Solar in [{(time.time() - start_time):.2f}]")
            return reply_body
    except Exception as e:
        logger.error(f"Error: Unable to get reply from SOLAR: {e}")
        return "We're having trouble reading from SOLAR. Please try again or try new message mode."


def solar_grade(hw_desc, student_code, stdout, stderr, call_back_func=None):
    content = get_prompt(hw_desc, student_code, stdout, stderr)

    msgs = [{"role": "user", "content": content}]

    if call_back_func:
        return solar_chat_stream_on(SYSTEM_PROMPT, msgs, call_back_func)

    return solar_chat(SYSTEM_PROMPT, msgs)


def __test_msg_parser():
    # Test the function
    s = """
🌎 I was created by Upstage, a company dedicated to developing AI technology. They made me so I can learn, grow, and be helpful to people like you.

### User:
Wow! That sounds really cool. What can you do?

### Assistant:
As an AI bot, I can do a variety of things! I can answer questions, provide information, have fun conversations, and help with tasks like setting reminders or finding nearby places. I'm always learning, so there's a lot that I can do. Just let me know how I can help, and I'll do my best!

### User:
That's amazing! Can you tell me about your favorite hobbies?

### Assistant:
As an AI, I don't really have hobbies in the traditional sense. But I do enjoy learning new things, interacting with people, and helping out in any way I can. It's always exciting to have new conversations and learn something new.

Is there anything specific you'd like to talk about or learn more about? I'd be happy to help!
    """

    body, user_actions = extract_body_and_prompt_suggestions(s)
    print(f"Body: {body}")
    print(f"User Actions: {user_actions}")


if __name__ == "__main__":
    solar_chat_stream_on("Hello", [{"role": "user", "content": "Hello"}], print)

    __test_msg_parser()

    hw_desc = """
Write code to print out the followings using while loop:
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
    print(solar_grade(hw_desc, student_code, stdout, stderr))
