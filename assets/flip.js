/* 表裏フリップの署名機構（単一 SSOT・全銀河で共有）。CSS は assets/flip.css。
   DOM 契約: .flip-card > (.flip-front iframe[src], .flip-back iframe[data-src])
             と .flip-btn[data-to-back][data-to-front]。
   - 同一ジェスチャ: rotateY(180) の見た目は CSS(var(--fade))。JS は状態・a11y・lifecycle のみ担当。
   - a11y: 非対面フェースを inert + aria-hidden（フォーカス／AT／ヒットテストから除外。
     backface-visibility は"描かない"だけで focus は外さないため必須）。
   - lifecycle: 裏面 iframe は初回フリップで data-src から起動し、表へ戻ったら src を解放
     ＝静止時（銀河表示）は WebGL 常駐を1本に戻す（モバイルの発熱／電池対策）。
   - degradation: JS／CDN 失敗時も作品面 iframe と「宇宙に戻る」は生存。このファイルはボタンだけを活性化する。 */
(function () {
  "use strict";
  var card = document.querySelector(".flip-card");
  var btn = document.querySelector(".flip-btn");
  if (!card || !btn) return;
  var frontFace = card.querySelector(".flip-front");
  var backFace = card.querySelector(".flip-back");
  var back = backFace && backFace.querySelector("iframe");
  if (!frontFace || !backFace || !back) return;

  var toBack = btn.getAttribute("data-to-back") || btn.textContent;
  var toFront = btn.getAttribute("data-to-front") || btn.textContent;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function setHidden(el, hidden) {
    el.inert = hidden;
    if (hidden) el.setAttribute("aria-hidden", "true");
    else el.removeAttribute("aria-hidden"); // aria-hidden="false" のアンチパターンを避け、除去で表現
  }
  function applyState(flipped) {
    setHidden(frontFace, flipped);
    setHidden(backFace, !flipped);
    btn.classList.toggle("active", flipped);
    btn.textContent = flipped ? toFront : toBack;
  }
  applyState(false); // 初期: 作品面（銀河）を表示・裏面は inert（HTML の inert 属性と一致）

  function releaseBackIfFront() {
    if (!card.classList.contains("flipped") && back.getAttribute("src")) {
      back.removeAttribute("src"); // 2つ目の WebGL を破棄。再フリップで data-src から再ロード（軌道状態は失うが常駐が減る）
    }
  }

  btn.addEventListener("click", function () {
    var flipped = card.classList.toggle("flipped");
    if (flipped && !back.getAttribute("src") && back.dataset.src) back.src = back.dataset.src; // 裏面へ: 曼荼羅を起こす（初回／再訪）
    applyState(flipped);
    if (!flipped && reduce) releaseBackIfFront(); // reduced-motion は transitionend が来ないので即時解放
  });

  card.addEventListener("transitionend", function (e) {
    if (e.propertyName === "transform" || e.propertyName === "-webkit-transform") releaseBackIfFront();
  });
})();
