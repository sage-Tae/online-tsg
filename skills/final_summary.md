# TSG-Agent Final Summary

**대상 논문**: `<PAPER_PATH>`  
**대상 코드**: `<CODE_DIR>`  
**파이프라인 실행**: `YYYY-MM-DD HH:MM` — `YYYY-MM-DD HH:MM` (총 X분)  
**모드**: `full` / `quick` / `report-only`  
**최종 상태**: `SUCCESS` / `PARTIAL_SUCCESS` / `ABORTED`

---

## 한 줄 결론

(예: "10건의 이슈 발견 중 CRITICAL 3건·MAJOR 4건 해소, MINOR 3건 보류. 재현성 PASS, 컴파일 통과. EJOR 제출 가능 상태.")

---

## Phase별 소요 시간

| Phase | 설명 | 시작 | 종료 | 소요 | 상태 |
|---|---|---|---|---|---|
| 0 | 준비·스냅샷 | HH:MM | HH:MM | ~1분 | ✓ |
| 1 | 병렬 분석 (Theorist+Experimenter) | HH:MM | HH:MM | ~X분 | ✓ |
| 2 | 종합·사용자 승인 | HH:MM | HH:MM | ~Y분 | ✓ |
| 3 | 수정 루프 | HH:MM | HH:MM | ~Z분 | ✓ |
| 4 | 최종 검증 | HH:MM | HH:MM | ~W분 | ✓ |
| 5 | 보고 | HH:MM | HH:MM | ~1분 | ✓ |

---

## 이슈 처리 현황

### 심각도별
| 심각도 | 발견 | 해소 | 보류 | 기각 |
|---|---|---|---|---|
| 🔴 CRITICAL | 3 | 3 | 0 | 0 |
| 🟡 MAJOR | 4 | 3 | 1 | 0 |
| 🟢 MINOR | 3 | 1 | 2 | 0 |
| **합계** | **10** | **7** | **3** | **0** |

### 출처별
| 출처 | 발견 | 해소 |
|---|---|---|
| Theorist (이론) | N | N |
| Experimenter (재현) | M | M |
| Orchestrator (P-C consistency) | K | K |

---

## 수정 이력 (주요 항목)

### 논문 수정 (`main.tex`)
| 작업 ID | 위치 | 변경 요약 |
|---|---|---|
| F-T1-001 | line 226 | Def 5 excess: benefit → cost convention |
| F-T2-002 | line 242–246 | LP 부등식 일관성 |
| F-T3-003 | label + refs | `thm:thm3` → `thm:core-inheritance` |
| ... | ... | ... |

### 코드 수정 (`$CODE_DIR`)
| 작업 ID | 파일 | 변경 요약 |
|---|---|---|
| C-E1-001 | dispatch.py | NN+insertion step 추가 |
| C-E3-002 | run_experiments.py | seed propagation 명시 |
| ... | ... | ... |

### 수치 변화 (논문)
| 위치 | Before | After | 이유 |
|---|---|---|---|
| Abstract $\bar r^{\ast\ast}$ | 1.344 | 1.356 | NN+insertion 반영 후 재계산 |
| Table 7 NN Empty count | 19 | 21 | 동일 |
| ... | ... | ... | ... |

**사용자 주의**: 수치 변화가 있는 항목은 논문 제출 전 **수동 검토** 권장.

---

## 재현성 최종 상태

- 수치 재현 성공률: **X/Y (%)**
- Paper-code alignment: **PASS / MINOR_MISMATCH / MAJOR_MISMATCH**
- 동일 seed 재현 일치: **PASS / FAIL**

상세: `reproducibility_report.md`

---

## 컴파일 결과

| 항목 | 값 |
|---|---|
| Errors | 0 |
| Warnings | 0 / N |
| Undefined references | 0 |
| Overfull hbox | 0 |
| 페이지 수 | 23 |
| 파일 크기 | 264 KB |

컴파일 로그: `$WORKDIR/exp_logs/final_compile.log`

---

## 잔여 권고 (수정 안 한 항목)

### 보류 (DEFERRED)
| ID | 이슈 | 보류 사유 | 사용자 조치 |
|---|---|---|---|
| M-E4-007 | Appendix Figure 5 caption 문구 | MINOR, 시간 제약 | 선택적 수동 수정 |
| ... | ... | ... | ... |

### 사용자 수동 확인 필요
| 항목 | 이유 |
|---|---|
| CRediT author statement | 실제 기여도 재확인 필요 |
| `[REPOSITORY_URL_PLACEHOLDER]` | 실제 GitHub/OSF URL로 교체 |
| Cover letter | 본 파이프라인은 건드리지 않음 |
| Bibliography 2024–2025년 항목 | arXiv → published 상태 최신화 |

---

## Git 상태

### 시작 시점
- 논문: `tsg-agent-YYYYMMDD-HHMMSS` 태그
- 코드: `tsg-agent-YYYYMMDD-HHMMSS` 태그

### 변경 후 Commit 제안
```bash
cd $(dirname $PAPER)
git add main.tex
git commit -m "tsg-agent: N개 이슈 수정 (CRITICAL A건, MAJOR B건)"

cd $CODE_DIR
git add .
git commit -m "tsg-agent: 코드 정합성 개선 (C-E1-001, C-E3-002)"
```

### 롤백 방법 (문제 발견 시)
```bash
cd $(dirname $PAPER) && git reset --hard tsg-agent-YYYYMMDD-HHMMSS
cd $CODE_DIR && git reset --hard tsg-agent-YYYYMMDD-HHMMSS
```

---

## 산출물 목록

```
$WORKDIR/
├── issue_log.md              ← 모든 이슈 이력 + 처리 결과
├── reproducibility_report.md ← 재현성 검증 상세
├── wbs.md                    ← 수정 계획 (승인 당시)
├── final_summary.md          ← 이 문서
├── theorist_report.md        ← Theorist 원본
├── experimenter_report.md    ← Experimenter 원본
└── exp_logs/                 ← 실행 로그 (install, smoke, rerun 등)
    ├── install.log
    ├── smoke.log
    ├── table4_6.csv
    ├── table7_*.csv
    ├── table8_scaleup.csv
    └── final_compile.log
```

---

## 파이프라인 평가 (자체)

- 에이전트 협업 부드러움: GOOD / OK / ROUGH
- Orchestrator 개입 빈도: LOW (루틴) / MEDIUM / HIGH (판단 필요 많음)
- 사용자 개입 횟수: N회 (승인 게이트, P-C consistency 결정 등)

**개선 제안** (다음 실행 시):
- (있으면 기록)
