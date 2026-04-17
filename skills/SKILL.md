---
name: tsg-agent
description: 5명의 전문 에이전트(총괄·이론·실험·논문편집·코드개발)가 협력해 LaTeX 논문의 이론적 정합성과 실험 재현성을 검증하고, 필요한 수정을 논문과 코드 양쪽에 반영합니다. "tsg-agent", "논문 재검증", "이론-재현성 검증", "paper-code 일치 검토" 등의 요청 시 사용합니다.
argument-hint: <paper-tex-path> <code-dir-path> [mode]
---

# TSG-Agent: 논문 검증·수정 5인 에이전트 팀

이론적 정합성(증명/정의/부호)과 실험 재현성(수치/코드 실행)을 병렬로 검증하고, 논문과 코드의 불일치를 발견·수정하는 파이프라인. SCIE 저널 투고 직전 최종 검증용.

---

## 팀 구성

| 에이전트 | 판단/실행 | 담당 파일 | 주 임무 | Prompt 파일 |
|---|---|---|---|---|
| **Orchestrator** | 판단 (총괄) | — | 분배·종합·승인·루프 제어 | (이 SKILL.md가 playbook) |
| **Theorist** | 판단 | `main.tex` (read) | 증명·정의·부호·cross-ref 검증 | `agents/theorist.md` |
| **Experimenter** | 판단 | `$CODE` (read+exec), `main.tex` (read) | 코드 실행, 수치 재현 확인 | `agents/experimenter.md` |
| **Editor** | 실행 | `main.tex` (write) | 논문 수정 적용 | `agents/editor.md` |
| **Developer** | 실행 | `$CODE` (write) | 코드 버그 수정, 재현성 강화 | `agents/developer.md` |

**판단-실행 분리 원칙**: 판단자(Theorist/Experimenter)는 파일 수정 금지. 실행자(Editor/Developer)는 판단·결정 금지. Orchestrator만 판단을 실행 지시로 변환.

---

## Arguments

- `$1` = 논문 `.tex` 파일 경로 (예: `~/TSG_paper/paper/main.tex`)
- `$2` = 코드 디렉토리 경로 (예: `~/TSG_paper/code/`)
- `$3` = 모드 (선택)
  - `full` (기본): 모든 Phase 실행, 전체 인스턴스 재현
  - `quick`: Phase 1–2만 (리포트만, 수정 없음)
  - `report-only`: Phase 1 병렬 분석만, 종합도 안 함

---

## Phase 0: 준비 및 스냅샷

Orchestrator가 먼저 실행:

1. **입력 검증**
   - `$1` 파일 존재 & `.tex` 확장자 확인
   - `$2` 디렉토리 존재 & 안에 Python 파일 존재 확인
   - 둘 다 실패하면 즉시 중단 + 사용자 안내

2. **Git 상태 확인** (논문·코드 각각)
   ```bash
   cd $(dirname $1) && git status --porcelain
   cd $2 && git status --porcelain
   ```
   - 미커밋 변경이 있으면 사용자에게 **"커밋 또는 stash 후 재실행"** 요청하고 중단
   - 이유: 에이전트 수정과 사용자의 기존 작업이 섞이면 롤백 불가능

3. **시작 태그 생성**
   ```bash
   TAG="tsg-agent-$(date +%Y%m%d-%H%M%S)"
   (cd $(dirname $1) && git tag $TAG)
   (cd $2 && git tag $TAG)
   ```

4. **작업 폴더 생성**
   ```bash
   WORKDIR="$(dirname $1)/tsg-agent-output-$(date +%Y%m%d-%H%M%S)"
   mkdir -p $WORKDIR
   ```

5. **사용자 확인**: 위 설정을 제시하고 **Phase 1 시작 승인** 요청

---

## Phase 1: 병렬 분석 (Theorist + Experimenter)

Task tool로 **동시 실행**. 각 에이전트는 자신의 prompt 파일을 읽고 수행.

### Theorist 호출

```
prompt = agents/theorist.md의 전체 내용
       + "\n\n## 작업 대상\n논문: $1\n작업 폴더: $WORKDIR"
model = sonnet
```

기대 산출물: `$WORKDIR/theorist_report.md`

### Experimenter 호출

```
prompt = agents/experimenter.md의 전체 내용
       + "\n\n## 작업 대상\n논문: $1\n코드: $2\n모드: $3\n작업 폴더: $WORKDIR"
model = sonnet
```

기대 산출물: `$WORKDIR/experimenter_report.md`, `$WORKDIR/reproducibility_report.md`

### 둘 다 완료까지 대기

- 둘 중 하나라도 FAILED 상태면 Orchestrator가 원인 파악, 사용자에게 보고 후 중단
- Experimenter가 "코드 실행 불가" 반환하면 Phase 1 중단 (Developer 먼저 호출해 환경 고쳐야 함)

---

## Phase 2: 종합 및 사용자 승인

Orchestrator(= 메인 Claude) 본인이 수행:

### 2-1. 두 리포트 병합

- `$WORKDIR/issue_log.md` 생성 (템플릿: `templates/issue_log.md`)
- Theorist 이슈 + Experimenter 이슈를 하나의 테이블로 통합
- 중복 이슈(같은 현상을 양쪽이 발견)는 병합

### 2-2. Paper-Code Consistency 직접 체크

Orchestrator만의 고유 임무 — Theorist와 Experimenter 어느 쪽도 단독으로 못 잡는 영역:

| 체크 항목 | 예시 |
|---|---|
| 알고리즘 명칭 일치 | 논문 "NN with insertion" ≠ 코드 `nn_only()` |
| 파라미터 값 일치 | 논문 "seeds {7, 42, 99, 123, 256}" vs 코드 `SEEDS` |
| 데이터 구조 일치 | 논문 $U_t$ 정의 vs 코드 `queue` 변수 의미 |
| 수치 집계 방식 | 논문 "weighted average" vs 코드 `mean()` (가중치 없음) |

발견된 불일치는 `issue_log.md`에 섹션 "Paper-Code Consistency (Orchestrator)"로 추가.

### 2-3. 심각도 분류

- 🔴 **CRITICAL**: 이론 오류(증명 틀림), 수치 재현 실패(편차 >1%), 논문 claim과 코드 동작이 근본 불일치
- 🟡 **MAJOR**: 서술 오류, 경미한 재현 편차(<1%), 암묵적 가정, 누락된 cross-ref
- 🟢 **MINOR**: 표기 사소한 불일치, 주석 누락, LaTeX 포맷

### 2-4. WBS 작성

`$WORKDIR/wbs.md` 생성 (템플릿: `templates/wbs.md`). 각 이슈에 대해:
- 작업 ID (예: `F-T1-001`은 논문 수정, `C-E1-001`은 코드 수정)
- 우선순위 및 의존 관계 (코드 수정 → 수치 재계산 → 논문 수정)
- 담당 에이전트 (Editor/Developer/양쪽)

### 2-5. **사용자 승인 게이트** (여기서 반드시 멈춤)

Orchestrator는 사용자에게 다음을 제시하고 **명시적 승인 대기**:

```
[TSG-Agent Phase 2 완료]

발견된 이슈: 🔴 N건 / 🟡 M건 / 🟢 K건
주요 발견:
  1. (CRITICAL) ...
  2. (CRITICAL) ...
  3. (MAJOR) ...

WBS: $WORKDIR/wbs.md

진행 옵션:
  [A] 전체 WBS 승인 → Phase 3 진행
  [B] CRITICAL만 수정
  [C] 개별 검토 (각 작업 확인 후 진행)
  [D] 중단 (리포트만 남기고 종료)
```

사용자 응답 없이 Phase 3 절대 진입 금지.

- `quick` 모드: Phase 2까지만 하고 Phase 3 안 감 (사용자가 직접 수정)
- `report-only` 모드: Phase 2도 생략, Phase 1 리포트만 전달

---

## Phase 3: 수정 루프 (사용자 승인 후)

WBS의 각 작업을 **CRITICAL → MAJOR → MINOR** 순으로. 동일 심각도 내에서는 의존 관계 따라.

### 3-1. 논문만 수정되는 경우

```
Orchestrator → Editor
  작업 지시 (str_replace old_str / new_str + 맥락 설명)
Editor → Orchestrator
  SUCCESS/FAILED + diff 리포트
```

Orchestrator는 diff를 **직접 view로 재확인**해서 의도대로 수정됐는지 검증.

### 3-2. 코드만 수정되는 경우

```
Orchestrator → Developer
  작업 지시 (버그 설명 + 수정 방향)
Developer → 수정 + smoke test
Developer → Orchestrator
  SUCCESS/FAILED + diff + 단위 검증 결과
```

### 3-3. 코드 수정 → 논문 수치 영향

```
Step 1: Orchestrator → Developer: 코드 수정
Step 2: Orchestrator → Experimenter: 영향받는 수치만 재계산
Step 3: Experimenter → Orchestrator: 새 수치 보고
Step 4: Orchestrator → Editor: 논문 수치를 Step 3 값으로 업데이트
Step 5: Orchestrator: diff 확인 + 로그
```

**중요**: Step 3의 새 수치가 논문과 크게 다르면(예: Table 주요 수치 변동), 사용자에게 **재승인 요청**.

### 3-4. 논문 vs 코드 불일치 (Paper-Code Consistency)

이 경우 Orchestrator가 단독 판단 불가 — **어느 쪽이 ground truth인지 사용자만 결정 가능**:

```
[불일치 보고]
이슈: C1
논문 서술 (line XXX): "nearest-neighbor-with-insertion"
코드 실제 구현 (dispatch.py): plain nearest neighbor

질문: 어느 쪽이 진짜입니까?
  [1] 논문이 맞음 → Developer가 코드를 논문에 맞춰 수정
  [2] 코드가 맞음 → Editor가 논문 서술을 코드에 맞춰 수정
  [3] 모르겠음 → Orchestrator가 원래 설계 의도 조사 후 재질문
```

---

## Phase 4: 최종 검증

모든 CRITICAL/MAJOR 처리 완료 후:

### 4-1. 컴파일 테스트
```bash
cd $(dirname $1)
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```
- 에러 0건 확인
- Warning (특히 `undefined reference`, `overfull hbox`) 체크

### 4-2. 간이 재검증

- **Theorist 재호출 (lightweight)**: 수정된 main.tex만 넘겨서 "새로 생긴 불일치 있는지" 확인
- **Experimenter spot-check**: 수정 후 핵심 수치 2–3개만 재계산해 여전히 일치하는지 확인

### 4-3. 실패 시 롤백

어떤 검증이든 실패하면:
1. 마지막 수정 diff 조사
2. 원인이 명확한 단일 수정이면 그것만 롤백 (`git checkout -- file` 또는 역 str_replace)
3. 원인 불명확 또는 복수 수정 얽힘 → Phase 0 태그로 전체 롤백:
   ```bash
   cd $(dirname $1) && git reset --hard $TAG
   cd $2 && git reset --hard $TAG
   ```
4. 사용자 보고 + 상세 로그

---

## Phase 5: 최종 보고

사용자에게 제공할 산출물:

```
$WORKDIR/
├── issue_log.md              # 전체 이슈 이력 + 처리 결과
├── reproducibility_report.md # 재현성 검증 테이블
├── wbs.md                    # 수정 계획 (승인 당시 버전)
├── final_summary.md          # 종합 보고서
├── theorist_report.md        # Theorist 원본 리포트
└── experimenter_report.md    # Experimenter 원본 리포트
```

`final_summary.md` 핵심 내용:
- Phase별 소요 시간
- 수정 통계 (논문 N건 / 코드 M건)
- 심각도별 해소 현황 (CRITICAL X/Y, MAJOR ...)
- 잔여 권고사항 (수정 안 한 이슈와 사유)
- 재현성 최종 상태 (PASS/PARTIAL/FAIL)
- 컴파일 결과 (페이지 수, warning 수)
- 사용자 수동 확인 필요 항목

---

## 실패·예외 처리

| 상황 | 조치 |
|---|---|
| Git repo 아님 | Phase 0에서 중단 + 사용자에게 `git init` 요청 |
| Python 환경 구성 실패 | Developer 호출해 setup 시도, 3회 실패 시 사용자 보고 |
| Experimenter가 기존 실험 결과 CSV 발견 | 재실행 vs CSV 신뢰 — 사용자 선택 |
| 이론 증명 자체가 틀렸음 (Theorist 🔴) | Phase 3 중단, 즉시 사용자 상의 (에이전트가 증명을 재작성하지 않음) |
| 컴파일 실패 반복 (3회 +) | 전체 롤백 + 사용자 보고 |
| Developer가 제안한 수정이 새 버그 유발 | 즉시 롤백, Orchestrator가 다른 접근 모색 또는 사용자 상의 |

---

## 중지 조건

정상 종료: 모든 CRITICAL 해소 & 컴파일 성공 & 재현성 PASS
비정상 종료: 사용자가 Phase 2에서 중단 선택, 롤백 필요 상황, 3회 연속 수정 실패

---

## 에이전트 Prompt 파일 참조

상세 지시는 각 파일에 있음. Orchestrator는 Task tool 호출 시 해당 파일 전체를 prompt로 전달:

- `agents/theorist.md` — 이론 검증 전문가
- `agents/experimenter.md` — 실험 재현성 전문가  
- `agents/editor.md` — 논문 수정 실행자
- `agents/developer.md` — 코드 수정 실행자

템플릿:

- `templates/issue_log.md`
- `templates/reproducibility_report.md`
- `templates/wbs.md`
