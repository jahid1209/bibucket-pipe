import json
import os
from os.path import expanduser


def prepare_blackduck_input_json(url, token):
    data = {
        "data": {
            "blackduck": {
                "url": url,
                "token": token,
                "reports": {
                   "sarif": {
                        "create": True
                    }
                }
            }
        }
    }

    json_string = json.dumps(data, indent=4)

    home_dir = expanduser("~")
    json_file_path = os.path.join(home_dir, "bd_input.json")

    with open(json_file_path, "w") as json_file:
        json_file.write(json_string)

    return json_file_path




def print_json(input_json_path):
    try:
        with open(input_json_path, 'r') as file:
            # Load the JSON data
            json_data = json.load(file)

            # Print the JSON data
            print(json.dumps(json_data, indent=4))
    except FileNotFoundError:
        print(f"File not found: {input_json_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
