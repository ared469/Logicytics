import json
import os
import platform
import subprocess

from __lib_actions import Actions


def open_file(file: str) -> None:
    """
    Opens a specified file using its default application in a cross-platform manner.
    Args:
        file (str): The path to the file to be opened.
    Returns:
        None
    """
    file_path = os.path.realpath(file)
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(("open", file_path))
        else:  # Linux variants
            subprocess.call(("xdg-open", file_path))
    except Exception as e:
        print(f"Error opening file: {e}")


def update_json_file(filename: str, new_array: list) -> None:
    """
    Updates a JSON file with a new array of current files.
    Args:
        filename (str): The path to the JSON file to be updated.
        new_array (list): The list of current files to be written to the JSON file.
    Returns:
        None
    """
    try:
        with open(filename, "r+") as f:
            data = json.load(f)
            data["CURRENT_FILES"] = new_array
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in the file: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")


def prompt_user(question: str, file_to_open: str = None) -> bool:
    """
    Prompts the user with a question and optionally opens a file if the answer is not 'yes'.
    Args:
        question (str): The question to ask the user.
        file_to_open (str, optional): The file to open if the user doesn't answer 'yes'.
    Returns:
        bool: True if the user's answer is 'yes', otherwise False.
    """
    answer = input(question + " (yes or no):- ")
    if answer.lower() != "yes":
        if file_to_open:
            open_file(file_to_open)
        print(
            "Please ensure you fix the issues/problem and try again with the checklist."
        )
        return False
    return True


def dev_checks() -> None:
    """
    Performs a series of checks to ensure that the developer has followed the required guidelines and best practices.
    This function prompts the developer with a series of questions to ensure that they have followed the required
    contributing guidelines, added files with a specific naming convention, added the file to the CODE directory,
    added docstrings and comments to their code, tested their code, ensured that each file contains only one feature,
    and has included the proper flags in their code.
    Returns:
        None
    """
    checks = [
        ("Have you read the required contributing guidelines?", "../CONTRIBUTING.md"),
        ("Have you made files you don't want to be run start with '_'?", "."),
        ("Have you added the file to CODE dir?", "."),
        ("Have you added docstrings and comments?", "../CONTRIBUTING.md"),
        ("Have you tested your code?", "__Test__.py"),
        ("Is each file containing no more than 1 feature?", "../CONTRIBUTING.md"),
        ("Have you added flags comment?", "../CONTRIBUTING.md"),
        ("Have you NOT modified _wrapper.py without authorization?", "Logicytics.py"),
    ]

    for question, file_to_open in checks:
        if not prompt_user(question, file_to_open):
            return

    files = Actions.check_current_files(".")
    print(files)
    if not prompt_user("Does the list above include your added files?"):
        print("Something went wrong! Please contact support.")
        return

    update_json_file("config.json", files)
    print(
        "Great Job! Please tick the box in the GitHub PR request for completing steps in --dev"
    )


if __name__ == "__main__":
    dev_checks()
