import songplayer

file = open("resources/shelter", "r")
text = file.read()

shelter = songplayer.converter.text_to_data(text)
player = songplayer.SmoothPlayer()
player.play_keyboard(shelter, countdown=1)