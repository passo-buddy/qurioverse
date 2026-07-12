# qurioverse

好奇心の宇宙 — 全表現活動を集約する公開静的サイト（アート作品）。ビルドなし・素の HTML/CSS/JS。唯一の外部依存 = three@0.161.0 CDN importmap（入口のみ・銀河ページと同一版に揃える）。

- **設計正本**: `~/nexus-home/ideas/explorations/2026-07-12-expression-universe-site-design.md`（IA・メタファー辞書・段階導入）
- **デザイントークン SSOT**: `assets/tokens.css` — 色・字・動きのハードコード禁止（全ページこのファイル経由）
- **動きの不変条件**: すべて遅い（drift 60s+ / pulse 7s / fade 1.6s）。速いアニメ禁止＝宇宙の時間感覚
- **銀河 HTML は生成物**（galaxy-forge run 相の出力のコピー）— 直接編集禁止。変更はエンジン側で行い再コピー
- **研究の銀河（kenkyu）の HTML は gitignore** — publish フラグ整備（fail-closed）まで commit しない
- **デプロイ（Pages 有効化・ドメイン設定）は人間承認**（R5）。repo = github.com/passo-buddy/qurioverse
- 検証: `python3 -m http.server` で 入口→各銀河→宇宙に戻る の導線 + トークン一貫を目視（V-4/V-5）
