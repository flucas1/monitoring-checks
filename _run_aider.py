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
    PROMPT = "Transform the attached python file to be async. Avoid to_thread, get_event_loop and get_running_loop. For python imports do not use 'from'. Remove legacy subprocess, urllib and concurrent.futures. If no changes are needed it is OK. Do no modify the file name."
    
    await run_aider(DIRECTORY, MODEL, PROMPT)

if __name__ == "__main__":
    asyncio.run(main())