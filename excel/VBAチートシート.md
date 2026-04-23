# VBA チートシート ─ 1日目 + 2日目 総まとめ

> 演習中に困ったときの参照用。コードはそのままコピーして使えます。

---

## 基本構造

```vba
' プロシージャ（実行単位）
Sub プロシージャ名()
    ' 処理
End Sub

' 関数（戻り値あり）
Function 関数名(引数 As 型) As 戻り値の型
    関数名 = 戻り値
End Function
```

---

## 変数・定数

```vba
' 変数の宣言
Dim 変数名 As 型

' よく使う型
Dim i       As Long      ' 整数（大きな数も扱える）
Dim name    As String    ' 文字列
Dim price   As Double    ' 小数点あり数値
Dim flag    As Boolean   ' True / False
Dim ws      As Worksheet ' ワークシートオブジェクト
Dim wb      As Workbook  ' ブックオブジェクト

' 定数（変わらない値に使う）
Const MAX_ROW As Long = 1000
Const FOLDER  As String = "C:\data\"
```

---

## セルの操作

```vba
' セルの指定
Cells(行, 列)           ' Cells(2, 3) = C2 セル
Range("A1")             ' 名前で指定
Range("A1:C10")         ' 範囲で指定

' 値の読み書き
Cells(2, 1).Value = "田中"      ' 書き込み
Dim name As String
name = Cells(2, 1).Value        ' 読み込み

' 書式
Cells(1, 1).Font.Bold = True                    ' 太字
Cells(1, 1).Interior.Color = RGB(46, 64, 87)   ' 背景色
Cells(2, 3).NumberFormat = "#,##0"              ' 数値書式

' 最終行の取得（定番パターン）
Dim lastRow As Long
lastRow = Cells(Rows.Count, 1).End(xlUp).Row    ' A列の最終行
```

---

## 条件分岐

```vba
' 基本
If 条件 Then
    ' 処理
ElseIf 条件2 Then
    ' 処理
Else
    ' それ以外
End If

' 比較演算子
' =  等しい   <>  等しくない
' >  より大   >=  以上
' <  より小   <=  以下

' 論理演算子
If A > 0 And B > 0 Then   ' かつ
If A > 0 Or  B > 0 Then   ' または
If Not flag Then           ' 否定
```

---

## 繰り返し処理

```vba
' 回数指定（For〜Next）
Dim i As Long
For i = 2 To lastRow
    ' 処理
Next i

' 条件指定（Do While〜Loop）
Dim fileName As String
fileName = Dir("C:\data\*.xlsx")
Do While fileName <> ""
    ' 処理
    fileName = Dir()   ' 次のファイルへ
Loop

' 全シートをループ（For Each）
Dim ws As Worksheet
For Each ws In ThisWorkbook.Worksheets
    ' 処理
Next ws

' ループを途中で抜ける
Exit For    ' For ループを抜ける
Exit Do     ' Do ループを抜ける
```

---

## ブックとシートの操作

```vba
' ブックを開く / 閉じる
Workbooks.Open "C:\data\ファイル.xlsx"
ActiveWorkbook.Close SaveChanges:=False   ' 保存しないで閉じる

' このブックのパス
Dim path As String
path = ThisWorkbook.Path   ' フォルダパス（末尾に \ なし）

' フォルダ内のファイルを取得
Dim f As String
f = Dir("C:\data\*.xlsx")         ' 最初の .xlsx ファイル名
Do While f <> ""
    Debug.Print f
    f = Dir()                     ' 次のファイル名
Loop

' シートを変数に代入（Set が必要）
Dim ws As Worksheet
Set ws = Worksheets("シート名")
Set ws = ThisWorkbook.Worksheets("集計")

' シートを追加して名前をつける
Worksheets.Add(After:=Worksheets(Worksheets.Count)).Name = "新シート"

' シートを削除
Application.DisplayAlerts = False
Worksheets("削除するシート").Delete
Application.DisplayAlerts = True

' 全シートをループ
For Each ws In ThisWorkbook.Worksheets
    Debug.Print ws.Name
Next ws
```

---

## デバッグ

```vba
' イミディエイトウィンドウに出力（Ctrl+G で開く）
Debug.Print "値：" & 変数名
Debug.Print "行:" & i & "  列:" & j

' ブレークポイント：行の左端クリック、または F9
' ステップ実行：F8（1行ずつ実行）
' 変数の確認：停止中にマウスオーバー
```

---

## エラーハンドリング

```vba
' 基本パターン
Sub サンプル()
    On Error GoTo ErrorHandler

    ' 処理
    Workbooks.Open "C:\data.xlsx"

    Exit Sub                     ' ← これがないと ErrorHandler も実行される！

ErrorHandler:
    MsgBox "エラー番号：" & Err.Number & vbCrLf _
         & "内容："       & Err.Description
    Application.ScreenUpdating = True
End Sub

' シートの存在確認（定番パターン）
Dim ws As Worksheet
On Error Resume Next
Set ws = Worksheets("シート名")
On Error GoTo 0
If Not ws Is Nothing Then
    ' シートが存在する場合の処理
End If

' Err オブジェクト
Err.Number       ' エラー番号
Err.Description  ' エラーの説明
```

---

## Function

```vba
' 定義
Function 最終行取得(ws As Worksheet, col As Long) As Long
    最終行取得 = ws.Cells(ws.Rows.Count, col).End(xlUp).Row
End Function

' 文字列を返す Function
Function 評価判定(売上 As Long) As String
    If     売上 >= 1000000 Then
        評価判定 = "A"
    ElseIf 売上 >= 500000 Then
        評価判定 = "B"
    Else
        評価判定 = "C"
    End If
End Function

' 呼び出し
Dim lastRow As Long
lastRow = 最終行取得(ActiveSheet, 1)

Dim grade As String
grade = 評価判定(Cells(i, 4).Value)
```

---

## パフォーマンス最適化

```vba
' 処理前に停止する
Application.ScreenUpdating  = False              ' 画面更新を止める（速度向上）
Application.Calculation     = xlCalculationManual  ' 自動計算を止める
Application.DisplayAlerts   = False              ' 確認ダイアログを非表示

' 処理後に必ず元に戻す（後片付け Sub にまとめるのが定番）
Application.ScreenUpdating  = True
Application.Calculation     = xlCalculationAutomatic
Application.DisplayAlerts   = True
```

---

## よく使う関数・メソッド

```vba
' 文字列操作
Len("Hello")                   ' 文字数 → 5
Left("Hello", 3)               ' 左から3文字 → "Hel"
Right("Hello", 3)              ' 右から3文字 → "llo"
Mid("Hello", 2, 3)             ' 2文字目から3文字 → "ell"
Replace("A_B", "_", "/")       ' 置換 → "A/B"
Split("A,B,C", ",")            ' 分割 → 配列 ["A","B","C"]
Trim("  Hello  ")              ' 前後の空白除去 → "Hello"
UCase("hello")                 ' 大文字 → "HELLO"
LCase("HELLO")                 ' 小文字 → "hello"

' 数値操作
Int(3.7)                       ' 切り捨て → 3
Round(3.456, 2)                ' 四捨五入 → 3.46
Abs(-5)                        ' 絶対値 → 5

' 日付操作
Now()                          ' 現在の日時
Date()                         ' 今日の日付
Year(Now())                    ' 年を取得
Month(Now())                   ' 月を取得
Day(Now())                     ' 日を取得

' 型変換
CStr(123)                      ' 数値 → 文字列
CLng("123")                    ' 文字列 → Long
CDbl("3.14")                   ' 文字列 → Double
CDate("2024/01/15")            ' 文字列 → Date
IsNumeric("123")               ' 数値か判定 → True/False

' ファイル操作
Dir("C:\data\*.xlsx")          ' ファイル名を取得
ThisWorkbook.Path              ' このブックのフォルダパス

' ユーザー操作
MsgBox "メッセージ"
MsgBox "完了", vbInformation, "タイトル"
InputBox("入力してください", "タイトル")
```

---

## ダイアログの種類（MsgBox）

```vba
' ボタン定数
vbOKOnly       ' OK のみ（デフォルト）
vbOKCancel     ' OK と キャンセル
vbYesNo        ' はい と いいえ
vbYesNoCancel  ' はい / いいえ / キャンセル

' アイコン定数
vbInformation  ' 情報
vbQuestion     ' 質問
vbExclamation  ' 警告
vbCritical     ' エラー

' 戻り値
vbOK      ' 1
vbCancel  ' 2
vbYes     ' 6
vbNo      ' 7

' 使用例
Dim ret As Integer
ret = MsgBox("実行しますか？", vbYesNo + vbQuestion, "確認")
If ret = vbNo Then Exit Sub
```

---

## 改行文字

```vba
vbCrLf      ' Windows の改行（よく使う）
vbLf        ' Unix の改行
Chr(10)     ' vbLf と同じ
```

---

## キーボードショートカット（VBE）

| ショートカット | 操作 |
|---|---|
| `Alt + F11` | VBE を開く / 閉じる |
| `F5` | マクロを実行 |
| `F8` | ステップ実行（1行ずつ） |
| `F9` | ブレークポイントの設定 / 解除 |
| `Ctrl + G` | イミディエイトウィンドウを開く |
| `Ctrl + Space` | 入力候補を表示 |
| `Ctrl + Z` | 元に戻す |
| `Ctrl + Home` | コードの先頭へ移動 |
