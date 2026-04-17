# WBS — Fix Plan

**생성 시각**: `YYYY-MM-DD HH:MM`  
**총 이슈**: N (🔴 a / 🟡 b / 🟢 c)  
**승인 상태**: `PENDING_USER_APPROVAL` / `APPROVED` / `PARTIAL_APPROVAL` / `REJECTED`

---

## 수정 원칙

1. **심각도 순**: 🔴 CRITICAL → 🟡 MAJOR → 🟢 MINOR
2. **의존 관계 존중**: 코드 수정 후 재계산, 그 결과로 논문 수정
3. **Atomic**: 한 작업 ID = 한 번의 논리적 변경
4. **Rollback-safe**: 각 작업은 독립적으로 되돌릴 수 있어야 함

---

## Priority 1: 🔴 CRITICAL

제출 전 반드시 해소. 하나라도 실패 시 파이프라인 중단.

| 순서 | 작업 ID | 이슈 요약 | 대상 파일 | 담당 | 의존 | 예상 소요 |
|---|---|---|---|---|---|---|
| 1 | F-T1-001 | Def 5 부호 convention 수정 | main.tex:226 | Editor | — | 1 edit |
| 2 | F-T2-002 | LP Eq.(1) "i.e." 부등식 수정 | main.tex:242-246 | Editor | #1 (선행) | 1 edit |
| 3 | C-E1-001 | NN+insertion 구현 불일치 | dispatch.py | Developer → Experimenter → Editor | — | 1 code + 1 rerun + 1 paper |

**작업 #3 세부**:
1. Developer: `dispatch.py`에 insertion step 추가
2. Experimenter: Table 7 NN 행 재계산
3. Editor: 논문 수치 (Abstract, Table 6, 7) 업데이트

---

## Priority 2: 🟡 MAJOR

가능하면 이번 라운드에서 처리. 못 하면 reviewer revision 때 대응.

| 순서 | 작업 ID | 이슈 요약 | 대상 | 담당 | 의존 |
|---|---|---|---|---|---|
| 4 | F-T3-003 | `thm:thm3` 라벨 개명 | main.tex (선언+참조) | Editor | — |
| 5 | F-E2-004 | 환경 README 재현 명령 보강 | README.md | Developer | — |
| ... | ... | ... | ... | ... | ... |

---

## Priority 3: 🟢 MINOR

시간 허용 시 처리. 선택적.

| 순서 | 작업 ID | 이슈 요약 | 대상 | 담당 |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

---

## 의존 관계 그래프

```
F-T1-001 (Def 5 부호)
   ↓
F-T2-002 (LP 부호) — #1과 일관성 보장

C-E1-001 (코드 수정)
   ↓
(Experimenter 재계산)
   ↓
F-C1-001-EDIT (논문 수치 업데이트)

F-T3-003 (라벨 개명) — 독립
F-E2-004 (README) — 독립
```

---

## 사용자 결정 필요 항목

WBS 승인 전 사용자 입력이 필요한 이슈:

| ID | 이슈 | 옵션 | 기본 권장 |
|---|---|---|---|
| C1 | 논문 vs 코드 불일치 (NN+insertion) | [A] 논문이 맞음 → 코드 수정 / [B] 코드가 맞음 → 논문 수정 / [C] 조사 필요 | pending |
| E-ENV-1 | requirements.txt에 scipy 버전 pin 추가 | [A] 승인 / [B] 거부 | pending |

---

## 예상 결과

이 WBS 전체 실행 시:

| 지표 | 현재 | 실행 후 예상 |
|---|---|---|
| 🔴 이슈 | N | 0 |
| 🟡 이슈 | M | K |
| 논문 수정 라인 | — | ~X 라인 |
| 코드 수정 라인 | — | ~Y 라인 |
| 논문 수치 변동 | — | Abstract 2개, Table 2개 |
| 재현성 | PARTIAL | PASS |

---

## 사용자 승인

이 WBS로 Phase 3 수정 루프를 진행하시겠습니까?

- [ ] **[A] 전체 승인** — WBS 전체 순차 실행
- [ ] **[B] CRITICAL만 진행** — 🔴 만 처리하고 나머지는 보류
- [ ] **[C] 개별 검토** — 각 작업 직전마다 확인 후 진행
- [ ] **[D] 중단** — 리포트만 남기고 종료

**사용자 메모** (옵션): 

```
(예: "C1 이슈는 논문이 정답입니다. F-T3-003 라벨 개명은 건너뛰세요.")
```

---

## 승인 후 진행 로그

(Phase 3 진행 시 작업 순서대로 실시간 기록)

| 시각 | 작업 ID | 상태 | 결과 요약 |
|---|---|---|---|
|  |  |  |  |
