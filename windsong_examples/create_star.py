import songplayer

star = songplayer.Song()

star.time_signature = [2,2]
star.bpm = 120
star.add_note(1, ("C",3))
star.add_note(2, ("C",3))
star.add_note(3, ("G",3))
star.add_note(4, ("G",3))
star.add_note(5, ("A",3))
star.add_note(6, ("A",3))
star.add_note(7, ("G",3))
star.add_note(9, ("F",3))
star.add_note(10, ("F",3))
star.add_note(11, ("E",3))
star.add_note(12, ("E",3))
star.add_note(13, ("D",3))
star.add_note(14, ("D",3))
star.add_note(15, ("C",3))

player = songplayer.Player()
player.play(star, countdown=1)