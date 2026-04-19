# Ch.2 Copilot プロンプトガイド

**URL：** https://copilot.microsoft.com  
JupyterLab（左）・Copilot（右）を並べて作業してください。

---

## 質問の型（毎回この5点を揃える）

```
【やりたいこと】〇〇したい
【使うライブラリ】matplotlib / seaborn
【データの形】df という DataFrame、178行×14列（数値13列 + 品種名列）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】〇〇の書き方がわからない
```
> 💡 **【困っていること】に何を書けばよいかわからない場合は、「どう書けばよいかわからない」とそのまま書いて OK です。**  
> Copilot はそれでも十分に答えてくれます。

> ⛔ **このガイドを使わないセクション（AI 禁止）**  
> 各 STEP の「気づきメモ」・**問3（仮説の言語化）** は自分の言葉で書きます。Copilot は使いません。

---

## ❌ 悪い例 vs ✅ 良い例

### ❌ 情報不足で精度が下がる

```
グラフを描く方法を教えてください。
```

### ✅ 文脈を伝えると精度が上がる

```
【やりたいこと】alcohol と proline の散布図を品種ごとに色分けして描きたい
【使うライブラリ】matplotlib
【データの形】df という DataFrame。「品種名」列に wine_0/wine_1/wine_2、「alcohol」「proline」列に float値、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】for ループで品種ごとに scatter() を繰り返す書き方がわからない
```

---

## 回答が長すぎてわからないとき

```
もっとシンプルにしてください。最小限のコードだけ教えてください。
```

```
各行に「何をしているか」のコメントをつけてください。
```

---

## STEP 1｜ヒストグラム

### alcohol のヒストグラムを描く（Q1-1）

```
【やりたいこと】「alcohol」列のヒストグラムを描きたい
【使うライブラリ】matplotlib
【データの形】df という DataFrame。「alcohol」列は float型、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】plt.hist() の基本的な書き方と、タイトル・軸ラベルの付け方がわからない
```

### 別の列でヒストグラムを試したい

```
【やりたいこと】「proline」列のヒストグラムを描きたい
【使うライブラリ】matplotlib
【データの形】plt.hist(df["alcohol"], bins=20) はすでに動いている
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】列名と bins の数を変えるだけでよいか確認したい
```

### 品種ごとに色を分けてヒストグラムを重ねる（STEP1 まとめ）

```
【やりたいこと】「品種名」列でグループに分けて、alcohol のヒストグラムを同じグラフに重ねて描きたい。品種ごとに色を変えたい
【使うライブラリ】matplotlib
【データの形】df という DataFrame。「品種名」列に wine_0/wine_1/wine_2、「alcohol」列に float値、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】for ループで品種ごとに hist() を繰り返して同じグラフに重ねる書き方と、alpha（透明度）の指定方法がわからない
```

> 💡 `alpha=0.5` を指定すると半透明になり、重なった部分も見えやすくなります。

---

## STEP 2｜箱ひげ図（品種別比較）

### 品種別箱ひげ図を描く（Q2-1）

```
【やりたいこと】「alcohol」列を品種ごとに比較する箱ひげ図を描きたい
【使うライブラリ】matplotlib の df.boxplot()
【データの形】df という DataFrame。「品種名」列に wine_0/wine_1/wine_2、「alcohol」列に float値
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】df.boxplot(column="...", by="...") の書き方と、タイトルが2行出てしまうのを消す方法がわからない
```

> 💡 タイトルが2行出るときは `plt.suptitle("")` を追加すると消えます。

### 別の変数で箱ひげ図を試したい

```
【やりたいこと】「proline」列を品種別に比較する箱ひげ図を描きたい
【使うライブラリ】matplotlib
【データの形】df.boxplot(column="alcohol", by="品種名") はすでに動いている
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】column の列名を変えるだけでよいか確認したい
```

---

### 品種ごとの proline 平均を計算する

```
【やりたいこと】品種ごとに「proline」の平均を groupby で計算して、mean_proline という変数に保存したい
【使うライブラリ】pandas
【データの形】df という DataFrame。「品種名」列に wine_0/wine_1/wine_2、「proline」列に float値、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】groupby("品種名")["proline"].mean() の書き方と、結果を変数に入れる方法がわからない
```

### 品種別平均を棒グラフで表示する

```
【やりたいこと】mean_proline（品種ごとの proline 平均）を棒グラフで表示したい
【使うライブラリ】matplotlib
【データの形】mean_proline は品種名をインデックスにした Series（3件）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】Series の .plot(kind="bar") の書き方と、タイトル・軸ラベル・xticks の回転指定がわからない
```

---

## 問1｜散布図（品種別色分け）

### for ループで品種別散布図を描く

```
【やりたいこと】品種ごとに色を変えた散布図を描きたい。wine_0=赤、wine_1=青、wine_2=緑
【使うライブラリ】matplotlib
【データの形】df という DataFrame。「品種名」列でグループ化し、「alcohol」と「proline」を X・Y軸にする
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】for ループで品種ごとに plt.scatter() を繰り返す書き方がわからない
```

### 凡例（legend）を表示したい

```
【やりたいこと】散布図に品種名の凡例（legend）を表示したい
【使うライブラリ】matplotlib
【データの形】plt.scatter(..., label=name) は書いているが凡例が表示されない
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】plt.legend() を追加すればよいか、位置を指定する方法もわからない
```

### 別の変数ペアで試したい

```
【やりたいこと】「flavanoids」と「color_intensity」の品種別散布図を描きたい
【使うライブラリ】matplotlib
【データの形】alcohol vs proline の散布図コードはすでにある。変数名だけ変えればよいか確認したい
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】コードのどこを変えればよいか教えてほしい
```

---

## 問2｜数値列の確認と相関ヒートマップ

### ヒートマップの前に数値列だけを確認する（Q2-0）

```
【やりたいこと】DataFrame から数値型（float・int）の列だけを取り出して、列名の一覧を確認したい
【使うライブラリ】pandas
【データの形】df は 178行×14列（数値13列 + 品種名1列）。「品種名」は文字列型
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】数値型の列だけを自動で抽出する方法がわからない
```

> 💡 `df.select_dtypes(include="number")` で数値列だけの DataFrame が返ります。`.columns.tolist()` で列名一覧を取得できます。

---

### 全数値列の相関行列を計算する

```
【やりたいこと】df の数値列だけを選んで相関行列（corr）を計算し、変数に保存したい
【使うライブラリ】pandas
【データの形】df は 178行×14列。「品種名」列（文字列）は除外したい
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】select_dtypes(include="number") で数値列を選んで corr() を計算する書き方がわからない
```

> 💡 `corr = df.select_dtypes(include="number").corr()` と書くと品種名列を自動で除いた相関行列が得られます。

### 相関行列をヒートマップで表示する

```
【やりたいこと】corr（相関行列）をヒートマップで可視化したい。各セルに数値も表示したい
【使うライブラリ】seaborn の heatmap
【データの形】corr は df.select_dtypes(include="number").corr() の結果（13×13 の DataFrame）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】sns.heatmap() の annot・fmt・cmap の引数の意味と書き方がわからない
```

### 相関係数が強いペアだけ抜き出したい

```
【やりたいこと】corr.abs().unstack() で全ペアの相関係数を取り出し、0.7 以上のペアだけ表示したい
【使うライブラリ】pandas
【データの形】corr は df.select_dtypes(include="number").corr() の結果（DataFrame）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】自分自身との相関（=1.0）を除いて、絶対値が 0.7 以上のペアだけ取り出すコードがわからない
```

---

## 問4（発展）｜pairplot

### pairplot を描く

```
【やりたいこと】特定の列だけで pairplot を描きたい。品種ごとに色分けしたい
【使うライブラリ】seaborn の pairplot
【データの形】df から ["alcohol", "proline", "flavanoids", "color_intensity", "品種名"] の列だけ使う
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】sns.pairplot() の hue 引数の使い方と、alpha（透明度）の指定方法がわからない
```

---

## よくあるエラーと対処

### グラフが文字化けする

```
【やりたいこと】グラフの日本語ラベルが □□□ になるのを直したい
【使うライブラリ】japanize_matplotlib
【データの形】import japanize_matplotlib は書いているが文字化けする
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】japanize_matplotlib を import してもグラフの日本語が豆腐（□）になる場合の対処法を教えてほしい
```

### KeyError: '列名'

```
【やりたいこと】df["proline"] にアクセスしようとしたら KeyError が出た
【使うライブラリ】pandas
【データの形】df は load_wine() から作成した DataFrame、178行
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】KeyError: 'proline' というエラーの意味と、実際の列名を確認する方法を教えてほしい
```

> 💡 `print(df.columns.tolist())` で列名一覧を確認できます。

### plt.show() を忘れてグラフが出ない

```
【やりたいこと】グラフを表示したい。コードを実行しても何も出ない
【使うライブラリ】matplotlib
【データの形】plt.hist() は書いているが実行しても出力がない
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】plt.show() を最後に追加すればよいか、他に原因があるか確認してほしい
```
