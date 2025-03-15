# Audio Player

This project is a simple audio player built using Python with the wxPython and ffmpeg-python libraries. It provides a graphical user interface (GUI) for playing audio files, including features for play, pause, stop, and seek.

## Project Structure

```
audio-player
├── src
│   ├── main.py        # Entry point of the application
│   ├── player.py      # Contains the AudioPlayer class for audio playback
│   └── utils.py       # Utility functions for loading and converting audio files
├── requirements.txt    # List of dependencies
└── README.md           # Project documentation
```

## Installation

To set up the project, you need to have Python installed on your machine. Then, you can install the required libraries using pip. 

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the dependencies:

```
pip install -r requirements.txt
```

## Usage

To run the audio player, execute the following command:

```
python src/main.py
```

This will launch the audio player GUI, allowing you to load and play audio files.

## Features

- Play, pause, and stop audio playback
- Seek to different positions in the audio track
- Support for various audio formats using ffmpeg

## License

This project is licensed under the MIT License.