# データサイエンス実践コース｜Jupyter Lab 環境構築手順

> 対象：Windows / Mac 共通  
> 所要時間：約 20〜30 分（インターネット環境が必要です）

---

## 本書で構築できる環境

| 項目 | 内容 |
|------|------|
| Python バージョン | 3.11.9 |
| 仮想環境ツール | venv |
| 実行環境 | Jupyter Lab |
| 主なライブラリ | pandas / numpy / matplotlib / seaborn / japanize-matplotlib / Pillow / scikit-learn |

---

## 【目次】

1. Python をインストールする
2. 仮想環境を作成 → 起動する
3. ライブラリを一括インストールする
4. Jupyter Lab を起動する
5. 動作確認をする

---

## 凡例

| マーク | 意味 |
|--------|------|
| 💻 | PC 上（ブラウザ・エクスプローラー等）での作業 |
| ⚙️ | コマンドプロンプト（Windows）またはターミナル（Mac）での作業 |
| ⚠️ | 重要な注意事項 |
| ✅ | 確認ポイント |

---

## 任意：Pyenv（複数 Python を管理したい方のみ）

PC 内にすでに別バージョンの Python が入っている場合は、**pyenv** で管理することを推奨します。  
初めて Python をインストールする方は **手順 1 から**進めてください。

- Windows：https://note.com/bhrtaym/n/nc8ea8b14216e
- Mac：https://qiita.com/mitusati/items/d5d9428b044c8b45d1e2

---

## 1. Python をインストールする

> ⚠️ Pyenv を使う方はこの手順をスキップし、手順 2 へ進んでください。

### 💻 1-1. ダウンロードサイトにアクセスする

以下のサイトにアクセスして **Python 3.11.9** をダウンロードします。

| OS | URL |
|----|-----|
| Windows | https://pythonlinks.python.jp/ja/index.html |
| Mac | https://www.python.org/downloads/macos/ |

リストの中から **Python 3.11.9** を選んでダウンロードしてください。

---

### 💻 1-2. インストーラーを実行する

ダウンロードしたファイルをダブルクリックして実行してください。

**Windows の場合**

> ⚠️ インストール画面の最初に表示される **「Add python.exe to PATH」に必ずチェックを入れてください。**  
> チェックを忘れた場合は、インストーラーをもう一度実行してやり直せます。

インストーラーの指示に従って「Install Now」をクリックします。

**Mac の場合**

インストーラーの指示に従って進めてください（デフォルト設定で問題ありません）。

---

### ⚙️ 1-3. Python のバージョンを確認する

コマンドプロンプト（Windows）またはターミナル（Mac）を開き、以下を実行します。

```
# Windows
python -V

# Mac
python3 -V
```

以下のように表示されれば成功です。

```
Python 3.11.9
```

> ✅ `3.11.x` と表示されれば OK です（xの数値は問いません）

---

### 💻 1-4. 作業フォルダを作成する

任意の場所に、今回のコース用フォルダを作成してください。

**推奨：デスクトップに作成**

```
例）
Windows: C:\Users\ユーザー名\Desktop\ds_course
Mac:     /Users/ユーザー名/Desktop/ds_course
```

> 💡 フォルダ名・パスに **日本語・スペースは使わないでください**（エラーの原因になります）

---

## 2. 仮想環境を作成 → 起動する

**仮想環境とは？**  
プロジェクトごとに独立した Python 環境のことです。  
ライブラリのバージョンを固定して管理できるため、環境汚染を防げます。

---

### ⚙️ 2-1. 作業フォルダへ移動する

コマンドプロンプト／ターミナルで以下を実行し、1-4 で作成したフォルダへ移動します。

```
# Windows
cd C:\Users\ユーザー名\Desktop\ds_course

# Mac
cd /Users/ユーザー名/Desktop/ds_course
```

> 💡 フォルダをエクスプローラーで開いた状態でパスをコピーすると楽です

---

### ⚙️ 2-2. 仮想環境を作成する（初回のみ）

作業フォルダへ移動できたら、以下のコマンドで仮想環境を作成します。  
（環境名 `ds_env` は変更可能ですが、英数字のみにしてください）

```
# Windows
py -3.11 -m venv ds_env

# Mac
python3.11 -m venv ds_env
```

> ✅ フォルダ内に `ds_env` というフォルダが作成されれば成功です  
> ⚠️ この手順は初回のみです。次回以降は 2-3 から実行してください

---

### ⚙️ 2-3. 仮想環境を起動する

作成した仮想環境を起動します。

```
# Windows（コマンドプロンプト）
ds_env\Scripts\activate.bat

# Windows（PowerShell）
ds_env\Scripts\Activate.ps1

# Mac
source ds_env/bin/activate
```

> ✅ コマンドプロンプトの先頭に `(ds_env)` が表示されれば起動成功です

```
# 起動前
C:\Users\ユーザー名\Desktop\ds_course>

# 起動後（左に環境名が付く）
(ds_env) C:\Users\ユーザー名\Desktop\ds_course>
```

> ⚠️ 以降の手順はすべて **`(ds_env)` が表示された状態**で実行してください  
> 新しいウィンドウを開いた場合は、必ず 2-3 から実行して仮想環境を起動してください

---

## 3. ライブラリを一括インストールする

### 💻 3-1. requirements.txt を作業フォルダに置く

コース資料として配布された **`requirements.txt`** を、1-4 で作成した作業フォルダ（`ds_course`）の中にコピーしてください。

```
ds_course/
├── ds_env/          ← 仮想環境フォルダ（自動生成）
└── requirements.txt ← ← ← ここに置く
```

`requirements.txt` に含まれるライブラリ：

| ライブラリ | 用途 |
|-----------|------|
| pandas | データ操作・集計 |
| numpy | 数値計算・配列処理 |
| matplotlib | グラフ描画 |
| seaborn | 統計グラフ描画 |
| japanize-matplotlib | matplotlib の日本語表示対応 |
| Pillow | 画像処理 |
| scikit-learn | 機械学習モデル構築・評価 |
| jupyterlab | Jupyter Lab 本体 |

---

### ⚙️ 3-2. pip をアップグレードする

まず pip（パッケージ管理ツール）を最新版にします。

```
pip install --upgrade pip
```

---

### ⚙️ 3-3. requirements.txt から一括インストールする

```
pip install -r requirements.txt
```

> ⚠️ インターネット接続が必要です  
> ⏱️ 目安：2〜5分程度（回線速度によって異なります）

---

### ⚙️ 3-4. インストールを確認する

以下のコマンドで、インストール済みライブラリの一覧を表示します。

```
pip list
```

以下のライブラリがすべてリストに表示されれば成功です。

```
✅ pandas
✅ numpy
✅ matplotlib
✅ seaborn
✅ japanize-matplotlib
✅ Pillow
✅ scikit-learn
✅ jupyterlab
```

---

## 4. Jupyter Lab を起動する

### ⚙️ 4-1. Jupyter Lab を起動する

> ⚠️ 仮想環境 `(ds_env)` が起動した状態で実行してください（2-3 参照）

```
jupyter lab
```

コマンドを実行すると、ブラウザが自動的に開き、以下のような画面が表示されます。

```
[ブラウザで http://localhost:8888/lab が開く]
```

**Jupyter Lab が開かない場合**

ブラウザで以下の URL を直接入力してください。

```
http://localhost:8888/lab
```

---

### 💻 4-2. Notebook ファイルを開く

Jupyter Lab の左側のファイルブラウザから、コース資料の Notebook（`.ipynb` ファイル）を開いてください。

```
ds_course/
├── ds_env/
├── requirements.txt
└── notebooks/           ← コース資料フォルダ
    ├── ch1_data_analysis.ipynb
    ├── ch2_visualization.ipynb
    ├── ch3_image_processing.ipynb
    ├── ch4_machine_learning.ipynb
    └── ch5_comprehensive_exercise.ipynb
```

> 💡 Jupyter Lab を終了するには、コマンドプロンプト／ターミナルで `Ctrl + C` を押してください

---

## 5. 動作確認をする

Jupyter Lab で `ch1_data_analysis.ipynb` を開き、最初のセルを実行してください。

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib
from sklearn.datasets import load_wine
from PIL import Image, ImageFilter

print("準備OK！")
```

**実行方法**：セルを選択して `Shift + Enter` を押す

| 結果 | 対応 |
|------|------|
| ✅ `準備OK！` と表示された | 環境構築完了です！ |
| ⚠️ `ModuleNotFoundError` が出た | 手順 3 に戻り、インストールを再確認してください |
| ⚠️ その他のエラーが出た | 講師に声をかけてください |

---

## よくあるエラーと対処法

### ❓ `python -V` を実行しても Python が見つからない

**Windows の場合**  
→ Python インストール時に「Add python.exe to PATH」のチェックが外れていた可能性があります。  
→ 手順 1-2 からやり直してください。

**Mac の場合**  
→ `python3 -V` と入力してください（Mac では `python3` コマンドを使います）

---

### ❓ `activate` を実行しても `(ds_env)` が表示されない

- 現在のディレクトリが `ds_course` フォルダになっているか確認してください（手順 2-1）
- `ds_env` フォルダが `ds_course` フォルダ内に存在するか確認してください（手順 2-2）

---

### ❓ PowerShell で `activate` 実行時にエラーが出る

PowerShell のスクリプト実行ポリシーの制限がかかっている場合があります。  
以下のコマンドを実行してから再度お試しください。

```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### ❓ `pip install -r requirements.txt` がエラーになる

- `(ds_env)` が表示された状態（仮想環境が起動中）か確認してください
- `requirements.txt` が作業フォルダ内にあるか確認してください
- インターネットに接続されているか確認してください

---

### ❓ Jupyter Lab 起動後、ブラウザが開かない

ブラウザで `http://localhost:8888/lab` を直接入力してください。  
それでも開かない場合は、ターミナルに表示されている URL（`http://127.0.0.1:8888/lab?token=...`）をコピーしてブラウザに貼り付けてください。

---

## 毎回の起動手順（2回目以降）

環境が構築できたあとは、毎回以下の手順で起動してください。

```
# ① コマンドプロンプト / ターミナルを開く

# ② 作業フォルダへ移動
cd /Users/ユーザー名/Desktop/ds_course  ← Macの例

# ③ 仮想環境を起動（(ds_env) が表示されるまで）
source ds_env/bin/activate    ← Mac
ds_env\Scripts\activate.bat   ← Windows（コマンドプロンプト）

# ④ Jupyter Lab を起動
jupyter lab
```

---

*以上で環境構築は完了です。当日は講師の指示に従って Notebook を開いてください。*
