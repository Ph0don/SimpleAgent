import sys
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv('keys.env')
api_key =  os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

from functions.call_function import call_function

from enum import IntFlag, auto
class CLIFlag(IntFlag):
    VERBOSE = 1

def get_flags(args):
    flags = 0
    string_flags = {"--verbose":CLIFlag.VERBOSE}
    for arg in args:
        if arg in string_flags:
            flags = flags | string_flags[arg]
    return flags
        

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <prompt>")
        sys.exit(1)
    flags = get_flags(sys.argv)

    available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,
                schema_run_python_file,
                schema_write_file
            ])

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    user_prompt = sys.argv[1]
    messages = [
                types.Content(role="user", parts=[types.Part(text=user_prompt)]),
            ]
    for x in range(20):
        response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt))
        for candidate in response.candidates:
            messages.append(candidate.content)
        print(response.text)
        responses = []
        if response.function_calls:
            for call in response.function_calls:
                res = call_function(call, (flags | CLIFlag.VERBOSE) == flags)
                if not res.parts[0].function_response.response:
                    raise Exception("Fatal Error: function returned without response")
                responses.append(res.parts[0])
                if (flags | CLIFlag.VERBOSE) == flags:
                    print(f"-> {res.parts[0].function_response.response}")
        else:
            if response.text is not None:
                break
        if (flags | CLIFlag.VERBOSE) == flags:
            print(f"User prompt: {user_prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
    
        messages.append(types.Content(role="user", parts=responses))

if __name__ == "__main__":
    main()

