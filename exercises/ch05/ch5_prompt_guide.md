# Ch.5 Copilot プロンプトガイド

**URL：** https://copilot.microsoft.com  
JupyterLab（左）・Copilot（右）を並べて作業してください。

> **Ch.5 のポイント：** 「Ch.1〜4 で使ったコードを組み合わせるだけ」です。  
> 詰まったら「Ch.〇〇 でやった〇〇と同じことをしたい」と伝えると Copilot が理解しやすくなります。

---

> ⛔ **このガイドを使わないセクション（AI 禁止）**
> 各 Step の「気づきメモ」・**考察セクション** は自分の言葉で書きます。Copilot は使いません。

---

## 質問の型（毎回この5点を揃える）

```
【やりたいこと】〇〇したい
【使うライブラリ】pandas / scikit-learn / matplotlib / seaborn
【データの形】df は 569行×31列（30特徴量 + 診断列）の DataFrame
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】〇〇の書き方がわからない
```
> 💡 **【困っていること】に何を書けばよいかわからない場合は、「どう書けばよいかわからない」とそのまま書いて OK です。**  
> Copilot はそれでも十分に答えてくれます。


---

## Step 1｜データ読み込み・確認（Ch.1 の復習）

### Q1-1：データを DataFrame に変換する

```
【やりたいこと】load_breast_cancer() で読み込んだデータを pandas の DataFrame に変換したい
【使うライブラリ】pandas、scikit-learn の load_breast_cancer
【データの形】cancer.data が特徴量（569行×30列）、cancer.target がラベル（0=悪性, 1=良性）の numpy 配列
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】cancer.feature_names を列名に指定して DataFrame を作り、末尾に「診断結果」列（malignant / benign）を追加する方法がわからない
```

### Q1-1（補足）：データの型と欠損値を確認する

```
【やりたいこと】DataFrame の列の型・欠損値の有無を確認したい
【使うライブラリ】pandas
【データの形】df は 569行×31列（30特徴量 + 診断列）の DataFrame
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】df.info() と df.isnull().sum() の使い方と見方がわからない
```

> 💡 Ch.1 で学んだ「最初に必ずやる」習慣です。`df.info()` → `df.isnull().sum()` の順に実行してください。

### Q1-2：件数と基本統計量を確認する

```
【やりたいこと】診断ラベルごとの件数と、主要な特徴量の平均・最大・最小を確認したい
【使うライブラリ】pandas
【データの形】df は 569行×31列（30特徴量 + 診断列）の DataFrame
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】df["診断結果"].value_counts() と df.describe() の使い方がわからない
```

---

## Step 2｜EDA・可視化（Ch.2 の復習）

### 悪性・良性で分けてヒストグラムを重ねる

```
【やりたいこと】df の「mean radius」列を、診断ラベル（0=悪性, 1=良性）で分けてヒストグラムを重ねて表示したい
【使うライブラリ】matplotlib
【データの形】df["診断結果"] == "malignant" が悪性、"benign" が良性の DataFrame
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】2つの hist() を同じグラフに重ねる書き方と、alpha（透明度）の使い方がわからない
```

### seaborn で箱ひげ図を描く

```
【やりたいこと】seaborn の boxplot で「mean radius」を 診断ラベルごとに比較する箱ひげ図を描きたい
【使うライブラリ】seaborn
【データの形】df は 569行×31列。x="診断結果"、y="mean radius" を指定する
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】sns.boxplot() の x・y・data の指定方法がわからない
```

### 相関ヒートマップを描く

```
【やりたいこと】df の列名が「mean」で始まる列だけ抜き出して、相関行列のヒートマップを描きたい
【使うライブラリ】pandas、seaborn
【データの形】df は 569行×31列。column.startswith("mean") で列を絞り込む
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】列名の条件でフィルタする方法と、sns.heatmap() に annot=True で数値を表示する書き方がわからない
```

---

## Step 3｜モデル学習（Ch.3 の復習）

### train_test_split で分割する

```
【やりたいこと】X と y を train_test_split でテスト 20%・訓練 80% に分割したい
【使うライブラリ】scikit-learn の train_test_split
【データの形】X は 569行×30列の DataFrame（診断結果列を除く）、y は 569件の診断結果 Series
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】test_size=0.2 と random_state の指定方法がわからない
```

### RandomForest で学習・予測する

```
【やりたいこと】RandomForestClassifier を使って、X_train と y_train で学習し、X_test で予測したい
【使うライブラリ】scikit-learn の RandomForestClassifier
【データの形】X_train は訓練データの numpy array、y_train は訓練ラベルの配列
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】モデル作成 → fit → predict の 3ステップの書き方がわからない
```

> 💡 Ch.3 と全く同じ型です。`model = RandomForestClassifier(n_estimators=100, random_state=42)` → `model.fit()` → `model.predict()` の順に書くだけです。

---

## Step 4｜評価（Ch.3 の復習）

### 正解率を計算する

```
【やりたいこと】y_test（正解）と y_pred（予測）から正解率を計算したい
【使うライブラリ】scikit-learn の accuracy_score
【データの形】y_test・y_pred はどちらも長さ 114 の Series または配列
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】accuracy_score の引数の順番（正解 vs 予測）がわからない
```

### 混同行列をヒートマップで表示する

```
【やりたいこと】y_test と y_pred で混同行列を計算し、seaborn のヒートマップで表示したい
【使うライブラリ】scikit-learn の confusion_matrix、seaborn、pandas
【データの形】y_test・y_pred はどちらも長さ 114。ラベルは malignant / benign
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】confusion_matrix の結果を DataFrame に変換してヒートマップで表示する方法がわからない
```

### 特徴量重要度を棒グラフで表示する

```
【やりたいこと】model.feature_importances_ を使い、重要度の高い上位10特徴量を横棒グラフで表示したい
【使うライブラリ】pandas、matplotlib
【データの形】X.columns は 30特徴量の列名、model.feature_importances_ も長さ30
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】sort_values() で降順にして tail() で上位10件を取り出し、barh() で横棒グラフを描く方法がわからない
```

---

## 発展｜Precision / Recall

### Precision と Recall を計算する

```
【やりたいこと】y_test と y_pred から Precision（適合率）と Recall（再現率）を計算したい
【使うライブラリ】scikit-learn の precision_score、recall_score
【データの形】y_test・y_pred はどちらも長さ 114。ラベルは malignant / benign
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】precision_score と recall_score のインポート方法と引数の意味がわからない
```

---

## よくあるエラーと対処

| エラー | 原因 | 対処 |
|-------|------|------|
| `NameError: name 'cancer' is not defined` | 最初のセルを実行していない | 最初のインポートセルを再実行する |
| `ValueError: could not convert string to float` | 列に文字列が混じっている | `df.info()` で型を確認する |
| グラフが表示されない | `plt.show()` を忘れている | セル末尾に `plt.show()` を追加する |
| `AttributeError: 'DataFrame' has no attribute 'feature_importances_'` | model ではなく df に対して呼んでいる | `model.feature_importances_` と書く |
