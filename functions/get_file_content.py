import os
from functions.config import *
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
   
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_FILE_READ_CHARS)
            if len(file_content_string) == MAX_FILE_READ_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at {MAX_FILE_READ_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return "Error: " + str(e)

# Gemini Function Schema
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads contents of the given file path relative to the working directory. Constrained to only read MAX_FILE_READ_CHARS bytes from a file in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read from, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
