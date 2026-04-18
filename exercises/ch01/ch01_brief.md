---
marp: true
theme: default
paginate: true
backgroundColor: #F7F8FA
color: #1A1A2E
style: |
  section {
    font-family: 'Hiragino Sans', 'Meiryo', sans-serif;
    font-size: 22px;
  }
  h1 { color: #1E2E4A; border-bottom: 4px solid #E86A2C; padding-bottom: 8px; }
  h2 { color: #1E2E4A; }
  h3 { color: #2D4A7A; }
  section.title {
    background: #1E2E4A; color: #FFFFFF;
    text-align: center; justify-content: center;
  }
  section.title h1 { color: #FFFFFF; border-bottom: 4px solid #E86A2C; font-size: 40px; }
  section.title h2 { color: #E8C87A; font-size: 24px; }
  section.title p  { color: #BDC8D8; font-size: 18px; }
  table { border-collapse: collapse; width: 100%; font-size: 19px; }
  th { background: #1E2E4A; color: #FFF; padding: 8px 12px; }
  td { padding: 7px 12px; border-bottom: 1px solid #DDE3EE; }
  tr:nth-child(even) td { background: #EEF2F7; }
  blockquote {
    border-left: 5px solid #E86A2C; background: #FFF7F2;
    padding: 8px 16px; margin: 12px 0; font-style: normal; color: #1A1A2E;
  }
  code { background: #E8EDF2; padding: 2px 6px; border-radius: 4px; font-size: 16px; }
  pre  { background: #1E2E4A; color: #E8F0FF; padding: 14px; border-radius: 8px; font-size: 15px; }
---

<!-- _class: title -->

# Ch.1　データ読み込み・集計

## 演習ブリーフィング

使用データ：ワインデータ（`load_wine()`）178件・13特徴量・3品種  
演習ファイル：`exercises/ch01/ch1_data_analysis_student.ipynb`

---

# 今日作るもの

> **品種別・主要指標の集計表**

```
          alcohol   proline   flavanoids  ...
品種名
Barolo      ??.?    ????.?      ??.?
Grignolino  ??.?     ???.?      ??.?
Barbera     ??.?     ???.?      ??.?
```

集計して「**どの品種がどの変数で特徴的か**」を自分の言葉でまとめる。

### これは実務でいうと…

| 業界 | 対応するアウトプット |
|------|------------------|
| 小売・EC | カテゴリ別・地域別の月次売上集計表 |
| 製造 | ラインごとの生産量・不良率サマリー |
| マーケティング | 顧客セグメント別 KPI レポート |

> 「毎月 Excel で手作業していた集計」をコードで自動化したもの

---

# 演習の進め方（40分）

**対象ファイル：** `exercises/ch01/ch1_data_analysis_student.ipynb`

| # | やること | 難易度 | 目安 |
|---|---------|--------|------|
| 準備 | ライブラリ読み込み・データ読み込み | — | 5分 |
| データ確認 | `head` / `info` / `describe` / `isnull` の4点確認 | — | 5分 |
| **問1** | 品種ごとのデータ件数を確認する（`value_counts`） | ★☆☆ | 7分 |
| **問2** | 品種別の集計表を作る（`groupby`） | ★★☆ | 13分 |
| **問3** | 集計結果から考察する | ★★☆ | 10分 |
| 問4 | 条件でデータを絞り込む（発展） | ★★★ | 余り次第 |

> ✅ **問3まで完了すれば十分です。問4は時間が余った人向け**

---

# Copilot の使い方

**ブラウザで開く：** https://copilot.microsoft.com

### 質問テンプレート（コピーして使う）

```
【やりたいこと】品種ごとに alcohol と proline の平均を集計したい
【使うライブラリ】pandas
【データの形】178行・「品種名」列に Barolo/Grignolino/Barbera が入っている
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】groupby の書き方がわからない
```

詳しいテンプレート集 → `exercises/ch01/ch1_prompt_guide.md`

### 使うタイミング

| タイミング | ルール |
|-----------|--------|
| 問1〜2・問4（コード） | ✅ 積極的に使う |
| **問3（考察）** | ❌ **考察文は自分で書く** |

---

# よくあるエラーと対処

| エラー | 原因 | 対処 |
|--------|------|------|
| `KeyError: '列名'` | 列名のスペルミス・大文字小文字の違い | `df.columns` で正確な列名を確認する |
| `ValueError` AND条件 | 括弧が足りない | 各条件を `()` で囲む |
| `NameError: not defined` | 変数がまだ定義されていない | 上のセルから順に実行し直す |
| `SyntaxError` | 括弧・クォートの閉じ忘れ | Copilot に「構文エラーを直して」と依頼する |

---

<!-- _class: title -->

# では、始めてください 🚀

## `ch1_data_analysis_student.ipynb` を開いて  
## 上から順に実行してください

問3の考察まで完了を目指しましょう
