import os
import subprocess
import pathlib

def run_aider_sequentially(target_dir: str, prompt: str):
    directory = pathlib.Path(target_dir)
    
    target_files = [f for f in directory.iterdir() if f.is_file() and f.name.startswith("check_")]
    
    if not target_files:
        print(f"No files starting with 'check_' found in {target_dir}")
        return

    custom_env = os.environ.copy()
    custom_env["OLLAMA_API_BASE"] = "http://127.0.0.1:11434"

    for file_path in target_files:
        print(f"\n--- Processing: {file_path.name} ---")
        
        command = [
            "aider",
            str(file_path),
            "--message", prompt,
            "--model", "ollama/qwen3-coder-next:latest",
            "--encoding", "utf8",
            "--edit-format", "whole",
            "--no-auto-commits",
            "--yes" 
        ]
        
        try:
            subprocess.run(command, env=custom_env, check=True)
            print(f"Successfully processed {file_path.name}")
        except subprocess.CalledProcessError as e:
            print(f"Aider failed on {file_path.name} with error: {e}")

if __name__ == "__main__":
    DIRECTORY = "."  
    PROMPT = "In the attached python file replace time.sleep with await asyncio.sleep and make the needed functions async too. If no changes are needed it is OK."
    
    run_aider_sequentially(DIRECTORY, PROMPT)
