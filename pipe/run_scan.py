import os
import subprocess


def invoke_synopsys_bridge(extracted_directory, input_json):
    bridge_executable_path = os.path.join(extracted_directory, "synopsys-bridge")

    command = [bridge_executable_path, "--stage", "blackduck", "--input", input_json]

    return_code = subprocess.call(command)

    return return_code