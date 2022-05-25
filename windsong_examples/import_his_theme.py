import songplayer

shelter = songplayer.converter.midi_to_data("resources/LyricWulf - His Theme.mid", track=4, truncate_silence=True, transpose_semitones=1)

player = songplayer.TimedPlayer()
player.play_lyre(shelter, countdown=1)