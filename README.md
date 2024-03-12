# Healthy salad

Api server connect with Line webhook for recvieve message content and connect with GCP for use Vertex AI prediction.

## Installation

1. Clone the repository
2. Create a virtual environment

```bash
python -m venv .venv
```

3. Activate the virtual environment

- Windows

```cmd
.venv\Scripts\activate
```

- Linux/macOS

```bash
source .venv/bin/activate
```

4. Install the required packages

```bash
pip install -r requirements.txt
```

5. Run the application to show the list of available commands

```bash
python src/index.py
```

## Command for usage

```bash
python src/index.py <COMMAND>
```

### Command lists

- List all routes

```bash
route:list
```

- Start api server

```bash
server:start
```

- Space for testing

```bash
pg
```
