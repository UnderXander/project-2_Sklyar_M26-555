from pathlib import Path

from .core import get_command, welcome
from .utils import load_metadata


def run():
    welcome()
    filepath = Path(__file__).resolve().parent / "db_meta.json"
    metadata = load_metadata(filepath=filepath)
    while True:
        command = get_command(metadata=metadata)
        if command == "exit":
            break
