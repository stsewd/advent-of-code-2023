from pathlib import Path
import re
from textwrap import dedent

words_to_digits = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def get_first_digit(line: str) -> str:
    digit = None
    i_end = len(line) - 1

    # Check for digits
    for i, c in enumerate(line):
        if c.isdigit():
            digit = c
            i_end = i - 1
            break

    # If we didn't find a digit, or if the digit is not in the first 3 characters,
    # we need to check for words.
    if i_end < 2:
        assert digit is not None
        return digit

    # Check for words
    for digit_in_words in words_to_digits:
        index = line.find(digit_in_words, 0, i_end + 1)
        if index != -1:
            digit = words_to_digits[digit_in_words]
            if index < 2:
                break
            i_end = index + len(digit_in_words) - 1

    assert digit is not None
    return digit


def get_last_digit(line: str) -> str:
    digit = None
    i_start = 0

    # Check for digits
    for i, c in enumerate(reversed(line)):
        if c.isdigit():
            digit = c
            i_start = len(line) - i - 1
            break

    if i_start > len(line) - 3:
        assert digit is not None
        return digit

    # Check for words
    for digit_in_words in words_to_digits:
        index = line.rfind(digit_in_words, i_start)
        if index != -1:
            digit = words_to_digits[digit_in_words]
            if index > len(line) - 3:
                break
            i_start = index

    assert digit is not None
    return digit


def solve(text: str) -> int:
    """
    A solution using only string methods.

    This solution is slower than solve2, but it's more imperative.
    """
    total = 0
    for line in text.splitlines():
        first_digit = get_first_digit(line)
        last_digit = get_last_digit(line)
        number = int(first_digit + last_digit)
        total += number
    return total


def solve2(text: str) -> int:
    """
    A shorter solution using regex.

    This solution ended up being faster than the first solution.

    First solution 2.88
    Second solution 1.33

    Tested with 1000 iterations.
    """
    total = 0
    first_digit_pattern = re.compile(
        r"(\d|one|two|three|four|five|six|seven|eight|nine)"
    )
    last_digit_pattern = re.compile(
        r".*(\d|one|two|three|four|five|six|seven|eight|nine).*$"
    )
    for line in text.splitlines():
        match = first_digit_pattern.search(line)
        assert match is not None
        first_digit = match.group(1)

        match = last_digit_pattern.search(line)
        assert match is not None
        last_digit = match.group(1)

        number = words_to_digits.get(first_digit, first_digit) + words_to_digits.get(
            last_digit, last_digit
        )
        total += int(number)
    return total


def main():
    input_text = Path("01.txt").read_text()
    print(solve(input_text))


if __name__ == "__main__":
    main()


def test():
    text = dedent(
        """
        two1nine
        eightwothree
        abcone2threexyz
        xtwone3four
        4nineeightseven2
        zoneight234
        7pqrstsixteen
        """
    ).strip()
    assert solve(text) == 281
    assert solve2(text) == 281

    text = Path("01.txt").read_text()
    assert solve(text) == 52834
    assert solve2(text) == 52834
