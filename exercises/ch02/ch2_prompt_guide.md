# Ch.2 Copilot プロンプトガイド

**URL：** https://copilot.microsoft.com  
JupyterLab（左）・Copilot（右）を並べて作業してください。

---

## 質問の型（毎回この5点を揃える）

```
【やりたいこと】〇〇したい
【使うライブラリ】matplotlib / seaborn
【データの形】DataFrame。列名は〇〇、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】〇〇の書き方がわからない
```

---

## ❌ 悪い例 vs ✅ 良い例

### ❌ 情報不足で精度が下がる

```
グラフを描く方法を教えてください。
```

### ✅ 文脈を伝えると精度が上がる

```
【やりたいこと】品種ごとのアルコール度数を棒グラフで比較したい
【使うライブラリ】matplotlib
【データの形】df という DataFrame。「品種名」列に Barolo/Grignolino/Barbera、「alcohol」列に float値、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】groupby で計算した平均を棒グラフにする書き方がわからない
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

### 別の列でヒストグラムを描く

```
【やりたいこと】「proline」列のヒストグラムを描きたい
【使うライブラリ】matplotlib
【データの形】df という DataFrame。「proline」列は float型、178件
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】plt.hist() の基本的な書き方と、タイトル・軸ラベルの付け方がわからない
```

### bins の数を変えたい

```
【やりたいこと】ヒストグラムのバーの数を 10・20・30 と変えて見た目がどう変わるか確認したい
【使うライブラリ】matplotlib
【データの形】plt.hist(df["proline"], bins=20) は動いている
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】bins の数を変えるだけで良いか、他に変えるべき引数があるか知りたい
```

---

## STEP 2｜ボックスプロット

### 品種別ボックスプロットを描く

```
【やりたいこと】「flavanoids」列を品種ごとに比較するボックスプロットを描きたい
【使うライブラリ】matplotlib の df.boxplot()
【データの形】df という DataFrame。「品種名」列に Barolo/Grignolino/Barbera、「flavanoids」列に float値
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】df.boxplot(column="...", by="...") の書き方と、タイトルが2行出てしまうのを消す方法がわからない
```

> 💡 タイトルが2行出るときは `plt.suptitle("")` を追加すると消えます。

### ボックスプロットを横向きにしたい

```
【やりたいこと】ボックスプロットを横向き（vert=False）にしたい
【使うライブラリ】matplotlib
【データの形】df.boxplot(column="proline", by="品種名") は動いている
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】縦向きを横向きにするオプションがわからない
```

---

## STEP 3｜相関ヒートマップ

### ヒートマップを描く

```
【やりたいこと】DataFrame の相関ヒートマップを描きたい。数値を各セルに表示したい
【使うライブラリ】seaborn の heatmap
【データの形】corr = df.corr() で相関行列が計算されている。df は 178行×13列の float型
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】sns.heatmap() の annot・fmt・cmap の引数の意味と書き方がわからない
```

### 相関係数が強いペアだけ抜き出したい

```
【やりたいこと】corr.abs().unstack() で全ペアの相関係数を取り出し、0.5 以上のペアだけ表示したい
【使うライブラリ】pandas
【データの形】corr は df.corr() の結果（DataFrame）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】自分自身との相関（=1.0）を除いて、絶対値が 0.5 以上のペアだけ取り出すコードがわからない
```

---

## 問1｜棒グラフ

### groupby の結果を棒グラフにする

```
【やりたいこと】df.groupby("品種名")["alcohol"].mean() の結果を棒グラフにしたい
【使うライブラリ】matplotlib（pandas の plot）
【データの形】mean_alcohol = df.groupby("品種名")["alcohol"].mean() は動いている（Series型）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】Series を棒グラフにする .plot(kind="bar") の書き方と、X軸ラベルを傾けずに表示する方法がわからない
```

### 3品種に別々の色をつけたい

```
【やりたいこと】棒グラフの各棒（3品種）に異なる色をつけたい
【使うライブラリ】matplotlib
【データの形】mean_alcohol.plot(kind="bar") は動いている
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】color=["色1", "色2", "色3"] のように指定する書き方がわからない
```

---

## 問2｜散布図（品種別色分け）

### for ループで品種別散布図を描く

```
【やりたいこと】品種ごとに色を変えた散布図を描きたい。Barolo=赤、Grignolino=青、Barbera=緑
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
