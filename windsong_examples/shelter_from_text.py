import songplayer

file = open("resources/shelter", "r")
text = file.read()

shelter = songplayer.converter.text_to_data(text)
player = songplayer.Player()
player.play(shelter, countdown=1)