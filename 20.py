import sys
import pytest
from pathlib import Path
from textwrap import dedent

FLIP_FLOP = "%"
CONJUNCTION = "&"
HIGH = "high"
LOW = "low"


def solve(text: str) -> int:
    # Type, destinations, state
    config = {}
    for line in text.splitlines():
        name, destinations = line.split(" -> ")
        destinations = destinations.split(", ")
        if name.startswith(FLIP_FLOP):
            config[name[1:]] = [FLIP_FLOP, destinations, False]
        elif name.startswith(CONJUNCTION):
            config[name[1:]] = [CONJUNCTION, destinations, {}]
        else:
            config[name] = ["", destinations, ""]

    # Fill state for conjunctions.
    for name, (_, destinations, _) in config.items():
        for destination in destinations:
            if destination in config and config[destination][0] == CONJUNCTION:
                config[destination][2][name] = LOW

    # TODO: use this to detect cycles,
    # so the calculation can be done more efficiently.
    # states = {}
    high_signals_n = 0
    low_signals_n = 0

    for _ in range(1000):
        low_signals_n += 1
        signals_to_process = [
            ("broadcaster", dest, LOW) for dest in config["broadcaster"][1]
        ]
        while signals_to_process:
            new_signals_to_process = []
            for src, dest, signal in signals_to_process:
                if signal == HIGH:
                    high_signals_n += 1
                else:
                    low_signals_n += 1

                if dest not in config:
                    continue

                type_, destinations, state = config[dest]
                if type_ == FLIP_FLOP:
                    if signal == HIGH:
                        continue
                    new_signal = LOW if state else HIGH
                    for subdest in destinations:
                        new_signals_to_process.append((dest, subdest, new_signal))
                    config[dest][2] = not state
                elif type_ == CONJUNCTION:
                    state[src] = signal
                    new_signal = LOW if all(v == HIGH for v in state.values()) else HIGH
                    for subdest in destinations:
                        new_signals_to_process.append((dest, subdest, new_signal))

            signals_to_process = new_signals_to_process

    return high_signals_n * low_signals_n


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(solve(p.read_text()))


def test():
    text = dedent(
        """
        broadcaster -> a, b, c
        %a -> b
        %b -> c
        %c -> inv
        &inv -> a
        """
    ).strip()
    assert solve(text) == 32000000

    text = dedent(
        """
        broadcaster -> a
        %a -> inv, con
        &inv -> b
        %b -> con
        &con -> output
        """
    ).strip()
    assert solve(text) == 11687500


def test_input():
    p = Path("20.txt")
    if not p.exists():
        pytest.skip(f"{p} does not exist")
    text = p.read_text()
    assert solve(text) == 839775244
