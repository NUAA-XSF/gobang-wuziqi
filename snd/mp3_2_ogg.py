import os.path as path

from pydub import AudioSegment

snd_dir = path.dirname(path.abspath(__file__))
AudioSegment.from_mp3(path.join(snd_dir, 'song18.mp3')).export(path.join(snd_dir, 'song18.ogg'), format='ogg')
