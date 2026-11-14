
from pathlib import Path

import numpy as np
import soundfile as sf

from algorithms.wiener_filter import enhance


# 프로젝트 루트 경로
BASE_DIR = Path(__file__).resolve().parent

# 입력 및 출력 폴더
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

# 현재 Wiener Filter 지원 샘플링 주파수
EXPECTED_SAMPLE_RATE = 16000


def process_file(input_path: Path):
    """WAV 파일 하나를 읽어 Wiener Filter를 적용하고 저장한다."""

    # WAV 읽기: 항상 (samples, channels) 형태
    noisy, sample_rate = sf.read(
        input_path,
        dtype="float32",
        always_2d=True
    )

    # 현재 알고리즘의 샘플링 주파수 제한 확인
    if sample_rate != EXPECTED_SAMPLE_RATE:
        raise ValueError(
            f"지원하지 않는 샘플링 주파수: {sample_rate} Hz "
            f"(필요: {EXPECTED_SAMPLE_RATE} Hz)"
        )

    original_samples, original_channels = noisy.shape

    # Wiener Filter 적용
    enhanced = np.asarray(
        enhance(noisy, sample_rate=sample_rate)
    )

    # 출력 형태 정규화
    if enhanced.ndim == 1 and original_channels == 1:
        enhanced = enhanced.reshape(-1, 1)

    # 출력 검증
    if enhanced.ndim != 2:
        raise ValueError("출력 신호의 차원이 올바르지 않습니다.")

    if enhanced.shape[0] != original_samples:
        raise ValueError("입력과 출력의 샘플 수가 다릅니다.")

    if enhanced.shape[1] != original_channels:
        raise ValueError("입력과 출력의 채널 수가 다릅니다.")

    if not np.all(np.isfinite(enhanced)):
        raise ValueError("출력 신호에 NaN 또는 Inf가 포함되어 있습니다.")

    # 동일한 파일명으로 저장
    output_path = OUTPUT_DIR / input_path.name

    sf.write(
        output_path,
        enhanced,
        sample_rate
    )

    return output_path


def main():
    # 폴더 자동 생성
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # input 폴더의 WAV 파일 탐색
    wav_files = sorted(
        path for path in INPUT_DIR.iterdir()
        if path.is_file() and path.suffix.lower() == ".wav"
    )

    if not wav_files:
        print("처리할 WAV 파일이 없습니다.")
        print(f"테스트 WAV 파일을 다음 폴더에 넣어주세요: {INPUT_DIR}")
        return

    print(f"총 {len(wav_files)}개 WAV 파일 처리 시작")
    print("-" * 50)

    success_count = 0
    failure_count = 0

    for input_path in wav_files:
        try:
            output_path = process_file(input_path)

            success_count += 1
            print(f"[성공] {input_path.name} -> {output_path.name}")

        except Exception as error:
            failure_count += 1
            print(f"[실패] {input_path.name}: {error}")

    print("-" * 50)
    print(f"전체 파일: {len(wav_files)}개")
    print(f"성공: {success_count}개")
    print(f"실패: {failure_count}개")
    print(f"결과 저장 위치: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
