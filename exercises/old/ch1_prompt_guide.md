# Ch.1 ブラウザ版AI プロンプトガイド

> **使い方：** JupyterLab を左画面、ブラウザ版AIを右画面に並べて作業してください。  
> プロンプトをコピー＆ペーストして、AIに質問してください。

| ツール | URL |
|--------|-----|
| Microsoft Copilot | https://copilot.microsoft.com |
| ChatGPT | https://chat.openai.com |

---

## AIを使う「型」── 必ずこの形式で質問する

```
【やりたいこと】〇〇したい
【使うライブラリ】pandas / numpy など
【データの形】DataFrame で列名は〇〇、行数は〇〇件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】〇〇の書き方がわからない / 〇〇でエラーが出た
```

> 💡 **なぜこの型か：** AIへの質問は「文脈」が命です。  
> 「エラーが出た」だけでは答えが返せません。  
> 「どんなデータで・何をしようとして・どんなエラーか」をセットで伝えると、精度が上がります。

---

## AIを使うタイミングのルール

| タイミング | ルール |
|-----------|--------|
| 座学中 | ❌ **禁止** ― まず自分の頭で概念を理解する |
| 演習 問1〜2（コード） | ✅ **積極的に使う** ― 下のプロンプト例を活用 |
| 演習 問3（考察） | ✅ コードの質問はOK / **考察文は必ず自分で書く** |
| エラーが出たとき | ✅ **すぐ使ってOK** ― エラーメッセージごとコピーして質問する |

---

## P1-1｜データの形・欠損値を確認する

### 基本確認（head / info / describe）

```
【やりたいこと】pandasのDataFrameの基本情報を確認したい
【使うライブラリ】pandas
【データの形】DataFrame で178行、15列（float列とint列が混在）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】head() / info() / describe() の違いと使い分けを教えてほしい
```

### 欠損値の確認と処理

```
【やりたいこと】pandasで欠損値がある列を特定して、平均値で補完したい
【使うライブラリ】pandas
【データの形】DataFrame で各列の欠損件数を isnull().sum() で確認済み
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】fillna(mean()) の使い方と、列ごとに適用する方法を教えてほしい
```

### データ型が想定と違う場合

```
【やりたいこと】DataFrameの列の型を変換したい（object型を数値型に）
【使うライブラリ】pandas
【データの形】df.info()でDtypeがobjectになっている列がある
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】pd.to_numeric() を使う方法と、変換できない値がある場合の対処法
```

---

## P1-2｜品種ごとに件数を数える（value_counts）

### 基本的な使い方

```
【やりたいこと】pandasのDataFrameで品種列の値ごとに件数を集計して表示したい
【使うライブラリ】pandas
【データの形】DataFrameで「品種名」列が Barolo / Grignolino / Barbera の文字列、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】value_counts() の基本的な使い方と、結果を割合（%）で表示する方法
```

### 実務での応用例（自分の業務に当てはめて質問する場合）

```
【やりたいこと】pandasで「商品カテゴリ」ごとの件数と全体に占める割合を集計したい
【使うライブラリ】pandas
【データの形】DataFrame で「category」列が文字列、1000件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】value_counts(normalize=True) で割合を出す方法と、パーセント表示にする方法
```

---

## P1-3｜品種ごとに平均を集計する（groupby）

### 1列の集計

```
【やりたいこと】pandasのgroupbyで品種ごとのアルコール度数の平均を計算したい
【使うライブラリ】pandas
【データの形】DataFrameで「品種名」列と「alcohol」列がある、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】groupby().mean() の書き方と、小数点以下2桁で丸める方法
```

### 複数列を一度に集計

```
【やりたいこと】pandasのgroupbyで品種ごとに複数の列をまとめて集計したい
【使うライブラリ】pandas
【データの形】DataFrameで「品種名」「alcohol」「proline」「flavanoids」の列がある、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】複数列を指定するときのリストの書き方と、mean/max/minをまとめて出す agg() の使い方
```

### 実務での応用例

```
【やりたいこと】pandasで「地域」ごとに「月次売上」と「利益率」の平均・最大・最小を一覧表にしたい
【使うライブラリ】pandas
【データの形】DataFrameで「region」「monthly_sales」「profit_rate」の列がある
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】groupby().agg({'列名': ['mean','max','min']}) の書き方
```

---

## P1-4｜条件でデータを絞り込む（フィルタリング）

### 1条件で絞り込む

```
【やりたいこと】pandasで特定の条件を満たす行だけ取り出したい
【使うライブラリ】pandas
【データの形】DataFrameで「alcohol」列が数値、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】df[df["alcohol"] >= 13.5] の意味と、条件を変えて試す方法
```

### 複数条件で絞り込む（AND / OR）

```
【やりたいこと】pandasで「アルコール度数が13.5以上」かつ「プロリンが700以上」のデータを取り出したい
【使うライブラリ】pandas
【データの形】DataFrameで「alcohol」「proline」列がある、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】AND条件のときの & の書き方と、括弧が必要な理由
```

### 実務での応用例

```
【やりたいこと】pandasで「売上が100万円以上」かつ「直近30日以内」の顧客データを取り出したい
【使うライブラリ】pandas
【データの形】DataFrameで「sales」（数値）と「date」（datetime型）の列がある
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】数値条件と日付条件を組み合わせる方法。pd.to_datetime() を使うか？
```

---

## P1-5｜エラーが出たときの質問テンプレート

```
【やりたいこと】〇〇のコードを実行したい
【使うライブラリ】pandas
【データの形】〇〇のDataFrame
【環境】Python 3.8.6、Windows、JupyterLab
【エラーメッセージ】
（ここにエラーメッセージ全文をコピー&ペースト）
【実行したコード】
（ここにエラーが出たコードをコピー&ペースト）
```

### よくあるエラーと対処

| エラー | 原因 | 対処 |
|--------|------|------|
| `KeyError: '列名'` | 列名のスペルミス / 存在しない列名 | `df.columns` で列名一覧を確認 |
| `TypeError: can only concatenate str` | 文字列に数値を足している | 型変換（`int()` / `float()`）が必要 |
| `SyntaxError` | カッコ・クォートの閉じ忘れ | AIにコードを渡して「構文エラーを直して」と依頼 |
| `NameError: name '〇〇' is not defined` | 変数がまだ定義されていない | 上のセルから順番に実行し直す |
| `IndentationError` | インデントのズレ | スペースとタブが混在していないか確認 |

---

## AIへの上手な聞き方 ── よいプロンプトと悪いプロンプト

### ❌ 悪い例

```
pandasでエラーが出ました。直してください。
```
→ 情報が少なすぎて、AIは答えられない

### ✅ 良い例

```
【やりたいこと】品種ごとのアルコール度数の平均を出したい
【使うライブラリ】pandas
【データの形】DataFrameで「品種名」列（文字列）と「alcohol」列（float）、178件
【環境】Python 3.8.6、Windows、JupyterLab
【エラーメッセージ】
KeyError: 'alcohol'

【実行したコード】
df.groupby("品種名")["Alcohol"].mean()
```

→ AIはすぐ「`"Alcohol"` ではなく `"alcohol"` が正しい列名です」と答えられる

### 💡 回答が長すぎてわからないときの追加プロンプト

```
もっとシンプルなコードで教えてください。初心者向けに1行で説明してください。
```

```
今のコードを3行以内に短くして、各行にコメントをつけてください。
```
