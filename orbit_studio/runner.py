"""
runner.py - Find a command's inputs and output by reading the finished argument list.

This module provides a single reader pattern for determining a command's inputs
and output from the finished argument list, replacing per-check searches for `-i`
or taking the last argument as the output.
"""

import sys
from typing import List, Optional, Tuple


def find_inputs_and_output(args: List[str]) -> Tuple[List[str], str]:
    """
    Find the input files and output file from a finished argument list.

    Uses a single reader pattern: scan the argument list once to find all `-i`
    prefixed inputs, and the last non-flag argument as the output.

    Args:
        args: The finished argument list (e.g. from sys.argv or a completed ffmpeg command).

    Returns:
        A tuple of (inputs, output) where:
        - inputs is a list of input file paths found via `-i` flags
        - output is the last non-flag argument in the list

    Example:
        >>> find_inputs_and_output(["ffmpeg", "-i", "input.mp4", "-i", "audio.wav", "output.mp4"])
        (["input.mp4", "audio.wav"], "output.mp4")
    """
    inputs: List[str] = []
    output: Optional[str] = None

    # Single pass: collect all -i prefixed inputs, track last non-flag arg as output
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "-i" and i + 1 < len(args):
            inputs.append(args[i + 1])
            i += 2
        elif arg.startswith("-") and arg != "-i":
            # Skip other flags, don't consume next arg
            i += 1
        else:
            # Non-flag argument: this is a candidate for output
            # We keep updating output so the last one wins
            output = arg
            i += 1

    if output is None:
        # Fallback: if no non-flag arg found, use last element
        output = ""

    return inputs, output  # type: ignore[return-value]


def find_single_input_and_output(args: List[str]) -> Tuple[Optional[str], str]:
    """
    Find a single input and output from a finished argument list.

    Convenience wrapper that returns at most one input (the last -i found)
    and the output.

    Args:
        args: The finished argument list.

    Returns:
        A tuple of (input_or_None, output)
    """
    inputs, output = find_inputs_and_output(args)
    return (inputs[-1] if inputs else None, output)


if __name__ == "__main__":
    # Simple CLI demo
    args = sys.argv[1:]
    inputs, output = find_inputs_and_output(args)
    print(f"Inputs: {inputs}")
    print(f"Output: {output}")
