#!/usr/bin/env python3
# -------------------------------------------------------------------------------

import asyncio
import sys

# -------------------------------------------------------------------------------


async def run_autopep8():
    error_count = 0

    AUTOPEP8_PATH = "C:\\Program Files\\Python314\\Scripts\\autopep8.exe"
    cmdline = [
        AUTOPEP8_PATH,
        "--in-place",
        "--recursive",
        "--ignore=E501",
        ".",
    ]
    process = await asyncio.create_subprocess_exec(
        *cmdline,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    if stdout:
        sys.stdout.buffer.write(stdout)
    if stderr:
        sys.stderr.buffer.write(stderr)

    error_count = process.returncode if process.returncode is not None else 1

    if error_count > 0:
        print("autopep8 process failing with " + str(error_count) + " error(s).")
    else:
        print("autopep8 process successful.")

    return error_count


async def run_flake8():
    error_count = 0

    PYTHON_PATH = "C:\\Program Files\\Python314\\python.exe"
    cmdline = [
        PYTHON_PATH,
        "-m",
        "flake8",
        "--select=E9,F821,F823,F831,F406,F407,F701,F702,F704,F706",
        ".",
    ]
    process = await asyncio.create_subprocess_exec(
        *cmdline,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    if stdout:
        sys.stdout.buffer.write(stdout)
    if stderr:
        sys.stderr.buffer.write(stderr)

    error_count = process.returncode if process.returncode is not None else 1

    if error_count > 0:
        print("flake8 process failing with " + str(error_count) + " error(s).")
    else:
        print("flake8 process successful.")

    return error_count


# -------------------------------------------------------------------------------


async def main():
    error_count = 0

    error_count += await run_autopep8()
    error_count += await run_flake8()

    if sys.__stdin__.isatty():
        input("Press Enter to continue...")

    if error_count > 0:
        sys.exit(1)

# -------------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())

# -------------------------------------------------------------------------------
