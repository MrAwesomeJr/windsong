import songplayer

lagtrain = songplayer.Song()

lagtrain_track = songplayer.converter.midi_to_data("Lagtrain.mid",
                                                       track=1,
                                                       truncate_silence=False,
                                                       transpose_semitones=-14,
                                                       round_beats=True)
print("track",1,"created")
lagtrain.append_song(lagtrain_track, beat_offset=0, inherit_bpm=True, inherit_time_signature=True)
print("track appended")

for i in (3,5,7):
    lagtrain_track = songplayer.converter.midi_to_data("Lagtrain.mid",
                                                       track=i,
                                                       truncate_silence=False,
                                                       transpose_semitones=-2,
                                                       round_beats=True)
    print("track",i,"created")
    lagtrain.append_song(lagtrain_track, beat_offset=0, inherit_bpm=True, inherit_time_signature=True)
    print("track appended")

lagtrain = lagtrain.sorted_song()
print("track sorted")

lagtrain.bpm = 100

# file = open("songs/lagtrain_simplified","w+")
# file.write(songplayer.converter.data_to_text(lagtrain))
# file.close()

# file = open("songs/lagtrain_simplified","r")
# lagtrain = songplayer.converter.text_to_data(file.read())

player = songplayer.TimedPlayer(lagtrain)
player.play_lyre(countdown=1,debug=True)