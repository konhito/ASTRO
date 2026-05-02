import json
from pathlib import Path


def save_post(data, path):
    path = Path(path)

    # create file if not exists
    if not path.exists():
        with open(path, "w") as f:
            json.dump([], f)

    # load existing data
    with open(path, "r") as f:
        existing = json.load(f)

    # append new data
    existing.extend(data)

    # save back
    with open(path, "w") as f:
        json.dump(existing, f, indent=2)
