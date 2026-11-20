"""Tests for runner.py one reader pattern."""

import pytest

from orbit_studio.runner import find_inputs_and_output, find_single_input_and_output


class TestFindInputsAndOutput:
    """Tests for the single reader pattern."""

    def test_basic_two_inputs_one_output(self):
        """Two -i inputs with output as last arg."""
        args = ["ffmpeg", "-i", "input.mp4", "-i", "audio.wav", "output.mp4"]
        inputs, output = find_inputs_and_output(args)
        assert inputs == ["input.mp4", "audio.wav"]
        assert output == "output.mp4"

    def test_single_input_one_output(self):
        """Single -i input with output as last arg."""
        args = ["ffmpeg", "-i", "source.mkv", "output.mp4"]
        inputs, output = find_inputs_and_output(args)
        assert inputs == ["source.mkv"]
        assert output == "output.mp4"

    def test_no_inputs_no_output(self):
        """Empty argument list edge case."""
        args = []
        inputs, output = find_inputs_and_output(args)
        assert inputs == []
        assert output == ""

    def test_no_inputs_with_output(self):
        """No -i flags, output is last arg."""
        args = ["ffmpeg", "input.mp4", "output.mp4"]
        inputs, output = find_inputs_and_output(args)
        assert inputs == []
        assert output == "output.mp4"

    def test_multiple_flags_without_i(self):
        """Other flags should be skipped, output is last non-flag arg."""
        args = ["ffmpeg", "-y", "-y", "input.mp4", "output.mp4"]
        inputs, output = find_inputs_and_output(args)
        assert inputs == []
        assert output == "output.mp4"

    def test_last_non_flag_wins(self):
        """When multiple non-flag args exist, the last one is the output."""
        args = ["ffmpeg", "input1.mp4", "input2.mp4", "output.mp4"]
        inputs, output = find_inputs_and_output(args)
        assert inputs == []
        assert output == "output.mp4"

    def test_i_flags_collected(self):
        """All -i flags and their values are collected."""
        args = ["ffmpeg", "-i", "a.mp4", "-i", "b.mp4", "-i", "c.mp4", "output.mp4"]
        inputs, output = find_inputs_and_output(args)
        assert inputs == ["a.mp4", "b.mp4", "c.mp4"]
        assert output == "output.mp4"

    def test_last_i_wins_for_single(self):
        """find_single_input_and_output returns only the last -i input."""
        args = ["ffmpeg", "-i", "first.mp4", "-i", "second.mp4", "output.mp4"]
        inp, output = find_single_input_and_output(args)
        assert inp == "second.mp4"
        assert output == "output.mp4"


class TestFindSingleInputAndOutput:
    """Tests for the convenience wrapper."""

    def test_returns_last_input(self):
        """Returns the last -i input, not all of them."""
        args = ["ffmpeg", "-i", "a.mp4", "-i", "b.mp4", "output.mp4"]
        inp, output = find_single_input_and_output(args)
        assert inp == "b.mp4"  # Last -i input
        assert output == "output.mp4"

    def test_no_i_returns_none(self):
        """When no -i flags exist, returns None for input."""
        args = ["ffmpeg", "input.mp4", "output.mp4"]
        inp, output = find_single_input_and_output(args)
        assert inp is None
        assert output == "output.mp4"

    def test_single_i_returns_that_input(self):
        """When exactly one -i exists, returns that input."""
        args = ["ffmpeg", "-i", "only.mp4", "output.mp4"]
        inp, output = find_single_input_and_output(args)
        assert inp == "only.mp4"
        assert output == "output.mp4"
