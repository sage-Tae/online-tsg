# tsg-agent

LaTeX 논문의 **이론적 정합성**과 **실험 재현성**을 5-에이전트 팀으로 검증·수정하는 Claude skill.

---

## 무엇을 하는가

논문 `.tex` 파일 + 실험 코드 디렉토리를 받아서:

1. **Theorist** — 증명·정의·부호 convention 검증
2. **Experimenter** — 코드를 실제로 돌려서 논문 수치 재현 확인
3. **Orchestrator** (메인 Claude) — 두 결과 종합 + 논문↔코드 일치성 독자 검사 + 수정 계획 수립
4. **Editor** — Orchestrator 지시에 따라 논문 수정 실행
5. **Developer** — Orchestrator 지시에 따라 코드 수정 실행

**판단-실행 분리**: 판단자(Theorist/Experimenter)는 파일 수정 금지. 실행자(Editor/Developer)는 판단 금지. Orchestrator만 판단을 실행 지시로 변환.

---

## 폴더 구조

```
tsg-agent/
├── SKILL.md                        ← 진입점 + Orchestrator playbook
├── README.md                       ← 이 문서
├── agents/
│   ├── theorist.md                 ← 이론 검증 전문가 프롬프트
│   ├── experimenter.md             ← 실험 재현 전문가 프롬프트
│   ├── editor.md                   ← 논문 수정 실행자 프롬프트
│   └── developer.md                ← 코드 수정 실행자 프롬프트
└── templates/
    ├── issue_log.md                ← 이슈 로그 템플릿
    ├── reproducibility_report.md   ← 재현성 보고 템플릿
    ├── wbs.md                      ← 수정 계획 템플릿
    └── final_summary.md            ← 최종 종합 보고 템플릿
```

---

## 설치 (사용자용)

이 폴더 전체를 다음 위치에 복사:

```bash
cp -r tsg-agent ~/.claude/skills/
```

또는 프로젝트 로컬 스킬로:
```bash
mkdir -p <project>/.claude/skills/
cp -r tsg-agent <project>/.claude/skills/
```

---

## 사용법

Claude Code 또는 Claude Desktop에서 다음 중 하나 입력:

```
tsg-agent /path/to/paper/main.tex /path/to/code/
```

또는 trigger 문구:
```
논문 재검증 해줘: 논문 /path/to/main.tex, 코드 /path/to/code/
```

모드 지정:
```
tsg-agent /path/to/main.tex /path/to/code/ quick
tsg-agent /path/to/main.tex /path/to/code/ report-only
```

### 모드 옵션
| 모드 | Phase 1 | Phase 2 | Phase 3 (수정) | Phase 4 (재검증) | 권장 상황 |
|---|---|---|---|---|---|
| `full` (기본) | ✓ | ✓ | ✓ | ✓ | 제출 직전 전체 검증 |
| `quick` | ✓ | ✓ | ✗ | ✗ | 이슈 목록만 받아서 직접 수정 |
| `report-only` | ✓ | ✗ | ✗ | ✗ | 초기 상태 진단만 |

---

## 사전 준비 (필수)

파이프라인 실행 전 다음을 확인:

1. **Git 관리**: 논문·코드 둘 다 git repo. 미커밋 변경 없어야 함 (스냅샷·롤백을 위해).
2. **코드 실행 가능성**: README가 있고 `requirements.txt` 혹은 `environment.yml`로 환경 재현 가능해야 함.
3. **논문 컴파일 가능성**: `pdflatex + bibtex`로 컴파일되는 상태여야 함.
4. **실행 시간 여유**: `full` 모드는 실험 규모에 따라 수 분 ~ 수 시간 소요.

---

## 주요 안전장치

- **Phase 0 git 태그**: 시작 시점 스냅샷. 언제든 롤백 가능.
- **Phase 2 사용자 승인 게이트**: 수정 시작 전 WBS 검토 후 명시적 승인.
- **Phase 4 재검증**: 수정 후 Theorist/Experimenter 재호출해 회귀 검사.
- **Paper-code 불일치는 사용자 결정 필수**: Orchestrator 독단 금지.
- **Developer 수정 후 항상 smoke test**: 실패 시 즉시 롤백.

---

## 언제 쓰면 좋은가

- 🎯 SCIE 저널 투고 **직전**: 최종 기술 rigor 점검
- 🎯 Major revision 준비 중: reviewer 공격점 선제 해결
- 🎯 새로 구현한 이론 결과의 코드 정합성 확인
- 🎯 공동 저자가 작성한 부분의 논문-코드 정렬 검토

---

## 언제 쓰지 말아야 하나

- ❌ 논문을 **처음부터 쓰는** 단계 → `latex-paper` skill 사용
- ❌ 문체·영어만 다듬고 싶은 경우 → `paper-polish` 또는 `polishing-paper-team`
- ❌ 코드가 아직 완성되지 않은 상태 (재현할 수치가 없음)
- ❌ Git으로 관리하지 않는 코드 (롤백 불가 → 위험)

---

## 참고

- 관련 스킬: `paper-polish` (단일 파이프라인 교정), `polishing-paper-team` (5명 병렬 리뷰, 주로 문체·구조·인용)
- 차별점: `tsg-agent`는 **코드 실행 + 논문↔코드 정렬 검증**이 핵심. 다른 스킬은 논문만 본다.

---

## 버전

- v1.0 — 초기 설계 (5 에이전트 구조 확정)
