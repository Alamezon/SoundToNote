import numpy as np
import librosa
import librosa.display
from scipy.signal import find_peaks

class FrequencyExtractor:

    def __init__(self, audio_file, window_size=2048, hop_size=256, threshold=0.5,
                 silence_threshold=30, min_duration=0.1, min_gap_duration=0.05):
        self.audio_file = audio_file
        self.window_size = window_size
        self.hop_size = hop_size
        self.threshold = threshold
        self.silence_threshold = silence_threshold
        self.min_duration = min_duration
        self.min_gap_duration = min_gap_duration
        self.audio = None
        self.sr = None
        self.stft = None
        self.frequencies = None
        self.times = None

    def load_audio(self):
        """Загружает аудиофайл и вычисляет STFT."""
        self.audio, self.sr = librosa.load(self.audio_file, sr=None)
        self.stft = np.abs(librosa.stft(self.audio, n_fft=self.window_size, hop_length=self.hop_size))
        self.frequencies = librosa.fft_frequencies(sr=self.sr, n_fft=self.window_size)
        self.times = librosa.frames_to_time(np.arange(self.stft.shape[1]), sr=self.sr, hop_length=self.hop_size)

    def filter_silence(self):
        """Фильтрует фреймы с низкой энергией (тишина)."""
        energies = np.sum(self.stft ** 2, axis=0)  # Энергия каждого окна
        return energies > self.silence_threshold  # Только значимые окна

    def get_fundamental_frequency(self, spectrum, peak_freqs, peak_amplitudes):
        """Определяет основную частоту, исключая гармоники."""
        if len(peak_freqs) > 1:
            base_freq = min(peak_freqs)  # Самая низкая частота
            harmonic_count = 0
            for freq in peak_freqs:
                ratio = freq / base_freq
                if np.abs(ratio - round(ratio)) < 0.1:  # Проверка на кратность
                    harmonic_count += 1

            if harmonic_count >= len(peak_freqs) / 2:
                return base_freq
            else:
                return peak_freqs[np.argmax(peak_amplitudes)]
        elif len(peak_freqs) == 1:
            return peak_freqs[0]
        return None

    def extract_frequencies(self):
        """Основной метод для выделения частот."""
        if self.audio is None or self.stft is None:
            self.load_audio()

        valid_frames = self.filter_silence()
        detected_frequencies = []
        current_frequency = None
        current_start_time = None

        for i, is_valid in enumerate(valid_frames):
            if not is_valid:  # Пропускаем тишину
                if current_frequency is not None:
                    # Рассчитываем длительность частоты до начала тишины
                    duration = self.times[i] - current_start_time
                    if duration >= self.min_duration:
                        detected_frequencies.append({
                            "start_time": current_start_time,
                            "frequency": current_frequency,
                            "duration": duration
                        })
                    current_frequency = None
                continue

            spectrum = self.stft[:, i]
            spectrum = spectrum / np.max(spectrum)  # Нормализация

            # Ищем пики в спектре
            peaks, properties = find_peaks(spectrum, height=self.threshold)
            peak_freqs = self.frequencies[peaks]
            peak_amplitudes = properties["peak_heights"]

            if len(peak_freqs) > 0:
                fundamental_freq = self.get_fundamental_frequency(spectrum, peak_freqs, peak_amplitudes)

                # Если новая частота отличается от текущей
                if current_frequency is None or np.abs(fundamental_freq - current_frequency) > 5:
                    if current_frequency is not None:
                        duration = self.times[i] - current_start_time
                        if duration >= self.min_duration:
                            detected_frequencies.append({
                                "start_time": current_start_time,
                                "frequency": current_frequency,
                                "duration": duration
                            })

                    # Начинаем новую частоту
                    current_frequency = fundamental_freq
                    current_start_time = self.times[i]

        # Добавляем последнюю частоту, если она активна
        if current_frequency is not None:
            duration = self.times[-1] - current_start_time
            if duration >= self.min_duration:
                detected_frequencies.append({
                    "start_time": current_start_time,
                    "frequency": current_frequency,
                    "duration": duration
                })

        return detected_frequencies
