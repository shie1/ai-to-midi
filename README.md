# AI to MIDI

Converts MIDI text to MIDI file format using Python and the mido library.

## Description

This project provides a Python script that converts MIDI text into a MIDI file. It parses the MIDI text, which contains a series of commands and events, and generates a corresponding MIDI file with the specified musical notes and events.

The script uses the mido library to handle MIDI file creation and manipulation.

## Requirements

- Python 3.x
- mido library

## Installation

1. Clone the repository:
   ```shell
   git clone https://github.com/your-username/ai-to-midi.git
2. Navigate to the project directory:
    ```shell
    cd ai-to-midi
3. Install the required dependencies:
    ```shell
    pip install -r requirements.txt
## Usage
1. Prepare a text file with the MIDI commands and events. The MIDI text should follow a specific format:
    ```
    MIDI 0
    T96
    MTrk
    0 PrCh ch=1 p=0 ; Program Change
    0 On ch=1 n=36 v=80 ; Turn on sound, C1, velocity = 80
    96 On ch=1 n=36 v=0 ; Turn off sound

    TrkEnd
    MTrk
2. Direct the script to the input file and pipe the output to a MIDI file:
    ```shell
    cat input.txt | python ai-to-midi.py >> output.mid
## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.