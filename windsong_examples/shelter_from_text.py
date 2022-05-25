import songplayer

file = open("resources/shelter", "r")
text = file.read()

shelter = songplayer.converter.text_to_data(text)
player = songplayer.TimedPlayer()
player.play_lyre(shelter, countdown=1)