/* week-born.js — 「新しく生まれた星」の共有クライアント（プレーン global・fail-open・0円）
   week-born.json（生 date のみ）を読み、client の now と窓比較する。boolean を焼かないので
   古い/未更新の JSON でも「嘘の今週」を出さず、該当0を返して静かに黙る（自己補正）。
   窓は WINDOW_DAYS の1定数で切替: 7=厳密「今週」/ 30=最近（現状の更新周期で可視）。 */
(function () {
  var WINDOW_DAYS = 30;
  function withinWindow(dateStr, days) {
    if (!dateStr) return false;
    var d = new Date(String(dateStr).slice(0, 10) + "T00:00:00");
    if (isNaN(d.getTime())) return false;              // 壊れた date は born=false（fail-open）
    var diff = (Date.now() - d.getTime()) / 86400000;
    return diff >= 0 && diff <= days;
  }
  async function load(url) {
    try {
      var r = await fetch(url, { cache: "no-cache" });
      if (!r.ok) return [];
      var j = await r.json();
      var items = Array.isArray(j) ? j : (j && j.items) || [];
      return items.filter(function (it) { return withinWindow(it.date, WINDOW_DAYS); });
    } catch (e) { return []; }                          // 不達=素の宇宙が残る
  }
  function bySlug(items, slug) { return items.filter(function (it) { return it.slug === slug; }); }
  function byGalaxy(items) {
    var m = {};
    items.forEach(function (it) { (m[it.slug] = m[it.slug] || []).push(it); });
    return m;
  }
  window.WeekBorn = { WINDOW_DAYS: WINDOW_DAYS, load: load, bySlug: bySlug, byGalaxy: byGalaxy, withinWindow: withinWindow };
})();
