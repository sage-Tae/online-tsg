# Reproducibility Report

**대상 논문**: `<PAPER_PATH>`  
**대상 코드**: `<CODE_DIR>`  
**재현 수행일**: `YYYY-MM-DD HH:MM`  
**모드**: `full` / `quick`  
**수행자**: Experimenter Agent

---

## 1. 환경

| 항목 | 값 |
|---|---|
| Python 버전 | 3.X.X |
| OS / Arch | Linux Ubuntu 24 / x86_64 |
| 설치 로그 | `$WORKDIR/exp_logs/install.log` |
| venv 경로 | `$WORKDIR/venv` |

### 주요 의존성
| 패키지 | 버전 | 필수/선택 |
|---|---|---|
| numpy |  | 필수 |
| scipy |  | 필수 |
| elkai |  | 선택 (LKH wrapper, n>20 실험에만) |
| ... |  |  |

### Seed 정책 관찰
- Seeds found in config: `{...}`
- Seed propagation: `explicit` / `implicit` / `missing`
- 동일 seed 2회 실행 완전 일치 여부: **PASS / FAIL**

---

## 2. 수치 재현 결과

### 2-1. Abstract & 요약 수치

| 주장 | 논문 값 | 재현 값 | Δ 절대 | Δ % | 상태 |
|---|---|---|---|---|---|
| $\bar r^{\ast\ast}$ | 1.344 | 1.3437 | 0.0003 | 0.02% | ✓ |
| $\bar r^{\ast}$ | 4.351 |  |  |  |  |
| 배수 (sharpness factor) | 3.24 |  |  |  |  |
| 12/12 empty prediction | 12 |  |  |  |  |
| 95/95 structural safeguard | 95 |  |  |  |  |

### 2-2. Table 단위 재현

#### Table 4 (Theorem 11 Contingency — 66 applicable)
| Cell | 논문 | 재현 | Δ | 상태 |
|---|---|---|---|---|
| Pred empty ∩ Obs empty | 12 |  |  |  |
| Pred empty ∩ Obs nonempty | 0 |  |  |  |
| Not pred ∩ Obs empty | 7 |  |  |  |
| Not pred ∩ Obs nonempty | 47 |  |  |  |

#### Table 6 (Pattern-level, 25 instances each)
| Pattern | 논문 $\bar r$ (sd) | 재현 $\bar r$ (sd) | 논문 $\bar r^{\ast\ast}$ (sd) | 재현 $\bar r^{\ast\ast}$ (sd) | 상태 |
|---|---|---|---|---|---|
| A | 1.125 (0.102) |  | 1.181 (0.059) |  |  |
| B1 | 1.286 (0.146) |  | 1.528 (0.124) |  |  |
| B2 | 1.312 (0.163) |  | 1.691 (0.064) |  |  |
| B5 | 1.808 (0.328) |  | --- |  |  |
| C | 1.199 (0.149) |  | 1.363 (0.169) |  |  |
| D | 1.415 (0.188) |  | --- |  |  |
| E | 1.370 (0.208) |  | 1.606 (0.043) |  |  |
| Overall | 1.359 (0.281) |  | 1.344 (0.194) |  |  |

#### Table 7 (Dispatch Policy Robustness, 525 policy-instance pairs)
| Policy | 논문 $\bar r$ | 재현 $\bar r$ | Core rate 논문 | Core rate 재현 | Empty 논문 | Empty 재현 | 상태 |
|---|---|---|---|---|---|---|---|
| NN | 1.359 |  | 0.891 |  | 19 |  |  |
| CI | 1.276 |  | 0.977 |  | 4 |  |  |
| BR | 1.257 |  | 1.000 |  | 0 |  |  |

#### Table 8 (Scale-up, 45 instances)
| Pattern | n | 논문 Core rate | 재현 | 논문 $\bar r$ | 재현 | 상태 |
|---|---|---|---|---|---|---|
| A | 20 | 0/5 |  | 1.167 |  |  |
| A | 30 | 0/5† |  | 1.187 |  |  |
| A | 50 | 0/5† |  | 1.211 |  |  |
| B2 | 20 | 5/5 |  | 1.762 |  |  |
| B2 | 30 | 5/5 |  | 1.804 |  |  |
| B2 | 50 | 5/5 |  | 2.128 |  |  |
| C | 20 | 0/5 |  | 1.335 |  |  |
| C | 30 | 0/5 |  | 1.282 |  |  |
| C | 50 | 0/5 |  | 1.282 |  |  |

### 2-3. 재현 요약 통계
- 시도한 수치: **N** 개
- 완벽 일치 (Δ<0.001): **X** 개
- 경미 편차 (Δ<1%): **Y** 개
- 심각 편차 (Δ≥1%): **Z** 개
- 재현 불가 (실행 에러): **W** 개

---

## 3. Paper-Code Alignment (후보 목록)

Experimenter는 중립 관찰만. 최종 판정은 Orchestrator.

| 논문 claim (line) | 코드 관찰 (파일:line) | Experimenter 코멘트 |
|---|---|---|
| "nearest-neighbor-with-insertion heuristic" (§6.1, line 420) | `dispatch.py:nn()` | insertion step 발견되지 않음. 불일치 후보 |
| "LKH heuristic via elkai" (§6.8, line 569) | `tsp.py:solve_tsp()` | `elkai.solve_int_matrix` 호출 확인. 일치 |
| "seeds {7,42,99,123,256}" (§6.1 Table 3) | `config.py:SEEDS` | `[7, 42, 99, 123, 256]` 확인. 일치 |

---

## 4. Runtime

| 항목 | 값 |
|---|---|
| 총 재현 소요 | X 분 |
| 인스턴스당 평균 | Y 초 |
| 가장 느린 실행 | Z 분 (Pattern A, n=50, seed=42) |
| 병렬 활용 | No / Yes (worker=N) |

---

## 5. Anomalies & Notes

- 이상 현상 관찰 사례 (없으면 "None")
- 시드를 바꿨을 때 특이한 변동 (예: seed=99에서 empty Core 1건 추가 발견)
- 환경 관련 주의점

---

## 6. 재현 실행 명령어 (완전 기록)

```bash
# 환경 구성
cd $CODE_DIR
python3 -m venv $WORKDIR/venv
source $WORKDIR/venv/bin/activate
pip install -r requirements.txt

# Table 4, 6 재현
python run_experiments.py \
  --patterns A B1 B2 B5 C D E \
  --sizes 5 7 10 12 15 \
  --seeds 7 42 99 123 256 \
  --policy nn \
  --output $WORKDIR/exp_logs/table4_6.csv

# Table 7 재현 (3개 정책)
for policy in nn ci br; do
  python run_experiments.py \
    --patterns A B1 B2 B5 C D E \
    --sizes 5 7 10 12 15 \
    --seeds 7 42 99 123 256 \
    --policy $policy \
    --output $WORKDIR/exp_logs/table7_${policy}.csv
done

# Table 8 scale-up
python run_experiments.py \
  --patterns A B2 C \
  --sizes 20 30 50 \
  --seeds 7 42 99 123 256 \
  --policy nn \
  --tsp_solver lkh \
  --output $WORKDIR/exp_logs/table8_scaleup.csv
```

---

## 7. 재현성 판정

**최종 판정**: **PASS** / **PARTIAL** / **FAIL**

판정 근거:
- (수치 대조 통계에 기반한 결론)
- (환경·seed 일관성)
- (Paper-code 주요 불일치 존재 여부)

**Orchestrator 후속 조치 제안**:
- 🔴 CRITICAL 이슈: 즉시 Developer/Editor 개입 필요
- 🟡 MAJOR 이슈: WBS에 포함
- 🟢 MINOR 이슈: 선택적 처리
