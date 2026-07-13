#!/usr/bin/env python3
"""build-week-born — 「新しく生まれた星」の単一スパインを生成（決定論・0円・AI不使用）。

公開済み成果物のみを read-only で読む（非公開ソースは一切触らない=fail-closed）:
  - galaxies/{kenkyu,kotoba,koe}/*-galaxy.html の埋め込み `const G = {…}`（既に publish 済み）
  - galaxies/hakken/discovery-constellation.html の埋め込み `const GRAPH = {…}`（D-12 title-only 済み）

出力 week-born.json = 生 date のみ（boolean を焼かない → 古い deploy でも「嘘の今週」を出さず、
client 側が Date.now() と窓比較して自己補正する）。star/作品の title・date・href だけを載せ、
summary/本文は載せない（D-7/D-12 準拠）。
"""
import json, re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def extract_object(html, marker):
    """`marker` 直後の JSON オブジェクトを、文字列を尊重した波括弧バランスで抜き出す。"""
    i = html.find(marker)
    if i < 0:
        return None
    i = html.find("{", i)
    if i < 0:
        return None
    depth, in_str, esc = 0, False, False
    for j in range(i, len(html)):
        c = html[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(html[i:j + 1])
                    except json.JSONDecodeError:
                        return None
    return None

def read_html(path):
    p = os.path.join(ROOT, path)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return f.read()

def norm_date(d):
    d = (d or "")[:10]
    return d if DATE_RE.match(d) else None

# galaxy=表示名, slug=導線キー, path=公開HTML, marker=埋め込み変数
GALAXIES = [
    ("研究の銀河", "kenkyu", "galaxies/kenkyu/explorations-galaxy.html", "const G ="),
    ("ことばの銀河", "kotoba", "galaxies/kotoba/note-galaxy.html", "const G ="),
    ("声の銀河", "koe", "galaxies/koe/voice-galaxy.html", "const G ="),
    ("発見の星座", "hakken", "galaxies/hakken/discovery-constellation.html", "const GRAPH ="),
]

def title_of(node, slug):
    # title を題に使う。summary を題にできるのは hakken(GRAPH・D-12 で title-only 化済み)だけ。
    # kenkyu/kotoba/koe の summary は非公開本文なので、title が空でも summary へ落とさない（fail-closed）。
    t = node.get("title") or ""
    if not t and slug == "hakken":
        t = node.get("summary") or ""
    return t

def check_window_sync():
    """WINDOW_DAYS の二重定義（week-born.js と hakken template）が食い違ったら build を落とす。"""
    js = read_html("assets/week-born.js") or ""
    tpl = read_html("galaxies/hakken/discovery-constellation.template.html") or ""
    a = re.search(r"WINDOW_DAYS\s*=\s*(\d+)", js)
    b = re.search(r"BORN_WINDOW_DAYS\s*=\s*(\d+)", tpl)
    if a and b and a.group(1) != b.group(1):
        print(f"✗ WINDOW_DAYS 不一致: week-born.js={a.group(1)} / hakken={b.group(1)}（同期させよ）", file=sys.stderr)
        sys.exit(2)

def main():
    check_window_sync()
    items = []
    for name, slug, path, marker in GALAXIES:
        html = read_html(path)
        if not html:
            print(f"  skip（未生成）: {path}", file=sys.stderr)
            continue
        obj = extract_object(html, marker)
        nodes = (obj or {}).get("nodes") or []
        n = 0
        for nd in nodes:
            d = norm_date(nd.get("date"))
            t = title_of(nd, slug).strip()
            if not d or not t:
                continue
            items.append({"galaxy": name, "slug": slug, "title": t, "date": d, "href": nd.get("url") or ""})
            n += 1
        print(f"  {name:8} ({slug}): {n} 星", file=sys.stderr)
    # date 降順（新しい順）で安定ソート
    items.sort(key=lambda x: (x["date"], x["slug"], x["title"]), reverse=True)
    out = {"schema": "week-born/v1", "note": "生 date のみ。client が Date.now() と窓比較する（boolean は焼かない）。", "items": items}
    with open(os.path.join(ROOT, "week-born.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"→ week-born.json: {len(items)} 星（全公開星の date/title/href・{len(out['note'])>0}）", file=sys.stderr)

if __name__ == "__main__":
    main()
