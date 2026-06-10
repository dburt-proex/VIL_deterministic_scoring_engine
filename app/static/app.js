const $ = (id) => document.getElementById(id);

const routeClass = (route) => `route-badge route-${route}`;

async function getJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`${response.status} ${response.statusText}: ${detail}`);
  }
  return response.json();
}

function renderMetrics(metrics) {
  $("totalSignals").textContent = metrics.total_signals ?? 0;
  $("averageScore").textContent = (metrics.average_vil_score ?? 0).toFixed(1);
  $("passRate").textContent = `${metrics.pass_rate ?? 0}%`;
  $("reviewLoad").textContent = metrics.review_load ?? 0;
  $("haltCount").textContent = metrics.halt_count ?? 0;
}

function renderResult(result) {
  $("latestResult").className = "score-card";
  $("latestResult").innerHTML = `
    <span class="${routeClass(result.route)}">${result.route}</span>
    <div class="score-main">${result.vil_score.toFixed(1)}</div>
    <p class="reason">${result.reason}</p>
    <div class="breakdown">
      <div><span>Weighted Signal</span><strong>${result.weighted_signal_score.toFixed(1)}</strong></div>
      <div><span>Verifiability Cap</span><strong>${result.verifiability_score.toFixed(1)}</strong></div>
    </div>
    <div class="breakdown">
      <div><span>Signal Type</span><strong>${result.signal_type}</strong></div>
      <div><span>Source</span><strong>${result.source}</strong></div>
    </div>
    <p class="reason"><strong>Recommended action:</strong> ${result.recommended_action}</p>
    <p class="reason"><strong>Audit:</strong> ${result.audit.audit_id}</p>
  `;
}

function renderAudits(audits) {
  const rows = audits.map((item) => `
    <tr>
      <td><span class="${routeClass(item.route)}">${item.route}</span></td>
      <td>${item.vil_score.toFixed(1)}</td>
      <td>${item.signal_type}</td>
      <td>${item.source}</td>
      <td>${item.reason}</td>
    </tr>
  `).join("");

  $("auditRows").innerHTML = rows || `<tr><td colspan="5">No audit records yet.</td></tr>`;
}

function buildPayload() {
  const riskFlags = $("riskFlags").value
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean);

  const metadata = {};
  if ($("industry").value.trim()) metadata.industry = $("industry").value.trim();
  if ($("workflow").value.trim()) metadata.workflow = $("workflow").value.trim();

  return {
    source: $("source").value.trim(),
    signal_type: $("signalType").value,
    content: $("content").value.trim(),
    metadata,
    source_pointers: [{ type: "dashboard", value: "manual commercial dashboard intake" }],
    risk_flags: riskFlags,
  };
}

async function refreshDashboard() {
  const [metrics, audits] = await Promise.all([
    getJson("/metrics"),
    getJson("/audits?limit=25"),
  ]);
  renderMetrics(metrics);
  renderAudits(audits);
}

$("scoreForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const result = await getJson("/score", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(buildPayload()),
  });
  renderResult(result);
  await refreshDashboard();
});

$("refreshBtn").addEventListener("click", refreshDashboard);
refreshDashboard().catch((error) => console.error(error));
