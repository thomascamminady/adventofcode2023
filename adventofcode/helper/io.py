import urllib.request
from typing import Any
import os

import numpy as np
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from rich import print
import pathlib


def website_to_text(day: int, year: int = 2023) -> None:
    url = f"https://adventofcode.com/{year}/day/{day}"

    webpage = str(urllib.request.urlopen(url).read())
    soup = BeautifulSoup(webpage, features="html.parser")

    text = str(soup.get_text())
    text = text.split("\\n")
    # write text to file
    for line in text:
        print(line.strip())


def input_to_int_matrix(riddle_input: str) -> np.ndarray:
    return np.array(
        [[int(_) for _ in line] for line in riddle_input.splitlines()], dtype=int
    )


def get_day(file: str) -> int:
    return int(file.split("/")[-2])


def save_riddle_input(
    day: int, riddle: str, folder_prefix: str = "adventofcode/"
) -> None:
    """Save riddle input to a file"""
    folder_prefix += f"""{str(day).zfill(2)}"""
    if not os.path.exists(folder_prefix):
        pathlib.Path(folder_prefix).mkdir(parents=True, exist_ok=True)
    with open(f"{folder_prefix}/_riddle.txt", "w") as f:
        f.write(riddle)


def get_cookie() -> str:
    """Get cookie from file"""
    with open("adventofcode/helper/cookie.txt", "r") as f:
        cookie = f.read()
    return cookie


def get_example_input(day: int, year: int = 2023) -> str:
    file = f"adventofcode/{str(day).zfill(2)}/_example.txt"
    with open(file, "r") as f:
        return f.read()


def get_riddle_input(day: int, year: int = 2023) -> str:
    if os.path.exists(file := f"adventofcode/{str(day).zfill(2)}/_riddle.txt"):
        with open(file, "r") as f:
            return f.read()

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    riddle_input = get_text_from_url(url)
    return riddle_input


def get_text_from_url(url: str) -> str:
    """Get input from url, using cookies"""

    # Get input
    response = requests.get(url, cookies={"session": get_cookie()})
    return response.text


def tag_visible(element) -> bool:
    if element.parent.name in [
        "style",
        "script",
        "head",
        "title",
        "meta",
        "[document]",
    ]:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body) -> str:
    soup = BeautifulSoup(body, "html.parser")
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return " ".join(t.strip() for t in visible_texts)


def read_only_text_from_url(url: str) -> str:
    """Get input from url, without cookies"""

    response = requests.get(url, cookies={"session": get_cookie()})
    text = text_from_html(response.text)

    # throw everything away before the first occurence of the word Day
    text = text.split("Day", 1)[1]
    #  throw everything away after the text "Answer:"
    text = text.split("Answer:", 1)[0]
    return text


def submit_answer(day: int, level: int, answer: Any, year: int = 2023) -> None:
    print(f"################### day {day}, level {level} ################### ")
    print(answer)

    if answer == 0:
        print("Not submitting 0.")
        return

    print(f"Submit for level {level}? (y/N)")
    if input() != "y":
        return

    # The Advent of Code API endpoint for submitting solutions
    submit_url = f"https://adventofcode.com/{year}/day/{day}/answer"

    # Create the payload with your solution and the riddle input
    payload = {
        "level": f"{level}",  # The level number (1 or 2)
        "answer": str(answer),
        "debug": "1",
    }

    # Send the HTTP POST request to the API endpoint with the payload
    response = requests.post(
        submit_url, json=payload, cookies={"session": get_cookie()}
    )
    print(response.text)
    # Check the status code of the response to verify that the submission was successful
    if response.status_code == 200:
        print("Solution submitted successfully!")
    else:
        print("Failed to submit solution. Response status code: ", response.status_code)
