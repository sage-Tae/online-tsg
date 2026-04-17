# Online TSG Research - Theory Validation Session

## 한 줄 요약
Online TSG의 이론 결과(Theorem 5, Lemma 5.1/5.2, Corollary 5.1/5.2)를
실험으로 수치 검증한다.

---

## 핵심 정의

### c(S): Coalition Cost (시점 독립적)
```
c(S) = depot(0,0) 출발, S만 방문하는 최적 TSP 비용
       earlyTime_i = arrival_time_i 반영
       S가 같으면 항상 동일한 값
```

### F: Feasible Coalition 집합
```
F = {S | S ⊆ U_t for some event t}
  = 운행 중 어느 시점에 동시에 대기했던 고객 집합들
```

### CW(S): Concurrent Waiting Interval
```
CW(S) = ∩_{i∈S} [arrival_time_i, serve_time_i)
       = S의 모든 고객이 동시에 대기 중인 시간 구간

S ∈ F  ↔  CW(S) ≠ ∅
```

### δ_i: Subadditivity Gap
```
δ_i = c({i}) + c(N\{i}) - c*(N)
    = 고객 i의 대연합 비용 절감 기여도
    (작을수록 i가 tour에 기여를 적게 함)
```

### r, r*, r**: Competitive Ratio 관련
```
c*(N)  = depot 출발 최적 TSP 비용 (Static)
C(N)   = Online TSP 알고리즘 실제 비용

r      = C(N) / c*(N)          (실제 competitive ratio)
r*     = ∑c({i}) / c*(N)       (Theorem 2 임계값, 느슨함)
r**    = 1 + min_i δ_i / c*(N) (Theorem 5 임계값, 타이트함)
```

### k: 최대 동시 대기 고객 수
```
k = max over all events t of |U_t|
  = 운행 중 가장 많은 고객이 동시에 대기한 수
```

---

## 증명된 이론 결과

### Theorem 5 (Core 소멸 충분조건)
```
C(N)_online > c*(N) + min_i δ_i  →  Core = ∅

동치: r > r** = 1 + min_i δ_i / c*(N)  →  Core = ∅

증명 핵심:
  i* = argmin_i δ_i 로 놓으면
  Core ≠ ∅ 가정 시:
    y_{i*} ≤ c({i*})              (IR)
    y(N\{i*}) ≤ c(N\{i*})         (coalition rationality, N\{i*} ∈ F 필요)
    y(N\{i*}) = C(N) - y_{i*}     (efficiency)
  → C(N) ≤ c({i*}) + c(N\{i*}) = c*(N) + δ_{i*} 모순
```

### Lemma 5.1 (N\{i} ∈ F 동치조건)
```
N\{i} ∈ F  ↔  CW(N\{i}) ≠ ∅
           ↔  max_{j≠i} arrival_time_j < min_{j≠i} serve_time_j

즉: i를 제외한 모든 고객 중
    마지막 도착자가 첫 서비스 완료자보다 먼저 도착해야 함
```

### Lemma 5.2 (완전 순차 도착)
```
Definition: 완전 순차 도착
  serve_time_{π_k} < arrival_time_{π_{k+1}} for all k
  (다음 고객이 도착하기 전에 현재 고객이 서비스 받음)

Lemma 5.2:
  완전 순차 도착 → N\{i} ∉ F for all i
```

### Corollary 5.1
```
완전 순차 도착 → Theorem 5에 의한 Core 소멸 없음
(N\{i*} ∉ F이므로 Step 3 성립 안 함)
```

### Corollary 5.2 (k-순차 일반화)
```
k = max_t |U_t|  (최대 동시 대기 고객 수)

k < n-1  →  N\{i} ∉ F for all i
          →  Theorem 5 발동 안 됨
          →  Core 안전
```

---

## 검증할 것 (4가지)

### 검증 1: Lemma 5.1
```
모든 S에 대해:
  CW(S) 계산: max(arrival_times) < min(serve_times) 확인
  S ∈ F 여부와 일치하는지 확인
  → 일치율 100% 이어야 함
```

### 검증 2: Lemma 5.2
```
완전 순차 도착 인스턴스 (패턴 B, interval=5):
  serve_time_{π_k} < arrival_time_{π_{k+1}} 확인
  N\{i} ∉ F for all i 확인
  → 일치율 100% 이어야 함
```

### 검증 3: Theorem 5
```
각 인스턴스마다:
  δ_i = c({i}) + c(N\{i}) - c*(N) 계산
  min_i δ_i, r** 계산
  C(N) > c*(N) + min_i δ_i → Core = ∅ 예측
  실제 Core 여부와 비교
  → 충분조건이므로 예측=Empty이면 실제도 Empty
    (역은 성립 안 해도 됨)
```

### 검증 4: Corollary 5.2
```
각 인스턴스의 k 계산
k < n-1 → Core 안전 예측
실제 Core 여부와 비교
```

---

## 프로젝트 구조
```
TSG_experiment/
├── CLAUDE.md           ← 이 파일
├── src/
│   ├── simulator.py    ← 기존 (이미 구현됨)
│   ├── tsp.py          ← 기존 (이미 구현됨)
│   ├── nucleolus.py    ← 기존 (이미 구현됨)
│   └── metrics.py      ← 기존 (이미 구현됨)
├── experiments/
│   ├── run_all.py      ← 기존 (이미 실행됨)
│   └── validate_theory.py  ← 새로 만들 것
├── results/
│   ├── summary.csv     ← 기존 결과
│   └── theorem5_validation.csv  ← 새로 저장
└── skills/
    └── validate-theory.md
```

---

## 구현 원칙
- 기존 src/ 코드 재사용
- results/summary.csv의 인스턴스 그대로 사용
- 에러 발생 시 errors.log 기록 후 계속
- 개입 없이 끝까지 실행
