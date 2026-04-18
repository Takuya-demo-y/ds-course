---
marp: true
theme: default
paginate: true
---

# Ch.4　時系列データと異常検知
## ── 演習ブリーフィング

**本日の演習時間：35分**  
（問3まで完了で合格）

---

## 今日作るもの

**時系列の異常検知グラフ**

```
          ↑
   5    ●← 異常！（赤い点）
   0    ～～～～～～～～
  -1    ← 正常（青い線）
        ─────────────→ 時刻 t
         t=50        t=150
```

→ **正常なパターンから飛び出した点を自動で検出する**

---

## Ch.3 と今日の違いはここだけ

| | Ch.3（分類） | Ch.4（異常検知） |
|--|------------|----------------|
| **使うモデル** | RandomForestClassifier | **LinearRegression** |
| **y に渡すもの** | 品種ラベル（カテゴリ） | **次の時刻の値（数値）** |
| **コードの型** | `fit → predict` | **同じ！`fit → predict`** |
| **評価方法** | accuracy（正解率） | **予測誤差 → 異常スコア** |

> 🔑 **型はまったく同じです。今日の新要素はラグ特徴量だけ！**

---

## 演習の進め方

1. **データ生成セル**（実行するだけ）を最初に実行する
2. **STEP 1**：折れ線グラフでスパイクを目視確認
3. **STEP 2**：`shift()` でラグ特徴量を作る
4. **問1**：正常期間（最初の80点）で `model.fit()`
5. **問2**：全期間で `model.predict()` → 異常スコア計算
6. **問3（ゴール）**：しきい値で異常判定 → グラフにハイライト
7. **問4（発展）**：時間が余ったら

---

## Copilot の使い方

**URL：** https://copilot.microsoft.com

**質問の型（5点セット）を必ず入れる：**

```
【やりたいこと】〇〇したい
【使うライブラリ】pandas / numpy / scikit-learn
【データの形】df は 197行×4列（value, lag1, lag2, lag3）
【環境】Python 3.8.6、Windows、JupyterLab
【困っていること】〇〇の書き方がわからない
```

詳細な例は **`ch4_prompt_guide.md`** を参照してください。

---

## よくあるエラーと対処

| エラー | 原因 | 対処 |
|-------|------|------|
| `ValueError: Input contains NaN` | `dropna()` を忘れている | `df = df.dropna()` を実行 |
| 配列の長さが合わない | `df` の行数と `y_pred` の長さが不一致 | `print(df.shape)` で確認 |
| グラフが表示されない | `plt.show()` を忘れている | セル末尾に `plt.show()` を追加 |
| `AttributeError` | インポートを忘れている | 最初のセルを再実行 |

---

## 問3 のゴールイメージ

```python
# 正常は青い折れ線、異常は赤い点でハイライト
plt.plot(df["t"], df["value"], color="steelblue", label="正常")
plt.scatter(df["t"][is_anomaly], df["value"][is_anomaly],
            color="red", zorder=5, label="異常")
plt.title("異常検知の結果")
plt.legend()
plt.show()
```

> t=50 と t=150 の付近に赤い点が表示されれば成功です！
