#!/usr/bin/env python3
"""
データサイエンス実践コース - SVGスライド一括生成スクリプト
実行方法: python generate_slides_svg.py
生成先 : slides_svg/ フォルダ（51枚の SVG ファイル）
"""

import os
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import japanize_matplotlib  # noqa: F401

OUTPUT = 'slides_svg'
W, H = 960, 540   # PowerPoint 16:9 (px)

# ---- 章カラー ---------------------------------------------------
C = {
    'intro':   '#2C3E50',
    'ch1':     '#4A90D9',
    'ch2':     '#5BA85A',
    'ch3':     '#E8A838',
    'ch4':     '#C0392B',
    'summary': '#8E44AD',
}
LIGHT = {k: v + '22' for k, v in C.items()}   # 薄い背景用（非使用）

# ================================================================
#  基本ユーティリティ
# ================================================================

def new_fig():
    fig = plt.figure(figsize=(9.6, 5.4), facecolor='white', dpi=100)
    ax  = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(H, 0)   # (0,0) = 左上
    ax.axis('off')
    return fig, ax

def save(fig, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, format='svg', bbox_inches='tight', pad_inches=0)
    plt.close(fig)

def rect(ax, x, y, w, h, fc, ec='none', lw=1, radius=0):
    if radius:
        p = FancyBboxPatch((x, y), w, h,
                           boxstyle=f'round,pad={radius}',
                           facecolor=fc, edgecolor=ec, linewidth=lw)
    else:
        p = Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw)
    ax.add_patch(p)

def txt(ax, x, y, s, fs=14, color='#1a1a2e', bold=False, ha='left', va='top',
        mono=False, alpha=1.0):
    kw = dict(fontsize=fs, color=color, ha=ha, va=va, alpha=alpha,
              fontweight='bold' if bold else 'normal')
    if mono:
        kw['fontfamily'] = 'monospace'
    ax.text(x, y, str(s), **kw)

def header(ax, color, label):
    rect(ax, 0, 0, W, 34, fc=color)
    txt(ax, 44, 17, label, fs=10, color='white', bold=True, va='center')

def slide_title(ax, title, y=52, fs=24):
    txt(ax, 44, y, title, fs=fs, bold=True)
    rect(ax, 44, y + fs + 6, W - 88, 2, fc='#ecf0f1')

def hbox(ax, x, y, w, h, text, bg, border, tc='#1a1a2e', fs=12, lw=3):
    rect(ax, x, y, w, h, fc=bg, ec='none')
    rect(ax, x, y, lw, h, fc=border)
    lines = text.split('\n')
    lh = h / (len(lines) + 0.3)
    for i, ln in enumerate(lines):
        txt(ax, x + lw + 10, y + lh * (i + 0.75), ln, fs=fs, color=tc)

def bullets(ax, items, x=64, y0=108, fs=14, color='#2c3e50',
            lh=28, accent='#4A90D9', sub_fs=10.5):
    y = y0
    for item in items:
        t = item['text'] if isinstance(item, dict) else item
        s = item.get('sub', '') if isinstance(item, dict) else ''
        em = item.get('emoji', '▸') if isinstance(item, dict) else '▸'
        txt(ax, x - 18, y + 2, em, fs=9.5, color=accent, va='top')
        txt(ax, x, y, t, fs=fs, color=color, va='top')
        y += lh
        if s:
            txt(ax, x + 10, y - 4, s, fs=sub_fs, color='#7f8c8d', va='top')
            y += 18
    return y

def code_block(ax, code, x, y, w, h, fs=10.5):
    rect(ax, x, y, w, h, fc='#1e1e2e', ec='#555', lw=1, radius=4)
    lines = code.strip().split('\n')
    lh = (h - 16) / max(len(lines), 1)
    for i, ln in enumerate(lines):
        txt(ax, x + 12, y + 10 + lh * (i + 0.45), ln,
            fs=fs, color='#cdd6f4', va='center', mono=True)

def table(ax, headers, rows, x=44, y=108, col_ws=None, row_h=30,
          color='#2C3E50', fs=12):
    n = len(headers)
    total_w = W - 88
    if col_ws is None:
        col_ws = [total_w // n] * n
    # header row
    cx = x
    for i, (h_txt, cw) in enumerate(zip(headers, col_ws)):
        rect(ax, cx, y, cw, row_h, fc=color, ec='white', lw=1)
        txt(ax, cx + 10, y + row_h * 0.5, h_txt, fs=fs,
            color='white', bold=True, va='center')
        cx += cw
    # data rows
    for ri, row in enumerate(rows):
        cy = y + row_h * (ri + 1)
        cx = x
        bg = '#f8f9fa' if ri % 2 else 'white'
        for ci, (cell, cw) in enumerate(zip(row, col_ws)):
            rect(ax, cx, cy, cw, row_h, fc=bg, ec='#ecf0f1', lw=0.5)
            txt(ax, cx + 10, cy + row_h * 0.5, cell, fs=fs,
                color='#2c3e50', va='center')
            cx += cw
    return y + row_h * (len(rows) + 1)

def flow(ax, boxes, y=220, h=70, colors=None, gap=6):
    n = len(boxes)
    arrow_w = 24
    box_w = (W - 88 - arrow_w * (n - 1)) // n
    x = 44
    for i, label in enumerate(boxes):
        fc = colors[i] if colors else C['ch1']
        rect(ax, x, y, box_w, h, fc=fc, radius=6)
        lines = label.split('\n')
        lh = h / (len(lines) + 0.2)
        for j, ln in enumerate(lines):
            txt(ax, x + box_w * 0.5, y + lh * (j + 0.75), ln,
                fs=11, color='white', bold=True, ha='center', va='center')
        x += box_w
        if i < n - 1:
            txt(ax, x + 2, y + h * 0.5, '→', fs=15, color='#95a5a6',
                va='center')
            x += arrow_w

def two_col(ax, left, right, y0=108, col_h=380,
            lbg='#EBF5FB', lbc='#4A90D9',
            rbg='#FEF9E7', rbc='#E8A838'):
    cw = (W - 88 - 16) // 2
    for i, (bg, bc, content) in enumerate([(lbg, lbc, left), (rbg, rbc, right)]):
        cx = 44 + i * (cw + 16)
        rect(ax, cx, y0, cw, col_h, fc=bg, ec=bc, lw=2, radius=6)
        if 'title' in content:
            txt(ax, cx + 16, y0 + 14, content['title'],
                fs=13, color=bc, bold=True)
        items = content.get('items', [])
        y_i = y0 + 40
        for item in items:
            txt(ax, cx + 22, y_i, '・' + item, fs=11.5,
                color='#2c3e50', va='top')
            y_i += 26

def steps(ax, step_items, x=44, y0=110, accent='#4A90D9'):
    y = y0
    for num, title, sub in step_items:
        # circle
        circle = plt.Circle((x + 18, y + 18), 18, color=accent, zorder=2)
        ax.add_patch(circle)
        txt(ax, x + 18, y + 18, str(num), fs=12, color='white',
            bold=True, ha='center', va='center')
        txt(ax, x + 46, y + 4, title, fs=14, color='#2c3e50', bold=True, va='top')
        if sub:
            txt(ax, x + 48, y + 24, sub, fs=10, color='#7f8c8d', va='top')
        y += 58
    return y

# ================================================================
#  タイトルスライド
# ================================================================

def title_slide(badge, title, subtitle, meta, color):
    fig, ax = new_fig()
    # gradient simulation: stacked rectangles
    for i in range(H):
        alpha = i / H
        r1, g1, b1 = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        r = int(r1 * (1 - alpha * 0.5))
        g = int(g1 * (1 - alpha * 0.5))
        b = int(b1 + (min(255, b1 + 80) - b1) * (1 - alpha))
        rect(ax, 0, i, W, 1, fc=f'#{r:02x}{g:02x}{b:02x}')
    # badge pill
    rect(ax, W//2 - 100, 90, 200, 28, fc=(1.000, 1.000, 1.000, 0.00), ec='none')
    bw = len(badge) * 7 + 40
    rect(ax, W//2 - bw//2, 85, bw, 28, fc='#ffffff33', ec='#ffffff55', lw=1, radius=10)
    txt(ax, W//2, 99, badge, fs=11, color='white', bold=True, ha='center', va='center')
    # title
    lines = title.split('\n')
    for i, ln in enumerate(lines):
        txt(ax, W//2, 145 + i * 55, ln, fs=36, color='white',
            bold=True, ha='center', va='center')
    # subtitle
    sub_lines = subtitle.split('\n')
    for i, ln in enumerate(sub_lines):
        txt(ax, W//2, 260 + len(lines) * 30 + i * 26, ln,
            fs=18, color=(1.000, 1.000, 1.000, 0.85), ha='center', va='center')
    # meta
    txt(ax, W//2, H - 60, meta, fs=13, color=(1.000, 1.000, 1.000, 0.55),
        ha='center', va='center')
    return fig

# ================================================================
#  Chapter 0: オリエンテーション
# ================================================================

def gen_ch0():
    ch = 'intro'; cl = C[ch]; lbl = 'オリエンテーション'

    slides = []

    # 0-1 タイトル
    slides.append(('01_title',
        title_slide('2026年度 研修プログラム',
                    'データサイエンス\n実践コース',
                    'Pythonでデータ分析を体験する1日',
                    '9:00〜16:30 ／ Jupyter Lab（ローカル環境）', cl)))

    # 0-2 今日のゴール
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '今日のゴール')
    hbox(ax, 44, 90, W - 88, 58,
         '「Pythonでデータ分析がどうやってできるのか、\nデータサイエンティストとして こういうことができる という実務イメージを持つ」',
         '#EBF5FB', '#4A90D9', tc='#1A5276', fs=12.5)
    bullets(ax, [
        {'text': 'データを読み込んで集計できる', 'emoji': '✅'},
        {'text': 'グラフでデータの傾向を確認できる', 'emoji': '✅'},
        {'text': '画像データが数値の配列だとわかる', 'emoji': '✅'},
        {'text': '機械学習モデルを作って評価できる', 'emoji': '✅'},
        {'text': '生成AIをコーディングに活用できる', 'emoji': '✅'},
    ], y0=164, lh=30, accent=cl)
    hbox(ax, 44, 430, W - 88, 40,
         '❌ Pythonの文法を完全に覚える必要なし　❌ コードをゼロから書けなくても大丈夫',
         '#FEF9E7', '#E8A838', tc='#7D6608', fs=12)
    slides.append(('02_goals', fig))

    # 0-3 DSの仕事フロー
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'データサイエンティストの仕事フロー')
    flow(ax,
         ['① データ\n収集・準備', '② EDA\n探索的分析', '③ 可視化\n仮説立て', '④ モデル\n構築・評価', '⑤ 結果の\n解釈・報告'],
         y=110, h=80,
         colors=[C['ch1'], C['ch2'], C['ch3'], C['ch4'], C['summary']])
    txt(ax, W//2, 205, '← 今日体験する範囲 →', fs=10.5, color='#7f8c8d', ha='center')
    table(ax,
          ['作業', '実務での時間比率（目安）'],
          [['データ収集・クリーニング', '約 40〜50%'],
           ['EDA・可視化', '約 20〜30%'],
           ['モデル構築・評価', '約 10〜20%'],
           ['結果の解釈・報告', '約 10〜20%']],
          y=220, row_h=32, col_ws=[520, 352], color=cl, fs=12.5)
    hbox(ax, 44, 480, W - 88, 38,
         'ポイント：モデルを「作ること」より、データ理解と結果解釈の方が圧倒的に時間がかかります',
         '#EAFAF1', '#5BA85A', tc='#1E8449', fs=12)
    slides.append(('03_ds_flow', fig))

    # 0-4 スケジュール
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '本日のスケジュール')
    table(ax,
          ['時間', 'チャプター', '内容', '形式'],
          [['9:00〜9:20', 'オリエンテーション', '今日の流れ・生成AIルール', '座学'],
           ['9:20〜10:20', 'Ch.1 データ読み込み・集計', 'pandas 基本操作', '座学20分＋演習40分'],
           ['10:30〜11:30', 'Ch.2 データ可視化・EDA', 'matplotlib / seaborn', '座学20分＋演習40分'],
           ['11:30〜12:30', 'Ch.3 画像処理入門', 'Pillow × NumPy', '座学20分＋演習40分'],
           ['13:30〜14:30', 'Ch.4 機械学習モデル構築', 'scikit-learn', '座学20分＋演習40分'],
           ['14:40〜16:10', 'Ch.5 総合演習', '乳がん診断データで自力実装', '演習90分'],
           ['16:10〜16:30', 'まとめ・振り返り', '気づきの整理・次のステップ', '座学']],
          y=60, row_h=32, col_ws=[140, 260, 360, 112], color=cl, fs=11.5)
    slides.append(('04_schedule', fig))

    # 0-5 生成AIルール
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '生成AIの活用ルール（本日共通）')
    txt(ax, W//2, 90, '生成AIは「賢いコーディング補助ツール」です', fs=14,
        color='#2C3E50', bold=True, ha='center')
    two_col(ax,
        {'title': '✅ AIに任せてよいこと',
         'items': ['コードの書き方がわからない', 'ライブラリのオプションを調べたい',
                   'エラーメッセージを修正したい', 'グラフの見た目を整えたい',
                   'ボイラープレートを生成したい']},
        {'title': '⚡ 自分でやること',
         'items': ['何を分析するかを決める', 'グラフから仮説を立てる',
                   '欠損値の処理方針を判断する', '結果の数値を解釈する',
                   'ビジネス上の示唆を導き出す']},
        y0=108, col_h=310,
        lbg='#EBF5FB', lbc='#4A90D9', rbg='#FEF9E7', rbc='#E8A838')
    hbox(ax, 44, 432, W - 88, 40,
         '「AIのコードが多すぎてわからない」を防ぐため、コードは少しずつ生成させましょう',
         '#FDEDEC', '#C0392B', tc='#922B21', fs=12)
    slides.append(('05_ai_rules', fig))

    # 0-6 プロンプトテンプレート
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'AIへの質問の仕方：プロンプトテンプレート')
    code_block(ax,
               '【目的】ワインデータの品種ごとにアルコール度数の平均を集計したい\n'
               '【使うライブラリ】pandas\n'
               '【制約】Python 3.8、インターネット接続なし、外部ライブラリ追加不可\n'
               '【わからない点】groupby の書き方を教えてください',
               44, 92, W - 88, 100)
    table(ax,
          ['悪いプロンプト例', '問題点'],
          [['「機械学習のコードを書いて」', '範囲が広すぎる → 理解できないコードが大量に出る'],
           ['「このデータを分析して」', '分析の目的が決まっていない'],
           ['「エラーを直して」（コードを貼るだけ）', 'なぜエラーが起きたか理解できない']],
          y=210, row_h=36, col_ws=[300, 572], color='#C0392B', fs=12)
    hbox(ax, 44, 440, W - 88, 40,
         '🔑 目的 → ライブラリ → 制約 → わからない点 の4点を必ず書く',
         '#EAFAF1', '#5BA85A', tc='#1E8449', fs=13)
    slides.append(('06_prompt', fig))

    # 0-7 使用データ
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '本日の環境と使用データ')
    hbox(ax, 44, 80, W - 88, 50,
         '🖥️ 環境：ローカル Jupyter Lab（インターネット接続不要）\n'
         '📦 ライブラリ：インストール済み環境のみ使用（追加インストール不要）',
         '#EBF5FB', '#4A90D9', tc='#1A5276', fs=12.5)
    table(ax,
          ['チャプター', 'データセット', '概要', '読み込み方'],
          [['Ch.1〜4', 'ワインデータ load_wine()', 'イタリア産ワイン 178件・13特徴量・3品種', 'sklearn.datasets'],
           ['Ch.3', '手書き数字 load_digits()', '手書き数字 1,797枚・8×8ピクセル', 'sklearn.datasets'],
           ['Ch.5', '乳がん診断 load_breast_cancer()', '腫瘍データ 569件・30特徴量・2クラス', 'sklearn.datasets']],
          y=148, row_h=40, col_ws=[100, 230, 390, 152], color=cl, fs=11.5)
    hbox(ax, 44, 432, W - 88, 40,
         '✅ すべて scikit-learn 内蔵データ → 追加ダウンロード不要',
         '#EAFAF1', '#5BA85A', tc='#1E8449', fs=13)
    slides.append(('07_data', fig))

    # 0-8 動作確認
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '動作確認をしましょう')
    txt(ax, 44, 80, 'notebooks/ch1_data_analysis.ipynb を Jupyter Lab で開き、最初のセルを実行してください',
        fs=12, color='#7f8c8d')
    code_block(ax,
               'import pandas as pd\nimport numpy as np\n'
               'import matplotlib.pyplot as plt\nimport seaborn as sns\n'
               'import japanize_matplotlib\nfrom sklearn.datasets import load_wine\n'
               'from PIL import Image, ImageFilter\n\nprint("準備OK！")',
               44, 104, W - 88, 200)
    bullets(ax, [
        {'text': 'エラーなく実行できた → 準備完了です！', 'emoji': '✅'},
        {'text': 'エラーが出た場合 → 講師に申し出てください', 'emoji': '⚠️'},
    ], y0=322, lh=36, accent=cl)
    slides.append(('08_check', fig))

    return slides

# ================================================================
#  Chapter 1: データ読み込み・集計
# ================================================================

def gen_ch1():
    ch = 'ch1'; cl = C[ch]; lbl = 'Ch.1 データ読み込み・集計'
    slides = []

    # 1-1 タイトル
    slides.append(('01_title',
        title_slide('Ch.1 ／ 9:20〜10:20', 'データ読み込み・集計',
                    'pandas で始めるデータ分析の第一歩',
                    '座学 20分 ＋ 演習 40分', cl)))

    # 1-2 できること
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'この章で「できるようになること」')
    steps(ax, [
        ('1', 'データを読み込んで「何件・何列ある？」を確認できる',
         'head() / info() / describe()'),
        ('2', '欠損値（空白データ）を見つけて処理できる',
         'isnull() / fillna() / dropna()'),
        ('3', '条件でデータを絞り込み（フィルタリング）できる',
         'df[ df["列"] > 値 ]'),
        ('4', 'グループごとに集計して傾向を掴める',
         'groupby("品種").mean()'),
    ], y0=100, accent=cl)
    slides.append(('02_goals', fig))

    # 1-3 pandasとは
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'pandas とは')
    hbox(ax, 44, 82, W - 88, 44,
         'Python でデータ分析をするための最重要ライブラリ。「行×列」の表形式データ（DataFrame）を自在に操作できる',
         '#EBF5FB', '#4A90D9', tc='#1A5276', fs=13)
    two_col(ax,
        {'title': 'Excel でできること',
         'items': ['表の表示・編集', 'フィルタリング', '集計・ピボット', 'グラフ作成']},
        {'title': 'pandas でできること（＋α）',
         'items': ['Excelと同じことがすべてできる', '大量データ（数百万件）も高速処理',
                   '自動化・再現性（コードで記録）', '機械学習との連携']},
        y0=138, col_h=250,
        lbg='#f0f8ff', lbc='#4A90D9', rbg='#e8f8e8', rbc='#5BA85A')
    hbox(ax, 44, 408, W - 88, 40,
         'データサイエンティストが毎日使う基本ツール',
         '#EAFAF1', '#5BA85A', tc='#1E8449', fs=13)
    slides.append(('03_pandas', fig))

    # 1-4 3つのメソッド
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'データを手に入れたら：必ずこの3つを実行')
    table(ax,
          ['メソッド', '何がわかるか', '確認するポイント'],
          [['df.head()', '先頭5行を表示', '列名・値の形式・データの「顔」'],
           ['df.info()', '列名・データ型・欠損件数', '型が正しいか・欠損がないか'],
           ['df.describe()', '平均・最大・最小・標準偏差', '異常に大きい値・値の範囲']],
          y=100, row_h=40, col_ws=[200, 220, 452], color=cl, fs=12.5)
    code_block(ax,
               'wine = load_wine()\ndf = pd.DataFrame(wine.data, columns=wine.feature_names)\n\n'
               'df.head()      # 先頭確認\ndf.info()      # 型・欠損確認\ndf.describe()  # 統計量確認',
               44, 260, W - 88, 140)
    slides.append(('04_methods', fig))

    # 1-5 欠損値とは
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '欠損値（NaN）とは')
    hbox(ax, 44, 82, W - 88, 52,
         '⚠️ 現実のデータには必ず「空白」が存在します。そのままモデルに入れるとエラーになります。',
         '#FEF9E7', '#E8A838', tc='#7D6608', fs=13)
    bullets(ax, [
        {'text': 'NaN = Not a Number（値が記録されていない）',
         'sub': '原因：入力ミス・センサー故障・アンケート未回答 など'},
        {'text': '確認方法：df.isnull().sum() で各列の欠損件数を表示'},
        {'text': '欠損率：df.isnull().sum() / len(df) * 100'},
    ], y0=150, lh=42, accent=cl)
    code_block(ax,
               '# 各列の欠損件数を確認\ndf.isnull().sum()\n\n'
               '# 欠損率（%）を確認\n(df.isnull().sum() / len(df) * 100).round(1)',
               44, 330, W - 88, 130)
    slides.append(('05_nan', fig))

    # 1-6 欠損値の処理方針
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '欠損値の処理方針')
    table(ax,
          ['方法', 'コード', '使う場面', 'リスク'],
          [['削除', 'df.dropna()', '欠損が少量かつランダムな場合', 'データ量が減る'],
           ['平均値で補完', 'df.fillna(df.mean())', '数値データで欠損が一定量ある場合', '分布が変わる可能性'],
           ['グループ別平均', 'groupby + transform', 'グループ間に差がある場合', 'コードが複雑']],
          y=100, row_h=44, col_ws=[150, 220, 310, 192], color=cl, fs=12)
    hbox(ax, 44, 344, W - 88, 44,
         '⚠️ 「どれが正解」は一概に言えない。データの性質とビジネス要件に合わせて判断する',
         '#FEF9E7', '#E8A838', tc='#7D6608', fs=13)
    slides.append(('06_nan_handling', fig))

    # 1-7 フィルタリングと集計
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'フィルタリングと集計')
    txt(ax, 44, 90, '🔍 フィルタリング：条件で絞り込む', fs=13, color=cl, bold=True)
    code_block(ax,
               '# アルコール度数が 13.5 以上\nhigh_alc = df[df["alcohol"] >= 13.5]\n\n'
               '# 複数条件（& で AND）\nfiltered = df[(df["alcohol"] >= 13.5) & (df["color_intensity"] >= 5.0)]',
               44, 110, W - 88, 112)
    txt(ax, 44, 236, '📊 groupby：グループごとに集計する', fs=13, color=cl, bold=True)
    code_block(ax,
               '# 品種ごとの平均を集計\ndf.groupby("品種")[["alcohol", "proline"]].mean().round(2)\n\n'
               '# ソート\ndf.sort_values("proline", ascending=False).head()',
               44, 256, W - 88, 112)
    hbox(ax, 44, 380, W - 88, 40,
         '実務例：「都道府県ごと」「月ごと」の売上平均集計が groupby 一発で出来る',
         '#EBF5FB', '#4A90D9', tc='#1A5276', fs=12.5)
    slides.append(('07_filter', fig))

    # 1-8 演習の進め方
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '演習の進め方（40分）')
    txt(ax, 44, 88, 'notebooks/ch1_data_analysis.ipynb の演習セクション',
        fs=12, color='#7f8c8d')
    steps(ax, [
        ('問1', '品種ごとのデータ件数を確認する', 'ヒント：value_counts()'),
        ('問2', 'プロリン含有量が最も多い品種を特定する', 'ヒント：groupby → mean → sort_values'),
        ('問3', 'アルコール度数が高く色が濃いワインを絞り込む', 'ヒント：複数条件フィルタ'),
        ('問4', '（発展）欠損値補完を品種ごとの平均に変更する', 'ヒント：groupby + transform'),
    ], y0=106, accent=cl)
    hbox(ax, 44, 430, W - 88, 40,
         '✅ 問3まで完了すれば十分です。問4は発展問題です。',
         '#EAFAF1', '#5BA85A', tc='#1E8449', fs=12.5)
    slides.append(('08_exercise', fig))

    # 1-9 まとめ
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'Ch.1 まとめ')
    table(ax,
          ['操作', 'コード', 'ポイント'],
          [['形を確認', 'head() / info() / describe()', 'この3つを最初に必ず実行'],
           ['欠損値確認', 'isnull().sum()', '欠損があるか確認してから進む'],
           ['欠損値補完', 'fillna(平均値)', '削除か補完かはデータ次第'],
           ['フィルタ', 'df[df["列"] > 値]', '条件に合う行だけ取り出す'],
           ['集計', 'groupby("列").mean()', 'グループごとの傾向を掴む']],
          y=88, row_h=36, col_ws=[180, 300, 392], color=cl, fs=12)
    hbox(ax, 44, 390, W - 88, 44,
         '➡️ 次は Ch.2 データ可視化・EDA：集計で見えた数値を「グラフ」で直感的に理解します',
         '#EBF5FB', '#4A90D9', tc='#1A5276', fs=13)
    slides.append(('09_summary', fig))

    return slides

# ================================================================
#  Chapter 2: データ可視化・EDA
# ================================================================

def gen_ch2():
    ch = 'ch2'; cl = C[ch]; lbl = 'Ch.2 データ可視化・EDA'
    slides = []

    slides.append(('01_title',
        title_slide('Ch.2 ／ 10:30〜11:30', 'データ可視化・EDA',
                    'グラフから「仮説」を立てる探索的データ分析',
                    '座学 20分 ＋ 演習 40分', cl)))

    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'EDA（探索的データ分析）とは')
    hbox(ax, 44, 82, W - 88, 52,
         'モデルを作る前に、データの 特徴・傾向・外れ値・相関 を可視化によって把握する作業',
         '#EAFAF1', '#5BA85A', tc='#1E8449', fs=13.5)
    two_col(ax,
        {'title': '❌ EDA をしないと…',
         'items': ['データの異常に気づかない', '重要でない変数にも同じ手間をかける',
                   'モデルの結果が「なぜか」わからない', '間違った仮説でモデルを作ってしまう']},
        {'title': '✅ EDA をすると…',
         'items': ['欠損・外れ値を早期発見できる', '効果的な変数を絞り込める',
                   '「この変数が重要そう」と仮説が立てられる', 'モデルの結果を説明できる']},
        y0=148, col_h=240,
        lbg='#FDEDEC', lbc='#C0392B', rbg='#EAFAF1', rbc='#5BA85A')
    hbox(ax, 44, 412, W - 88, 40,
         'データサイエンティストの業務時間の 20〜30% は EDA が占めます',
         '#EBF5FB', '#4A90D9', tc='#1A5276', fs=12.5)
    slides.append(('02_eda', fig))

    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'グラフの種類と使い分け')
    txt(ax, 44, 88, '「何を見たいか」でグラフを選ぶ', fs=13, color=cl, bold=True)
    table(ax,
          ['グラフ', 'コード', '目的', '例'],
          [['📊 ヒストグラム', 'plt.hist()', '1変数の分布の形を見る', '年齢・売上の分布'],
           ['📦 箱ひげ図', 'df.boxplot()', 'グループ間の分布を比較', '地域別の気温比較'],
           ['🔵 散布図', 'plt.scatter()', '2変数の関係を見る', '身長と体重の関係'],
           ['🌡️ ヒートマップ', 'sns.heatmap()', '多変数の相関を一覧', '特徴量間の相関係数'],
           ['📈 棒グラフ', 'plt.bar()', 'グループ間の値を比較', '品種ごとの平均値']],
          y=108, row_h=36, col_ws=[200, 200, 260, 212], color=cl, fs=12)
    hbox(ax, 44, 408, W - 88, 40,
         '💡 グラフ生成のコードは AIに任せてOK。「何を見たいか」を決めるのが自分の仕事です',
         '#FEF9E7', '#E8A838', tc='#7D6608', fs=12.5)
    slides.append(('03_graph_types', fig))

    # ヒストグラム
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'ヒストグラム：データの分布を見る')
    bullets(ax, [
        {'text': '横軸：値の範囲', 'sub': '縦軸：その範囲に含まれるデータ件数'},
        {'text': '山が左に偏っている → 低い値が多い'},
        {'text': '2つの山がある → 2つのグループが混在？'},
        {'text': '品種別に色分けすることで「品種ごとの違い」がわかる'},
    ], y0=100, lh=38, accent=cl)
    code_block(ax,
               '# 品種ごとのヒストグラム\nfor name, group in df.groupby("品種"):\n'
               '    plt.hist(group["alcohol"], bins=15, alpha=0.6, label=name)\n'
               'plt.legend()\nplt.show()',
               44, 312, W - 88, 100)
    hbox(ax, 44, 426, W - 88, 40,
         '🔍 観察：Barolo は他の品種よりアルコール度数が高い傾向がある',
         '#EAFAF1', '#5BA85A', tc='#1E8449', fs=12.5)
    slides.append(('04_histogram', fig))

    # 箱ひげ図
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '箱ひげ図：グループ間の分布を比較する')
    table(ax,
          ['要素', '意味'],
          [['中央の線（赤）', '中央値（Q2）：データを半分に分ける値'],
           ['箱の上端', '第3四分位数（Q3）：上位25%の境界'],
           ['箱の下端', '第1四分位数（Q1）：下位25%の境界'],
           ['ひげの先', '外れ値以外の最大・最小'],
           ['点（◆）', '外れ値']],
          y=100, row_h=36, col_ws=[200, 672], color=cl, fs=12.5)
    code_block(ax,
               'df.boxplot(column="color_intensity", by="品種",\n'
               '           medianprops=dict(color="red", linewidth=2))\nplt.show()',
               44, 332, W - 88, 68)
    hbox(ax, 44, 414, W - 88, 40,
         '🔍 観察：Barolo は色が特に濃く、Grignolino は淡い傾向がある',
         '#EAFAF1', '#5BA85A', tc='#1E8449', fs=12.5)
    slides.append(('05_boxplot', fig))

    # 散布図と相関
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '散布図と相関係数')
    table(ax,
          ['相関係数 r', '意味'],
          [['r ≈ +1', '強い正の相関（一方が増えると他方も増える）'],
           ['r ≈ 0', '相関なし（2変数に関係がない）'],
           ['r ≈ −1', '強い負の相関（一方が増えると他方は減る）']],
          y=96, row_h=40, col_ws=[160, 712], color=cl, fs=13)
    code_block(ax,
               '# 相関行列とヒートマップ\ncorr = df.corr()\nsns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0)',
               44, 270, W - 88, 76)
    hbox(ax, 44, 360, W - 88, 44,
         '⚠️ 相関 ≠ 因果関係\n例）アイスが売れると溺死者が増える → 原因は「夏（気温）」',
         '#FEF9E7', '#E8A838', tc='#7D6608', fs=12.5)
    hbox(ax, 44, 420, W - 88, 40,
         '💡 相関が高い変数 = 予測に使える候補（ただし多重共線性に注意）',
         '#EBF5FB', '#4A90D9', tc='#1A5276', fs=12.5)
    slides.append(('06_scatter', fig))

    # EDAフロー
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'EDA の標準フロー（実務でも使えます）')
    steps(ax, [
        ('1', 'データの形を確認（Ch.1で学習済み）',
         'head() / info() / describe() / isnull().sum()'),
        ('2', '各変数の分布を見る',
         'ヒストグラム・箱ひげ図 → 外れ値・歪みを発見'),
        ('3', 'グループ間の違いを比較する',
         '品種/カテゴリ別の箱ひげ図・棒グラフ'),
        ('4', '変数間の関係を確認する',
         '散布図・相関ヒートマップ → 重要な変数の候補を特定'),
        ('5', '気づきを「仮説」として言語化する',
         '「〇〇が高い品種は △△ も高い → 分類に効きそう」'),
    ], y0=96, accent=cl)
    slides.append(('07_eda_flow', fig))

    # 演習
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '演習の進め方（40分）')
    txt(ax, 44, 88, 'notebooks/ch2_visualization.ipynb の演習セクション',
        fs=12, color='#7f8c8d')
    steps(ax, [
        ('問1', '棒グラフで品種ごとの平均アルコール度数を比較する',
         'コードはAIで生成OK'),
        ('問2', '相関ヒートマップを参考に2変数を選んで散布図を作る',
         '「なぜその変数を選んだか」を必ず記録する'),
        ('問3', 'グラフから「仮説」を1つ言語化する',
         '「〇〇という特徴量が △△ という理由から品種の分類に効くと思う」'),
    ], y0=108, accent=cl)
    hbox(ax, 44, 424, W - 88, 44,
         '⚡ 問3の「仮説の言語化」が最も重要です。グラフを作るだけで終わらないように！',
         '#FEF9E7', '#E8A838', tc='#7D6608', fs=12.5)
    slides.append(('08_exercise', fig))

    # まとめ
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'Ch.2 まとめ')
    table(ax,
          ['グラフ', 'コード', '使い場面'],
          [['ヒストグラム', 'plt.hist()', '1変数の分布を確認'],
           ['箱ひげ図', 'df.boxplot()', 'グループ間の比較'],
           ['散布図', 'plt.scatter()', '2変数の関係確認'],
           ['相関ヒートマップ', 'sns.heatmap(df.corr())', '全変数の相関を一覧']],
          y=88, row_h=40, col_ws=[200, 280, 392], color=cl, fs=12.5)
    hbox(ax, 44, 360, W - 88, 48,
         '🔑 EDA の本当の目的は「グラフを作ること」ではなく、「仮説を立てること」',
         '#EAFAF1', '#5BA85A', tc='#1E8449', fs=13.5)
    hbox(ax, 44, 422, W - 88, 40,
         '➡️ 次は Ch.3 画像処理入門：数値データの次は「画像データ」を扱います',
         '#EBF5FB', '#4A90D9', tc='#1A5276', fs=12.5)
    slides.append(('09_summary', fig))

    return slides

# ================================================================
#  Chapter 3: 画像処理入門
# ================================================================

def gen_ch3():
    ch = 'ch3'; cl = C[ch]; lbl = 'Ch.3 画像処理入門'
    slides = []

    slides.append(('01_title',
        title_slide('Ch.3 ／ 11:30〜12:30', '画像処理入門',
                    'Pillow × NumPy で学ぶ「画像 ＝ 数値の配列」',
                    '座学 20分 ＋ 演習 40分', cl)))

    # ユースケース
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'なぜ画像処理を学ぶのか')
    txt(ax, 44, 86, '画像はデータの一種 → Python で扱える → 実務で広く使われている',
        fs=13, color='#7f8c8d')
    uc = [
        ('🏭 製造業', '製品の傷・欠陥を\n自動検出'),
        ('🏥 医療', 'レントゲン・MRI\n画像の解析'),
        ('🏪 小売・物流', '商品の棚卸し\n在庫確認'),
        ('🏦 金融', '書類・帳票の\n文字認識（OCR）'),
        ('🌾 農業', '衛星画像で\n生育状況を分析'),
    ]
    bw = (W - 88 - 16 * 4) // 5
    for i, (title_t, desc) in enumerate(uc):
        colors_u = [C['ch1'], C['ch2'], C['ch3'], C['ch4'], C['summary']]
        rect(ax, 44 + i * (bw + 16), 112, bw, 160,
             fc=colors_u[i], ec='none', radius=6)
        txt(ax, 44 + i * (bw + 16) + bw//2, 128, title_t, fs=12, color='white',
            bold=True, ha='center')
        for j, ln in enumerate(desc.split('\n')):
            txt(ax, 44 + i * (bw + 16) + bw//2, 160 + j * 22, ln, fs=11.5,
                color=(1.000, 1.000, 1.000, 0.90), ha='center')
    hbox(ax, 44, 294, W - 88, 44,
         '今日学ぶこと：画像の正体（数値配列）、Pillowでの基本操作、フィルタ処理',
         '#FEF9E7', '#E8A838', tc='#7D6608', fs=13)
    slides.append(('02_usecases', fig))

    # 画像の正体
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '画像の正体：数値の2次元配列')
    hbox(ax, 44, 82, W - 88, 40,
         '「画像を見る」＝「数値の表を見る」（8×8ピクセルの手書き数字「0」の場合）',
         '#FEF9E7', '#E8A838', tc='#7D6608', fs=12.5)
    # ピクセルグリッド（数値表示）
    sample = [[0,0,5,13,9,1,0,0],[0,0,13,15,10,15,5,0],[0,3,15,2,0,11,8,0],
              [0,4,12,0,0,8,8,0],[0,5,8,0,0,9,8,0],[0,4,11,0,1,12,7,0],
              [0,2,14,5,10,12,0,0],[0,0,6,13,10,0,0,0]]
    cell = 36
    for r_i, row in enumerate(sample):
        for c_i, val in enumerate(row):
            brightness = 1.0 - val / 16.0
            fc = f'#{int(brightness*255):02x}{int(brightness*255):02x}{int(brightness*255):02x}'
            rect(ax, 44 + c_i * cell, 136 + r_i * cell, cell - 1, cell - 1, fc=fc, ec='#ddd', lw=0.5)
            tc = 'black' if brightness > 0.4 else 'white'
            txt(ax, 44 + c_i * cell + cell//2, 136 + r_i * cell + cell//2,
                str(val), fs=9, color=tc, ha='center', va='center')
    txt(ax, 44, 436, '数値配列（0〜16）', fs=11, color='#7f8c8d')
    # グレースケール画像
    for r_i, row in enumerate(sample):
        for c_i, val in enumerate(row):
            brightness = 1.0 - val / 16.0
            fc = f'#{int(brightness*255):02x}{int(brightness*255):02x}{int(brightness*255):02x}'
            rect(ax, 380 + c_i * cell, 136 + r_i * cell, cell - 1, cell - 1, fc=fc, ec='none')
    txt(ax, 380, 436, '画像として表示', fs=11, color='#7f8c8d')
    hbox(ax, 600, 136, W - 644, 260,
         '値が大きい（16）\n→ 明るい（白）\n\n値が小さい（0）\n→ 暗い（黒）\n\n画像 ＝ 数値配列\nだから NumPy で\n計算・統計処理できる！',
         '#EAFAF1', '#5BA85A', tc='#1E8449', fs=12)
    slides.append(('03_pixel', fig))

    # グレースケールとRGB
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'グレースケールとカラー（RGB）の違い')
    two_col(ax,
        {'title': '🔲 グレースケール',
         'items': ['1チャンネル（明るさのみ）',
                   '配列の形：(縦, 横)',
                   '値の範囲：0〜255',
                   '色情報なし']},
        {'title': '🌈 カラー（RGB）',
         'items': ['3チャンネル（赤・緑・青）',
                   '配列の形：(縦, 横, 3)',
                   '各チャンネルの値：0〜255',
                   '3つの数値の組み合わせで色を表現']},
        y0=100, col_h=180, lbg='#f8f8f8', lbc='#BDC3C7', rbg='#FFF3E0', rbc='#E8A838')
    hbox(ax, 44, 298, W - 88, 52,
         'グレースケール変換とは？\n色情報（RGB）を捨てて、明るさだけを残す処理',
         '#FDEDEC', '#C0392B', tc='#922B21', fs=12.5)
    code_block(ax,
               '# カラー画像をグレースケールに変換\nimg = Image.open("photo.jpg")  # mode = "RGB"\n'
               'img_gray = img.convert("L")       # mode = "L"（グレースケール）',
               44, 366, W - 88, 76)
    hbox(ax, 44, 456, W - 88, 40,
         '💡 グレースケール変換後は「赤と緑の区別」ができなくなる（色情報の喪失）',
         '#FEF9E7', '#E8A838', tc='#7D6608', fs=12.5)
    slides.append(('04_grayscale', fig))

    # Pillowの基本操作
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'Pillow（PIL）の基本操作')
    txt(ax, 44, 84, 'numpy array ↔ PIL Image の変換が基本', fs=12, color='#7f8c8d')
    flow(ax,
         ['numpy array\n(数値の配列)', 'PIL Image\n(画像オブジェクト)', 'resize/filter\n/convert', '処理後の\nPIL Image'],
         y=104, h=64,
         colors=[C['ch1'], C['ch3'], C['ch2'], C['ch4']])
    code_block(ax,
               '# numpy array → PIL Image\narr_scaled = (digits.images[0] / 16.0 * 255).astype(np.uint8)\n'
               'img = Image.fromarray(arr_scaled, mode="L")\n\n'
               '# リサイズ（8×8 → 80×80）\nimg_large = img.resize((80, 80), Image.NEAREST)\n\n'
               '# PIL Image → numpy array\narr_back = np.array(img_large)   # shape: (80, 80)',
               44, 186, W - 88, 180)
    slides.append(('05_pillow', fig))

    # フィルタ処理
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'フィルタ処理：画像の見え方を変える')
    table(ax,
          ['フィルタ名', '効果'],
          [['BLUR', '周辺ピクセルの平均 → エッジがなめらかに（ぼかし）'],
           ['SHARPEN', '中心を強調 → エッジが際立つ（シャープ化）'],
           ['CONTOUR', '差分を抽出 → 境界線（輪郭）だけが残る'],
           ['EMBOSS', '凹凸感を表現（浮き彫り）'],
           ['SMOOTH', 'BLURより弱いなめらかさ']],
          y=96, row_h=36, col_ws=[180, 692], color=cl, fs=12.5)
    code_block(ax,
               'from PIL import Image, ImageFilter\n\n'
               'img_blur    = img.filter(ImageFilter.BLUR)\n'
               'img_contour = img.filter(ImageFilter.CONTOUR)\n'
               'img_sharp   = img.filter(ImageFilter.SHARPEN)',
               44, 302, W - 88, 100)
    hbox(ax, 44, 416, W - 88, 44,
         'フィルタの仕組み：周辺ピクセルの値を使った計算（畳み込み演算）',
         '#EBF5FB', '#4A90D9', tc='#1A5276', fs=13)
    slides.append(('06_filter', fig))

    # ピクセル統計
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '画像データの統計分析')
    hbox(ax, 44, 82, W - 88, 44,
         '画像 ＝ 数値 → 統計量を計算できる → 機械学習の特徴量として使える！',
         '#EAFAF1', '#5BA85A', tc='#1E8449', fs=13.5)
    bullets(ax, [
        {'text': '平均ピクセル値 → 画像の「明るさ」を数値化'},
        {'text': '標準偏差 → 明暗のばらつき（コントラスト）'},
        {'text': '最大・最小 → 最も明るい/暗い箇所'},
        {'text': '0超のピクセル数 → 「描かれている量」'},
    ], y0=142, lh=34, accent=cl)
    code_block(ax,
               'arr = np.array(img_large)\n\n'
               'print("明るさ（平均）:", arr.mean())\n'
               'print("コントラスト:", arr.std())\n'
               'print("描画率:", (arr > 0).mean() * 100, "%")',
               44, 330, W - 88, 120)
    slides.append(('07_stats', fig))

    # 演習
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '演習の進め方（40分）')
    txt(ax, 44, 88, 'notebooks/ch3_image_processing.ipynb の演習セクション',
        fs=12, color='#7f8c8d')
    steps(ax, [
        ('問1', '好きな数字（0〜9）を選んで、フィルタ処理の前後を並べて表示する', ''),
        ('問2', '同じ数字の複数枚を並べて表示し、手書きのばらつきを確認する',
         '→ AIにとって「なぜ難しいか」を体感する'),
        ('問3', 'フィルタ前後でピクセル値の統計がどう変わるか確認する',
         '→ なぜ変化するか理由を考えましょう'),
        ('問4', '（発展）NumPyで2値化処理（閾値でモノクロに変換）を実装する',
         'ヒント：np.where(条件, 255, 0)'),
    ], y0=108, accent=cl)
    slides.append(('08_exercise', fig))

    # まとめ
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'Ch.3 まとめ')
    table(ax,
          ['操作', 'コード'],
          [['numpy → PIL Image', 'Image.fromarray(arr, mode="L")'],
           ['PIL Image → numpy', 'np.array(img)'],
           ['リサイズ', 'img.resize((幅, 高さ), Image.NEAREST)'],
           ['グレースケール変換', 'img.convert("L")'],
           ['フィルタ適用', 'img.filter(ImageFilter.BLUR)'],
           ['ピクセル統計', 'np.array(img).mean() / .std()']],
          y=88, row_h=34, col_ws=[240, 632], color=cl, fs=12.5)
    hbox(ax, 44, 406, W - 88, 42,
         '🔑 画像 ＝ 数値の2次元配列。だから NumPy で統計処理・機械学習に活用できる',
         '#EAFAF1', '#5BA85A', tc='#1E8449', fs=13)
    hbox(ax, 44, 460, W - 88, 38,
         '➡️ 午後は Ch.4 機械学習モデル構築。いよいよモデルを作ります！',
         '#EBF5FB', '#4A90D9', tc='#1A5276', fs=12.5)
    slides.append(('09_summary', fig))

    return slides

# ================================================================
#  Chapter 4: 機械学習モデル構築
# ================================================================

def gen_ch4():
    ch = 'ch4'; cl = C[ch]; lbl = 'Ch.4 機械学習モデル構築'
    slides = []

    slides.append(('01_title',
        title_slide('Ch.4 ／ 13:30〜14:30', '機械学習モデル構築',
                    'scikit-learn で学ぶデータ → 学習 → 評価の流れ',
                    '座学 20分 ＋ 演習 40分', cl)))

    # ワークフロー
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '機械学習の全体ワークフロー')
    flow(ax,
         ['① データ準備\n・分割', '② 前処理\nスケーリング', '③ モデル\n学習', '④ 予測', '⑤ 評価'],
         y=108, h=72,
         colors=[C['ch1'], C['ch2'], C['ch3'], C['ch4'], C['summary']])
    table(ax,
          ['ステップ', 'コード', '目的'],
          [['①', 'train_test_split()', '学習用データとテスト用データを分ける'],
           ['②', 'StandardScaler()', '変数のスケール（大きさ）を揃える'],
           ['③', 'model.fit(X_train, y_train)', '訓練データでモデルを学習する'],
           ['④', 'model.predict(X_test)', 'テストデータで予測値を出力する'],
           ['⑤', 'accuracy_score() / confusion_matrix()', '予測の正確さを測る']],
          y=198, row_h=34, col_ws=[60, 300, 512], color=cl, fs=12)
    slides.append(('02_workflow', fig))

    # データ分割
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'なぜデータを「分割」するのか')
    # bar visualization
    rect(ax, 44, 90, 780, 52, fc='#4A90D9', radius=4)
    rect(ax, 836, 90, 96, 52, fc='#E8A838', radius=4)
    txt(ax, 44 + 390, 116, '訓練データ（80% = 142件）', fs=13, color='white', bold=True, ha='center', va='center')
    txt(ax, 836 + 48, 116, 'テスト\n（20%）', fs=11, color='white', bold=True, ha='center', va='center')
    two_col(ax,
        {'title': '❌ なぜ「覚えたデータで答え合わせ」はダメか？',
         'items': ['丸暗記のように見えて実力がわからない（過学習）',
                   '本番環境での性能が予測できない']},
        {'title': '✅ テストデータ ＝「未知のデータ」',
         'items': ['本番環境での性能を事前に確認できる',
                   '「試験で練習問題 ≠ 本番問題」にする']},
        y0=158, col_h=180, lbg='#FDEDEC', lbc='#C0392B', rbg='#EAFAF1', rbc='#5BA85A')
    code_block(ax,
               'X_train, X_test, y_train, y_test = train_test_split(\n'
               '    X, y, test_size=0.2, random_state=42, stratify=y  # stratify: 品種比率を保つ\n)',
               44, 356, W - 88, 72)
    slides.append(('03_split', fig))

    # スケーリング
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'なぜスケーリングが必要か')
    hbox(ax, 44, 82, W - 88, 48,
         '⚠️ アルコール度数（約12〜15）とプロリン含有量（約278〜1680）→ スケールが全く違う！\n'
         '→ 大きい値の変数が不当に影響力を持ってしまう',
         '#FDEDEC', '#C0392B', tc='#922B21', fs=12.5)
    hbox(ax, 44, 144, W - 88, 44,
         'StandardScaler：各変数を 平均0・標準偏差1 になるよう変換 → すべての変数のスケールが揃う',
         '#EBF5FB', '#4A90D9', tc='#1A5276', fs=12.5)
    code_block(ax,
               'scaler = StandardScaler()\n\n'
               '# fit は訓練データのみ！\nX_train_scaled = scaler.fit_transform(X_train)\n\n'
               '# テストデータは transform のみ\nX_test_scaled = scaler.transform(X_test)\n\n'
               '# ❌ 絶対NG: scaler.fit_transform(X_test) ← データリーク！',
               44, 202, W - 88, 180)
    hbox(ax, 44, 396, W - 88, 48,
         '🔑 最重要ルール：scaler.fit() は訓練データのみ！\nテストデータには transform() だけを使う（データリーク防止）',
         '#FDEDEC', '#C0392B', tc='#922B21', fs=13)
    slides.append(('04_scaling', fig))

    # ランダムフォレスト
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'ランダムフォレストとは')
    txt(ax, W//2, 84, '「たくさんの決定木の多数決」', fs=16, color=cl, bold=True, ha='center')
    # 3 trees
    tc = [C['ch1'], C['ch2'], C['ch3']]
    preds = ['Barolo', 'Barolo', 'Grignolino']
    for i in range(3):
        x_c = 140 + i * 200
        rect(ax, x_c - 70, 110, 140, 120, fc=tc[i], ec='none', radius=6)
        txt(ax, x_c, 130, f'決定木 {i+1}', fs=12, color='white', bold=True, ha='center')
        txt(ax, x_c, 165, f'予測: {preds[i]}', fs=11.5, color='white', ha='center')
        txt(ax, x_c, 238, '↓', fs=14, color='#95a5a6', ha='center')
    rect(ax, 660, 110, 150, 120, fc=C['summary'], ec='none', radius=6)
    txt(ax, 735, 135, '多数決', fs=12, color='white', bold=True, ha='center')
    txt(ax, 735, 160, '最終予測:', fs=11, color='white', ha='center')
    txt(ax, 735, 182, 'Barolo (2:1)', fs=12, color='white', bold=True, ha='center')
    code_block(ax,
               'model = RandomForestClassifier(n_estimators=100, random_state=42)\nmodel.fit(X_train_scaled, y_train)\ny_pred = model.predict(X_test_scaled)',
               44, 260, W - 88, 80)
    bullets(ax, [
        {'text': '各決定木がバラバラなデータ・特徴量で学習する → 多様性が生まれる'},
        {'text': '多数決で最終結果 → 一つの木のミスをカバー（過学習しにくい）'},
    ], y0=356, lh=34, accent=cl)
    slides.append(('05_rf', fig))

    # 混同行列
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '混同行列（Confusion Matrix）の読み方')
    # 混同行列グリッド
    cx, cy, cw, ch_ = 60, 100, 350, 280
    cells = [
        ('TP（正解）', '陽性→陽性と予測', '✅', '#D5F5E3', '#1E8449'),
        ('FN（見逃し）', '陽性→陰性と予測', '⚠️', '#FDEDEC', '#922B21'),
        ('FP（誤検知）', '陰性→陽性と予測', '⚠️', '#FEF9E7', '#9A7D0A'),
        ('TN（正解）', '陰性→陰性と予測', '✅', '#D5F5E3', '#1E8449'),
    ]
    txt(ax, cx + cw//4, cy - 16, '予測: 陽性', fs=11, bold=True, ha='center', color='#555')
    txt(ax, cx + 3*cw//4, cy - 16, '予測: 陰性', fs=11, bold=True, ha='center', color='#555')
    txt(ax, cx - 18, cy + ch_//4, '実際\n: 陽性', fs=11, bold=True, ha='center', color='#555', va='center')
    txt(ax, cx - 18, cy + 3*ch_//4, '実際\n: 陰性', fs=11, bold=True, ha='center', color='#555', va='center')
    for i, (label, desc, em, bg, tc_c) in enumerate(cells):
        r_i, c_i = divmod(i, 2)
        ex = cx + c_i * cw//2; ey = cy + r_i * ch_//2
        rect(ax, ex, ey, cw//2 - 2, ch_//2 - 2, fc=bg, ec='white', lw=2)
        txt(ax, ex + cw//4, ey + 14, em, fs=15, ha='center', va='top', color=tc_c)
        txt(ax, ex + cw//4, ey + 38, label, fs=12, ha='center', bold=True, color=tc_c)
        txt(ax, ex + cw//4, ey + 58, desc, fs=10, ha='center', color=tc_c)
    # 右側の説明
    table(ax,
          ['指標', '計算式', '重視する場面'],
          [['Accuracy', '(TP+TN) / 全体', '全般的な正確さ'],
           ['Precision', 'TP / (TP+FP)', '誤検知を減らしたい場合'],
           ['Recall', 'TP / (TP+FN)', '見逃しを防ぎたい場合']],
          x=440, y=108, row_h=44, col_ws=[120, 170, 172], color=cl, fs=11.5)
    hbox(ax, 44, 404, W - 88, 44,
         '対角成分（TP + TN）= 正解した件数　対角以外 = 誤分類 → どう間違えたかが重要',
         '#FEF9E7', '#E8A838', tc='#7D6608', fs=12.5)
    slides.append(('06_confusion', fig))

    # 正解率の落とし穴
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '正解率（Accuracy）だけでは不十分な場合')
    hbox(ax, 44, 82, W - 88, 40,
         '📊 例：1,000件中 990件が「陰性」、10件が「陽性」のデータ',
         '#EBF5FB', '#4A90D9', tc='#1A5276', fs=13)
    flow(ax,
         ['「全部陰性」と\n予測するモデル', '正解率 = 99%\n（高い！）',
          '陽性10件を\n全部見逃している！', 'Recall = 0%\n使えないモデル'],
         y=138, h=72,
         colors=[C['ch1'], C['ch2'], C['ch4'], C['summary']])
    table(ax,
          ['業務シーン', '重視する指標', '理由'],
          [['医療検査（がん検診）', 'Recall（再現率）', '陽性の見逃しが命取り（FN を減らす）'],
           ['迷惑メールフィルタ', 'Precision（適合率）', '正常メールを誤削除したくない（FP を減らす）'],
           ['不良品検査', 'Recall（再現率）', '不良品の見逃しはクレームに直結']],
          y=228, row_h=40, col_ws=[200, 220, 452], color=cl, fs=12)
    hbox(ax, 44, 408, W - 88, 44,
         '🔑 正解率は必ず見る指標だが、混同行列と合わせて評価することが重要',
         '#EAFAF1', '#5BA85A', tc='#1E8449', fs=13)
    slides.append(('07_accuracy_trap', fig))

    # 特徴量重要度
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '特徴量重要度：何が予測に効いているか')
    bullets(ax, [
        {'text': 'ランダムフォレストが自動的に計算する'},
        {'text': 'どの特徴量が予測にどれだけ貢献しているか'},
        {'text': '値の合計 = 1.0　大きいほど「予測に効いている」'},
        {'text': 'Ch.2のEDAで「プロリンが重要そう」と仮説 → 特徴量重要度で検証できる！', 'emoji': '💡'},
    ], y0=100, lh=38, accent=cl)
    code_block(ax,
               'importances = pd.Series(model.feature_importances_, index=wine.feature_names)\n'
               'importances = importances.sort_values(ascending=True)\nimportances.plot(kind="barh")\nplt.title("特徴量重要度")\nplt.show()',
               44, 280, W - 88, 100)
    slides.append(('08_importance', fig))

    # まとめ
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'Ch.4 まとめ')
    table(ax,
          ['ステップ', 'コード', '重要な注意点'],
          [['データ分割', 'train_test_split(..., stratify=y)', 'stratify でクラス比を保つ'],
           ['スケーリング（学習）', 'scaler.fit_transform(X_train)', 'fit は訓練データのみ！'],
           ['スケーリング（テスト）', 'scaler.transform(X_test)', 'fit_transform は使わない'],
           ['モデル学習', 'model.fit(X_train_scaled, y_train)', '—'],
           ['評価', 'accuracy_score + confusion_matrix', '必ずセットで確認']],
          y=86, row_h=34, col_ws=[180, 310, 382], color=cl, fs=11.5)
    hbox(ax, 44, 388, (W - 88 - 16) // 2, 44,
         '🔑 最重要①\nscaler.fit は訓練データのみ（データリーク防止）',
         '#FDEDEC', '#C0392B', tc='#922B21', fs=12)
    hbox(ax, 44 + (W - 88 - 16) // 2 + 16, 388, (W - 88 - 16) // 2, 44,
         '🔑 最重要②\n正解率だけでなく混同行列も必ず確認',
         '#FDEDEC', '#C0392B', tc='#922B21', fs=12)
    hbox(ax, 44, 446, W - 88, 42,
         '➡️ 次は Ch.5 総合演習。新しいデータで Ch.1〜4 の流れを自力で実施！',
         '#EBF5FB', '#4A90D9', tc='#1A5276', fs=13)
    slides.append(('09_summary', fig))

    return slides

# ================================================================
#  Chapter 5: まとめ・振り返り
# ================================================================

def gen_ch5():
    ch = 'summary'; cl = C[ch]; lbl = 'まとめ・振り返り'
    slides = []

    slides.append(('01_title',
        title_slide('まとめ ／ 16:10〜16:30', 'まとめ・振り返り',
                    '今日1日で体験したデータサイエンティストの仕事',
                    '', cl)))

    # 今日体験したこと
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '今日体験したこと')
    items = [
        ('Ch.1\npandas', 'head/info/describe\n欠損値処理\ngroupby・filter', C['ch1']),
        ('Ch.2\nEDA', 'ヒストグラム\n箱ひげ図\n散布図・heatmap', C['ch2']),
        ('Ch.3\n画像処理', '画像＝数値配列\nPillow操作\nフィルタ処理', C['ch3']),
        ('Ch.4\n機械学習', 'train_test_split\nStandardScaler\nRF・混同行列', C['ch4']),
        ('Ch.5\n総合演習', '全部使って自力実装\n仮説→検証→解釈\nAI活用しながら', C['summary']),
    ]
    bw = (W - 88 - 16 * 4) // 5
    for i, (ch_title, content, color) in enumerate(items):
        bx = 44 + i * (bw + 16)
        rect(ax, bx, 90, bw, 260, fc=color, ec='none', radius=6)
        for j, ln in enumerate(ch_title.split('\n')):
            txt(ax, bx + bw//2, 106 + j * 22, ln, fs=13, color='white',
                bold=True, ha='center')
        for j, ln in enumerate(content.split('\n')):
            txt(ax, bx + bw//2, 160 + j * 24, ln, fs=11, color=(1.000, 1.000, 1.000, 0.90),
                ha='center')
    hbox(ax, 44, 370, W - 88, 40,
         'これが データサイエンティストの仕事の縮小版 です',
         '#EBF5FB', '#4A90D9', tc='#1A5276', fs=13)
    slides.append(('02_today', fig))

    # 仕事フロー再確認
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, 'データサイエンティストの仕事フロー（再確認）')
    flow(ax,
         ['データを\n読み込む', 'データを\n理解する(EDA)', '仮説を\n立てる',
          'モデルを\n作る', '結果を\n解釈する'],
         y=100, h=76,
         colors=[C['ch1'], C['ch2'], C['ch3'], C['ch4'], C['summary']])
    table(ax,
          ['ステップ', '今日のChapter', '使ったツール・概念'],
          [['データを読み込む', 'Ch.1', 'pandas: load_*() / head / info'],
           ['データを理解する', 'Ch.1・2', 'describe / isnull / ヒストグラム / 箱ひげ図'],
           ['仮説を立てる', 'Ch.2', '散布図 / 相関ヒートマップ / 言語化'],
           ['モデルを作る', 'Ch.4', 'train_test_split / StandardScaler / RandomForest'],
           ['結果を解釈する', 'Ch.4・5', '混同行列 / 特徴量重要度 / ビジネス示唆']],
          y=194, row_h=34, col_ws=[200, 140, 532], color=cl, fs=12)
    slides.append(('03_flow', fig))

    # AI活用まとめ
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '生成AI活用の整理')
    two_col(ax,
        {'title': '🤖 生成AIの役割',
         'items': ['コードの書き方を教える', 'エラーメッセージを修正する',
                   'ライブラリのオプションを調べる', 'グラフの見た目を整える',
                   'ボイラープレートを自動生成する']},
        {'title': '⚡ あなた（DS）の役割',
         'items': ['何を分析するかを決める', 'グラフから仮説を立てる',
                   '欠損値の処理方針を判断する', '結果の数値を解釈する',
                   'ビジネス上の示唆を導き出す']},
        y0=100, col_h=290,
        lbg='#EBF5FB', lbc='#4A90D9', rbg='#FEF9E7', rbc='#E8A838')
    hbox(ax, 44, 412, W - 88, 52,
         '🔑 AIは「コーディングの補助ツール」\n分析の目的・設定と結果の解釈は、データサイエンティスト（あなた）の仕事',
         '#EAFAF1', '#5BA85A', tc='#1E8449', fs=13)
    slides.append(('04_ai', fig))

    # 次のステップ
    fig, ax = new_fig()
    header(ax, cl, lbl)
    slide_title(ax, '次のステップ：今日の先にあること')
    boxes = [
        ('📚 実践力の強化\n（近い将来）',
         '・より多くのデータで練習（Kaggle）\n・SQLでデータ取得を学ぶ\n・統計学の基礎を補強\n・自分の業務データで分析',
         C['ch1'], 44, 88, (W - 88 - 16) // 2, 190),
        ('🚀 専門スキルの深化\n（将来的に）',
         '・深層学習（画像・テキスト処理）\n・時系列分析\n・A/Bテスト設計\n・MLOps・本番環境への展開',
         C['ch2'], 44 + (W - 88 - 16)//2 + 16, 88, (W - 88 - 16)//2, 190),
        ('🎯 今すぐできること',
         '・今日のNotebookをもう一度手を動かして実行する\n・気になった特徴量を深掘りしてみる\n・別のパラメータでモデルを試す',
         C['ch3'], 44, 294, (W - 88 - 16) // 2, 160),
        ('💡 学習のコツ',
         '・「完全に理解してから」より「使いながら理解する」\n・AIをうまく使って実装スピードを上げる\n・コードより「解釈」の練習に時間をかける',
         C['ch4'], 44 + (W - 88 - 16)//2 + 16, 294, (W - 88 - 16)//2, 160),
    ]
    for title_t, content, color, bx, by, bw, bh in boxes:
        rect(ax, bx, by, bw, bh, fc=color + '18', ec=color, lw=2, radius=6)
        txt(ax, bx + 16, by + 14, title_t, fs=12, color=color, bold=True)
        for j, ln in enumerate(content.split('\n')):
            txt(ax, bx + 16, by + 52 + j * 24, ln, fs=11, color='#2c3e50')
    slides.append(('05_next', fig))

    # クロージング
    fig, ax = new_fig()
    # 背景
    for i in range(H):
        alpha = i / H
        r = int(0x4a * (1 - alpha * 0.5))
        g = int(0x1a * (1 - alpha * 0.5))
        b = int(0x6e + (min(255, 0xad) - 0x6e) * alpha)
        rect(ax, 0, i, W, 1, fc=f'#{r:02x}{g:02x}{b:02x}')
    txt(ax, W//2, 110, 'おつかれさまでした！', fs=38, color='white',
        bold=True, ha='center', va='center')
    # 3つのキーメッセージ
    messages = [
        '① DSの仕事の大半はEDA（データ理解）',
        '② 生成AIはコードを書く「道具」、解釈はあなたの仕事',
        '③ 「使いながら理解する」で十分です',
    ]
    rect(ax, 80, 160, W - 160, 220, fc=(1.000, 1.000, 1.000, 0.12), ec=(1.000, 1.000, 1.000, 0.20), lw=1, radius=8)
    txt(ax, W//2, 180, '🔑 今日覚えてほしい3つのこと', fs=15, color='white', bold=True, ha='center')
    for i, msg in enumerate(messages):
        txt(ax, W//2, 218 + i * 44, msg, fs=15, color=(1.000, 1.000, 1.000, 0.90), ha='center')
    rect(ax, 80, 400, W - 160, 62, fc=(1.000, 1.000, 1.000, 0.10), ec=(1.000, 1.000, 1.000, 0.15), lw=1, radius=8)
    txt(ax, W//2, 431, 'アンケートへのご回答をお願いします（5分）', fs=14,
        color=(1.000, 1.000, 1.000, 0.85), ha='center', va='center')
    slides.append(('06_closing', fig))

    return slides

# ================================================================
#  メイン：全スライドを生成して保存
# ================================================================

def main():
    os.makedirs(OUTPUT, exist_ok=True)
    chapters = [
        ('ch00_orientation', gen_ch0()),
        ('ch01_pandas',      gen_ch1()),
        ('ch02_eda',         gen_ch2()),
        ('ch03_image',       gen_ch3()),
        ('ch04_ml',          gen_ch4()),
        ('ch05_summary',     gen_ch5()),
    ]
    total = 0
    for ch_prefix, slides in chapters:
        for idx, (name, fig) in enumerate(slides, 1):
            fname = f'{OUTPUT}/{ch_prefix}_{idx:02d}_{name}.svg'
            save(fig, fname)
            print(f'  Saved: {fname}')
            total += 1
    print(f'\n✅ 完了：{total} 枚の SVG ファイルを {OUTPUT}/ に出力しました')

if __name__ == '__main__':
    main()
