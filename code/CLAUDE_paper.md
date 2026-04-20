# Online TSG Paper - Transportation Science 제출 준비

## 현재 상태 (완료된 것)
논문 paper/main.tex이 완성되어 있음.
- 저자: Seyun Jeong, Hyunchul Tae (both at Korea Institute of Industrial Technology, KITECH)
- Related Work 4개 스트림
- Theorem 6, 11, 13, Corollary 14 + 증명
- Figure 1~5
- References 19개 (tae2020 포함)
- Example 4 Solomon C101 기반, 수치 검증 완료
- Conclusion Platform-design 단락 추가

## 폴더 구조
```
~/Documents/claude/TSG_paper/
  paper/
    main.tex          ← 완성된 논문
    references.bib    ← 완성된 참조
  figures/
  results/
  skills/
```

## 핵심 정의 (참조용)
- c(S): depot 출발 최적 TSP 비용 (시점 독립적)
- F: {S | S ⊆ U_t for some event t}
- r: C(N)_online / c*(N)
- r**: 1 + min_i δ_i / c*(N)
- k: max_t |U_t|

## 저자 정보
1저자: Seyun Jeong
  Korea Institute of Industrial Technology (KITECH)
  Cheonan, Republic of Korea
  Email: jeongsseyyun@kitech.re.kr

2저자: Hyunchul Tae (corresponding author)
  Korea Institute of Industrial Technology (KITECH)
  Cheonan, Republic of Korea
  Email: sage@kitech.re.kr

## Transportation Science 제출 요건
- 페이지: 본문+참조+표+그림 최대 35페이지
- Double-anonymous: 제출용 blind 버전 필요 (저자/소속 제거)
- 스타일: INFORMS Transportation Science 공식 템플릿
- 제출: ScholarOne (mc.manuscriptcentral.com/transci)

## 구현 원칙
- 개입 없이 끝까지 완성
- LaTeX 컴파일 에러 없어야 함
