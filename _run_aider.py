import os
import asyncio
import pathlib


async def process_file(file_path: pathlib.Path, model: str, prompt: str, custom_env: dict):
    print(f"\n--- Processing: {file_path.name} ---")

    command = [
        "aider",
        str(file_path),
        "--message", prompt,
        "--model", model,
        "--encoding", "utf8",
        "--edit-format", "whole",
        "--no-auto-commits",
        "--yes"
    ]

    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            env=custom_env
        )

        await process.communicate()

        if process.returncode == 0:
            print(f"Successfully processed {file_path.name}")
        else:
            print(f"Aider failed on {file_path.name} with exit code: {process.returncode}")

    except Exception as e:
        print(f"Aider failed on {file_path.name} with error: {e}")


async def run_aider(target_dir: str, model: str, prompt: str):
    directory = pathlib.Path(target_dir)

    target_files = [f for f in directory.iterdir() if f.is_file() and f.name.startswith("check_")]

    if not target_files:
        print(f"No files starting with 'check_' found in {target_dir}")
        return

    custom_env = os.environ.copy()
    custom_env["OLLAMA_API_BASE"] = "http://127.0.0.1:11434"

    # Process files sequentially in the async event loop
    for file_path in target_files:
        await process_file(file_path, model, prompt, custom_env)


async def main():
    DIRECTORY = "."
    MODEL = "ollama/qwen3-coder-next:latest"
    PROMPT = []
    PROMPT.append("Keep the comments.")
    PROMPT.append("Review the attached python for issues and transform to async.")
    PROMPT.append("The main function is always defined as 'async def main(forcedargs=None):'.")
    PROMPT.append("Avoid to_thread, get_event_loop and get_running_loop.")
    PROMPT.append("For python imports do not use 'from'.")
    PROMPT.append("Remove legacy subprocess, urllib and concurrent.futures.")
    PROMPT.append("Prefer \" rather than ' for string delimitator.")
    PROMPT.append("Avoid f\" and .format syntax, use concatenation instead.")
    PROMPT.append("The arguments should be parsed with argparse, in a function defined as 'def parse_args(forcedargs=None):' that is invoked from main, and returning the args.")
    PROMPT.append("The last function in the code is 'main' and the previous one is 'parse_args'.")
    PROMPT.append("After the call to 'parse_args', this should be executed 'setcandebug(args.debug)'.")
    PROMPT.append("There is always a command line argument '-d' '--debug'.")

    await run_aider(DIRECTORY, MODEL, " ".join(PROMPT))

if __name__ == "__main__":
    asyncio.run(main())
