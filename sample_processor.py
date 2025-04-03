import wave
import numpy as np
import pyaudio
import matplotlib.pyplot as plt


class SampleProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.read_wav_file()

    def read_wav_file(self):
        with wave.open(self.file_path, 'rb') as wav_file:
            self.params = wav_file.getparams()
            self.frames = wav_file.readframes(self.params.nframes)
            self.audio_data = np.frombuffer(self.frames, dtype=np.int16)

    def reverse(self):
        self.audio_data = self.audio_data[::-1]
        return self

    def change_amplitude(self, factor):
        self.audio_data = np.int16(self.audio_data * factor)
        return self
    
    def reverberate(self, factor, overwrite=False):
        delay = int(0.1 * self.params.framerate)
        reverb = np.zeros_like(self.audio_data)
    
        for i in range(len(self.audio_data)):
            reverb[i] = self.audio_data[i] + (self.audio_data[i - delay] * factor if i >= delay else 0)
    
        if overwrite:
            self.audio_data = reverb
    
        return self

    def convolution(self, kernel):
        kernel = np.array(kernel)
        convolved_data = np.convolve(self.audio_data, kernel)
        convolved_data = convolved_data / np.max(np.abs(convolved_data)) * 32767
        
        return self

    def show_info(self):
        print("Number of frames:", self.params.nframes)
        print("Number of channels:", self.params.nchannels)
        print("Sample width:", self.params.sampwidth)
        print("Frame rate:", self.params.framerate)
        print("Compression Type:", self.params.comptype)
        print("Compression Name:", self.params.compname)
        return self
    
    def show_plot(self):
        plt.plot(self.audio_data)
        plt.show()
        return self
    
    def save(self, file_path):
        with wave.open(file_path, 'wb') as wav_file:
            wav_file.setparams(self.params)
            wav_file.writeframes(self.audio_data.tobytes())
        return self
    
    def play(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(self.params.sampwidth),
                        channels=self.params.nchannels,
                        rate=self.params.framerate,
                        output=True)
        stream.write(self.audio_data.tobytes())
        stream.stop_stream()
        stream.close()
        p.terminate()
        return self

# Example usage:
# audio = AudioProcessor('path_to_your_file.wav')
# audio.reverse().change_amplitude(0.5).play()