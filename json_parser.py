import json
import re

def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None
    return None

def parse_json(self, response: str):
    try:
        start = response.index("{")
        end = response.rindex("}") + 1
        json_str = response[start:end]
        return json.loads(json_str)
    except (ValueError, json.JSONDecodeError) as e:
        print("Error parsing JSON:", e)
        return None