import asyncio
import sys

AUTOPEP8_PATH = "C:\\Python311\\Scripts\\autopep8.exe"
PYTHON_PATH = "C:\\Python311\\python.exe"


async def run_autopep8():
    proc = await asyncio.create_subprocess_exec(
        AUTOPEP8_PATH,
        "--in-place",
        "--recursive",
        "--ignore=E501",
        ".",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        sys.stdout.buffer.write(stdout)
    if stderr:
        sys.stderr.buffer.write(stderr)
    return proc.returncode


async def run_flake8():
    proc = await asyncio.create_subprocess_exec(
        PYTHON_PATH,
        "-m",
        "flake8",
        "--select=E9,F821,F823,F831,F406,F407,F701,F702,F704,F706",
        ".",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        sys.stdout.buffer.write(stdout)
    if stderr:
        sys.stderr.buffer.write(stderr)
    return proc.returncode


async def main():
    await run_autopep8()
    await run_flake8()
    input("Press Enter to continue...")


asyncio.run(main())
