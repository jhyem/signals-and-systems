"""Wiener speech enhancement for the Signals and Systems challenge.

Derived from the team's original noise_reduction_baselines.ipynb implementation.
Changes for this candidate:
  - Wiener gain floor: 0.05 (baseline) -> 0.15 (validation experiment)
  - Standalone `enhance(noisy, sample_rate=16000)` interface
  - Accept mono or (samples, channels) waveform, preserving shape

No clean/reference audio or validation metadata is used during enhancement.
Requires NumPy and SciPy. Does not require Colab, PESQ, or dataset files.
"""

import numpy as np
from scipy import signal
from scipy.ndimage import uniform_filter1d

# Shared baseline parameters. Only the gain floor differs from the baseline.
N_FFT = 512
HOP = 128
NOISE_FRACTION = 0.20
WIENER_SMOOTHING = 0.98
WIENER_GAIN_FLOOR = 0.15


def _waveform(x):
    """Check a mono waveform, reproducing baseline numeric precision."""
    x = np.asarray(x, dtype=np.float64)
    if x.ndim != 1 or x.size == 0 or not np.isfinite(x).all():
        raise ValueError("Expected a nonempty, finite mono waveform.")
    return x


def _stft_audio(x, sample_rate):
    x = _waveform(x)
    if x.size < N_FFT:
        x = np.pad(x, (0, N_FFT - x.size))
    return signal.stft(
        x,
        fs=sample_rate,
        window="hann",
        nperseg=N_FFT,
        noverlap=N_FFT - HOP,
        nfft=N_FFT,
        boundary="zeros",
        padded=True,
    )


def _inverse_stft(z, length, sample_rate):
    _, y = signal.istft(
        z,
        fs=sample_rate,
        window="hann",
        nperseg=N_FFT,
        noverlap=N_FFT - HOP,
        nfft=N_FFT,
        input_onesided=True,
        boundary=True,
    )
    if len(y) < length:
        raise ValueError("Inverse STFT produced insufficient samples.")
    return _waveform(y[:length])


def _estimate_noise_power(z, times, length, sample_rate):
    """Fixed noise PSD from lowest-energy complete frames (team baseline)."""
    power = np.abs(z) ** 2
    # Exclude artificially quiet frames from STFT boundary padding.
    centers = np.rint(times * sample_rate).astype(int)
    full = np.flatnonzero(
        (centers >= N_FFT // 2) & (centers + N_FFT // 2 <= length)
    )
    if not len(full):
        full = np.arange(power.shape[1])
    energy = power[:, full].mean(axis=0)
    count = max(1, int(np.ceil(NOISE_FRACTION * len(full))))
    selected = full[np.argsort(energy, kind="stable")[:count]]
    estimate = power[:, selected].mean(axis=1)
    return np.maximum(uniform_filter1d(estimate, size=3, mode="nearest"), 1e-18)


def _enhance_mono(noisy, sample_rate):
    x = _waveform(noisy)
    _, times, z = _stft_audio(x, sample_rate)
    power = np.abs(z) ** 2
    noise = _estimate_noise_power(z, times, len(x), sample_rate)
    posterior_snr = power / noise[:, None]
    enhanced = np.empty_like(z)
    previous_clean_power = np.zeros_like(noise)

    for frame in range(z.shape[1]):
        instantaneous = np.maximum(posterior_snr[:, frame] - 1.0, 0.0)
        if frame == 0:
            prior_snr = instantaneous
        else:
            prior_snr = (
                WIENER_SMOOTHING * previous_clean_power / noise
                + (1 - WIENER_SMOOTHING) * instantaneous
            )
        gain = np.clip(
            prior_snr / (1 + prior_snr), WIENER_GAIN_FLOOR, 1
        )
        enhanced[:, frame] = gain * z[:, frame]
        previous_clean_power = np.abs(enhanced[:, frame]) ** 2
    return _inverse_stft(enhanced, len(x), sample_rate)


def enhance(noisy, sample_rate=16000):
    """Remove noise from input samples, returning the same shape as input.

    Args:
        noisy: mono 1D array or (samples, channels) array (e.g. soundfile.read).
        sample_rate: input sampling rate. This challenge uses 16,000 Hz.

    Returns:
        Enhanced samples as a float64 NumPy array, with original shape.
    """
    if sample_rate != 16000:
        raise ValueError("This challenge baseline supports 16,000 Hz only.")
    samples = np.asarray(noisy)
    if samples.ndim == 1:
        return _enhance_mono(samples, sample_rate)
    if samples.ndim == 2 and samples.shape[0] > 0 and samples.shape[1] > 0:
        return np.column_stack([
            _enhance_mono(samples[:, ch], sample_rate)
            for ch in range(samples.shape[1])
        ])
    raise ValueError("Expected a 1D mono or 2D (samples, channels) audio array.")
