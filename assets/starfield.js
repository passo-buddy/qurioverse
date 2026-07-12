/* サブページの背景星野 — 依存ゼロ・固定シード（決定論）・遅い瞬きのみ。
   本文の可読性を優先して淡く敷く（z-index:-1）。 */
(function () {
  const cv = document.createElement("canvas");
  cv.setAttribute("aria-hidden", "true");
  cv.style.cssText = "position:fixed;inset:0;z-index:-1;pointer-events:none;";
  document.body.prepend(cv);
  const ctx = cv.getContext("2d");

  function lcg(seed) {
    let s = seed >>> 0;
    return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296;
  }

  let stars = [];
  function build() {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    cv.width = innerWidth * dpr;
    cv.height = innerHeight * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const rnd = lcg(20260712);
    const n = Math.round((innerWidth * innerHeight) / 5200);
    stars = Array.from({ length: n }, () => ({
      x: rnd() * innerWidth,
      y: rnd() * innerHeight,
      r: 0.3 + rnd() * 1.0,
      tw: 5 + rnd() * 10,
      ph: rnd() * Math.PI * 2,
      warm: rnd() < 0.2,
    }));
  }

  function draw(tms) {
    const t = tms / 1000;
    ctx.clearRect(0, 0, innerWidth, innerHeight);
    for (const s of stars) {
      const a = 0.18 + 0.3 * (0.5 + 0.5 * Math.sin((t / s.tw) * Math.PI * 2 + s.ph));
      ctx.beginPath();
      ctx.arc(s.x, s.y + Math.sin(t / 70 + s.ph) * 2, s.r, 0, Math.PI * 2);
      ctx.fillStyle = s.warm
        ? "rgba(242,202,107," + (a * 0.8).toFixed(3) + ")"
        : "rgba(236,227,208," + a.toFixed(3) + ")";
      ctx.fill();
    }
    requestAnimationFrame(draw);
  }

  build();
  addEventListener("resize", build);
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) {
    draw(0); /* 一枚だけ */
  } else {
    requestAnimationFrame(draw);
  }
})();
