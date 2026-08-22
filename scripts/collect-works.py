#!/usr/bin/env python3
"""作品の星団 works.json 生成（決定論・0円）。
   YouTube = 公式RSS（実データ・直近~15本・タイトル/リンク/日付/再生数/サムネ）
   Instagram = 手動（galaxies/sakuhin/works.instagram.json を編集）
   アプリ = 手動（galaxies/sakuhin/works.apps.json を編集）
   使い方: python3 scripts/collect-works.py  → galaxies/sakuhin/works.json を再生成し commit。
   RSS は直近~15本のみ返す（公式仕様）。ネット不通時は既存 works.json の YT を保持（fail-open）。
   ※ predeploy には入れない（外部fetch＝非hermetic）。YT を最新化したい時に手動実行→commit。"""
import json, os, re, sys, urllib.request, html as _html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAKUHIN = os.path.join(ROOT, "galaxies", "sakuhin")
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}

YT_HANDLE = "@straisingchildren6357"
YT_CFG = {"platform": "youtube", "name": "YouTube", "handle": "straisingchildren6357",
          "url": "https://www.youtube.com/@straisingchildren6357",
          "hue": "232,146,106", "metric": "views", "source": "youtube-rss"}

def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20).read().decode("utf-8", "ignore")

def resolve_channel_id(handle):
    # /videos ページの canonical/og:url/externalId から取得する。
    # 素の "channelId" はページ内のおすすめ等の別チャンネルを先に拾うため使わない
    # （@handle のトップに出るおすすめ動画チャンネルを誤取得したバグの修正）。
    h = fetch("https://www.youtube.com/" + handle + "/videos")
    for pat in (
        r'<link rel="canonical" href="https://www\.youtube\.com/channel/(UC[0-9A-Za-z_-]{22})"',
        r'<meta property="og:url" content="https://www\.youtube\.com/channel/(UC[0-9A-Za-z_-]{22})"',
        r'"externalId":"(UC[0-9A-Za-z_-]{22})"',
    ):
        m = re.search(pat, h)
        if m:
            return m.group(1)
    return None

def yt_works(cid, limit=15):
    xml = fetch("https://www.youtube.com/feeds/videos.xml?channel_id=" + cid)
    out = []
    for e in re.findall(r"<entry>(.*?)</entry>", xml, re.S)[:limit]:
        vid = re.search(r"<yt:videoId>(.*?)</yt:videoId>", e)
        title = re.search(r"<title>(.*?)</title>", e)
        pub = re.search(r"<published>(.*?)</published>", e)
        views = re.search(r'views="(\d+)"', e)
        if not vid or not title:
            continue
        vid = vid.group(1)
        out.append({
            "title": _html.unescape(title.group(1)),
            "url": "https://www.youtube.com/watch?v=" + vid,
            "date": (pub.group(1)[:10] if pub else ""),
            "engagement": int(views.group(1)) if views else 0,
            "thumb": "https://i.ytimg.com/vi/%s/hqdefault.jpg" % vid,
        })
    return out

def load_json(path):
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else None

def main():
    apps = load_json(os.path.join(SAKUHIN, "works.apps.json"))
    if apps:
        apps.setdefault("source", "manual")
        apps.pop("_note", None)

    ig = load_json(os.path.join(SAKUHIN, "works.instagram.json"))
    if ig:
        ig.setdefault("source", "manual")
        ig.pop("_note", None)

    yt = None
    try:
        cid = resolve_channel_id(YT_HANDLE)
        if not cid:
            raise RuntimeError("channel_id 解決失敗")
        yt = dict(YT_CFG); yt["works"] = yt_works(cid)
        print("YouTube: channel_id=%s works=%d" % (cid, len(yt["works"])))
    except Exception as ex:
        print("YouTube fetch failed (fail-open, keep existing):", ex)
        cur = load_json(os.path.join(SAKUHIN, "works.json")) or {}
        for c in cur.get("clusters", []):
            if c.get("platform") == "youtube":
                yt = c

    clusters = [c for c in (apps, ig, yt) if c and c.get("works")]
    if not clusters:
        print("ERROR: no clusters with works — aborting (既存 works.json は保持)"); sys.exit(1)
    out = {
        "_note": "自動生成（scripts/collect-works.py）。YouTube=公式RSS（実データ・直近~15本）/ Instagram=手動（works.instagram.json を編集）/ アプリ=手動（works.apps.json を編集）。",
        "clusters": clusters,
    }
    with open(os.path.join(SAKUHIN, "works.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2); f.write("\n")
    print("wrote works.json:", [(c["platform"], c.get("source"), len(c["works"])) for c in clusters])

if __name__ == "__main__":
    main()
