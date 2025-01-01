# PuterAI-Python SDK

**Note**: This is a quick fork on [mowhn](https://github.com/mowhn/PuterAi-python_SDK)'s work, I just made it easier and clean it bit and using FastAPI instead of Flask.

PuterAI Python SDK provides a simple way to interact with the Puter AI API for chatbot interactions and text-to-speech (TTS) generation. This SDK allows you to integrate chatbot and TTS functionalities into your own applications.

## Features

- **Chatbot Interaction**: Communicate with a chatbot powered by Puter AI.
- **Text-to-Speech (TTS)**: Convert any text into audio using AWS Polly TTS service.

## Project Structure

The project consists of multiple components:

- **`login.py`**: Script to handle user login and retrieve an API token then save it to `.env` file for further requests.
- **`cli.py`**: A simple command-line interface that allows users to interact with the Puter chatbot or generate TTS output.
- **`server.py`**: A FastAPI-based API server that runs on `http://127.0.0.1:8000` to exposes endpoints for chatbot and TTS functionalities, it also serves a simple HTML front-end to interact with the chatbot and generate TTS via a browser.

## Requirements

To run this project, you need to install the following dependencies:

- `requests`: To handle HTTP requests.
- `fastapi`: To create the API server.
- `uvicorn`: To run the server.
- `python-dotenv`: To load environment variables from a .env file.

You can install the required dependencies with:

```bash
pip install -r requirements.txt
```

## Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/bitsnaps/PuterAPI-sdk.git
cd PuterAPI-sdk
```

2. **Setup .env File manually or use login.py script (recommended)**

Create a `.env` file in both the `cli` and `API` directories and include your `API_TOKEN`:

```env
API_TOKEN=your_api_token_here
```

3. **Get the API Token**

To quickly obtain your `API_TOKEN`, you must first run `login.py` to log in and retrieve the token:

- Run `login.py`:

  ```bash
  cd cli
  python login.py
  ```

  This will prompt you for your username and password, and if the login is successful, it will output the `API_TOKEN` and save into the `.env` file in both the `cli.py` and `server.py` scripts.

  **Note**:
  - If you don't have a Puter AI account, you can sign up at <a href="https://puter.com/?r=N5Y0ZYTF" target="_blank">
  <img src="https://img.shields.io/badge/Sign/Up/for/PuterAI-Click/Here-brightgreen" alt="Sign Up for PuterAI" /> (This is my referral link, so we'll both get +1Gb extra free space).
  
</a>

4. **Running the Project**

- Run the API Server:

  ```bash
  python server.py
  
  # or using uvicorn:
  uvicorn server:app --reload
  ```

  This will start the FastAPI server on `http://127.0.0.1:8000`.
  
  You can check your server by running this command (you must have `curl` command installed in your system):
  ```bash
  curl -X POST \
    http://127.0.0.1:8000/chat \
    -H 'Content-Type: application/json' \
    -d '{"message": "Hello, how are you?"}'
  ```
  
- Use the Command-Line Interface (CLI):

  To interact with the chatbot or generate TTS from the command line, run:

  ```bash
  python cli.py
  ```

5. **Front-End Example**

You can open the `index.html` file in a browser to interact with the Puter chatbot and generate TTS:

- **Chat with the Bot**: Enter a message and receive a response from the bot.
- **Generate TTS**: Enter text to convert into speech, and play the generated audio.

## Endpoints

The FastAPI exposes the following endpoints:

- **POST `/chat`**: Accepts a JSON object with a `message` field and returns a bot response.

  Example request:

  ```json
  {
    "message": "Hello, bot!"
  }
  ```

- **POST `/tts`**: Accepts a JSON object with a `text` field and returns the corresponding TTS audio.

  Example request:

  ```json
  {
    "text": "Hello, this is a test."
  }
  ```


## LICENSE

This project is licensed under the MIT License - see the [LICENSE](https://github.com/bitsnaps/PuterAPI-sdk/blob/main/LICENSE) file for details.

---

Enjoy building with Puter!
