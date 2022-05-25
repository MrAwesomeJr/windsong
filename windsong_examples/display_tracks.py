import mido

mid = mido.MidiFile("resources/Never Gonna Give You Up.mid")

for index, track in enumerate(mid.tracks):
    print(index, track.name)