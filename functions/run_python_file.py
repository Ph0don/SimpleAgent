import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        try:
            completed_proc = subprocess.run(["python",abs_file_path] + args, capture_output=True, timeout=30)
        except Exception as e:
            return f"Error: executing Python file: {e}"
        proc_metrics = f"STDOUT: {completed_proc.stdout}\nSTDERR: {completed_proc.stderr}\n"
        ret_code = completed_proc.check_returncode()
        if ret_code is not None:
            proc_metrics += f"Process exited with code {ret_code}\n"
        if len(completed_proc.stdout) == 0:
            proc_metrics += "No output produced\n"
        return proc_metrics
    except Exception as e:
        return "Error: " + str(e)

# Gemini Function Schema
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a given python file and returns its execution metrics (stdout, stderr, return code), constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be executed, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="A list of string arguments to be passed into the function. Empty if not provided",
                items=types.Schema(type=types.Type.STRING, description="A single string argument")
            ),

        },
        required=["file_path"]
    ),
)
