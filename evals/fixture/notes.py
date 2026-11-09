"""Tiny notes module used by the agent evals."""


def make_title(raw):
    """Return the note title for raw user input."""
    return raw


def word_count(text):
    """Count the words in text."""
    return len(text.split(" "))
