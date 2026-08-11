# ⭐ 원신 캐릭터 빌드 뷰어

원신 **올인원 준종결표 (ver 6.7)** 스프레드시트를 캐릭터별로 보기 좋게 정리한 반응형 웹 뷰어입니다.

🔗 **라이브:** https://hyuking97.github.io/Genshin/

## 기능

- **캐릭터 뷰** — 권장 레벨/특성, 역할군, 성유물, 주 옵션(시계·성배·왕관), 부옵션, 추천 무기별 권장 스탯, 비고
- **무기 뷰** — 무기를 고르면 그 무기를 쓰는 캐릭터 전원과 각자의 권장 스탯 표시
- **검색** — 부분검색 · 초성(`ㅁㅂㅋ`) · 영타(`akqlzk`) · 영문명(`mavuika`) 모두 실시간 지원
- **원소 필터** — 불/물/얼음/번개/바람/바위/풀
- **반응형 + 라이트/다크 모드**, 캐릭터 아이콘·원소 정보 임베드 (외부 통신 없이 동작)

## 파일 구성

| 파일 | 설명 |
|------|------|
| `index.html` | 완성된 자립형 사이트 (모든 데이터·이미지 임베드) |
| `sheet.csv` | 원본 스프레드시트 데이터 (CSV) |
| `parse.py` | CSV → 구조화 JSON (`data.json`) |
| `fetch_images.py` | 캐릭터 아이콘·원소·영문명·페이몬 아이콘 수집 (`images.json`, `paimon.json`) |
| `fetch_weapons.py` | 무기 아이콘·희귀도 수집 (`weapons.json`) |
| `build_site.py` | 위 데이터로 `index.html` 생성 |

## 다시 빌드하기

```bash
pip install Pillow
python parse.py          # sheet.csv -> data.json
python fetch_images.py   # 캐릭터 아이콘/원소/영문명 -> images.json, paimon.json
python fetch_weapons.py  # 무기 아이콘 -> weapons.json
python build_site.py     # -> genshin-build.html
cp genshin-build.html index.html
```

> `fetch_images.py`, `fetch_weapons.py`는 네트워크가 필요합니다(아이콘·API).

## 출처 / 참고

- 데이터: **원신 올인원 준종결표 ver. LUNA VIII (6.7)** — 제작자의 주관적 의견이 포함되어 참고용입니다.
- 캐릭터 아이콘 · 원소 · 영문명: [Project Amber (ambr.top)](https://ambr.top)
- 스프레드시트를 자동 변환한 것으로 일부 표기가 원본과 다를 수 있습니다.
