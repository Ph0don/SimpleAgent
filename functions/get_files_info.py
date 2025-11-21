import os
import google.genai
from google.genai import types
def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(abs_working_dir, directory))
    if not abs_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'
    try:
        contents = os.listdir(abs_path)
        dir_contents_string = ""
        for item in contents:
            path = os.path.join(abs_path, item)
            dir_contents_string += f"- {item}: file_size={os.path.getsize(path)}, is_dir={not os.path.isfile(path)}\n"
    except Exception as e:
        return e
    return dir_contents_string

# Gemini Function Schema
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
