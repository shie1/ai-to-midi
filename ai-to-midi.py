import mido
import sys
import tempfile


def parse_midi_text(midi_text):
    midi_file = mido.MidiFile()
    track = mido.MidiTrack()
    midi_file.tracks.append(track)

    for line in midi_text.split("\n"):
        if line.startswith(";") or line.strip() == "":
            continue

        line = line.split("\t")[0]  # Remove any tabs and everything after them
        tokens = line.split()

        if tokens[0] == "MIDI" and len(tokens) >= 3:
            format_type = int(tokens[1])
            time_division = tokens[2]
            midi_file.type = format_type
            midi_file.ticks_per_beat = int(time_division[1:])
        elif tokens[0] == "MTrk":
            track = mido.MidiTrack()
            midi_file.tracks.append(track)
        elif tokens[0] == "TrkEnd":
            track.append(mido.MetaMessage("end_of_track"))
        elif len(tokens) >= 5:
            if tokens[1] == "On":
                channel = int(tokens[2].split("=")[1])
                note = int(tokens[3].split("=")[1])
                velocity = int(tokens[4].split("=")[1])
                track.append(
                    mido.Message(
                        "note_on", channel=channel, note=note, velocity=velocity
                    )
                )
            elif tokens[1] == "Off":
                channel = int(tokens[2].split("=")[1])
                note = int(tokens[3].split("=")[1])
                track.append(mido.Message("note_off", channel=channel, note=note))

    return midi_file


if __name__ == "__main__":
    ## if piped from stdin
    midi_text = ""
    if not sys.stdin.isatty():
        midi_text = sys.stdin.read()
    ## if file is passed as argument
    elif len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            midi_text = f.read()

    midi_file = parse_midi_text(midi_text)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        midi_file.save(temp_file.name)
        temp_file.seek(0)
        sys.stdout.buffer.write(temp_file.read())
