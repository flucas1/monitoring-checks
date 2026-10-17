#!/usr/bin/env python3
# -------------------------------------------------------------------------------

import os
import asyncio
import pathlib

# -------------------------------------------------------------------------------

async def process_file(file_path: pathlib.Path, model: str, prompt: str, custom_env: dict):
    print(f"\n--- Processing: {file_path.name} ---")

    cmdline = [
        "aider",
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
            print(f"Successfully processed {file_path.name}")
            success = True
        else:
            print(f"Aider failed on {file_path.name} with exit code: {process.returncode}")

    except Exception as e:
        print(f"Aider failed on {file_path.name} with error: {e}")
    
    return success


async def run_aider(target_dir: str, model: str, prompt: str):
    directory = pathlib.Path(target_dir)

    pattern = "check_"

    target_files = [f for f in directory.iterdir() if f.is_file() and f.name.startswith(pattern)]

    if not target_files:
        print(f"No files starting with '" + pattern + "' found in {target_dir}")
        return

    custom_env = os.environ.copy()
    custom_env["OLLAMA_API_BASE"] = "http://127.0.0.1:11434"

    # Process files sequentially in the async event loop
    failedfiles = []
    for file_path in target_files:
        success = await process_file(file_path, model, prompt, custom_env)
        if success == False:
            failedfiles.append(file_path)
    print("failed files: " + str(failedfiles))

# -------------------------------------------------------------------------------

async def main():
    DIRECTORY = "."
    #MODEL = "ollama/qwen3-coder-next:latest"
    #MODEL = "ollama/qwen3.8:latest"
    MODEL = "ollama/mgraffam/qwen3.8-coder390:27b"
    PROMPT = []
    PROMPT.append("Keep the comments.")
    PROMPT.append("Review the attached python for issues and transform to async.")
    PROMPT.append("The main function is always defined as 'async def main(forcedargs=None):'.")
    PROMPT.append("Avoid asyncio.to_thread, asyncio.get_event_loop and asyncio.get_running_loop.")
    PROMPT.append("File reading and writing should be always async.")
    PROMPT.append("For python imports do not use 'from'.")
    PROMPT.append("Remove legacy subprocess, urllib, requests and concurrent.futures and replace them with async alternatives.")
    PROMPT.append("Prefer \" rather than ' for string delimitator.")
    PROMPT.append("Avoid f\" and .format syntax, use concatenation instead.")
    PROMPT.append("The arguments should be parsed with argparse, in a function defined as 'def parse_args(forcedargs=None):' that is invoked from main, and returning the args.")
    PROMPT.append("The last function in the code is 'main' and the previous one is 'parse_args'.")
    PROMPT.append("After the call to 'parse_args', this should be executed 'setcandebug(args.debug)'.")
    PROMPT.append("There is always a command line argument '-d' '--debug'.")
    PROMPT.append("The option '-d' is the last one of the command line arguments.")
    PROMPT.append("All command line arguments should have short and long form.")
    PROMPT.append("Prefer using the 'exitnagios' function rather than sys.exit")
    PROMPT.append("The function 'asyncio.create_subprocess_exec' should assigned to a variable named named 'process'.")

    await run_aider(DIRECTORY, MODEL, " ".join(PROMPT))

# -------------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())

# -------------------------------------------------------------------------------