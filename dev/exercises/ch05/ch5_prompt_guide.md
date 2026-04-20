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

### 主要 3 変数のヒストグラムを横並びで描く

```
【やりたいこと】「mean radius」「mean texture」「mean area」の 3 変数のヒストグラムを、1行3列に横並びで描きたい
【使うライブラリ】matplotlib
【データの形】df は 569行×31列。使う列は mean radius / mean texture / mean area
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】plt.subplots(1, 3) で複数グラフを並べて、zip() で axes と列名をペアにしてループする書き方がわからない
```

### 2変数の散布図を診断結果で色分けして描く（追加）

```
【やりたいこと】「mean radius」と「mean area」の散布図を診断結果（malignant / benign）で色分けして描きたい
【使うライブラリ】matplotlib
【データの形】df は 569行×31列。「診断結果」列に malignant / benign の文字列、「mean radius」「mean area」列に float値
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】for ループで診断ラベルごとに plt.scatter() を繰り返して色分けする書き方がわからない
```

---

### seaborn で箱ひげ図を描く

```
【やりたいこと】seaborn の boxplot で「mean radius」を 診断ラベルごとに比較する箱ひげ図を描きたい
【使うライブラリ】seaborn
【データの形】df は 569行×31列。x="診断結果"、y="mean radius" を指定する
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】sns.boxplot() の x・y・data の指定方法がわからない
```

### 全数値列の相関行列を計算する

```
【やりたいこと】df の数値列だけを選んで相関行列（corr）を計算し、変数に保存したい
【使うライブラリ】pandas
【データの形】df は 569行×31列（30特徴量 + 診断結果列）。「診断結果」列（文字列）は除外したい
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】select_dtypes(include="number") で数値列を選んで corr() を計算する書き方がわからない
```

> 💡 `corr = df.select_dtypes(include="number").corr()` と書くと診断結果列を自動で除いた 30×30 の相関行列が得られます。

### 相関行列をヒートマップで表示する

```
【やりたいこと】corr（全数値列の相関行列）をヒートマップで可視化したい
【使うライブラリ】seaborn
【データの形】corr は 30×30 の DataFrame（df.select_dtypes(include="number").corr() の結果）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】sns.heatmap() の cmap・center の引数の意味と、figsize を大きくする書き方がわからない
```

> 💡 30列あるので `figsize=(16, 12)` 程度に大きくしてください。`center=0` で無相関（0）が白になります。

---

## Step 1（追加）｜クラスバランス割合確認

### クラスバランスを割合で確認する

```
【やりたいこと】df["診断結果"] の benign・malignant それぞれが全体の何 % かを割合で確認したい
【使うライブラリ】pandas
【データの形】df という DataFrame、569行×31列（診断結果列に benign / malignant の文字列）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】value_counts() に normalize=True を追加して割合表示にする方法がわからない
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

## Step 3（追加）｜1件だけ予測

### テストデータの1件目を予測する

```
【やりたいこと】X_test の1行目だけを取り出して、model.predict() で診断結果を予測して実際の y_test と比べたい
【使うライブラリ】scikit-learn の predict
【データの形】X_test は 114行×30列の DataFrame、y_test は 114件の診断結果 Series
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】iloc で1行だけ取り出す方法と、predict() に渡す形式がわからない
```

> 💡 Ch.3 の「1件だけ予測」と全く同じ型です。`X_test.iloc[[0]]` で1行を取り出し、`model.predict(sample)` で予測します。

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

### 混同行列をラベル付き DataFrame で print する（追加）

```
【やりたいこと】confusion_matrix の結果を、行・列に「実際:malignant」のような診断ラベルをつけた DataFrame に変換して表示したい
【使うライブラリ】pandas、scikit-learn の confusion_matrix
【データの形】y_test・y_pred はどちらも長さ 114。ラベルは malignant / benign
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】numpy 配列の混同行列を pd.DataFrame() で変換して、index と columns に品種名を指定する書き方がわからない
```

### 訓練精度とテスト精度を比較して過学習を確認する（追加）

```
【やりたいこと】X_train でも predict して訓練精度を計算し、テスト精度と比べて過学習がないか確認したい
【使うライブラリ】scikit-learn の accuracy_score
【データの形】X_train は 455行×30列、y_train は 455件の診断結果
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】訓練精度を計算してテスト精度との差を表示する方法がわからない
```

### 特徴量重要度の DataFrame を作る

```
【やりたいこと】model.feature_importances_（重要度の配列）と X.columns（列名）をセットにした DataFrame を作りたい
【使うライブラリ】pandas
【データの形】X.columns は 30特徴量の列名、model.feature_importances_ は長さ30の配列
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】pd.DataFrame({"特徴量": ..., "重要度": ...}) で2列の DataFrame を作る書き方がわからない
```

### DataFrame を並べ替えて上位10件を取得する

```
【やりたいこと】feat_df を重要度の小さい順（ascending=True）に並べ替えて、上位10件（tail(10)）だけ取り出したい
【使うライブラリ】pandas
【データの形】feat_df は「特徴量」「重要度」の 2列 DataFrame（30行）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】sort_values(ascending=True) にして tail(10) で後ろ10件を取る意味がわからない
```

> 💡 `barh`（横棒グラフ）は下から上に描かれます。昇順で tail() すると重要度が大きいものが上に来ます。

### 特徴量重要度を横棒グラフで表示する（上位10件）

```
【やりたいこと】feat_df（重要度の小さい順・上位10件）を横棒グラフで表示したい
【使うライブラリ】matplotlib
【データの形】feat_df は「特徴量」「重要度」の 2列 DataFrame（10行）、sort_values(ascending=True).tail(10) 済み
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】plt.barh() の引数の順番と、figsize・tight_layout の書き方がわからない
```

### 特徴量重要度の DataFrame を降順で作り直して上位5件を表示する（追加）

```
【やりたいこと】model.feature_importances_ を変数名とセットにした DataFrame を作り、重要度の大きい順（降順）に並べ替えて上位5件を print で表示したい
【使うライブラリ】pandas
【データの形】X.columns は 30特徴量の列名、model.feature_importances_ は長さ30の配列
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】sort_values(ascending=False)（降順）にして head(5) で上位5件を表示する書き方がわからない
```

---

## 発展｜Precision / Recall

### Precision・Recall・F1スコアを一覧で確認する

```
【やりたいこと】良性・悪性それぞれの Precision・Recall・F1スコアを一覧で確認したい
【使うライブラリ】scikit-learn の classification_report
【データの形】y_test・y_pred はどちらも長さ 114。ラベルは malignant / benign
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】classification_report のインポート方法と print で表示する書き方がわからない
```

---

## よくあるエラーと対処

| エラー | 原因 | 対処 |
|-------|------|------|
| `NameError: name 'cancer' is not defined` | 最初のセルを実行していない | 最初のインポートセルを再実行する |
| `ValueError: could not convert string to float` | 列に文字列が混じっている | `df.info()` で型を確認する |
| グラフが表示されない | `plt.show()` を忘れている | セル末尾に `plt.show()` を追加する |
| `AttributeError: 'DataFrame' has no attribute 'feature_importances_'` | model ではなく df に対して呼んでいる | `model.feature_importances_` と書く |
