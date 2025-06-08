import numpy as np

def waveform_to_frames(waveform, frame_length, step):
    N = len(waveform)
    num_frames = 1 + (N - frame_length) // step
    frames = np.zeros((frame_length, num_frames))

    for t in range(num_frames):
        start = t * step
        end = start + frame_length
        frames[:, t] = waveform[start:end]

    return frames

def frames_to_stft(frames):
    return np.fft.fft(frames, axis=0)

def stft_to_spectrogram(stft):
    spectrogram = 20 * np.log10(np.abs(stft) + 1e-10)  # 避免 log(0)
    spectrogram -= np.amax(spectrogram)
    spectrogram = np.clip(spectrogram, -60, 0)
    return spectrogram


