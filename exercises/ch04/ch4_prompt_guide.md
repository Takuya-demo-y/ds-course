# Ch.4 Copilot プロンプトガイド

**URL：** https://copilot.microsoft.com  
JupyterLab（左）・Copilot（右）を並べて作業してください。

---

> ⛔ **このガイドを使わないセクション（AI 禁止）**
> 各 STEP の「気づきメモ」・**STEP 3（振り返り）** は自分の言葉で書きます。Copilot は使いません。

---

## 質問の型（毎回この5点を揃える）

```
【やりたいこと】〇〇したい
【使うライブラリ】pandas / numpy / scikit-learn
【データの形】df という DataFrame、120行×3列（time / value / lag_1）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】〇〇の書き方がわからない
```
> 💡 **【困っていること】に何を書けばよいかわからない場合は、「どう書けばよいかわからない」とそのまま書いて OK です。**  
> Copilot はそれでも十分に答えてくれます。


---

## STEP 1｜折れ線グラフ

### 時系列データを折れ線グラフで表示する

```
【やりたいこと】df の「value」列を折れ線グラフで表示したい
【使うライブラリ】matplotlib
【データの形】df という DataFrame、120行×2列（time / value）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】plt.plot() の基本的な書き方と、タイトル・軸ラベルの付け方がわからない
```

---

## STEP 2｜ラグ特徴量

### shift() でラグ特徴量を作る

```
【やりたいこと】df["value"] の1つ前の値を、lag_1 という新しい列として追加したい
【使うライブラリ】pandas
【データの形】df という DataFrame、120行×2列（time / value）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】shift(1) で1つ前の値を取り出せるか確認して、lag_1 列への代入方法を教えてほしい
```

### NaN を削除する

```
【やりたいこと】shift() で生じた先頭の NaN がある行を削除したい
【使うライブラリ】pandas
【データの形】df は shift(1) を使った後、先頭1行に NaN がある
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】dropna() の基本的な使い方がわからない
```

---

## 問1｜学習（fit）

### X と y に分ける

```
【やりたいこと】df から「lag_1」列だけを X として取り出したい
【使うライブラリ】pandas
【データの形】df という DataFrame、120行×3列（time / value / lag_1）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】複数の列を指定して DataFrame として取り出す書き方がわからない
```

### 最初の 80点を取り出す

```
【やりたいこと】DataFrame の最初の 80行だけを取り出して X_train として使いたい
【使うライブラリ】pandas
【データの形】X は 119行×1列の DataFrame（lag_1列のみ）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】iloc でのスライスの書き方がわからない
```

### LinearRegression で学習する

```
【やりたいこと】LinearRegression でモデルを作り、X_train と y_train で学習させたい
【使うライブラリ】scikit-learn の LinearRegression
【データの形】X_train は 80行×1列の DataFrame（lag_1列のみ）、y_train は 80件の Series
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】LinearRegression の使い方が Ch.3 の RandomForest と同じか確認したい
```

> 💡 `model = LinearRegression()` → `model.fit(X_train, y_train)` と書くだけで OK です（Ch.3 と同じ型）。

---

## 問2｜予測と異常スコア

### 全期間を予測する

```
【やりたいこと】学習済みの model で X 全体（119点）を予測したい
【使うライブラリ】scikit-learn
【データの形】X は 119行×1列の DataFrame（lag_1列のみ）。model.fit() は完了している
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】predict() に渡すのが X_train か X か迷っている
```

> 💡 全期間で予測するので `model.predict(X)` です（X_train ではない）。

### 異常スコア（絶対誤差）を計算する

```
【やりたいこと】df["value"] の値（pandas Series）と予測値（y_pred: numpy配列）の差の絶対値を計算したい
【使うライブラリ】numpy
【データの形】df["value"].values は長さ 119 の numpy 配列、y_pred も長さ 119
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】numpy で要素ごとに引き算して絶対値を取る書き方がわからない
```

---

## 問2-2｜異常スコアのグラフ確認

### 異常スコアの推移を折れ線グラフで確認する

```
【やりたいこと】df["score"]（長さ 119 の Series）を折れ線グラフで表示して、スコアが高い期間を確認したい
【使うライブラリ】matplotlib
【データの形】df["time"] を X軸、df["score"] を Y軸にする
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】pandas の Series を plt.plot() に渡す書き方がわからない
```

---

## 問3｜しきい値と可視化

### しきい値を設定する

```
【やりたいこと】score の上位 5%（95パーセンタイル）をしきい値として計算したい
【使うライブラリ】numpy
【データの形】score は長さ 119 の numpy 配列
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】np.percentile() の引数（配列と数値）の意味がわからない
```

### 異常フラグを作る

```
【やりたいこと】score > threshold の条件で True/False の配列（異常フラグ）を作りたい
【使うライブラリ】numpy
【データの形】score と threshold はどちらも数値。score は長さ 119 の配列
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】numpy 配列で条件比較をすると True/False の配列が得られる仕組みがわからない
```

### 正常と異常を色分けしてグラフを描く

```
【やりたいこと】折れ線グラフ（正常）と散布図（異常点）を重ねて描きたい。正常は青、異常は赤い点
【使うライブラリ】matplotlib
【データの形】df["time"]・df["value"] は Series、is_anomaly は True/False の配列
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】plt.plot() と plt.scatter() を同じグラフに重ねる書き方がわからない
```

> 💡 `is_anomaly` が True の点だけを `df["time"][is_anomaly]` のように取り出せます。

---

## 問4（発展）｜しきい値変更

### for ループでしきい値を変えて比べる

```
【やりたいこと】np.percentile(score, p) の p を 90・95・99 と変えて、それぞれの検出件数を表示したい
【使うライブラリ】numpy
【データの形】score は長さ 119 の numpy 配列
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】for ループで p を変えながら結果を print する書き方がわからない
```

---

## よくあるエラーと対処

### ValueError: Input contains NaN

```
【やりたいこと】model.fit(X_train, y_train) を実行したら ValueError が出た
【エラー内容】ValueError: Input contains NaN
【データの形】shift() を使った後、dropna() を忘れているかもしれない
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】NaN が残っている場所を確認して dropna() で消す方法を教えてほしい
```

> 💡 `df.isnull().sum()` で確認して、`df = df.dropna()` を実行してください。

### 配列の長さが合わない

```
【やりたいこと】abs(df["value"].values - y_pred) を計算したら形が合わないエラーが出た
【データの形】df は dropna() 後で 119行、y_pred は predict() の結果
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】numpy 配列の形（shape）を確認する方法と、なぜ長さが合わないかを教えてほしい
```

> 💡 `print(df.shape)` と `print(y_pred.shape)` で確認してください。
