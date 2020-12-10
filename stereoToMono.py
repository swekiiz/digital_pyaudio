from pydub import AudioSegment

filename = "SuperMario.wav"

sound = AudioSegment.from_wav(r'./music/' + filename)
sound = sound.set_channels(1)
sound.export(r'./music/' + filename[:-4] + 'Mono.wav', format="wav")
