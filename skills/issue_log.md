# Issue Log

**대상 논문**: `<PAPER_PATH>`  
**대상 코드**: `<CODE_DIR>`  
**파이프라인 시작**: `YYYY-MM-DD HH:MM`  
**모드**: `full` / `quick` / `report-only`  
**Git 시작 태그**: `tsg-agent-YYYYMMDD-HHMMSS`

---

## 요약

| 심각도 | Theorist | Experimenter | Orchestrator (P-C) | 총 |
|---|---|---|---|---|
| 🔴 CRITICAL | 0 | 0 | 0 | **0** |
| 🟡 MAJOR | 0 | 0 | 0 | **0** |
| 🟢 MINOR | 0 | 0 | 0 | **0** |

**전반 판정**: EXCELLENT / GOOD / NEEDS_FIX / CRITICAL

---

## Theorist Issues (이론 검증)

| ID | 위치 | 심각도 | 이슈 | 증거 | 제안 수정 | 상태 |
|---|---|---|---|---|---|---|
| T1 |  |  |  |  |  | OPEN |

**상태 범례**: `OPEN` · `ASSIGNED` · `IN_PROGRESS` · `FIXED` · `DEFERRED` · `REJECTED`

---

## Experimenter Issues (실험 재현성)

| ID | 위치 | 심각도 | 이슈 | 증거 | 제안 조치 | 상태 |
|---|---|---|---|---|---|---|
| E1 |  |  |  |  |  | OPEN |

---

## Paper-Code Consistency Issues (Orchestrator 단독 검출)

이 섹션은 Theorist(논문만 봄)와 Experimenter(코드 돌림)가 **각자는** 볼 수 없는 영역. Orchestrator가 두 리포트를 대조해 만든 결과.

| ID | 논문 서술 (line) | 코드 구현 (파일:line) | 심각도 | 결정 | 상태 |
|---|---|---|---|---|---|
| C1 |  |  |  | pending-user |  |

**결정 범례**:
- `paper-correct`: 논문이 맞음 → Developer가 코드 수정
- `code-correct`: 코드가 맞음 → Editor가 논문 수정  
- `both-wrong`: 둘 다 문제 → 사용자·Orchestrator 상의
- `pending-user`: 사용자 결정 대기

---

## Actions Taken (시간순)

| 시각 | 작업 ID | 에이전트 | 대상 | 지시 요약 | 결과 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

---

## 재검증 로그 (Phase 4)

Phase 4에서 Theorist/Experimenter 재호출 결과:

| 시각 | 에이전트 | 재검증 범위 | 새 이슈 | 회귀 여부 |
|---|---|---|---|---|
|  |  |  |  |  |

---

## Deferred & Rejected

(수정 안 하기로 한 이슈 모음)

| ID | 심각도 | 이슈 | 보류·기각 사유 |
|---|---|---|---|
|  |  |  |  |

---

## 참고 문서

- Theorist 원본 리포트: `theorist_report.md`
- Experimenter 원본 리포트: `experimenter_report.md`
- 재현성 보고서: `reproducibility_report.md`
- WBS (수정 계획): `wbs.md`
- 최종 종합 보고: `final_summary.md`
