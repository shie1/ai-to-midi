import mido
import sys
import tempfile


def parse_midi_text(midi_text):
    midi_text = midi_text.split("\n")
    midi_file = mido.MidiFile(
        ticks_per_beat=int(midi_text[1].split()[0][1:]),
        type=int(midi_text[0].split()[1]),
    )
    track = mido.MidiTrack()
    midi_file.tracks.append(track)

    current_time = 0

    for line in midi_text:
        if line.startswith(";") or line.strip() == "":
            continue

        line_parts = line.split("\t")
        line = line_parts[0]  # Remove any tabs and everything after them
        tokens = line.split()

        if tokens[0] == "MIDI" and len(tokens) >= 3:
            format_type = int(tokens[1])
            time_division = tokens[2]
            midi_file.type = format_type
            midi_file.ticks_per_beat = int(time_division[1:])
        elif tokens[0] == "MTrk":
            track = mido.MidiTrack()
            midi_file.tracks.append(track)
            current_time = 0
        elif tokens[0] == "TrkEnd":
            track.append(mido.MetaMessage("end_of_track", time=int(current_time)))
        elif len(tokens) >= 5:
            try:
                time = int(tokens[0])
                current_time = time
            except ValueError:
                continue  # Skip lines that don't represent MIDI events
            if tokens[1] == "On":
                channel = int(tokens[2].split("=")[1])
                note = int(tokens[3].split("=")[1])
                velocity = int(tokens[4].split("=")[1])
                track.append(
                    mido.Message(
                        "note_on",
                        channel=channel,
                        note=note,
                        velocity=velocity,
                        time=int(current_time),
                    )
                )
            elif tokens[1] == "Off":
                channel = int(tokens[2].split("=")[1])
                note = int(tokens[3].split("=")[1])
                track.append(
                    mido.Message(
                        "note_off",
                        channel=channel,
                        note=note,
                        time=int(current_time),
                    )
                )

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

    # Adjust the timing of MIDI events based on the previous event
    previous_time = 0
    for track in midi_file.tracks:
        for msg in track:
            msg.time -= previous_time
            previous_time += msg.time

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        midi_file.save(temp_file.name)
        temp_file.seek(0)
        sys.stdout.buffer.write(temp_file.read())
