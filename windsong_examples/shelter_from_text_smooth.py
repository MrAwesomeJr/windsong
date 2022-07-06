import songplayer

file = open("resources/shelter", "r")
text = file.read()

shelter = songplayer.converter.text_to_data(text)
player = songplayer.Player(timer=songplayer.StaticTimer())
player.play_keyboard(shelter, countdown=1)
