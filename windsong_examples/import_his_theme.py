import songplayer

his_theme = songplayer.converter.midi_to_data("resources/LyricWulf - His Theme.mid",
                                              track=4,
                                              truncate_silence=True,
                                              transpose_semitones=1)

player = songplayer.Player()
player.play(his_theme, countdown=1)
