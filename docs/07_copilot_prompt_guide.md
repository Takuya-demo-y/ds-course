# GitHub Copilot 活用ガイド（演習用）

> 対象：データサイエンス実践コース（1日版）受講生  
> Copilot の利用形式：**JupyterLab のサイドバーチャット（Copilot Chat）のみ**  
> 基本方針：**演習のコードはすべて Copilot に書いてもらう。自分の仕事は「何をしたいか」を言語化することと「結果を解釈すること」**

---

## 1. なぜ Copilot を使うのか

```
データサイエンティストの仕事
  ↓
「何を分析するか」「どの手法を使うか」「結果が何を意味するか」
                  ← ここが人間の仕事

「どう書くか」（コードの構文・引数の書き方）
                  ← ここは Copilot に任せる
```

> Copilot を使いこなせる人 ＝ 「目的を明確に言語化できる人」  
> プロンプトが曖昧だと良いコードは返ってきません。

---

## 2. Copilot Chat の開き方（ウェブブラウザ）

```
ブラウザで以下の URL を開く：
  Microsoft Copilot → https://copilot.microsoft.com
  GitHub Copilot   → https://github.com/copilot

※ JupyterLab のサイドバー機能は使いません。
   ブラウザのタブで Copilot Chat を開き、
   JupyterLab と並べて使ってください。
```

**推奨レイアウト：**
```
画面左半分: JupyterLab（ノートブック）
画面右半分: ブラウザ（Copilot Chat）
```

---

## 3. プロンプトの型（全チャプター共通テンプレート）

**すべての質問をこの型で書く習慣をつけてください。**

```
【やりたいこと】
　〇〇のデータで△△を実行したい

【使うライブラリ】
　pandas, matplotlib など（requirements.txt に載っているもの）

【データの形】
　DataFrame で列名は〇〇、行数は〇〇件

【環境】
　Python 3.8.6、Windows、JupyterLab

【わからない点】
　〇〇の書き方がわからない / 〇〇でエラーが出る
```

---

## 4. チャプター別テンプレートプロンプト集

---

### Ch.1 データ読み込み・集計

**[P1-1] データの基本情報を確認する**
```
【やりたいこと】
　ワインデータ（sklearn の load_wine）を pandas DataFrame に変換して、
　行数・列数・各列のデータ型・欠損値の件数を一覧で確認したい

【使うライブラリ】
　pandas, sklearn.datasets

【環境】
　Python 3.8.6、Windows、JupyterLab

【わからない点】
　head(), info(), describe(), isnull().sum() の使い方と
　それぞれ何を確認するための関数か教えて
```

**[P1-2] グループ別に集計する**
```
【やりたいこと】
　pandas DataFrame で「品種」列でグループ分けして、
　「alcohol」と「proline」の列の平均値を品種ごとに集計したい

【使うライブラリ】
　pandas

【データの形】
　DataFrame で列名は wine.feature_names に「品種」列を追加したもの

【わからない点】
　groupby() の使い方。mean() の前に列を指定する方法も教えて
```

**[P1-3] 条件でデータを絞り込む**
```
【やりたいこと】
　pandas DataFrame で「alcohol が 13.5 以上 かつ proline が 700 以上」
　の行だけを取り出したい

【使うライブラリ】
　pandas

【わからない点】
　複数条件のフィルタリングの書き方。& の使い方と括弧の必要性も教えて
```

---

### Ch.2 データ可視化・EDA

**[P2-1] ヒストグラムを作る**
```
【やりたいこと】
　ワインデータの「alcohol」列について、品種ごとにヒストグラムを重ねて表示したい
　品種は 0/1/2 の数値なので、色を変えて凡例も表示したい

【使うライブラリ】
　matplotlib, japanize_matplotlib

【環境】
　Python 3.8.6、Windows、JupyterLab

【わからない点】
　品種ごとにループして hist() を重ねる書き方を教えて
```

**[P2-2] 相関ヒートマップを作る**
```
【やりたいこと】
　ワインデータ全 13 特徴量の相関行列を計算して、
　seaborn のヒートマップで表示したい
　相関係数の数値も表示して、赤青のカラーマップを使いたい

【使うライブラリ】
　pandas, seaborn, matplotlib, japanize_matplotlib

【わからない点】
　DataFrame.corr() の結果を sns.heatmap() に渡す書き方を教えて
```

**[P2-3] 散布図を作る（品種別色分け）**
```
【やりたいこと】
　ワインデータで「alcohol」を X 軸、「proline」を Y 軸にして
　品種ごとに色を変えた散布図を作りたい

【使うライブラリ】
　matplotlib, japanize_matplotlib

【わからない点】
　品種でループして scatter() を重ねる書き方を教えて
　alpha（透明度）の設定方法も教えて
```

---

### Ch.3 異常検知

**[P3-1] 平均プロファイルを作って可視化する**
```
【やりたいこと】
　sklearn の load_digits() で読み込んだ手書き数字データから、
　数字「1」のサンプルだけ取り出して平均プロファイルを計算し、
　8×8 の画像として表示したい

【使うライブラリ】
　numpy, matplotlib, sklearn.datasets

【環境】
　Python 3.8.6、Windows、JupyterLab

【わからない点】
　numpy の条件インデックス（y == 1 の部分）の書き方と、
　mean(axis=0) の意味、reshape(8,8) の使い方を教えて
```

**[P3-2] 異常スコアを計算してランキングを出す**
```
【やりたいこと】
　各サンプルについて「平均プロファイルからの距離（Zスコアの平均）」を
　異常スコアとして計算して、スコアが高い順にトップ5の画像を表示したい

【使うライブラリ】
　numpy, matplotlib

【わからない点】
　Zスコアの計算式（(x - mean) / std）を関数として定義する書き方と、
　np.argsort()[::-1] でスコア順に並べる方法を教えて
```

**[P3-3] IsolationForest で異常検知する**
```
【やりたいこと】
　sklearn の IsolationForest を使って、
　数字「1」のサンプルの中から異常なものを検出したい
　contamination=0.05（5%を異常と判定）で実行して、
　異常と判定されたサンプルの画像を表示したい

【使うライブラリ】
　sklearn.ensemble.IsolationForest, numpy, matplotlib

【環境】
　Python 3.8.6、Windows、scikit-learn==0.23.2

【わからない点】
　fit() と predict() の書き方、-1 が異常・+1 が正常という判定の使い方を教えて
```

---

### Ch.4 機械学習モデル構築

**[P4-1] データを訓練・テストに分割する**
```
【やりたいこと】
　ワインデータ（178件・13特徴量・3品種）を
　訓練データ 80%、テストデータ 20% に分割したい
　品種の比率を訓練・テストで同じに保ちたい

【使うライブラリ】
　sklearn.model_selection.train_test_split

【環境】
　Python 3.8.6、Windows、scikit-learn==0.23.2

【わからない点】
　stratify パラメータの意味と使い方を教えて
```

**[P4-2] スケーリングを正しく適用する**
```
【やりたいこと】
　StandardScaler でスケーリングをしたい
　訓練データで fit_transform()、テストデータには transform() だけを使いたい
　なぜこの順番が重要なのか（データリーク防止）も教えて

【使うライブラリ】
　sklearn.preprocessing.StandardScaler

【環境】
　Python 3.8.6、Windows、scikit-learn==0.23.2

【わからない点】
　fit_transform と transform の違い、使い分けのルールを教えて
```

**[P4-3] ランダムフォレストで学習・予測する**
```
【やりたいこと】
　RandomForestClassifier を使ってワインの品種分類モデルを作りたい
　学習（fit）→ 予測（predict）→ 正解率（accuracy_score）の計算まで実行したい

【使うライブラリ】
　sklearn.ensemble.RandomForestClassifier
　sklearn.metrics.accuracy_score

【環境】
　Python 3.8.6、Windows、scikit-learn==0.23.2

【わからない点】
　n_estimators と random_state の意味、fit/predict の書き方を教えて
```

**[P4-4] 混同行列を表示する（scikit-learn 0.23.2 対応版）**
```
【やりたいこと】
　sklearn の confusion_matrix() で混同行列を計算して、
　seaborn の heatmap で可視化したい
　※ scikit-learn 0.23.2 のため ConfusionMatrixDisplay は使えない

【使うライブラリ】
　sklearn.metrics.confusion_matrix, seaborn, matplotlib

【環境】
　Python 3.8.6、Windows、scikit-learn==0.23.2

【わからない点】
　confusion_matrix の結果を DataFrame に変換して sns.heatmap に渡す書き方を教えて
　annot=True で数字を表示する方法も教えて
```

**[P4-5] 特徴量重要度を棒グラフで表示する**
```
【やりたいこと】
　学習済みの RandomForestClassifier から特徴量重要度を取り出して、
　重要度が高い順に横棒グラフで表示したい
　X 軸に特徴量名、Y 軸に重要度を表示したい

【使うライブラリ】
　pandas, matplotlib, japanize_matplotlib

【わからない点】
　model.feature_importances_ を pandas DataFrame に変換して
　sort_values() で降順に並べて barh() で表示する書き方を教えて
```

---

## 5. エラー対処のプロンプト型

**コードがエラーで動かないとき**
```
【状況】
　以下のコードを実行したらエラーが出ました

【コード】
　（エラーが出たコードをそのまま貼り付け）

【エラーメッセージ】
　（エラーメッセージをそのまま貼り付け）

【環境】
　Python 3.8.6、Windows、JupyterLab
　scikit-learn==0.23.2、pandas==1.1.4、numpy==1.19.4

【やりたかったこと】
　〇〇をしようとしていた

原因と修正方法を日本語で教えてください
```

**グラフが表示されないとき**
```
【状況】
　matplotlib でグラフを作ったが何も表示されない

【コード】
　（コードをそのまま貼り付け）

【環境】
　Python 3.8.6、Windows、JupyterLab、matplotlib==3.3.2

plt.show() の位置や設定の問題がないか確認して、修正したコードを教えてください
```

---

## 6. Copilot 活用のルール（再掲）

| タイミング | ルール | 理由 |
|-----------|--------|------|
| 座学中 | **使用禁止** | まず概念を自分の頭に入れる |
| 演習 問1・2 | **テンプレートを使って質問する** | 「何をしたいか」を言語化する練習 |
| 演習 問3（考察） | コードはOK・**考察文は自分で書く** | 解釈は人間の仕事 |
| 演習 問4（発展） | **自由に活用** | プロンプトの工夫も練習 |
| エラー対処 | **エラーメッセージを必ず貼る** | エラーなしに正確な回答はできない |

---

## 7. よくある NG プロンプト と 改善例

| NG（曖昧） | OK（具体的） |
|-----------|------------|
| 「グラフを作って」 | 「ワインデータの alcohol を品種別にヒストグラムで重ねて表示して。matplotlib 使用、Python 3.8.6、Windows」 |
| 「機械学習して」 | 「RandomForestClassifier で 3 クラス分類して accuracy_score を出して。scikit-learn 0.23.2」 |
| 「エラーを直して」 | 「以下のエラーが出た：〈エラー文〉。コードは〈コード〉。Python 3.8.6、scikit-learn 0.23.2 で修正方法を教えて」 |
| 「説明して」 | 「groupby().mean() が何をしているか、初心者向けに日本語で説明して。具体例も一つ見せて」 |

---

*文書終端*
