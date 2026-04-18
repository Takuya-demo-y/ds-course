# Ch.3 Copilot プロンプトガイド

**URL：** https://copilot.microsoft.com  
JupyterLab（左）・Copilot（右）を並べて作業してください。

---

## 質問の型（毎回この5点を揃える）

```
【やりたいこと】〇〇したい
【使うライブラリ】scikit-learn
【データの形】X は 178行×13列の DataFrame、y は品種名の Series
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】〇〇の書き方がわからない
```

---

## ❌ 悪い例 vs ✅ 良い例

### ❌ 情報不足

```
機械学習を実装する方法を教えてください。
```

### ✅ 文脈を伝えると精度が上がる

```
【やりたいこと】RandomForest でワイン品種を分類したい
【使うライブラリ】scikit-learn の RandomForestClassifier
【データの形】X は 178行×13列の DataFrame（数値のみ）、y は品種名の Series（3クラス）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】model.fit() の引数に何を渡せばいいかわからない
```

---

## STEP 1｜X と y を作る

### 品種名列を除いた DataFrame を作る

```
【やりたいこと】df から「品種名」列だけ除いた DataFrame を作りたい
【使うライブラリ】pandas
【データの形】df は 178行×14列。「品種名」列だけ取り除きたい
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】特定の列を除く df.drop() の書き方がわからない
```

### 特定の列だけ取り出す

```
【やりたいこと】df の「品種名」列だけを取り出して y という変数に入れたい
【使うライブラリ】pandas
【データの形】df は 178行×14列の DataFrame
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】1列だけ取り出す書き方がわからない
```

---

## STEP 2｜訓練/テスト分割

### train_test_split の使い方

```
【やりたいこと】X と y を 7:3 の割合で訓練用とテスト用に分割したい
【使うライブラリ】scikit-learn の train_test_split
【データの形】X は DataFrame（178行×13列）、y は Series（178件）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】train_test_split の引数（test_size と random_state）の意味と書き方がわからない
```

### 分割後の件数確認

```
【やりたいこと】train_test_split で分割後の X_train と X_test の件数を確認したい
【使うライブラリ】pandas
【データの形】X_train と X_test は DataFrame
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】DataFrame の行数を確認する方法がわからない
```

---

## 問1｜モデルの学習と予測

### RandomForest モデルを作る

```
【やりたいこと】RandomForestClassifier を作りたい。木を100本使い、結果が毎回同じになるようにしたい
【使うライブラリ】scikit-learn の RandomForestClassifier
【データの形】X は 178行×13列の数値 DataFrame、y は文字列の品種名 Series
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】n_estimators と random_state の意味と書き方がわからない
```

### model.fit() の使い方

```
【やりたいこと】RandomForestClassifier に訓練データを学習させたい
【使うライブラリ】scikit-learn
【データの形】X_train は 124行×13列の DataFrame、y_train は 124件の Series
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】model.fit() に渡す引数の順番がわからない
```

### model.predict() の使い方

```
【やりたいこと】学習済みの model でテストデータの品種を予測したい
【使うライブラリ】scikit-learn
【データの形】X_test は 54行×13列の DataFrame。model.fit() は完了している
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】predict() に渡すのは X_test か X_train か迷っている
```

---

## 問2｜正解率の計算

### accuracy_score の使い方

```
【やりたいこと】y_test（正解）と y_pred（予測）を比べて正解率を計算したい
【使うライブラリ】scikit-learn の accuracy_score
【データの形】y_test と y_pred はどちらも 54件の品種名（文字列）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】accuracy_score() の引数の順番がわからない
```

### 正解率をパーセントで表示する

```
【やりたいこと】accuracy_score の結果（0〜1 の小数）を % 表示にしたい
【使うライブラリ】Python の print
【データの形】acc = 0.9259... のような float
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】f文字列で % 表示にするフォーマット指定の書き方がわからない
```

---

## 問3｜混同行列

### confusion_matrix の使い方

```
【やりたいこと】confusion_matrix で品種ごとの正解・不正解を確認したい
【使うライブラリ】scikit-learn の confusion_matrix
【データの形】y_test と y_pred はどちらも 54件の品種名（文字列）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】confusion_matrix() の引数の順番がわからない
```

### 混同行列をヒートマップで表示する

```
【やりたいこと】confusion_matrix の結果をヒートマップで可視化したい。各マスに数値も表示したい
【使うライブラリ】seaborn の heatmap
【データの形】cm は confusion_matrix() の結果（3×3 の numpy 配列）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】sns.heatmap() の annot・fmt の意味と、X軸・Y軸にラベルをつける方法がわからない
```

> 💡 scikit-learn 0.23.2 では `ConfusionMatrixDisplay` は使えません。`sns.heatmap()` を使ってください。

---

## 問4（発展）｜特徴量重要度

### feature_importances_ を取り出す

```
【やりたいこと】RandomForest の特徴量重要度を列名とセットで取り出したい
【使うライブラリ】scikit-learn + pandas
【データの形】model は学習済み RandomForestClassifier。X.columns で列名が取得できる
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】model.feature_importances_ を DataFrame や Series にまとめる方法がわからない
```

### 特徴量重要度を棒グラフで表示する

```
【やりたいこと】特徴量重要度を値が大きい順に横棒グラフで表示したい
【使うライブラリ】pandas の plot + matplotlib
【データの形】importances は特徴量名がインデックスの Series（重要度の降順にソート済み）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】Series を横棒グラフ（barh）で描く書き方がわからない
```

---

## よくあるエラーと対処

### ValueError: could not convert string to float

```
【やりたいこと】model.fit(X_train, y_train) を実行したらエラーが出た
【使うライブラリ】scikit-learn
【エラー内容】ValueError: could not convert string to float
【データの形】X_train に文字列の列が含まれているかもしれない
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】このエラーの原因と直し方を教えてほしい
```

> 💡 X に `品種名` 列が残っていると起きます。`df.drop(columns=["品種名"])` で除いてください。

### NameError: name 'y_pred' is not defined

```
【やりたいこと】accuracy_score(y_test, y_pred) を実行したら NameError が出た
【使うライブラリ】scikit-learn
【エラー内容】NameError: name 'y_pred' is not defined
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】y_pred が未定義になる原因を教えてほしい
```

> 💡 `model.predict(X_test)` のセルを先に実行してください。セルは上から順番に実行する必要があります。
