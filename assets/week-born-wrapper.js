/* week-born-wrapper.js — 銀河ラッパー共通の「新しく生まれた星」台帳 + iframe 縁 glow（fail-open・0円）
   window.WeekBorn（assets/week-born.js）を使う。slug は URL パスから自動導出するので3ラッパー共通で使える。
   0件週は何も足さない（前週の静けさ）。title は textContent（XSS 不可）・外部 href は target=_blank（宇宙を離れず別タブ）。 */
(async function () {
  if (!window.WeekBorn) return;
  var parts = location.pathname.split("/").filter(Boolean), last = parts[parts.length - 1] || "";
  var slug = last.indexOf(".") >= 0 ? parts[parts.length - 2] : last;
  var items = window.WeekBorn.bySlug(await window.WeekBorn.load("../../week-born.json"), slug);
  if (!items.length) return;
  document.body.appendChild(Object.assign(document.createElement("div"), { className: "wb-glow" }));
  var panel = document.createElement("aside"); panel.className = "wb-panel";
  var head = document.createElement("div"); head.className = "wb-head";
  head.textContent = "✦ 新しく生まれた星 — " + items.length; panel.appendChild(head);
  var ul = document.createElement("ul");
  items.slice(0, 5).forEach(function (it) {
    var li = document.createElement("li");
    if (it.href) {
      var a = document.createElement("a"); a.href = it.href; a.target = "_blank"; a.rel = "noopener";
      a.textContent = it.title; li.appendChild(a);
    } else { li.textContent = it.title; }
    ul.appendChild(li);
  });
  if (items.length > 5) {
    var li = document.createElement("li"); li.style.opacity = ".6";
    li.textContent = "ほか " + (items.length - 5) + " 星"; ul.appendChild(li);
  }
  panel.appendChild(ul); document.body.appendChild(panel);
})();
