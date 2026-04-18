# Ch.1 Copilot プロンプトガイド

**URL：** https://copilot.microsoft.com  
JupyterLab（左）・Copilot（右）を並べて作業してください。

---

## 質問の型（毎回この5点を揃える）

```
【やりたいこと】〇〇したい
【使うライブラリ】pandas
【データの形】DataFrame。列名は〇〇、行数は 178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】〇〇の書き方がわからない
```

> **なぜ型が必要か：** 「groupby を教えて」だけだと汎用的な説明が返ってきます。  
> 「このデータで・この列を・こうしたい」まで伝えると、すぐ使えるコードが返ってきます。

---

## ❌ 悪い例 vs ✅ 良い例

### ❌ 情報不足で精度が下がる

```
value_counts の使い方を教えてください。
```

```
エラーが出ました。直してください。
```

### ✅ 文脈を伝えると精度が上がる

```
【やりたいこと】品種ごとのデータ件数を数えて表示したい
【使うライブラリ】pandas
【データの形】DataFrame。「品種名」列に Barolo/Grignolino/Barbera が入っている、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】value_counts() の使い方がわからない
```

---

## 回答が長すぎてわからないとき

```
もっとシンプルにしてください。1〜2行のコードで教えてください。
```

```
各行に「何をしているか」のコメントをつけてください。
```

---

## データ確認（STEP 1〜4）

### 末尾5行を表示する（STEP 1 の「試してみましょう」）

```
【やりたいこと】DataFrame の末尾5行を表示したい
【使うライブラリ】pandas
【データの形】df という名前の DataFrame、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】head() の代わりに使うメソッドがわからない
```

---

### 特定の列だけ統計量を確認する（STEP 3 の「試してみましょう」）

```
【やりたいこと】「alcohol」列だけの平均・最大・最小を確認したい
【使うライブラリ】pandas
【データの形】df という DataFrame。「alcohol」列は float 型、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】describe() を特定の列だけに適用する書き方がわからない
```

---

### 欠損がある列だけ表示する（STEP 4 の「試してみましょう」）

```
【やりたいこと】isnull().sum() の結果から、欠損が1件以上ある列だけを取り出したい
【使うライブラリ】pandas
【データの形】missing = df.isnull().sum() の結果が Series になっている
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】Series の値が 0 より大きい要素だけを取り出す書き方がわからない
```

---

## 問1｜品種ごとの件数を数える（value_counts）

### 品種番号・品種名ごとに件数を数える

```
【やりたいこと】「品種名」列の値ごとに件数を数えて、多い順に表示したい
【使うライブラリ】pandas
【データの形】df という DataFrame。「品種名」列に Barolo/Grignolino/Barbera が入っている、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】value_counts() の基本的な書き方がわからない
```

---

### 件数を割合で表示する

```
【やりたいこと】品種ごとの件数を、実数ではなく割合（0〜1）で表示したい
【使うライブラリ】pandas
【データの形】df["品種名"].value_counts() は動いているが、割合にしたい
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】normalize=True の使い方と、結果が 0〜1 になる理由がわからない
```

---

## 問2｜品種別に集計する（groupby）

### 1列の平均を品種ごとに出す

```
【やりたいこと】品種ごとに「alcohol」列の平均を計算して表示したい
【使うライブラリ】pandas
【データの形】df という DataFrame。「品種名」列と「alcohol」列がある、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】groupby("品種名")["alcohol"].mean() という書き方は合っているか確認したい
```

---

### 複数の列をまとめて平均を出す

```
【やりたいこと】品種ごとに「alcohol」と「proline」の平均を1つの表にまとめて出したい
【使うライブラリ】pandas
【データの形】df という DataFrame。「品種名」「alcohol」「proline」列がある、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】複数列を指定するときの [ ] の書き方がわからない
```

---

### 平均・最大・最小・標準偏差を一度に出す

```
【やりたいこと】品種ごとに「alcohol」と「proline」の平均・最大・最小・標準偏差を一度に出したい
【使うライブラリ】pandas
【データの形】df.groupby("品種名")[["alcohol","proline"]] まで書いてある
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】.agg() に複数の集計方法を渡す書き方がわからない
```

---

### 特定の列の最大値だけを品種ごとに出す

```
【やりたいこと】品種ごとに「alcohol」の最大値だけを確認したい
【使うライブラリ】pandas
【データの形】df という DataFrame。「品種名」と「alcohol」列がある、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】groupby のあとに .mean() ではなく最大値を出すメソッドの名前がわからない
```

---

## 問4｜条件でデータを絞り込む（フィルタリング）

### 1つの条件で絞り込む

```
【やりたいこと】「alcohol」が 13.5 以上のワインだけを取り出したい
【使うライブラリ】pandas
【データの形】df という DataFrame。「alcohol」列は float 型、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】df[df["alcohol"] >= 13.5] という書き方で合っているか確認したい
```

---

### AND 条件で絞り込む（よくつまずくポイント）

```
【やりたいこと】「alcohol が 13.5 以上」かつ「proline が 700 以上」のワインだけ取り出したい
【使うライブラリ】pandas
【データの形】df という DataFrame。「alcohol」と「proline」列がある、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】2つの条件を & でつなぐとき、括弧が必要と聞いたがどこに付けるかわからない
```

---

### 絞り込んだデータで品種ごとに集計する

```
【やりたいこと】条件で絞り込んだ DataFrame を品種ごとに groupby して平均を出したい
【使うライブラリ】pandas
【データの形】high_alc という名前の絞り込み済み DataFrame。「品種名」「alcohol」「proline」列がある
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】絞り込んだ変数に対して groupby を使う書き方がわからない
```

---

## エラーが出たときのテンプレート

エラーメッセージとコードをそのままコピーして貼り付けてください。

```
【やりたいこと】〇〇したい
【使うライブラリ】pandas
【データの形】df という DataFrame、178件
【環境】Python 3.8.6、Windows、JupyterLab
【エラーメッセージ】
← ここにエラーメッセージ全文を貼り付ける

【実行したコード】
← ここにエラーが出たコードを貼り付ける
```

---

## よくあるエラーと原因・対処

| エラー | よくある原因 | 確認・対処 |
|--------|------------|----------|
| `KeyError: 'alcohol'` | 列名のスペルミス・大文字小文字 | `df.columns` を実行して正確な列名を確認する |
| `KeyError: '品種名'` | 品種名列がまだ作られていない | データ読み込みセルを実行したか確認する |
| `ValueError` (AND条件) | 括弧が足りない | `df[(条件1) & (条件2)]` のように各条件を `()` で囲む |
| `NameError: 'df' is not defined` | df がまだ定義されていない | 上のセルを順番に実行し直す |
| `AttributeError: 'str' object` | 文字列にメソッドを使っている | `df["列名"]` を `df.groupby("列名")` に修正 |
| `SyntaxError` | 括弧・クォートの閉じ忘れ | Copilot に「このコードの構文エラーを直して」と依頼する |
