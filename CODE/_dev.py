from __future__ import annotations
from __lib_class import *

log_dev = Log(debug=DEBUG)
log_dev_funcs = {
    "INFO": log_dev.info,
    "WARNING": log_dev.warning,
    "ERROR": log_dev.error,
    "CRITICAL": log_dev.critical,
    None: log_dev.debug,
}


def open_file(file: str) -> None:
    """
    Opens a specified file using its default application in a cross-platform manner.
    Args:
        file (str): The path to the file to be opened.
    Returns:
        None
    """
    if not file == "":
        file_path = os.path.realpath(file)
        try:
            subprocess.call(file_path, shell=False)
        except Exception as e:
            print(f"Error opening file: {e}")


def update_json_file(filename: str, new_data: list | str, key: str) -> None:
    """
    Updates a JSON file with a new array of current files.
    Args:
        filename (str): The path to the JSON file to be updated.
        new_data (list | str): The list of current files to be written to the JSON file.
        key (str): The key in the JSON file to be updated.
    Returns:
        None
    """
    try:
        with open(filename, "r+") as f:
            data = json.load(f)
            data[key] = new_data
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
    except FileNotFoundError:
        log_dev.error(f"File not found: {filename}")
    except json.JSONDecodeError:
        log_dev.error(f"Error decoding JSON in the file: {filename}")
    except Exception as e:
        log_dev.error(f"An error occurred: {e}")


def prompt_user(question: str, file_to_open: str = None) -> bool:
    """
    Prompts the user with a question and optionally opens a file if the answer is not 'yes'.
    Args:
        question (str): The question to ask the user.
        file_to_open (str, optional): The file to open if the user doesn't answer 'yes'.
    Returns:
        bool: True if the user's answer is 'yes', otherwise False.
    """
    try:
        answer = input(question + " (yes or no):- ")
        if answer.lower() != "yes":
            if file_to_open:
                open_file(file_to_open)
            print(
                "Please ensure you fix the issues/problem and try again with the checklist."
            )
            return False
        return True
    except Exception as e:
        log_dev.error(e)


def dev_checks() -> bool:
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
        ("Have you tested your code?", "../TESTS/TEST.py"),
        ("Is each file containing no more than 1 feature?", "../CONTRIBUTING.md"),
        (
            "Have you NOT modified __wrapper__.py without authorization?",
            "Logicytics.py",
        ),
    ]
    try:
        for question, file_to_open in checks:
            if not prompt_user(question, file_to_open):
                return False

        remind = False
        if prompt_user("Is the update a major or minor upgrade (non-patch update)?"):
            if not prompt_user(
                    "Did You Build the EXE with Advanced Installer?",
                    "../Logicytics.aip",
            ):
                return False
            else:
                remind = True

        files = Actions.check_current_files(".")
        print(files)
        if not prompt_user("Does the list above include your added files?"):
            log_dev.error("Something went wrong! Please contact support.")
            return False

        update_json_file("config.json", files, "CURRENT_FILES")
        update_json_file("config.json", input(f"Enter the new version of the project (Old version is {VERSION}):"),
                         "VERSION")
        print(
            "Great Job! Please tick the box in the GitHub PR request for completing steps in --dev"
        )
        if remind:
            print("Remember to upload the EXE files on the PR!")
        return True
    except Exception as e:
        log_dev.error(e)
        return False


def run_dev():
    Actions().mkdir()
    if dev_checks():
        test_files = []
        for item in os.listdir("../TESTS"):
            if (
                    item.lower().endswith(".py")
                    and item.lower() != "__init__.py"
                    and item.lower() != "test.py"
            ):
                full_path = os.path.abspath(os.path.join("../TESTS", item))
                test_files.append(full_path)
                log_dev.info(f"Found test file: {item} - Full path: {full_path}")
        for item in test_files:
            log_dev.info(Actions().run_command(f"python {item}"))
