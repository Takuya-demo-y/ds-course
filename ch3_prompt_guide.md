# Ch.3 Copilot プロンプトガイド

**URL：** https://copilot.microsoft.com  
JupyterLab（左）・Copilot（右）を並べて作業してください。

---

> ⛔ **このガイドを使わないセクション（AI 禁止）**
> 各問の「気づきメモ」・**STEP3（考察・振り返り）** は自分の言葉で書きます。Copilot は使いません。

---

## 質問の型（毎回この5点を揃える）

```
【やりたいこと】〇〇したい
【使うライブラリ】scikit-learn
【データの形】X は 178行×13列の DataFrame、y は品種名の Series
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】〇〇の書き方がわからない
```
> 💡 **【困っていること】に何を書けばよいかわからない場合は、「どう書けばよいかわからない」とそのまま書いて OK です。**  
> Copilot はそれでも十分に答えてくれます。


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

## STEP 1｜X と y を作る・データを分割する

### Q1-1：品種名列を除いた DataFrame を作る

```
【やりたいこと】df から「品種名」列だけ除いた DataFrame を作りたい
【使うライブラリ】pandas
【データの形】df は 178行×14列。「品種名」列だけ取り除きたい
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】特定の列を除く df.drop() の書き方がわからない
```

### Q1-1（b）：品種名列だけ取り出して y に入れる

```
【やりたいこと】df の「品種名」列だけを取り出して y という変数に入れたい
【使うライブラリ】pandas
【データの形】df は 178行×14列の DataFrame
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】1列だけ取り出す書き方がわからない
```

### Q1-2：train_test_split でデータを分割する

```
【やりたいこと】X と y を 8:2 の割合で訓練用とテスト用に分割したい
【使うライブラリ】scikit-learn の train_test_split
【データの形】X は DataFrame（178行×13列）、y は Series（178件）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】train_test_split の引数（test_size=0.2 と random_state）の意味と書き方がわからない
```

### Q1-2：分割後の件数を確認する

```
【やりたいこと】train_test_split で分割後の X_train と X_test の件数を確認したい
【使うライブラリ】pandas
【データの形】X_train は 142行×13列、X_test は 36行×13列の DataFrame
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】DataFrame の行数を確認する方法がわからない
```

### Q1-2（追加）：訓練データのクラス分布を確認する

```
【やりたいこと】y_train の品種ごとの件数を確認して、クラスが偏っていないかチェックしたい
【使うライブラリ】pandas
【データの形】y_train は 142件の品種名 Series（wine_0 / wine_1 / wine_2 の文字列）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】Series を value_counts() で集計する書き方がわからない
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
【データの形】X_train は 142行×13列の DataFrame、y_train は 142件の Series
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】model.fit() に渡す引数の順番がわからない
```

### model.predict() の使い方

```
【やりたいこと】学習済みの model でテストデータの品種を予測したい
【使うライブラリ】scikit-learn
【データの形】X_test は 36行×13列の DataFrame。model.fit() は完了している
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】predict() に渡すのは X_test か X_train か迷っている
```

---

## 問2｜正解率の計算

### accuracy_score の使い方

```
【やりたいこと】y_test（正解）と y_pred（予測）を比べて正解率を計算したい
【使うライブラリ】scikit-learn の accuracy_score
【データの形】y_test と y_pred はどちらも 36件の品種名（文字列）
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
【データの形】y_test と y_pred はどちらも 36件の品種名（文字列）
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

### 混同行列を品種名付きの DataFrame で表示する（追加）

```
【やりたいこと】confusion_matrix の結果を、行・列に品種名のラベルをつけた DataFrame に変換して表示したい
【使うライブラリ】pandas、scikit-learn の confusion_matrix
【データの形】y_test と y_pred はどちらも 36件の品種名（wine_0 / wine_1 / wine_2）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】confusion_matrix の numpy 配列を pandas DataFrame に変換して、行・列に品種名をつける書き方がわからない
```

### Q3-2（a）：特徴量重要度を DataFrame にまとめる

```
【やりたいこと】model.feature_importances_（重要度の配列）と X.columns（列名）をセットにした DataFrame を作りたい
【使うライブラリ】pandas
【データの形】model は学習済み RandomForestClassifier。X.columns に 13 列の特徴量名、model.feature_importances_ は長さ13の配列
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】pd.DataFrame({"特徴量": ..., "重要度": ...}) で2列の DataFrame を作る書き方がわからない
```

### Q3-2（b）：DataFrame を重要度の小さい順に並べ替える

```
【やりたいこと】feat_df を「重要度」列で小さい順（ascending=True）に並べ替えたい
【使うライブラリ】pandas
【データの形】feat_df は「特徴量」「重要度」の 2列 DataFrame（13行）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】sort_values() で ascending=True（昇順）にする意味と、横棒グラフとの関係がわからない
```

> 💡 `barh`（横棒グラフ）は下から上に描かれます。昇順にしておくと重要度が大きいものが上に来ます。

### Q3-2（c）：特徴量重要度を横棒グラフで表示する

```
【やりたいこと】feat_df（重要度の小さい順に並べ替え済み）を横棒グラフで表示したい
【使うライブラリ】matplotlib
【データの形】feat_df は「特徴量」「重要度」の 2列 DataFrame（13行）、sort_values(ascending=True) 済み
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】plt.barh() の引数（列名 vs 重要度）と、figsize・tight_layout の書き方がわからない
```

---

## 問1-b（追加）｜モデルの設定確認

### 学習後のモデル設定（木の本数・特徴量数）を確認する

```
【やりたいこと】学習済みの RandomForest モデルが何本の木を使い、何個の特徴量を学習したか確認したい
【使うライブラリ】scikit-learn の RandomForestClassifier
【データの形】model は学習済みの RandomForestClassifier
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】n_estimators と n_features_in_ の属性の使い方がわからない
```

---

## 問1-c（追加）｜1件だけ予測する

### テストデータの1件目を取り出してモデルで予測する

```
【やりたいこと】X_test の1行目だけを取り出して、model.predict() で品種を予測して実際の品種と比べたい
【使うライブラリ】scikit-learn の predict
【データの形】X_test は 36行×13列の DataFrame、y_test は 36件の品種名 Series
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】iloc で1行だけ取り出す方法と、predict() に渡す形式がわからない
```

---

## 問2-b（追加）｜訓練精度 vs テスト精度

### 訓練データでも予測して過学習を確認する

```
【やりたいこと】X_train で model.predict() して訓練精度を計算し、テスト精度と比べて過学習がないか確認したい
【使うライブラリ】scikit-learn の accuracy_score
【データの形】X_train は 142行×13列、y_train は 142件の品種名
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】訓練精度を計算してテスト精度との差を表示する方法がわからない
```

---

## 問3 まとめ（追加）｜classification_report

### Precision・Recall・F1スコアを一覧で確認する

```
【やりたいこと】品種ごとの Precision・Recall・F1スコアを classification_report で一覧表示したい
【使うライブラリ】scikit-learn の classification_report
【データの形】y_test と y_pred はどちらも 36件の品種名（文字列）、3クラス
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】classification_report のインポート方法と使い方がわからない
```

---

## 問3 まとめ（追加 b）｜特徴量重要度の上位5件を数値で確認する

### 重要度の大きい順に並べ替えて上位5件を表示する

```
【やりたいこと】model.feature_importances_ を使い、重要度が高い順に並べ替えた DataFrame を作って上位5件を print で表示したい
【使うライブラリ】pandas
【データの形】X.columns に 13 列の特徴量名、model.feature_importances_ は長さ13の配列
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】DataFrame を sort_values(ascending=False)（降順）にして head(5) で上位5件だけ取り出す書き方がわからない
```

---

## 問4（発展）｜Precision / Recall

### 品種ごとの Precision・Recall を計算する

```
【やりたいこと】品種ごとの Precision（適合率）と Recall（再現率）を計算して表示したい
【使うライブラリ】scikit-learn の precision_score、recall_score
【データの形】y_test と y_pred はどちらも 36件の品種名（文字列）、3クラス
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】precision_score と recall_score のインポート方法と、average=None の意味がわからない
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
