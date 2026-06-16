"use strict";

const state = {
  plots: [],
  landmarks: null,
  summary: null,
  sortKey: "rank",
  sortDir: 1,
  map: null,
  markerLayer: null,
  maxPrice: 15000000,
};

// ---- helpers --------------------------------------------------------------
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));

async function getJSON(url) {
  const r = await fetch(url);
  return r.json();
}
async function postJSON(url, body) {
  const r = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  });
  return r.json();
}

function inr(v) {
  if (v === null || v === undefined) return "—";
  v = Number(v);
  if (v >= 1e7) return "₹" + (v / 1e7).toFixed(2) + " Cr";
  if (v >= 1e5) return "₹" + (v / 1e5).toFixed(1) + " L";
  return "₹" + v.toLocaleString("en-IN");
}
function vband(b) { return b === null || b === undefined ? "gated" : b; }
function bandBadge(b) {
  const v = vband(b);
  return `<span class="badge b-${v}">${v}</span>`;
}

// ---- summary cards --------------------------------------------------------
function renderCards(s) {
  const ev = s.evaluation || {};
  const cards = [
    { k: "Canonical plots", v: s.canonical_plots, sub: `${s.candidates} raw candidates` },
    { k: "Localities", v: s.localities_with_data, sub: "with scored plots" },
    { k: "Flagged", v: s.flagged_plots, sub: `${s.value_gated_plots} value-gated` },
    { k: "Baseline coverage", v: s.coverage.coverage_pct + "%", sub: `${s.coverage.cells_meeting_gate}/${s.coverage.cells} cells ≥ ${s.coverage.min_comparables}` },
    { k: "Budget ceiling", v: inr(s.budget.ceiling), sub: `equity ${inr(s.budget.equity_min)}–${inr(s.budget.equity_max)}`, small: true },
    { k: "Evaluation", v: ev.status === "ok" ? "ρ " + ev.spearman : (ev.status || "—"), sub: ev.trusted ? "trusted" : "not trusted yet", small: true },
    { k: "Sprint", v: s.sprint.days_left + "d left", sub: `${s.sprint.weeks}-week window`, small: true },
  ];
  $("#cards").innerHTML = cards.map((c) =>
    `<div class="card"><div class="k">${c.k}</div>
     <div class="v ${c.small ? "small" : ""}">${c.v}</div>
     <div class="sub">${c.sub}</div></div>`).join("");

  if (ev.status === "gold set pending") {
    $("#gateNote").textContent = "⚠ Gold set pending — engine not yet trusted to widen scope (§4, §11)";
  }
}

// ---- map ------------------------------------------------------------------
function plotColor(p) {
  if (p.red_flags && p.red_flags.length) return "#f85149";
  if (p.value_band === "A") return "#3fb950";
  if (p.value_band === "B") return "#4ea1ff";
  if (p.value_band === null) return "#8a99a8";
  return "#d29922";
}

function initMap(lm) {
  if (typeof L === "undefined") {
    $("#map").innerHTML = '<div class="map-fallback">Map library (Leaflet) could not load — needs internet for tiles. The table and detail view work offline.</div>';
    return;
  }
  const map = L.map("map", { zoomControl: true }).setView([20.30, 85.81], 12);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19, attribution: "© OpenStreetMap",
  }).addTo(map);

  // NH-16 polyline
  if (lm.nh16 && lm.nh16.length) {
    L.polyline(lm.nh16.map((p) => [p.lat, p.lng]), { color: "#e3b341", weight: 4, opacity: .7, dashArray: "6 6" })
      .bindTooltip("NH-16 (approx.)").addTo(map);
  }
  // landmarks
  Object.entries(lm.landmarks).forEach(([name, c]) => {
    L.marker([c.lat, c.lng], {
      icon: L.divIcon({ className: "", html: `<div style="background:#7c5cff;color:#fff;border-radius:4px;padding:1px 5px;font-size:10px;white-space:nowrap">★ ${name}</div>`, iconSize: [0, 0] }),
    }).addTo(map);
  });

  state.map = map;
  state.markerLayer = L.layerGroup().addTo(map);

  $("#legend").innerHTML = `
    <div><span class="dot" style="background:#3fb950"></span>value A</div>
    <div><span class="dot" style="background:#4ea1ff"></span>value B</div>
    <div><span class="dot" style="background:#d29922"></span>value C/D</div>
    <div><span class="dot" style="background:#8a99a8"></span>gated</div>
    <div><span class="dot" style="background:#f85149"></span>red flag</div>
    <div><span style="color:#7c5cff">★</span> landmark · <span style="color:#e3b341">— NH-16</span></div>`;
}

function renderMarkers(plots) {
  if (!state.markerLayer) return;
  state.markerLayer.clearLayers();
  plots.forEach((p) => {
    if (p.lat === null || p.lng === null) return;
    const m = L.circleMarker([p.lat, p.lng], {
      radius: p.rank <= 5 ? 9 : 6,
      color: "#0f1419", weight: 1,
      fillColor: plotColor(p), fillOpacity: .9,
    });
    m.bindTooltip(`#${p.rank} ${p.locality} · ${inr(p.est_price)}`);
    m.on("click", () => openDrawer(p.id));
    state.markerLayer.addLayer(m);
  });
}

// ---- filters + table ------------------------------------------------------
function currentFilters() {
  return {
    search: $("#searchBox").value.trim().toLowerCase(),
    tiers: $$(".f-tier:checked").map((c) => c.value),
    values: $$(".f-value:checked").map((c) => c.value),
    maxPrice: Number($("#priceRange").value),
    hideFlagged: $("#hideFlagged").checked,
  };
}

function applyFilters(plots) {
  const f = currentFilters();
  return plots.filter((p) => {
    if (f.hideFlagged && p.red_flags.length) return false;
    if (!f.tiers.includes(p.comfort_tier)) return false;
    if (!f.values.includes(vband(p.value_band))) return false;
    if (p.est_price !== null && p.est_price > f.maxPrice) return false;
    if (f.search) {
      const hay = (p.locality + " " + p.red_flags.join(" ") + " " + p.zoning_status).toLowerCase();
      if (!hay.includes(f.search)) return false;
    }
    return true;
  });
}

function sortPlots(plots) {
  const k = state.sortKey, dir = state.sortDir;
  return plots.slice().sort((a, b) => {
    let x = a[k], y = b[k];
    if (k === "value_band") { x = vband(x); y = vband(y); }
    if (x === null || x === undefined) x = "";
    if (y === null || y === undefined) y = "";
    if (typeof x === "number" && typeof y === "number") return (x - y) * dir;
    return String(x).localeCompare(String(y)) * dir;
  });
}

function renderTable(plots) {
  const rows = plots.map((p) => {
    const flagged = p.red_flags.length ? "flagged" : "";
    const top = p.rank <= 5 ? "top" : "";
    const flags = p.red_flags.length
      ? `<span class="flag-dot" title="${p.red_flags.join(', ')}">● ${p.red_flags.length}</span>` : "";
    const zoning = `<span class="${p.zoning_status === 'verify' ? 'zoning-verify' : ''}">${p.zoning_status}</span>`;
    return `<tr class="${flagged} ${top}" data-id="${p.id}">
      <td>${p.rank}</td>
      <td>${p.locality}</td>
      <td>${inr(p.est_price)}</td>
      <td>${p.price_per_sqft ? Math.round(p.price_per_sqft).toLocaleString("en-IN") : "—"}</td>
      <td>${p.area_sqft ? p.area_sqft.toLocaleString("en-IN") : "—"}</td>
      <td>${bandBadge(p.value_band)}</td>
      <td>${bandBadge(p.commercial_band)}</td>
      <td>${p.confidence}</td>
      <td class="tier-${p.comfort_tier}">${p.comfort_tier}</td>
      <td>${zoning}</td>
      <td>${flags}</td>
    </tr>`;
  }).join("");
  $("#plotTable tbody").innerHTML = rows || `<tr><td colspan="11" style="padding:20px;color:var(--muted)">No plots match the filters.</td></tr>`;
  $$("#plotTable tbody tr[data-id]").forEach((tr) =>
    tr.addEventListener("click", () => openDrawer(Number(tr.dataset.id))));
}

function refresh() {
  const filtered = applyFilters(state.plots);
  const sorted = sortPlots(filtered);
  renderTable(sorted);
  renderMarkers(sorted);
  $("#resultCount").textContent = `${sorted.length} of ${state.plots.length} plots`;
}

// ---- detail drawer --------------------------------------------------------
async function openDrawer(id) {
  const p = await getJSON("/api/plot/" + id);
  if (p.error) return;
  const d = p.distances_km || {};
  const distRows = Object.entries(d).map(([k, v]) =>
    `<div class="dist-bar"><span>${k}</span><span>${v} km</span></div>`).join("");
  const cmp = p.comparables;
  const cmpHtml = cmp
    ? `median ${Math.round(cmp.median_price_per_sqft).toLocaleString("en-IN")} ₹/sqft ·
       p25 ${Math.round(cmp.p25_price_per_sqft).toLocaleString("en-IN")} ·
       p75 ${Math.round(cmp.p75_price_per_sqft).toLocaleString("en-IN")} ·
       n=${cmp.n_comparables}`
    : "no baseline cell for this locality/band";
  const sources = p.sources.map((s) =>
    `<div class="src"><b>${s.source}</b> · ${s.source_id} · ${inr(s.price_inr)} · ${s.area_sqft || "—"} sqft
     ${s.url ? `· <a href="${s.url}" target="_blank">link</a>` : ""}</div>`).join("");
  const flags = p.red_flags.length
    ? `<div class="flags-list">${p.red_flags.map((f) => `<div class="flag">⚠ ${f}</div>`).join("")}</div>`
    : `<div style="color:var(--green)">none</div>`;
  const missing = p.missing_fields.length
    ? p.missing_fields.map((m) => `<span class="pill">${m}</span>`).join(" ") : "<span class='pill'>none</span>";
  const fin = p.financeability ? `<span class="flag-dot">${p.financeability}</span>` : "ok";

  $("#drawerBody").innerHTML = `
    <h2>#${p.rank} · ${p.locality}</h2>
    <div class="sub">${p.area_sqft || "?"} sqft · ${inr(p.est_price)} ·
      ${p.price_per_sqft ? Math.round(p.price_per_sqft).toLocaleString("en-IN") + " ₹/sqft" : "—"}</div>

    <div class="kv">
      <div class="k">Value band</div><div>${bandBadge(p.value_band)}</div>
      <div class="k">Commercial band</div><div>${bandBadge(p.commercial_band)}</div>
      <div class="k">Confidence</div><div>${p.confidence}</div>
      <div class="k">Zoning status</div><div class="${p.zoning_status === 'verify' ? 'zoning-verify' : ''}">${p.zoning_status}</div>
      <div class="k">Est. price</div><div>${inr(p.est_price)}</div>
      <div class="k">Required loan</div><div>${inr(p.required_loan)} <span class="tier-${p.comfort_tier}">(${p.comfort_tier})</span></div>
      <div class="k">Financeability</div><div>${fin}</div>
      <div class="k">Sources merged</div><div>${p.n_sources}</div>
    </div>

    <div class="section-h">Red flags</div>${flags}
    <div class="section-h">Missing fields</div><div>${missing}</div>
    <div class="section-h">Comparables (value gate)</div><div>${cmpHtml}</div>
    <div class="section-h">Distances</div>${distRows || "<div>no coordinates</div>"}
    <div class="section-h">Source listings</div>${sources || "<div>—</div>"}
    <div class="section-h">Due-diligence checklist</div>
    <div class="checklist">${(p.diligence_checklist || "").replace(/</g, "&lt;")}</div>
  `;
  $("#drawer").classList.remove("hidden");
}

// ---- run controls ---------------------------------------------------------
async function reloadData() {
  const [summary, plots, reports] = await Promise.all([
    getJSON("/api/summary"), getJSON("/api/plots"), getJSON("/api/reports"),
  ]);
  state.summary = summary;
  state.plots = plots;
  state.maxPrice = summary.budget.ceiling;
  const range = $("#priceRange");
  range.max = summary.budget.ceiling;
  if (!range.value || Number(range.value) === 0) range.value = summary.budget.ceiling;
  $("#priceLabel").textContent = inr(Number(range.value));
  renderCards(summary);
  $("#digestPre").textContent = reports.digest;
  $("#weeklyPre").textContent = reports.weekly;
  refresh();
}

async function doRun(scan) {
  const btn = scan ? $("#scanBtn") : $("#runBtn");
  const orig = btn.textContent;
  btn.disabled = true; btn.textContent = "Running…";
  $("#runStatus").textContent = scan ? "scanning all localities…" : "running…";
  try {
    if (scan) await postJSON("/api/scan", {});
    else await postJSON("/api/run", { locality: $("#localitySelect").value });
    await reloadData();
    $("#runStatus").textContent = "done · " + new Date().toLocaleTimeString();
  } catch (e) {
    $("#runStatus").textContent = "error";
  } finally {
    btn.disabled = false; btn.textContent = orig;
  }
}

// ---- wiring ---------------------------------------------------------------
function wire() {
  // tabs
  $$(".tab").forEach((t) => t.addEventListener("click", () => {
    $$(".tab").forEach((x) => x.classList.remove("active"));
    $$(".tab-panel").forEach((x) => x.classList.remove("active"));
    t.classList.add("active");
    $("#" + t.dataset.tab).classList.add("active");
    if (t.dataset.tab === "browse" && state.map) setTimeout(() => state.map.invalidateSize(), 50);
  }));

  // sorting
  $$("#plotTable thead th[data-sort]").forEach((th) =>
    th.addEventListener("click", () => {
      const k = th.dataset.sort;
      state.sortDir = state.sortKey === k ? -state.sortDir : 1;
      state.sortKey = k;
      refresh();
    }));

  // filters
  ["change", "input"].forEach((ev) => {
    $("#searchBox").addEventListener(ev, refresh);
    $("#priceRange").addEventListener(ev, () => {
      $("#priceLabel").textContent = inr(Number($("#priceRange").value));
      refresh();
    });
  });
  $$(".f-tier, .f-value, #hideFlagged").forEach((c) => c.addEventListener("change", refresh));
  $("#resetFilters").addEventListener("click", () => {
    $("#searchBox").value = "";
    $$(".f-tier, .f-value").forEach((c) => (c.checked = true));
    $("#hideFlagged").checked = false;
    $("#priceRange").value = state.maxPrice;
    $("#priceLabel").textContent = inr(state.maxPrice);
    refresh();
  });

  // run controls
  $("#runBtn").addEventListener("click", () => doRun(false));
  $("#scanBtn").addEventListener("click", () => doRun(true));

  // drawer
  $("#drawerClose").addEventListener("click", () => $("#drawer").classList.add("hidden"));
  $("#drawer").addEventListener("click", (e) => { if (e.target.id === "drawer") $("#drawer").classList.add("hidden"); });
}

async function boot() {
  wire();
  const [landmarks, localities] = await Promise.all([
    getJSON("/api/landmarks"), getJSON("/api/localities"),
  ]);
  state.landmarks = landmarks;
  $("#localitySelect").innerHTML = localities.map((l) =>
    `<option value="${l.label}">${l.label}${l.plots ? ` (${l.plots})` : ""}</option>`).join("");
  initMap(landmarks);
  await reloadData();
}

boot();
