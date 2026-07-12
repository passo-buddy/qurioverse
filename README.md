# Qurioverse — 好奇心の宇宙

全表現活動（研究・ことば・声・作品・手仕事）をひとつの宇宙として公開する静的サイト。
サイト＝宇宙 / 作品＝星 / 媒体＝銀河 / 思想＝銀河の裏面。中心には答えのない問いが空いている。

- 設計正本: `~/nexus-home/ideas/explorations/2026-07-12-expression-universe-site-design.md`
- 銀河の生成エンジン: `~/src/galaxy-forge/`（forge 相=1回だけAI / run 相=純決定論）

## 構成

```
index.html            宇宙（入口）— 星野 + 中心の空隙 + 銀河カード
galaxies/
  kenkyu/             研究の銀河（explorations）※ HTML 実体は gitignore — 下記参照
  kotoba/             ことばの銀河（note）
  koe/                声の銀河（観測準備中）
about/                観測者について
contact/              交信（Contact / ご依頼）
fuel/                 燃料補給（Support）
assets/tokens.css     デザイントークン（全ページ強制・唯一の共有CSS）
```

## ローカルで見る

```bash
cd qurioverse && python3 -m http.server 8080
# → http://localhost:8080/
```

## 銀河 HTML の同期（生成物のコピー元）

| 銀河 | コピー元 | 配置先 |
|---|---|---|
| ことば | `~/nexus-home/knowledge/note-galaxy/visualize/note-galaxy.html` | `galaxies/kotoba/` |
| 研究 | `~/nexus-home/knowledge/explorations-galaxy/visualize/explorations-galaxy.html` | `galaxies/kenkyu/` |

**研究の銀河の HTML は git 管理外（.gitignore）**。研究ノートには非公開情報がありえるため、
frontmatter `publish:` フラグ（既定 private の fail-closed）による公開版ビルドが整うまで
コミットしない（git 履歴に残さない）。ローカルでは上記コピーで導線が全通する。

## デザイントークン（宇宙の物理法則）

- 色: 深宇宙 `#060409–#0a0806` / 金 `#f2ca6b` / 乳白 `#ece3d0` / ミュート `#9a8f76`
- 字: 見出し=明朝 / 本文=ゴシック
- 動き: すべて遅い（drift 60s+・pulse 7s）。速いアニメ禁止
- 語彙: 星=作品 / 銀河=媒体 / 腕=テーマ / 空隙=未解決の問い / 交信=依頼 / 燃料=支援

## 公開（人間承認事項）

GitHub public 化・Pages デプロイ・ドメイン取得（qurioverse.com）はすべて人間承認のうえで実施。
週次同期（collectors → forge build → deploy）は公開後に GitHub Actions cron で構築予定（secrets 不要）。
