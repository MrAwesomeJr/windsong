import songplayer

lagtrain = songplayer.Song()

lagtrain_track = songplayer.converter.midi_to_data("resources/Lagtrain.mid",
                                                   track=1,
                                                   truncate_silence=False,
                                                   transpose_semitones=-14,
                                                   round_beats=True)
print("track",1,"created")
lagtrain.append_song(lagtrain_track, beat_offset=0, inherit_bpm=True, inherit_time_signature=True)
print("track appended")

for i in (5,):
    lagtrain_track = songplayer.converter.midi_to_data("resources/Lagtrain.mid",
                                                       track=i,
                                                       truncate_silence=False,
                                                       transpose_semitones=-2,
                                                       round_beats=True)
    print("track",i,"created")
    lagtrain.append_song(lagtrain_track, beat_offset=0, inherit_bpm=True, inherit_time_signature=True)
    print("track appended")

#song is sorted automatically on play

player = songplayer.TimedPlayer()
player.play_lyre(lagtrain, countdown=1, end_playback_beat=510, debug=True)