# windsong
Intended for use with genshin's windsong lyre, with keyboard access. Takes custom files (text files stored under /songs/) or midi files as input, or create notes in songs using songplayer.Song().add_note().
Does not currently support bpm changes, but you can play multiple "songs" in succession to imitate bpm changes.

At the moment, the library uses keyboard inputs to play music. This, along with creation of any derivative works (in this case, video or audio featuring the windsong lyre) treads the border on legality according to HoYoverse's ToS (https://genshin.hoyoverse.com/en/company/terms). Midi files found on the internet are also not always available for free use. Care is advised.

dependancies:
mido
keyboard

written in python 3.10


features to consider adding:
- automatic transposition
- export songs to midi
- notification for multiple tracks on midi converters
- potential support for other players
- file repair for broken song data files
