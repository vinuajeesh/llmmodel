# Local AI Desktop Assistant

A Python-based desktop application for running local GGUF AI models with advanced system integration capabilities. Built with CustomTkinter and Llama-cpp-python.

## Features

- **Local AI**: Runs GGUF models locally (no internet required for the AI itself).
- **Memory**: Remembers conversation history and allows you to "inject" long-term memories (e.g., "Remember that I am a developer").
- **Tools**:
    - **Web Search**: Can search the web using DuckDuckGo.
    - **Screen View**: Can take a screenshot of your primary monitor (context only).
    - **Network Scan**: Lists local network interfaces and IPs.
    - **CMD Execution**: Can run shell commands (Optional/Risky toggle).
    - **Reminders**: Set natural language reminders (e.g., "Remind me to check logs in 5 minutes").

## Prerequisites

- **Python 3.10+** installed.
- **C++ Compiler**:
    - **Windows**: Visual Studio Community with "Desktop development with C++".
    - **Linux**: `build-essential` or equivalent (`gcc`, `g++`).
    - **Mac**: Xcode Command Line Tools.
    - *Note: This is required to compile `llama-cpp-python`.*

## Installation

1.  Clone the repository.
2.  Install dependencies:

    ```bash
    pip install -r src/requirements.txt
    ```

    *Note: If you have a supported GPU (NVIDIA/AMD), follow the [llama-cpp-python installation guide](https://github.com/abetlen/llama-cpp-python) to enable hardware acceleration (e.g., `CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python`).*

## How to Run

1.  **Download a Model**:
    - Download a `.gguf` model file from HuggingFace (e.g., [Mistral-7B-Instruct-v0.3-GGUF](https://huggingface.co/maziyarpanahi/Mistral-7B-Instruct-v0.3-GGUF)).
    - Save it anywhere on your computer.

2.  **Start the App**:

    ```bash
    python main.py
    ```

3.  **Using the App**:
    - Click **Load Model** in the sidebar and paste the full path to your `.gguf` file.
    - Wait for the "Loaded" indicator.
    - Start chatting!
    - Toggle tools (Web, CMD, Screen, Network) using the switches below the chat bar.

## Tools Usage

- **Reminders**: Type "Remind me to [task] in [X] [seconds/minutes/hours]".
- **CMD**: Enable the "CMD (Risky)" toggle. Type "Run cmd [command]".
