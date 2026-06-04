/* TravelAI — Frontend Controller */

// ── DOM References ──────────────────────────────────────────────
const form = document.getElementById("travel-form");
const btnSubmit = document.getElementById("btn-submit");
const btnNewPlan = document.getElementById("btn-new-plan");
const btnRetry = document.getElementById("btn-retry");

const agentsSection = document.getElementById("agents-progress");
const resultsSection = document.getElementById("results-section");
const errorSection = document.getElementById("error-section");
const logsSection = document.getElementById("logs-section");
const logsContainer = document.getElementById("logs-container");
const logsSummary = document.getElementById("logs-summary");

// ── Theme Management ────────────────────────────────────────
const THEME_KEY = "travelai-theme";
const themeToggle = document.getElementById("theme-toggle");
const themeIcon = document.getElementById("theme-icon");

// Temas disponíveis
const THEMES = {
  dark: { icon: "🌙", label: "Modo Escuro" },
  light: { icon: "☀️", label: "Modo Claro" },
};

function getPreferredTheme() {
  // 1. Verificar localStorage
  const saved = localStorage.getItem(THEME_KEY);
  if (saved && THEMES[saved]) return saved;

  // 2. Verificar preferência do sistema
  if (
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: light)").matches
  ) {
    return "light";
  }

  // 3. Default: dark
  return "dark";
}

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  if (themeIcon) {
    themeIcon.textContent = THEMES[theme].icon;
  }
  localStorage.setItem(THEME_KEY, theme);

  // Atualizar aria-label
  if (themeToggle) {
    themeToggle.setAttribute(
      "aria-label",
      `Tema atual: ${THEMES[theme].label}. Clique para alternar.`,
    );
  }
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") || "dark";
  const next = current === "dark" ? "light" : "dark";
  applyTheme(next);
}

// Inicializar tema
const initialTheme = getPreferredTheme();
applyTheme(initialTheme);

// Event listener
if (themeToggle) {
  themeToggle.addEventListener("click", toggleTheme);
}

// Ouvir mudanças na preferência do sistema
if (window.matchMedia) {
  window
    .matchMedia("(prefers-color-scheme: light)")
    .addEventListener("change", (e) => {
      // Só mudar automaticamente se o usuário não tiver preferência salva
      if (!localStorage.getItem(THEME_KEY)) {
        applyTheme(e.matches ? "light" : "dark");
      }
    });
}

// ── Agent Steps Animation ────────────────────────────────────────

const AGENT_STEPS = [
  {
    id: "agent-maestro",
    badge: "🎯 Analisando...",
    done: "✅ Concluído",
    delay: 0,
  },
  {
    id: "agent-aereo",
    badge: "🔍 Buscando...",
    done: "✅ Concluído",
    delay: 1200,
  },
  {
    id: "agent-hotel",
    badge: "🔍 Buscando...",
    done: "✅ Concluído",
    delay: 1400,
  },
  {
    id: "agent-turismo",
    badge: "📝 Gerando...",
    done: "✅ Concluído",
    delay: 1600,
  },
  {
    id: "agent-consolidar",
    badge: "🔗 Consolidando...",
    done: "✅ Pronto!",
    delay: 3200,
  },
];

function setAgentStatus(id, status, badgeText) {
  const card = document.getElementById(id);
  if (!card) return;
  card.dataset.status = status;
  const badge = card.querySelector(".agent-status-badge");
  if (badge) badge.textContent = badgeText;
}

function runAgentAnimation() {
  // Reset todos
  AGENT_STEPS.forEach((s) => setAgentStatus(s.id, "waiting", "Aguardando"));

  AGENT_STEPS.forEach((step) => {
    setTimeout(
      () => setAgentStatus(step.id, "running", step.badge),
      step.delay,
    );
  });
}

function finishAgentAnimation(resultado) {
  const agentMap = {
    passagens_aereas: "agent-aereo",
    hoteis: "agent-hotel",
    roteiro_turistico: "agent-turismo",
  };

  ["agent-maestro"].forEach((id) => setAgentStatus(id, "done", "✅ Concluído"));

  Object.entries(agentMap).forEach(([key, id]) => {
    const agentResult = resultado?.resultado?.[key];
    const status = agentResult?.status === "erro" ? "error" : "done";
    const badge = status === "error" ? "❌ Erro" : "✅ Concluído";
    setAgentStatus(id, status, badge);
  });

  setAgentStatus("agent-consolidar", "done", "✅ Pronto!");
}

// ── Tabs ─────────────────────────────────────────────────────────
document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const target = btn.dataset.tab;
    document.querySelectorAll(".tab-btn").forEach((b) => {
      b.classList.remove("active");
      b.setAttribute("aria-selected", "false");
    });
    document
      .querySelectorAll(".tab-content")
      .forEach((c) => c.classList.remove("active"));
    btn.classList.add("active");
    btn.setAttribute("aria-selected", "true");
    document.getElementById(`tab-content-${target}`)?.classList.add("active");
  });
});

// ── Render Functions ──────────────────────────────────────────────

function formatCurrency(value, moeda = "BRL") {
  if (value == null) return "N/D";
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: moeda,
    maximumFractionDigits: 2,
  }).format(value);
}

function renderSummary(plan) {
  const s = plan.resumo;
  const pi = plan.plano_integrado;

  // Status badge
  const statusBadge = document.getElementById("status-badge");
  statusBadge.textContent =
    { sucesso: "✅ Sucesso", parcial: "⚠️ Parcial", erro: "❌ Erro" }[
      plan.status
    ] || plan.status;
  statusBadge.className = `summary-badge ${plan.status}`;

  // Title
  const title = document.getElementById("summary-title");
  title.textContent = `✈️ ${s.cidade_destino}${s.cidade_origem ? ` — partindo de ${s.cidade_origem}` : ""}`;

  // Stats
  const stats = document.getElementById("summary-stats");
  const dataIda = new Date(s.data_saida + "T12:00:00");
  const dataVolta = new Date(s.data_retorno + "T12:00:00");
  const formatDate = (d) =>
    d.toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    });

  stats.innerHTML = `
    <div class="stat-item">
      <span class="stat-label">Saída</span>
      <span class="stat-value">${formatDate(dataIda)}</span>
    </div>
    <div class="stat-item">
      <span class="stat-label">Retorno</span>
      <span class="stat-value">${formatDate(dataVolta)}</span>
    </div>
    <div class="stat-item">
      <span class="stat-label">Duração</span>
      <span class="stat-value">${s.duracao_dias} dias</span>
    </div>
    <div class="stat-item">
      <span class="stat-label">Noites</span>
      <span class="stat-value">${s.quantidade_noites} noites</span>
    </div>
  `;

  // Recommendation
  const rec = document.getElementById("summary-recommendation");
  rec.innerHTML = pi.recomendacao_geral
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n\n/g, "<br><br>");
}

function renderCosts(plan) {
  const ec = plan.plano_integrado.estimativa_custos;
  const container = document.getElementById("cost-cards");
  const items = [
    { icon: "✈️", label: "Passagens (ida+volta)", value: ec.passagens },
    { icon: "🏨", label: "Hospedagem Total", value: ec.hospedagem },
    { icon: "🎭", label: "Passeios (estimado)", value: ec.passeios },
    {
      icon: "💰",
      label: "Total Estimado",
      value: ec.total_estimado,
      highlight: true,
    },
  ];
  container.innerHTML = items
    .map(
      (item) => `
    <div class="cost-card ${item.highlight ? "highlight" : ""}">
      <div class="cost-icon">${item.icon}</div>
      <div class="cost-label">${item.label}</div>
      <div class="cost-value ${item.value == null ? "nd" : ""}">
        ${item.value != null ? formatCurrency(item.value, ec.moeda) : "Não disponível"}
      </div>
    </div>
  `,
    )
    .join("");
}

function renderFlights(passagensResult) {
  const container = document.getElementById("flights-content");
  if (!passagensResult || passagensResult.status === "erro") {
    container.innerHTML = `<div class="alert-item">⚠️ Não foi possível obter sugestões de passagens aéreas.</div>`;
    return;
  }

  const opcoes = passagensResult.data?.opcoes || [];
  const melhor = passagensResult.data?.melhor_opcao_sugerida;
  const limitacoes = passagensResult.data?.limitacoes || [];

  if (!opcoes.length) {
    container.innerHTML = `<div class="alert-item">Nenhuma opção de voo disponível.</div>`;
    return;
  }

  const bestCompanhia = melhor?.companhia;

  const flightCards = opcoes
    .map((op, i) => {
      const isBest = op.companhia === bestCompanhia && i === 0;
      const escalasText =
        op.escalas === 0
          ? "🟢 Direto"
          : op.escalas === 1
            ? "🟡 1 escala"
            : `🔴 ${op.escalas} escalas`;
      return `
      <div class="flight-card ${isBest ? "best" : ""}">
        ${isBest ? '<span class="best-badge">⭐ MELHOR OPÇÃO</span>' : ""}
        <div class="flight-airline">${op.companhia}</div>
        <div class="flight-route">
          <div class="flight-city">
            <strong>${op.origem?.split("(")[0].trim() || "—"}</strong>
            <span>Partida</span>
          </div>
          <div class="flight-arrow">→</div>
          <div class="flight-city">
            <strong>${op.destino}</strong>
            <span>Chegada</span>
          </div>
        </div>
        <div class="flight-meta">
          <div class="meta-item">
            <div class="meta-label">Duração</div>
            <div class="meta-value">⏱ ${op.duracao_estimada || "—"}</div>
          </div>
          <div class="meta-item">
            <div class="meta-label">Escalas</div>
            <div class="meta-value">${escalasText}</div>
          </div>
        </div>
        <div class="flight-price">
          ${op.preco_estimado != null ? `${formatCurrency(op.preco_estimado, op.moeda || "BRL")}<div class="price-per">por pessoa (est.)</div>` : '<span class="nd">N/D</span>'}
        </div>
      </div>
    `;
    })
    .join("");

  const limitacoesHtml = limitacoes.length
    ? `
    <div style="margin-top: 20px;">
      <div class="alerts-list">
        ${limitacoes.map((l) => `<div class="alert-item">⚠️ ${l}</div>`).join("")}
      </div>
    </div>
  `
    : "";

  container.innerHTML = `<div class="flight-cards">${flightCards}</div>${limitacoesHtml}`;
}

function renderHotels(hoteisResult) {
  const container = document.getElementById("hotels-content");
  if (!hoteisResult || hoteisResult.status === "erro") {
    container.innerHTML = `<div class="alert-item">⚠️ Não foi possível obter sugestões de hotéis.</div>`;
    return;
  }

  const opcoes = hoteisResult.data?.opcoes || [];
  const regioes = hoteisResult.data?.regioes_recomendadas || [];
  const limitacoes = hoteisResult.data?.limitacoes || [];

  const hotelCards = opcoes
    .map((h, i) => {
      const stars = h.categoria ? (h.categoria.match(/\d/) || [3])[0] : 3;
      const starStr = "⭐".repeat(parseInt(stars));
      const ratingNum = h.avaliacao ? parseFloat(h.avaliacao.split("/")[0]) : 0;
      const ratingPct = ((ratingNum / 10) * 100).toFixed(0);
      const highlightTags = (h.destaques || [])
        .slice(0, 4)
        .map((d) => `<span class="highlight-tag">${d}</span>`)
        .join("");

      return `
      <div class="hotel-card ${i === 0 ? "best" : ""}">
        <div class="hotel-card-header">
          ${i === 0 ? '<span class="best-badge">⭐ MELHOR OPÇÃO</span>' : ""}
          <div class="hotel-stars">${starStr} ${h.categoria || ""}</div>
          <div class="hotel-name">${h.nome}</div>
          <div class="hotel-location">${h.bairro || "Localização central"}</div>
        </div>
        <div class="hotel-body">
          ${
            ratingNum > 0
              ? `
            <div class="hotel-rating">
              <span class="rating-score">${ratingNum}</span>
              <div class="rating-bar"><div class="rating-fill" style="width: ${ratingPct}%"></div></div>
              <span style="font-size: 0.75rem; color: var(--text-muted)">/10</span>
            </div>
          `
              : ""
          }
          <div class="hotel-highlights">${highlightTags}</div>
          <div class="hotel-price">
            <div>
              <div class="price-main">${formatCurrency(h.preco_estimado_total, h.moeda)}</div>
              <div class="price-sub">total (est.)</div>
            </div>
            <div class="price-diaria">${formatCurrency(h.preco_estimado_diaria, h.moeda)}/noite</div>
          </div>
        </div>
      </div>
    `;
    })
    .join("");

  const regioesHtml = regioes.length
    ? `
    <div class="regions-section">
      <div class="regions-title">📍 Regiões Recomendadas para Hospedagem</div>
      <div class="regions-grid">
        ${regioes.map((r) => `<span class="region-tag">${r}</span>`).join("")}
      </div>
    </div>
  `
    : "";

  const limitacoesHtml = limitacoes.length
    ? `
    <div style="margin-top: 20px;">
      <div class="alerts-list">
        ${limitacoes.map((l) => `<div class="alert-item">⚠️ ${l}</div>`).join("")}
      </div>
    </div>
  `
    : "";

  container.innerHTML = `
    <div class="hotel-cards">${hotelCards}</div>
    ${regioesHtml}
    ${limitacoesHtml}
  `;
}

function renderItinerary(turismoResult) {
  const container = document.getElementById("itinerary-content");
  if (!turismoResult || turismoResult.status === "erro") {
    container.innerHTML = `<div class="alert-item">⚠️ Não foi possível gerar o roteiro turístico.</div>`;
    return;
  }

  const roteiro = turismoResult.data?.roteiro_por_dia || [];
  const dicas = turismoResult.data?.dicas || [];

  const timeIcons = { manha: "🌅 Manhã", tarde: "☀️ Tarde", noite: "🌙 Noite" };

  const dayCards = roteiro
    .map((dia) => {
      const dataObj = new Date(dia.data + "T12:00:00");
      const dateStr = dataObj.toLocaleDateString("pt-BR", {
        weekday: "long",
        day: "2-digit",
        month: "long",
      });

      const timeBlocks = ["manha", "tarde", "noite"]
        .map((period) => {
          const activities = dia[period] || [];
          if (!activities.length) return "";
          return `
        <div class="time-block">
          <div class="time-label">${timeIcons[period]}</div>
          <div class="time-activities">
            ${activities.map((a) => `<div class="activity-item">${a}</div>`).join("")}
          </div>
        </div>
      `;
        })
        .join("");

      const obsHtml = (dia.observacoes || []).length
        ? `
      <div class="day-obs">💡 ${dia.observacoes.join(" | ")}</div>
    `
        : "";

      return `
      <div class="day-card" id="day-${dia.dia}">
        <div class="day-header" onclick="toggleDay(${dia.dia})">
          <div class="day-number">${dia.dia}</div>
          <div class="day-info">
            <div class="day-date">${dateStr}</div>
            <div class="day-theme">${dia.tema}</div>
          </div>
          <div class="day-toggle">▼</div>
        </div>
        <div class="day-body">
          ${timeBlocks}
          ${obsHtml}
        </div>
      </div>
    `;
    })
    .join("");

  const dicasHtml = dicas.length
    ? `
    <div style="margin-top: 28px;">
      <div class="regions-title">💡 Dicas Práticas</div>
      <div class="tips-grid">
        ${dicas.map((d) => `<div class="tip-card">${d}</div>`).join("")}
      </div>
    </div>
  `
    : "";

  container.innerHTML = `
    <div class="itinerary-days">${dayCards}</div>
    ${dicasHtml}
  `;

  // Abre o primeiro dia automaticamente
  const firstDay = document.getElementById("day-1");
  if (firstDay) firstDay.classList.add("open");
}

function renderAlerts(plan) {
  const container = document.getElementById("alerts-content");
  const allAlerts = plan.alertas || [];

  // Coleta também alertas dos agentes
  const agentAlerts = [];
  Object.values(plan.resultado || {}).forEach((r) => {
    (r.alertas || []).forEach((a) => {
      if (!allAlerts.includes(a)) agentAlerts.push(a);
    });
  });

  const allUnique = [...new Set([...allAlerts, ...agentAlerts])];

  container.innerHTML = allUnique.length
    ? `
    <div class="alerts-list">
      ${allUnique.map((a) => `<div class="alert-item">${a}</div>`).join("")}
    </div>
  `
    : `<div class="tip-card">✅ Nenhum alerta crítico para esta viagem.</div>`;
}

// ── Day Toggle ────────────────────────────────────────────────────
window.toggleDay = function (dayNum) {
  const card = document.getElementById(`day-${dayNum}`);
  if (card) card.classList.toggle("open");
};

// ── Show / Hide Sections ──────────────────────────────────────────
function showSection(name) {
  [agentsSection, resultsSection, errorSection].forEach((s) =>
    s?.classList.add("hidden"),
  );
  if (name === "agents") agentsSection?.classList.remove("hidden");
  if (name === "results") resultsSection?.classList.remove("hidden");
  if (name === "error") errorSection?.classList.remove("hidden");
}

function hideAllSections() {
  [agentsSection, resultsSection, errorSection].forEach((s) =>
    s?.classList.add("hidden"),
  );
}

// ── Form Validation ───────────────────────────────────────────────
function validateForm(data) {
  let valid = true;

  // Reset
  document
    .querySelectorAll(".form-group")
    .forEach((g) => g.classList.remove("has-error"));

  if (!data.cidade_destino.trim()) {
    document
      .getElementById("cidade_destino")
      ?.closest(".form-group")
      ?.classList.add("has-error");
    valid = false;
  }
  if (!data.data_saida) {
    document
      .getElementById("data_saida")
      ?.closest(".form-group")
      ?.classList.add("has-error");
    valid = false;
  }
  if (!data.data_retorno) {
    document
      .getElementById("data_retorno")
      ?.closest(".form-group")
      ?.classList.add("has-error");
    valid = false;
  }
  if (
    data.data_saida &&
    data.data_retorno &&
    data.data_retorno <= data.data_saida
  ) {
    document
      .getElementById("data_retorno")
      ?.closest(".form-group")
      ?.classList.add("has-error");
    valid = false;
  }

  return valid;
}

// ── Submit Handler ────────────────────────────────────────────────
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(form);

  const data = {
    cidade_destino: formData.get("cidade_destino") || "",
    data_saida: formData.get("data_saida") || "",
    data_retorno: formData.get("data_retorno") || "",
    cidade_origem: formData.get("cidade_origem") || null,
    quantidade_viajantes: parseInt(formData.get("quantidade_viajantes")) || 1,
    ritmo_roteiro: formData.get("ritmo_roteiro") || "moderado",
    interesses: formData.getAll("interesses"),
    preferencia_voo: "melhor_custo_beneficio",
    preferencia_hotel: "melhor_custo_beneficio",
  };

  if (!validateForm(data)) return;

  // Limpa origem vazia
  if (!data.cidade_origem?.trim()) data.cidade_origem = null;

  // UI: loading state
  btnSubmit.disabled = true;
  btnSubmit.querySelector(".btn-text").textContent = "Processando...";
  btnSubmit.querySelector(".btn-loader")?.classList.add("hidden");
  btnSubmit.querySelector(".btn-icon").classList.add("hidden");

  hideAllSections();
  showSection("agents");
  runAgentAnimation();

  // Scroll suave para agentes
  agentsSection.scrollIntoView({ behavior: "smooth", block: "start" });

  // Limpa logs anteriores
  logsContainer.innerHTML = "";
  logsSummary.classList.add("hidden");
  logsSummary.innerHTML = "";

  try {
    // 1. Faz POST para iniciar processamento
    const response = await fetch("/api/plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const initResult = await response.json();

    if (!response.ok) {
      throw { detail: initResult.detail };
    }

    const requestId = initResult.request_id;

    // 2. Abre SSE para receber logs em tempo real
    const eventSource = new EventSource(`/api/stream/${requestId}`);

    // Mostra painel de logs
    logsSection.classList.remove("hidden");

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.event === "done") {
          // Processamento concluído
          eventSource.close();

          const result = data.result;

          // Atualiza cards de agentes
          finishAgentAnimation(result);

          // Mostra resumo dos logs
          const allSuccess = result.status === "sucesso";
          logsSummary.classList.remove("hidden");
          logsSummary.innerHTML = `
            <div class="logs-summary-${allSuccess ? "success" : "error"}">
              <span>${allSuccess ? "✅" : "⚠️"}</span>
              <span>Todas as operações foram concluídas ${allSuccess ? "com sucesso!" : "com alertas."}</span>
            </div>
          `;

          // Renderiza resultados
          setTimeout(() => {
            renderSummary(result);
            renderCosts(result);
            renderFlights(result.resultado?.passagens_aereas);
            renderHotels(result.resultado?.hoteis);
            renderItinerary(result.resultado?.roteiro_turistico);
            renderAlerts(result);

            // Reset tabs
            document.querySelectorAll(".tab-btn").forEach((b) => {
              b.classList.remove("active");
              b.setAttribute("aria-selected", "false");
            });
            document
              .querySelectorAll(".tab-content")
              .forEach((c) => c.classList.remove("active"));
            document.getElementById("tab-flights")?.classList.add("active");
            document
              .getElementById("tab-content-flights")
              ?.classList.add("active");

            showSection("results");
            resultsSection.scrollIntoView({
              behavior: "smooth",
              block: "start",
            });
          }, 800);
        } else {
          // Log normal - adiciona ao painel
          addLogEntry(data);
        }
      } catch (e) {
        console.error("Erro ao processar evento SSE:", e);
      }
    };

    eventSource.onerror = (err) => {
      console.error("Erro no SSE:", err);
      eventSource.close();

      // Tenta buscar resultado diretamente
      fetch(`/api/result/${requestId}`)
        .then((r) => r.json())
        .then((result) => {
          if (result.status !== "processing") {
            finishAgentAnimation(result);
            renderSummary(result);
            renderCosts(result);
            renderFlights(result.resultado?.passagens_aereas);
            renderHotels(result.resultado?.hoteis);
            renderItinerary(result.resultado?.roteiro_turistico);
            renderAlerts(result);
            showSection("results");
          }
        })
        .catch((e) => console.error("Erro ao buscar resultado:", e));
    };
  } catch (err) {
    console.error("Erro:", err);
    finishAgentAnimation(null);

    const messages = document.getElementById("error-messages");
    let errs = [];
    if (err.detail?.erros) errs = err.detail.erros;
    else if (typeof err.detail === "string") errs = [err.detail];
    else
      errs = ["Erro inesperado ao processar a solicitação. Tente novamente."];

    messages.innerHTML = errs
      .map((e) => `<div class="error-message">${e}</div>`)
      .join("");

    setTimeout(() => showSection("error"), 1000);
  } finally {
    btnSubmit.disabled = false;
    btnSubmit.querySelector(".btn-text").textContent = "Planejar Viagem";
    btnSubmit.querySelector(".btn-loader")?.classList.add("hidden");
    btnSubmit.querySelector(".btn-icon").classList.remove("hidden");
  }
});

// ── New Plan / Retry ──────────────────────────────────────────────
btnNewPlan?.addEventListener("click", () => {
  hideAllSections();
  form.scrollIntoView({ behavior: "smooth", block: "start" });
});

btnRetry?.addEventListener("click", () => {
  hideAllSections();
  form.scrollIntoView({ behavior: "smooth", block: "start" });
});

// ── Set min dates ─────────────────────────────────────────────────
window.addEventListener("DOMContentLoaded", () => {
  const today = new Date().toISOString().split("T")[0];
  const dataSaida = document.getElementById("data_saida");
  const dataRetorno = document.getElementById("data_retorno");

  if (dataSaida) dataSaida.min = today;
  if (dataRetorno) dataRetorno.min = today;

  dataSaida?.addEventListener("change", () => {
    if (dataRetorno && dataSaida.value) {
      dataRetorno.min = dataSaida.value;
    }
  });
});

// ── Log Entry Helper ──────────────────────────────────────
function addLogEntry(data) {
  const logEntry = document.createElement("div");
  logEntry.className = `log-entry log-${data.level || "info"}`;

  const time = new Date(data.timestamp).toLocaleTimeString("pt-BR");

  logEntry.innerHTML = `
    <span class="log-time">${time}</span>
    <span class="log-agent">[${data.agent.toUpperCase()}]</span>
    <span class="log-message">${data.message}</span>
  `;

  logsContainer.appendChild(logEntry);

  // Auto-scroll para o final
  logsContainer.scrollTop = logsContainer.scrollHeight;
}
