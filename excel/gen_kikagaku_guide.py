"""
VBAやさしいガイド.html → キカガク社内資料版 に変換するスクリプト
"""

with open("VBAやさしいガイド.html", encoding="utf-8") as f:
    src = f.read()

# ─── 1. <title> を変更 ────────────────────────────────────────
src = src.replace(
    "<title>VBAとはじめて話す本</title>",
    "<title>Excel VBA やさしいガイド｜株式会社キカガク 社内研修資料</title>"
)

# ─── 2. CSS の :root 直前に Kikagaku ブランド CSS を差し込む ──
KK_CSS = """
    /* ===== キカガク ブランドスタイル ===== */
    :root{
      --kk-primary:#1a3c6e;
      --kk-accent:#2563eb;
      --kk-accent-light:#eff6ff;
      --kk-bar-bg:#0f2445;
      --kk-bar-border:#2563eb;
    }
    /* トップバー */
    .kk-topbar{
      background:var(--kk-bar-bg);
      padding:10px 32px;
      display:flex;
      align-items:center;
      justify-content:space-between;
      border-bottom:3px solid var(--kk-bar-border);
    }
    .kk-brand{display:flex;align-items:center;gap:12px;}
    .kk-logo-mark{
      width:34px;height:34px;
      background:#fff;
      border-radius:7px;
      display:flex;align-items:center;justify-content:center;
      font-size:13px;font-weight:900;color:var(--kk-bar-bg);
      letter-spacing:-1px;font-family:'Consolas','Courier New',monospace;
    }
    .kk-company-name{
      color:#fff;font-size:14px;font-weight:700;letter-spacing:.04em;
    }
    .kk-doc-meta{display:flex;align-items:center;gap:10px;}
    .kk-doc-badge{
      background:rgba(255,255,255,.15);
      color:#fff;font-size:11px;font-weight:700;
      padding:3px 12px;border-radius:20px;letter-spacing:.06em;
    }
    .kk-doc-date{color:rgba(255,255,255,.55);font-size:11px;}
    /* メインヘッダー */
    .site-header{
      background:#fff;
      border-bottom:1px solid #e2e8f0;
      padding:36px 20px 28px;
      text-align:center;
    }
    .site-header h1{
      font-size:26px;font-weight:900;color:#0f172a;margin-bottom:8px;
      letter-spacing:-.02em;
    }
    .header-badge{
      display:inline-block;
      font-size:11px;font-weight:700;
      background:var(--kk-accent-light);color:var(--kk-accent);
      border-radius:20px;padding:3px 14px;margin-bottom:14px;
      letter-spacing:.06em;
    }
    /* セクション見出し */
    .sec-title{
      font-size:20px;font-weight:900;color:#0f172a;
      border-bottom:2px solid var(--kk-accent);
      padding-bottom:6px;
      display:inline-block;
    }
    /* 目次ボタン */
    #toc-btn{background:var(--kk-primary);}
    /* フッター */
    .kk-footer{
      text-align:center;
      padding:32px 20px;
      border-top:1px solid #e2e8f0;
      margin-top:60px;
      color:#94a3b8;
      font-size:12px;
    }
    .kk-footer strong{color:#64748b;}
"""

src = src.replace(
    "    :root{--blue:",
    KK_CSS + "\n    :root{--blue:"
)

# ─── 3. ヘッダー HTML を置換 ──────────────────────────────────
OLD_HEADER = """<header class="site-header">
  <div class="header-badge">Excel VBA 研修 1日目・2日目</div>
  <h1>&#x1F4D7; VBAとはじめて話す本</h1>
  <p class="sub">難しい言葉は後回し。まずは「なんとなくわかる」から始めましょう。</p>
  <div class="day-chips">
    <span class="chip chip-d1">&#x1F4D8; 1日目の内容</span>
    <span class="chip chip-d2">&#x1F4D9; 2日目の内容</span>
  </div>
</header>"""

NEW_HEADER = """<!-- キカガク トップバー -->
<div class="kk-topbar">
  <div class="kk-brand">
    <div class="kk-logo-mark">KK</div>
    <span class="kk-company-name">株式会社キカガク</span>
  </div>
  <div class="kk-doc-meta">
    <span class="kk-doc-badge">社内研修資料</span>
    <span class="kk-doc-date">Excel VBA 研修 1日目・2日目</span>
  </div>
</div>

<!-- メインヘッダー -->
<header class="site-header">
  <div class="header-badge">Excel VBA 研修 参考資料</div>
  <h1>VBA やさしいガイド</h1>
  <p class="sub">難しい言葉は後回し。まずは「なんとなくわかる」から始めましょう。</p>
  <div class="day-chips">
    <span class="chip chip-d1">1日目の内容</span>
    <span class="chip chip-d2">2日目の内容</span>
  </div>
</header>"""

src = src.replace(OLD_HEADER, NEW_HEADER)

# ─── 4. フッターを </body> 直前に差し込む ────────────────────
KK_FOOTER = """
<footer class="kk-footer">
  <strong>株式会社キカガク</strong> &nbsp;|&nbsp; Excel VBA 研修 社内資料<br>
  本資料は社内研修目的での利用に限ります。無断転載・配布はご遠慮ください。
</footer>
"""

src = src.replace("</body>", KK_FOOTER + "\n</body>")

# ─── 5. 出力 ─────────────────────────────────────────────────
with open("キカガク_VBAやさしいガイド.html", "w", encoding="utf-8") as f:
    f.write(src)

print("生成完了：キカガク_VBAやさしいガイド.html")
