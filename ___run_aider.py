#!/usr/bin/env python3
# -------------------------------------------------------------------------------

import sys
import os
import asyncio
import pathlib
import shutil
import aiofiles

# -------------------------------------------------------------------------------


async def process_file(file_path: pathlib.Path, model: str, prompt: str, custom_env: dict):
    print("\n--- Processing: " + file_path.name + " ---")

    cmdline = [
        shutil.which("aider"),
        str(file_path),
        "--message", prompt,
        "--model", model,
        "--encoding", "utf8",
        "--edit-format", "whole",
        "--no-auto-commits",
        "--no-stream",
        "--yes"
    ]

    success = False
    try:
        print("EXECUTING -> " + " ".join(cmdline))
        process = await asyncio.create_subprocess_exec(
            *cmdline,
            env=custom_env
        )

        await process.communicate()

        if process.returncode == 0:
            print("Successfully processed " + file_path.name)
            success = True
        else:
            print("Aider failed on " + file_path.name + " with exit code: " + str(process.returncode))

    except Exception as e:
        print("Aider failed on " + file_path.name + " with error: " + str(e))

    return success


async def run_aider(target_dir: str, model: str, prompt: str):
    error_count = 0

    directory = pathlib.Path(target_dir)

    starting_pattern = "check_"
    ending_pattern = ""
    exclude_files = ["___run_aider.py", "___run_fix_syntax.py"]
    shebang = "python"

    target_files = []
    for f in directory.iterdir():
        if f.is_file():
            if f.name not in exclude_files:
                if f.name.startswith(starting_pattern) and f.name.endswith(ending_pattern):
                    try:
                        async with aiofiles.open(f, "r", encoding="utf-8") as handle:
                            first_line = await handle.readline()
                            if shebang in first_line:
                                target_files.append(f)
                    except Exception as e:
                        print("Issue reading " + f.name + " with error: " + str(e))

    if not target_files:
        print("No valid files found in " + target_dir)
    else:
        for target_file in target_files:
            print("Matching " + target_file.name)

        custom_env = os.environ.copy()
        custom_env["OLLAMA_API_BASE"] = "http://127.0.0.1:11434"

        # Process files sequentially in the async event loop
        failedfiles = []
        for file_path in target_files:
            success = await process_file(file_path, model, prompt, custom_env)
            if success == False:
                failedfiles.append(file_path)
                error_count += 1
        print("failed files: " + str(failedfiles))

    return error_count


async def update_aider():
    error_count = 0

    cmdline = [sys.executable, "-m", "pip", "install", "--upgrade", "aider-chat"]

    process = await asyncio.create_subprocess_exec(
        *cmdline
    )
    await process.communicate()

    if process.returncode == 0:
        print("Aider updated successfully!")
    else:
        print("Update failed (exit code " + str(process.returncode) + "):")
        error_count += 1

    return error_count


# -------------------------------------------------------------------------------


def get_directory():
    return "."


def get_model():
    return "ollama/mgraffam/qwen3.8-coder390:27b"
    # return "ollama/qwen3-coder-next:latest"
    # return "ollama/qwen3.8:latest"


def get_prompt_lines():
    prompt_lines = []

    prompt_lines.append("Keep the comments.")
    prompt_lines.append("Review the attached python for issues and transform to async.")
    prompt_lines.append("Avoid asyncio.to_thread, asyncio.get_event_loop and asyncio.get_running_loop.")
    prompt_lines.append("File reading and writing should be always async.")
    prompt_lines.append("For python imports do not use 'from'.")
    prompt_lines.append("Remove legacy subprocess, urllib, requests and concurrent.futures and replace them with async alternatives.")
    prompt_lines.append("Time evolution should be done usign 'time.monotonic()'.")
    prompt_lines.append("Prefer \" rather than ' for string delimitator.")
    prompt_lines.append("Avoid f\" and .format syntax, use concatenation instead.")
    prompt_lines.append("The functions 'asyncio.create_subprocess_exec' and 'asyncio.create_subprocess_shell' should be assigned to a variable named named 'process', and the executable with arguments should be defined in a variable called cmdline.")
    prompt_lines.append("All calls to 'asyncio.create_subprocess_exec' or 'asyncio.create_subprocess_shell' should evaluate the process returncode.")
    prompt_lines.append("Executables should be full paths.")
    prompt_lines.append("Console printing should be done via the funcion 'infomsg', except in function 'exitnagios'.")
    prompt_lines.append("'socket.getaddrinfo', 'socket.gethostname' 'socket.gethostbyname' should be replaced with 'dns.asyncresolver'.")
    # prefer shutil calls over own code
    # all main functions should exit via sys.exit, no other sys.exit calls in the code are allowed

    prompt_lines.append("The main function is always defined as 'async def main(forcedargs=None):'.")
    prompt_lines.append("The arguments should be parsed with argparse, in a function defined as 'def parse_args(forcedargs=None):' that is invoked from main, and returning the args.")
    prompt_lines.append("The last function in the code is 'main' and the previous one is 'parse_args'.")
    prompt_lines.append("After the call to 'parse_args', this should be executed 'setcandebug(args.debug)'.")
    prompt_lines.append("There is always a command line argument '-d' '--debug'.")
    prompt_lines.append("The option '-d' is the last one of the command line arguments.")  # , but if there is a remainder of arguments, the remainder is the last one
    prompt_lines.append("All command line arguments should have short and long form.")
    prompt_lines.append("Prefer using the 'exitnagios' function rather than sys.exit")

    return prompt_lines

# -------------------------------------------------------------------------------


async def main():
    error_count = 0

    # error_count += await update_aider()

    error_count += await run_aider(get_directory(), get_model(), " ".join(get_prompt_lines()))

    if sys.__stdin__.isatty():
        input("Press Enter to continue...")
    if error_count > 0:
        sys.exit(1)

# -------------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())

# -------------------------------------------------------------------------------
