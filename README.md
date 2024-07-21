# Simple Valorant Bot

Discord bot that logs a user's valorant matches in a chosen discord server channel.

## Installation

### pip

Use pip to install the requirements

```bash
pip install -r requirements.txt
```

### Edit config.py

Ensure that the correct credentials are put in config.py

```python
API_KEY = "<API KEY from https://docs.henrikdev.xyz/valorant/general>"
TOKEN = "<Discord Bot Client Token>"
NAME = "<Name of user to be tracked>"
TAG = "<Tag of user to be tracked>"
```

## Usage

Start the bot up:

```bash
python3 index.py
```

In the server, run !start and then match history will automatically be posted in that channel.

Use !embed to switch between simple and fancy layout.
