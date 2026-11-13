# Baseline Algorithm Evaluation

## 1. 실험 목적

본 실험은 음성 잡음 제거 프로젝트의 후속 알고리즘 개선을 위한 Baseline 성능을 확보하는 것을 목적으로 한다.

기본 입력인 Noisy Audio를 기준으로 Basic Filter, Spectral Subtraction, Wiener Filter의 성능을 비교하였다.

모든 알고리즘은 전통적인 DSP 기반으로 구성하였으며, 동일한 Validation 데이터셋을 사용하여 성능을 평가하였다.

## 2. 실험 환경 및 평가 기준

| 항목 | 설정 |
|---|---|
| Dataset | Noise Reduction Challenge |
| Evaluation Split | Validation |
| 평가 파일 수 | 164개 |
| Sample Rate | 16,000 Hz |
| Audio Channel | Mono |
| Audio Duration | 3초 |
| Samples per File | 48,000 |
| STFT n_fft | 512 |
| STFT hop_length | 128 |
| PESQ Mode | Wideband (WB) |
| Primary Metric | PESQ-WB |
| Secondary Metric | SNR |

### 데이터 사용 원칙

- Train 데이터는 알고리즘 개발에 사용한다.
- Validation 데이터는 파라미터 조정 및 알고리즘 비교에 사용한다.
- Clean Audio는 평가를 위한 기준 신호로만 사용한다.
- 잡음 제거 함수에는 Noisy Audio만 입력한다.
- 모든 알고리즘은 동일한 Validation 파일을 대상으로 평가한다.

### 평가 지표

- PESQ-WB: 잡음 제거 후 음성 품질을 평가하는 주요 지표
- SNR: Clean 신호 대비 출력 신호의 잡음 수준을 확인하는 보조 지표

SNR은 다음 식으로 계산하였다.

\[
SNR=10\log_{10}\frac{\sum x_{clean}^2}{\sum(x_{clean}-x_{output})^2}
\]

각 지표는 파일별 계산값을 산술평균하여 집계하였다.

## 3. Baseline 알고리즘 설정

### Basic Filter

- High-pass Filter: 100 Hz
- Low-pass Filter: 3,500 Hz
- Band-stop Filter: 950–1,050 Hz
- Filter Order: 4

### Spectral Subtraction

- Subtraction Alpha: 1.5
- Spectral Floor: 0.02
- Noise Fraction: 0.20

### Wiener Filter

- Wiener Smoothing: 0.98
- Gain Floor: 0.05
- Noise Fraction: 0.20

### 공통 Noise Estimation

STFT 프레임 중 에너지가 낮은 프레임을 선택하여 평균 Noise Power Spectrum을 추정하는 방식을 사용하였다.

Noise Fraction은 0.20으로 설정하였다.

이 추정 방식은 Spectral Subtraction과 Wiener Filter에서 공통으로 사용하였으며, 후속 실험에서도 비교의 공정성을 위해 동일하게 유지하는 것을 권장한다.

## 4. 전체 Baseline 평가 결과

Validation 164개 파일에 대한 평가 결과는 다음과 같다.

| Method | Mean PESQ-WB | PESQ 개선량 | Mean SNR (dB) | SNR 개선량 (dB) |
|---|---:|---:|---:|---:|
| Noisy Input | 1.3947 | 0.0000 | 9.6341 | 0.0000 |
| Basic Filter | 1.4486 | +0.0539 | 9.0697 | -0.5645 |
| Spectral Subtraction | 1.5376 | +0.1429 | 12.5683 | +2.9341 |
| Wiener Filter | **1.5984** | **+0.2037** | **13.1196** | **+3.4854** |

모든 방법에서 PESQ 계산은 164개 파일에 대해 정상적으로 완료되었으며, 실패한 파일은 없었다.

## 5. 결과 분석

### 5.1 전체 성능 비교

Wiener Filter가 평균 PESQ-WB 1.5984로 가장 높은 성능을 보였다.

Noisy Input 대비 PESQ는 0.2037 증가하였으며, SNR은 약 3.4854 dB 개선되었다.

Spectral Subtraction은 평균 PESQ-WB 1.5376으로 두 번째로 높은 성능을 보였다.

Basic Filter는 PESQ가 소폭 증가했지만 SNR은 오히려 감소하였다. 단순 주파수 필터링만으로는 다양한 잡음 환경에서 충분한 성능 개선을 기대하기 어렵다는 점을 확인하였다.

따라서 현재 Baseline에서는 Wiener Filter를 가장 우수한 전체 성능의 기준 알고리즘으로 선정한다.

### 5.2 Noise Category별 결과

23개 Noise Category를 비교한 결과:

- Wiener Filter: 15개 Category에서 가장 높은 PESQ
- Spectral Subtraction: 2개 Category에서 가장 높은 PESQ
- Noisy Input: 6개 Category에서 가장 높은 PESQ

Wiener Filter는 전반적으로 우수한 성능을 보였으며, 특히 aircraft_cockpit, broadband_noise, shower, phone_dialing 등에서 상대적으로 높은 개선을 보였다.

Spectral Subtraction은 military_vehicle 및 traffic_vehicle에서 Wiener Filter보다 높은 PESQ를 기록하였다.

반면 bell, clap, click, door_moving, footsteps, machine_gun에서는 Noisy Input이 가장 높은 PESQ를 보였다.

다만 Noisy Input이 우세했던 Category 중 다수는 평가 파일 수가 매우 적었다. 특히 clap, click, door_moving, footsteps, machine_gun은 각각 1개 파일에 해당하므로, 해당 결과만으로 일반적인 알고리즘 성능을 판단하거나 특정 Category에 과도하게 최적화하지 않도록 주의해야 한다.

### 5.3 PESQ와 SNR의 차이

SNR이 개선되더라도 PESQ가 반드시 같은 수준으로 개선되는 것은 아니다.

따라서 후속 알고리즘의 최종 비교에서는 PESQ-WB를 우선적으로 고려하고, SNR과 청취 결과 및 스펙트로그램 분석을 함께 참고한다.

## 6. 후속 실험 방향

### Spectral Subtraction 개선

다음 파라미터를 조정하여 Validation 성능을 비교한다.

- Subtraction Alpha: 1.0, 1.2, 1.5, 1.8, 2.0
- Spectral Floor: 0.01, 0.02, 0.05, 0.10

Alpha는 잡음 제거 강도에 영향을 주며, Spectral Floor는 과도한 감쇠와 음성 손실을 조절하는 데 사용한다.

### Wiener Filter 개선

다음 파라미터를 조정하여 Validation 성능을 비교한다.

- Wiener Smoothing: 0.90, 0.95, 0.98, 0.99
- Gain Floor: 0.01, 0.05, 0.10, 0.15

Smoothing은 이전 프레임의 추정 결과를 반영하는 정도를 조절하며, Gain Floor는 음성 성분이 지나치게 감쇠되는 것을 제한한다.

### 공통 실험 원칙

- 동일한 Validation 164개 파일 사용
- PESQ-WB를 주요 평가 지표로 사용
- SNR을 보조 평가 지표로 사용
- Noise Estimation 방식은 공통으로 유지
- 실험별 파라미터와 결과를 함께 저장
- 최적 파라미터 선정 시 평균 성능뿐 아니라 Category별 성능과 음성 손실 여부도 확인

위 파라미터는 후속 실험을 위한 후보 범위이며, 최적값으로 확정된 것은 아니다.

## 7. 한계 및 주의 사항

- 현재 결과는 Baseline 설정에 대한 Validation 평가 결과이며, 최종 알고리즘 성능을 의미하지 않는다.
- 일부 Noise Category는 평가 파일 수가 적어 Category별 평균의 신뢰도에 한계가 있다.
- PESQ와 SNR은 서로 다른 특성을 평가하므로 한 지표만으로 음성 품질을 단정하지 않는다.
- 파라미터 변경 시 동일한 평가 조건을 유지해야 한다.
- Validation 결과를 반복적으로 확인하여 과도하게 최적화하지 않도록 주의한다.

## 8. 결과 파일

실험 결과 및 설정 파일은 다음 위치에 저장한다.

`results/baseline/evaluation/`

## 9. 현재 결론

현재 Baseline 비교에서는 Wiener Filter가 가장 높은 평균 PESQ-WB 및 SNR을 기록하였다.

따라서 Wiener Filter를 주요 개선 대상이자 전체 성능 비교 기준으로 활용하고, Spectral Subtraction은 별도의 개선 후보로 유지한다.

이후 각 알고리즘 담당자의 파라미터 개선 실험 결과를 동일한 Validation 조건으로 비교하여 최종 알고리즘을 선정한다.
