import songplayer

# lagtrain = songplayer.Song()
#
# lagtrain_track = songplayer.converter.midi_to_data("Lagtrain.mid",
#                                                    track=1,
#                                                    truncate_silence=False,
#                                                    transpose_semitones=-14,
#                                                    round_beats=True)
# print("track",1,"created")
# lagtrain.append_song(lagtrain_track, beat_offset=0, inherit_bpm=True, inherit_time_signature=True)
# print("track appended")
#
# for i in (3,4,5,6,7,13,14,15):
#     lagtrain_track = songplayer.converter.midi_to_data("Lagtrain.mid",
#                                                        track=i,
#                                                        truncate_silence=False,
#                                                        transpose_semitones=-2,
#                                                        round_beats=True)
#     print("track",i,"created")
#     lagtrain.append_song(lagtrain_track, beat_offset=0, inherit_bpm=True, inherit_time_signature=True)
#     print("track appended")
#
# lagtrain = lagtrain.sorted_song()
# print("track sorted")

# file = open("songs/lagtrain_full","w+")
# file.write(songplayer.converter.data_to_text(lagtrain))
# file.close()

file = open("songs/lagtrain_full","r")
lagtrain = songplayer.converter.text_to_data(file.read())

player = songplayer.TimedPlayer()
player.play_lyre(lagtrain, countdown=1, end_playback_beat=510, debug=True)