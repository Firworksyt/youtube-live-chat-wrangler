# YouTube Live Chat Wrangler

## Disclaimer

**IMPORTANT:** This project is in very early stages of development and is not ready for production use. It may contain bugs, lack proper error handling, and could change significantly in future updates. Use at your own risk.

## Description

YouTube Live Chat Wrangler is a tool designed to download and display live chat messages from YouTube videos. It allows users to easily view and search through chat logs from past live streams.

## Features

- Download chat logs from YouTube live streams
- Display chat messages with timestamps and usernames
- Live search functionality for filtering messages
- Support for custom YouTube emojis

## Installation

### Option 1: Using Docker (Recommended)

#### Requirements
- Docker
- Docker Compose

#### Steps
1. Clone this repository:
   ```
   git clone https://github.com/your-username/youtube-live-chat-wrangler.git
   cd youtube-live-chat-wrangler
   ```

2. Build and run the Docker container:
   ```
   docker-compose build
   docker-compose up -d
   ```

3. Access the application at `http://localhost:8000`

### Option 2: Using Python and pip

#### Requirements
- Python 3.9+
- pip

#### Steps
1. Clone this repository:
   ```
   git clone https://github.com/your-username/youtube-live-chat-wrangler.git
   cd youtube-live-chat-wrangler
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

5. Access the application at `http://localhost:8000`

## Usage

1. Enter a YouTube URL in the input field and click "Download Chat"
2. Once downloaded, the chat messages will be displayed
3. Use the search bar to filter messages

## Known Issues

- Performance may degrade with very large chat logs
- Some YouTube emojis may not display correctly but it does attempt to display member emojis

## Contributing

As this project is in its early stages, contributions are welcome but please be aware that significant changes may occur. If you'd like to contribute, please open an issue first to discuss your proposed changes.

## License

This project is licensed under the WTFPL - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by YouTube or Google. Use of this tool should comply with YouTube's terms of service.