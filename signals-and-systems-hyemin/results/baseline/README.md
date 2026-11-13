# Baseline Evaluation Results

## 1. Overview

전통적인 신호 처리 기반 음성 잡음 제거 알고리즘의 성능을 비교하기 위해 Validation 데이터셋 전체를 평가하였다.

- Dataset: Validation
- Number of audio files: 164
- Sampling rate: 16 kHz
- Audio duration: 3 seconds
- Evaluation metrics: PESQ-WB, SNR
- PESQ evaluation failures: 0

각 알고리즘은 Noisy Input을 입력으로 사용하며, Clean 음성은 성능 평가를 위한 참조 신호로만 사용한다.

## 2. Compared Methods

| Method | Description |
|---|---|
| Noisy Input | 잡음 제거 전 입력 신호 |
| Basic Filter | 기본 필터링 방식 |
| Lowpass | 저역 통과 필터 |
| Highpass | 고역 통과 필터 |
| Bandstop | 대역 저지 필터 |
| Spectral Subtraction | 스펙트럼 감산법 |
| Wiener Filter | Wiener 필터 |

## 3. Overall Evaluation Results

All 7 methods were evaluated on the same 164 validation audio files.

| Method | Mean SNR (dB) | ΔSNR (dB) | Mean PESQ | ΔPESQ |
|---|---:|---:|---:|---:|
| Noisy Input | 9.634 | 0.000 | 1.395 | 0.000 |
| Basic Filter | 9.070 | -0.564 | 1.449 | +0.054 |
| Lowpass | 9.641 | +0.007 | 1.422 | +0.028 |
| Highpass | 9.473 | -0.161 | 1.429 | +0.034 |
| Bandstop | 9.254 | -0.380 | 1.389 | -0.006 |
| Spectral Subtraction | 12.568 | +2.934 | 1.538 | +0.143 |
| Wiener Filter | 13.120 | +3.485 | 1.598 | +0.204 |

## 4. Results Analysis

### 4.1 Wiener Filter

Wiener Filter achieved the highest average PESQ and SNR among the evaluated methods.

- Mean PESQ: 1.598
- Mean SNR: 13.120 dB
- PESQ improvement: +0.204
- SNR improvement: +3.485 dB

### 4.2 Spectral Subtraction

Spectral Subtraction achieved the second-best performance in both metrics.

- Mean PESQ: 1.538
- Mean SNR: 12.568 dB
- PESQ improvement: +0.143
- SNR improvement: +2.934 dB

### 4.3 Conventional Filters

Basic Filter, Lowpass, Highpass, and Bandstop showed limited improvements compared with the two spectral processing methods.

In particular, Basic Filter improved PESQ slightly but decreased SNR. Bandstop showed a slight decrease in PESQ.

## 5. Conclusion

Wiener Filter is selected as the leading baseline method based on the current Validation results.

Spectral Subtraction is retained as a second strong baseline for further comparison.

Further experiments will investigate parameter optimization, noise-category-specific performance, and possible trade-offs between noise reduction and speech quality.

## 6. Evaluation Files

| File | Description |
|---|---|
| `run_config.json` | Experiment configuration |
| `validation_per_file.csv` | Per-file evaluation results |
| `validation_summary.csv` | Overall performance summary |
| `validation_common_subset.csv` | Comparison on common valid samples |
| `validation_by_noise_category.csv` | Results by noise category |
| `validation_by_noise_difficulty.csv` | Results by noise difficulty |
| `validation_by_target_snr_db.csv` | Results by target SNR |

## 7. Reproducibility

The experiment configuration is recorded in `evaluation/run_config.json`.

The corresponding implementation is available in `notebooks/02_baseline_comparison.ipynb`.
