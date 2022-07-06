import songplayer

rick = songplayer.Song()

track = songplayer.converter.midi_to_data("resources/Never Gonna Give You Up.mid",
                                          track=1,
                                          truncate_silence=False,
                                          transpose_semitones=-1,
                                          round_beats=True)
print("track",1,"created")
rick.append_song(track, beat_offset=0, inherit_bpm=True, inherit_time_signature=True)
print("track appended")

for i in (5,6,7,8,11):
    track = songplayer.converter.midi_to_data("resources/Never Gonna Give You Up.mid",
                                              track=i,
                                              truncate_silence=False,
                                              transpose_semitones=-1,
                                              round_beats=True)
    print("track",i,"created")
    rick.append_song(track, beat_offset=0, inherit_bpm=True, inherit_time_signature=True)
    print("track appended")

#song is sorted automatically on play

player = songplayer.Player()

player.play(rick, countdown=1, debug=True)