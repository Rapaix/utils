from scipy.io import wavfile
from tqdm import tqdm
import numpy as np
import os


def windows(signal,window_size, step_size):
    if type(window_size) is not int:
        raise AttributeError("")
    if type(step_size) is not int:
        raise AttributeError("")
    for i_start in range(0, len(signal),step_size):
        i_end = i_start + window_size
        if i_end >= len(signal):
            break
        yield signal[i_start:i_end]


def energy(samples):
    return np.sum(np.power(samples, 2.)) / float(len(samples))


def rising_edges(binary_signal):
    previous_value = 0
    index  = 0
    for x in  binary_signal:
        if x and not previous_value:
            yield index
        previous_value = x
        index += 1

# parameters
window_duration = 3
step_duration = None
silence_threshold = 1e-6

if step_duration is None:
    step_duration = window_duration / 10.
else:
    step_duration = step_duration
silence_threshold = silence_threshold


# input audio

sample_rate, samples = wavfile.read("audioTeste.wav", mmap=True)
output_filename_prefix = "Corte_"
max_amplitude = np.iinfo(samples.dtype).max
max_energy = energy([max_amplitude])

window_size = int(window_duration * sample_rate)
step_size = int(step_duration * sample_rate)

signal_windows = windows(
    signal=samples,
    window_size = window_size,
    step_size= step_size
)

window_energy = (energy(w)/ max_energy for w in tqdm(
    signal_windows,
    total= int(len(samples)/ float(step_size))

))

window_silence = (e > silence_threshold for e in window_energy)

cut_times = (r * step_duration for r in rising_edges(window_silence))
print("Finding silences")
cut_samples = [int(t * sample_rate) for t in cut_times]
cut_samples.append(-1)

cut_ranges = [(i, cut_samples[i], cut_samples[i+1]) for i in range(len(cut_samples) - 1)]
print(cut_ranges)

for i, start, stop in tqdm(cut_ranges):
    output_file_path = "{}_{:03d}.wav".format(
        os.path.join("", output_filename_prefix),
        i
    )
    if not False:
        print("Writing file {}".format(output_file_path))
        wavfile.write(
            filename=output_file_path,
            rate=sample_rate,
            data=samples[start:stop]
        )
    else:
        print("Not writing file {}".format(output_file_path))
