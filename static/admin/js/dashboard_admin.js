/**
 * JavaScript avanzado para el admin del dashboard
 * Funcionalidades: gráficos interactivos, actualización en tiempo real,
 * exportación, análisis predictivo
 */

// Importar componente Chart
import { Chart } from './chart-component.js'

// Variables globales
const dashboardCharts = {}
const realtimeInterval = null
let dashboardData = {}

// Inicialización cuando el DOM está listo
document.addEventListener("DOMContentLoaded", () => {
  initializeDashboard()
  setupEventListeners()
  startRealtimeUpdates()
})

/**
 * Inicializa el dashboard completo
 */
function initializeDashboard() {
  console.log("Inicializando dashboard ejecutivo...")

  // Inicializar gráficos
  initializeCharts()

  // Cargar datos iniciales
  loadDashboardData()

  // Configurar tooltips
  setupTooltips()

  // Configurar animaciones
  setupAnimations()
}

/**
 * Configura los event listeners
 */
function setupEventListeners() {
  // Botones del dashboard
  const refreshBtn = document.querySelector(".btn-refresh")
  if (refreshBtn) {
    refreshBtn.addEventListener("click", refreshDashboard)
  }

  const fullscreenBtn = document.querySelector(".btn-fullscreen")
  if (fullscreenBtn) {
    fullscreenBtn.addEventListener("click", toggleFullscreen)
  }

  const exportBtn = document.querySelector(".btn-export")
  if (exportBtn) {
    exportBtn.addEventListener("click", exportDashboard)
  }

  // Configurar alertas
  const configureAlertsBtn = document.querySelector(".btn-configure-alerts")
  if (configureAlertsBtn) {
    configureAlertsBtn.addEventListener("click", configureAlerts)
  }

  // Botones de recomendaciones
  const applyAllBtn = document.querySelector(".btn-apply-all")
  if (applyAllBtn) {
    applyAllBtn.addEventListener("click", applyAllRecommendations)
  }

  const scheduleBtn = document.querySelector(".btn-schedule")
  if (scheduleBtn) {
    scheduleBtn.addEventListener("click", scheduleRecommendations)
  }

  // Selector de período de comparación
  const periodSelector = document.getElementById("comparison-period")
  if (periodSelector) {
    periodSelector.addEventListener("change", updateComparison)
  }
}

/**
 * Inicializa todos los gráficos
 */
function initializeCharts() {
  // Gráfico de tendencia de aprobaciones
  initApprovalTrendChart()

  // Gráfico de distribución de ganado
  initCattleDistributionChart()

  // Gráfico de rendimiento IA
  initAIPerformanceChart()

  // Gráfico geográfico
  initGeographicChart()

  // Gráfico de actividad en tiempo real
  initRealtimeActivityChart()

  // Gráfico de proyección de crecimiento
  initGrowthPredictionChart()

  // Gráfico de evolución histórica
  initHistoricalEvolutionChart()
}

/**
 * Inicializa el gráfico de tendencia de aprobaciones
 */
function initApprovalTrendChart() {
  const ctx = document.getElementById("approval-trend-chart")
  if (!ctx) return

  dashboardCharts.approvalTrend = new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Ene", "Feb", "Mar", "Abr", "May", "Jun"],
      datasets: [
        {
          label: "Tasa de Aprobación",
          data: [78, 82, 85, 88, 91, 89],
          borderColor: "#28a745",
          backgroundColor: "rgba(40, 167, 69, 0.1)",
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: "#28a745",
          pointBorderColor: "#fff",
          pointBorderWidth: 2,
          pointRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          backgroundColor: "rgba(0, 0, 0, 0.8)",
          titleColor: "#fff",
          bodyColor: "#fff",
          borderColor: "#28a745",
          borderWidth: 1,
          callbacks: {
            label: (context) => `Aprobación: ${context.parsed.y}%`,
          },
        },
      },
      scales: {
        y: {
          beginAtZero: false,
          min: 70,
          max: 100,
          ticks: {
            callback: (value) => value + "%",
          },
          grid: {
            color: "rgba(0, 0, 0, 0.1)",
          },
        },
        x: {
          grid: {
            display: false,
          },
        },
      },
      interaction: {
        intersect: false,
        mode: "index",
      },
      animation: {
        duration: 2000,
        easing: "easeInOutQuart",
      },
    },
  })
}

/**
 * Inicializa el gráfico de distribución de ganado
 */
function initCattleDistributionChart() {
  const ctx = document.getElementById("cattle-distribution-chart")
  if (!ctx) return

  dashboardCharts.cattleDistribution = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Carne", "Leche", "Doble Propósito", "Reproducción"],
      datasets: [
        {
          data: [35, 28, 25, 12],
          backgroundColor: ["#dc3545", "#007bff", "#28a745", "#ffc107"],
          borderWidth: 0,
          hoverBorderWidth: 3,
          hoverBorderColor: "#fff",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            padding: 20,
            usePointStyle: true,
            font: {
              size: 12,
            },
          },
        },
        tooltip: {
          backgroundColor: "rgba(0, 0, 0, 0.8)",
          titleColor: "#fff",
          bodyColor: "#fff",
          callbacks: {
            label: (context) => {
              const label = context.label || ""
              const value = context.parsed
              const total = context.dataset.data.reduce((a, b) => a + b, 0)
              const percentage = ((value / total) * 100).toFixed(1)
              return `${label}: ${percentage}%`
            },
          },
        },
      },
      animation: {
        animateRotate: true,
        duration: 2000,
      },
    },
  })
}

/**
 * Inicializa el gráfico de rendimiento IA
 */
function initAIPerformanceChart() {
  const ctx = document.getElementById("ai-performance-chart")
  if (!ctx) return

  dashboardCharts.aiPerformance = new Chart(ctx, {
    type: "radar",
    data: {
      labels: ["Velocidad", "Precisión", "Calidad", "Eficiencia", "Innovación"],
      datasets: [
        {
          label: "Rendimiento Actual",
          data: [85, 92, 88, 90, 78],
          borderColor: "#6f42c1",
          backgroundColor: "rgba(111, 66, 193, 0.2)",
          borderWidth: 2,
          pointBackgroundColor: "#6f42c1",
          pointBorderColor: "#fff",
          pointBorderWidth: 2,
        },
        {
          label: "Objetivo",
          data: [90, 95, 90, 95, 85],
          borderColor: "#28a745",
          backgroundColor: "rgba(40, 167, 69, 0.1)",
          borderWidth: 2,
          borderDash: [5, 5],
          pointBackgroundColor: "#28a745",
          pointBorderColor: "#fff",
          pointBorderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
        },
      },
      scales: {
        r: {
          beginAtZero: true,
          max: 100,
          ticks: {
            stepSize: 20,
          },
        },
      },
      animation: {
        duration: 2000,
        easing: "easeInOutQuart",
      },
    },
  })
}

/**
 * Inicializa el gráfico geográfico
 */
function initGeographicChart() {
  const ctx = document.getElementById("geographic-chart")
  if (!ctx) return

  dashboardCharts.geographic = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Santa Cruz", "Beni", "La Paz", "Cochabamba", "Otros"],
      datasets: [
        {
          label: "Marcas Registradas",
          data: [45, 28, 18, 6, 3],
          backgroundColor: ["#007bff", "#28a745", "#ffc107", "#dc3545", "#6c757d"],
          borderRadius: 6,
          borderSkipped: false,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          backgroundColor: "rgba(0, 0, 0, 0.8)",
          titleColor: "#fff",
          bodyColor: "#fff",
          callbacks: {
            label: (context) => `${context.parsed.y}% del total`,
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 50,
          ticks: {
            callback: (value) => value + "%",
          },
        },
      },
      animation: {
        duration: 2000,
        easing: "easeInOutQuart",
      },
    },
  })
}

/**
 * Inicializa el gráfico de actividad en tiempo real
 */
function initRealtimeActivityChart() {
  const ctx = document.getElementById("realtime-activity-chart")
  if (!ctx) return

  // Generar datos iniciales
  const now = new Date()
  const labels = []
  const data = []

  for (let i = 29; i >= 0; i--) {
    const time = new Date(now.getTime() - i * 60000) // Cada minuto
    labels.push(time.toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" }))
    data.push(Math.floor(Math.random() * 20) + 5)
  }

  dashboardCharts.realtimeActivity = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Actividad",
          data: data,
          borderColor: "#17a2b8",
          backgroundColor: "rgba(23, 162, 184, 0.1)",
          borderWidth: 2,
          fill: true,
          tension: 0.4,
          pointRadius: 0,
          pointHoverRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 30,
        },
        x: {
          display: false,
        },
      },
      animation: {
        duration: 0, // Sin animación para tiempo real
      },
    },
  })
}

/**
 * Inicializa el gráfico de proyección de crecimiento
 */
function initGrowthPredictionChart() {
  const ctx = document.getElementById("growth-prediction-chart")
  if (!ctx) return

  dashboardCharts.growthPrediction = new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep"],
      datasets: [
        {
          label: "Datos Reales",
          data: [120, 135, 148, 162, 178, 195, null, null, null],
          borderColor: "#007bff",
          backgroundColor: "rgba(0, 123, 255, 0.1)",
          borderWidth: 3,
          fill: false,
          pointBackgroundColor: "#007bff",
        },
        {
          label: "Predicción",
          data: [null, null, null, null, null, 195, 210, 225, 240],
          borderColor: "#28a745",
          backgroundColor: "rgba(40, 167, 69, 0.1)",
          borderWidth: 3,
          borderDash: [10, 5],
          fill: false,
          pointBackgroundColor: "#28a745",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
        },
        tooltip: {
          backgroundColor: "rgba(0, 0, 0, 0.8)",
          titleColor: "#fff",
          bodyColor: "#fff",
        },
      },
      scales: {
        y: {
          beginAtZero: false,
          min: 100,
        },
      },
      animation: {
        duration: 2000,
        easing: "easeInOutQuart",
      },
    },
  })
}

/**
 * Inicializa el gráfico de evolución histórica
 */
function initHistoricalEvolutionChart() {
  const ctx = document.getElementById("historical-evolution-chart")
  if (!ctx) return

  dashboardCharts.historicalEvolution = new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023", "Q1 2024", "Q2 2024"],
      datasets: [
        {
          label: "Marcas Registradas",
          data: [450, 520, 580, 620, 680, 750],
          borderColor: "#007bff",
          backgroundColor: "rgba(0, 123, 255, 0.1)",
          yAxisID: "y",
        },
        {
          label: "Ingresos (Miles Bs.)",
          data: [180, 210, 235, 260, 290, 320],
          borderColor: "#28a745",
          backgroundColor: "rgba(40, 167, 69, 0.1)",
          yAxisID: "y1",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
        },
      },
      scales: {
        y: {
          type: "linear",
          display: true,
          position: "left",
          title: {
            display: true,
            text: "Marcas",
          },
        },
        y1: {
          type: "linear",
          display: true,
          position: "right",
          title: {
            display: true,
            text: "Ingresos (Miles Bs.)",
          },
          grid: {
            drawOnChartArea: false,
          },
        },
      },
      animation: {
        duration: 2000,
        easing: "easeInOutQuart",
      },
    },
  })
}

/**
 * Carga los datos del dashboard
 */
function loadDashboardData() {
  fetch("/admin/analytics/dashboarddatamodel/api/dashboard-data/")
    .then((response) => response.json())
    .then((data) => {
      dashboardData = data
      updateDashboardMetrics(data)
    })
    .catch((error) => {
      console.error("Error cargando datos del dashboard:", error)
      showNotification("Error al cargar datos del dashboard", "error")
    })
}

/**
 * Actualiza las métricas del dashboard
 */
function updateDashboardMetrics(data) {
  // Actualizar KPIs principales
  updateKPICard("marcas-registradas", data.marcas_registradas_mes_actual)
  updateKPICard("tiempo-procesamiento", data.tiempo_promedio_procesamiento)
  updateKPICard("porcentaje-aprobacion", data.porcentaje_aprobacion)
  updateKPICard("ingresos-mes", data.ingresos_mes_actual)

  // Actualizar métricas en tiempo real
  updateRealtimeMetrics(data)

  // Actualizar alertas
  updateAlerts(data.alertas)

  // Actualizar recomendaciones
  updateRecommendations(data)
}

/**
 * Actualiza una tarjeta KPI específica
 */
function updateKPICard(kpiId, value) {
  const kpiElement = document.getElementById(kpiId)
  if (!kpiElement) return

  const valueElement = kpiElement.querySelector(".kpi-value")
  if (valueElement) {
    valueElement.textContent = formatValue(value)
  }

  // Actualizar tendencia si existe
  const trendElement = kpiElement.querySelector(".kpi-trend")
  if (trendElement) {
    const trend = calculateTrend(value)
    trendElement.textContent = trend.text
    trendElement.className = `kpi-trend ${trend.class}`
  }
}

/**
 * Formatea un valor según su tipo
 */
function formatValue(value) {
  if (typeof value === "number") {
    if (value >= 1000000) {
      return (value / 1000000).toFixed(1) + "M"
    } else if (value >= 1000) {
      return (value / 1000).toFixed(1) + "K"
    } else {
      return value.toLocaleString()
    }
  }
  return value
}

/**
 * Calcula la tendencia de un valor
 */
function calculateTrend(value) {
  // Simulación de cálculo de tendencia
  const random = Math.random()
  if (random > 0.6) {
    return { text: "+12.5%", class: "trend-up" }
  } else if (random > 0.3) {
    return { text: "-5.2%", class: "trend-down" }
  } else {
    return { text: "0.0%", class: "trend-neutral" }
  }
}

/**
 * Actualiza las métricas en tiempo real
 */
function updateRealtimeMetrics(data) {
  const metricsContainer = document.querySelector(".metrics-grid")
  if (!metricsContainer) return

  // Simular actualización de métricas en tiempo real
  const metrics = [
    { id: "realtime-activity", value: Math.floor(Math.random() * 50) + 10 },
    { id: "realtime-approvals", value: Math.floor(Math.random() * 20) + 5 },
    { id: "realtime-revenue", value: Math.floor(Math.random() * 1000) + 500 },
    { id: "realtime-efficiency", value: Math.floor(Math.random() * 20) + 80 },
  ]

  metrics.forEach((metric) => {
    const element = document.getElementById(metric.id)
    if (element) {
      const valueElement = element.querySelector(".metric-value")
      if (valueElement) {
        valueElement.textContent = formatValue(metric.value)
      }
    }
  })
}

/**
 * Actualiza las alertas del sistema
 */
function updateAlerts(alertas) {
  const alertsContainer = document.querySelector(".alerts-grid")
  if (!alertsContainer) return

  // Limpiar alertas existentes
  alertsContainer.innerHTML = ""

  // Generar alertas basadas en los datos
  const alerts = generateAlerts(alertas)
  alerts.forEach((alert) => {
    const alertElement = createAlertElement(alert)
    alertsContainer.appendChild(alertElement)
  })
}

/**
 * Genera alertas basadas en los datos
 */
function generateAlerts(alertas) {
  const alerts = []
  
  if (alertas && alertas.length > 0) {
    alertas.forEach((alerta) => {
      alerts.push({
        type: "critical",
        icon: "🚨",
        title: "Alerta Crítica",
        message: alerta,
        time: new Date().toLocaleTimeString(),
      })
    })
  }

  // Agregar alertas simuladas
  if (Math.random() > 0.7) {
    alerts.push({
      type: "warning",
      icon: "⚠️",
      title: "Rendimiento Bajo",
      message: "El tiempo de procesamiento está por encima del promedio",
      time: new Date().toLocaleTimeString(),
    })
  }

  return alerts
}

/**
 * Crea un elemento de alerta
 */
function createAlertElement(alert) {
  const alertDiv = document.createElement("div")
  alertDiv.className = `alert ${alert.type}`
  alertDiv.innerHTML = `
    <div class="alert-icon">${alert.icon}</div>
    <div class="alert-content">
      <h4>${alert.title}</h4>
      <p>${alert.message}</p>
      <small>${alert.time}</small>
    </div>
    <div class="alert-actions">
      <button class="btn-action">Ver</button>
      <button class="btn-action">Dismiss</button>
    </div>
  `
  return alertDiv
}

/**
 * Actualiza las recomendaciones
 */
function updateRecommendations(data) {
  const recommendationsContainer = document.querySelector(".recommendations-list")
  if (!recommendationsContainer) return

  // Limpiar recomendaciones existentes
  recommendationsContainer.innerHTML = ""

  // Generar recomendaciones basadas en los datos
  const recommendations = generateRecommendations(data)
  recommendations.forEach((rec) => {
    const recElement = createRecommendationElement(rec)
    recommendationsContainer.appendChild(recElement)
  })
}

/**
 * Genera recomendaciones basadas en los datos
 */
function generateRecommendations(data) {
  const recommendations = []

  // Recomendación basada en tiempo de procesamiento
  if (data.tiempo_promedio_procesamiento > 5) {
    recommendations.push({
      priority: "high",
      title: "Optimizar Procesamiento",
      description: "El tiempo de procesamiento está por encima del objetivo. Considerar optimización de algoritmos.",
      impact: "Alto impacto en eficiencia",
      benefits: ["Reducción de tiempo", "Mejor experiencia", "Mayor productividad"],
    })
  }

  // Recomendación basada en aprobaciones
  if (data.porcentaje_aprobacion < 85) {
    recommendations.push({
      priority: "medium",
      title: "Mejorar Criterios de Aprobación",
      description: "La tasa de aprobación está por debajo del objetivo. Revisar criterios de evaluación.",
      impact: "Medio impacto en calidad",
      benefits: ["Mayor calidad", "Menos rechazos", "Mejor satisfacción"],
    })
  }

  return recommendations
}

/**
 * Crea un elemento de recomendación
 */
function createRecommendationElement(rec) {
  const recDiv = document.createElement("div")
  recDiv.className = "recommendation-item"
  recDiv.innerHTML = `
    <div class="rec-header">
      <h5>${rec.title}</h5>
      <span class="rec-priority ${rec.priority}">${rec.priority.toUpperCase()}</span>
    </div>
    <div class="rec-content">
      <p>${rec.description}</p>
      <div class="rec-benefits">
        ${rec.benefits.map(benefit => `<span class="benefit">${benefit}</span>`).join("")}
      </div>
    </div>
    <div class="rec-actions">
      <button class="btn-apply">Aplicar</button>
      <button class="btn-schedule">Programar</button>
    </div>
  `
  return recDiv
}

/**
 * Inicia las actualizaciones en tiempo real
 */
function startRealtimeUpdates() {
  // Actualizar cada 30 segundos
  setInterval(() => {
    updateRealtimeMetrics(dashboardData)
    updateRealtimeActivityChart()
  }, 30000)
}

/**
 * Actualiza el gráfico de actividad en tiempo real
 */
function updateRealtimeActivityChart() {
  if (!dashboardCharts.realtimeActivity) return

  const chart = dashboardCharts.realtimeActivity
  const data = chart.data.datasets[0].data

  // Agregar nuevo punto
  data.push(Math.floor(Math.random() * 20) + 5)
  data.shift()

  // Actualizar etiquetas
  const now = new Date()
  const labels = chart.data.labels
  labels.push(now.toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" }))
  labels.shift()

  chart.update("none")
}

/**
 * Refresca el dashboard completo
 */
function refreshDashboard() {
  showNotification("Actualizando dashboard...", "info")
  loadDashboardData()
  
  // Refrescar gráficos
  Object.values(dashboardCharts).forEach(chart => {
    if (chart && typeof chart.update === "function") {
      chart.update()
    }
  })
  
  setTimeout(() => {
    showNotification("Dashboard actualizado", "success")
  }, 1000)
}

/**
 * Alterna el modo pantalla completa
 */
function toggleFullscreen() {
  const dashboard = document.querySelector(".executive-dashboard-container")
  if (!dashboard) return

  if (!document.fullscreenElement) {
    dashboard.requestFullscreen()
    showNotification("Modo pantalla completa activado", "info")
  } else {
    document.exitFullscreen()
    showNotification("Modo pantalla completa desactivado", "info")
  }
}

/**
 * Exporta el dashboard
 */
function exportDashboard() {
  showNotification("Exportando dashboard...", "info")
  
  // Simular exportación
  setTimeout(() => {
    const link = document.createElement("a")
    link.download = `dashboard-${new Date().toISOString().split("T")[0]}.pdf`
    link.href = "#"
    link.click()
    
    showNotification("Dashboard exportado exitosamente", "success")
  }, 2000)
}

/**
 * Configura las alertas
 */
function configureAlerts() {
  showNotification("Abriendo configuración de alertas...", "info")
  // Aquí se abriría un modal de configuración
}

/**
 * Aplica todas las recomendaciones
 */
function applyAllRecommendations() {
  showNotification("Aplicando todas las recomendaciones...", "info")
  
  setTimeout(() => {
    showNotification("Recomendaciones aplicadas exitosamente", "success")
    // Recargar dashboard para reflejar cambios
    refreshDashboard()
  }, 1500)
}

/**
 * Programa las recomendaciones
 */
function scheduleRecommendations() {
  showNotification("Programando recomendaciones...", "info")
  
  setTimeout(() => {
    showNotification("Recomendaciones programadas para mañana", "success")
  }, 1000)
}

/**
 * Actualiza la comparación según el período seleccionado
 */
function updateComparison() {
  const periodSelector = document.getElementById("comparison-period")
  if (!periodSelector) return

  const selectedPeriod = periodSelector.value
  showNotification(`Actualizando comparación para ${selectedPeriod}...`, "info")
  
  // Aquí se actualizarían los datos de comparación
  setTimeout(() => {
    showNotification("Comparación actualizada", "success")
  }, 1000)
}

/**
 * Configura los tooltips
 */
function setupTooltips() {
  // Configurar tooltips personalizados
  const tooltipElements = document.querySelectorAll("[data-tooltip]")
  tooltipElements.forEach(element => {
    element.addEventListener("mouseenter", showTooltip)
    element.addEventListener("mouseleave", hideTooltip)
  })
}

/**
 * Muestra un tooltip
 */
function showTooltip(event) {
  const tooltip = document.createElement("div")
  tooltip.className = "custom-tooltip"
  tooltip.textContent = event.target.getAttribute("data-tooltip")
  tooltip.style.position = "absolute"
  tooltip.style.backgroundColor = "rgba(0, 0, 0, 0.8)"
  tooltip.style.color = "white"
  tooltip.style.padding = "8px 12px"
  tooltip.style.borderRadius = "4px"
  tooltip.style.fontSize = "12px"
  tooltip.style.zIndex = "1000"
  tooltip.style.pointerEvents = "none"
  
  document.body.appendChild(tooltip)
  
  const rect = event.target.getBoundingClientRect()
  tooltip.style.left = rect.left + "px"
  tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + "px"
  
  event.target._tooltip = tooltip
}

/**
 * Oculta un tooltip
 */
function hideTooltip(event) {
  if (event.target._tooltip) {
    event.target._tooltip.remove()
    event.target._tooltip = null
  }
}

/**
 * Configura las animaciones
 */
function setupAnimations() {
  // Configurar animaciones de entrada
  const animatedElements = document.querySelectorAll(".kpi-card, .chart-container, .metric-card")
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1"
        entry.target.style.transform = "translateY(0)"
      }
    })
  })
  
  animatedElements.forEach(element => {
    element.style.opacity = "0"
    element.style.transform = "translateY(20px)"
    element.style.transition = "opacity 0.5s ease, transform 0.5s ease"
    observer.observe(element)
  })
}

/**
 * Muestra una notificación
 */
function showNotification(message, type = "info") {
  const notification = document.createElement("div")
  notification.className = `notification notification-${type}`
  notification.textContent = message
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 12px 20px;
    border-radius: 6px;
    color: white;
    font-weight: 600;
    z-index: 10000;
    animation: slideIn 0.3s ease-out;
  `
  
  // Colores según tipo
  const colors = {
    success: "#28a745",
    error: "#dc3545",
    warning: "#ffc107",
    info: "#17a2b8"
  }
  
  notification.style.backgroundColor = colors[type] || colors.info
  
  document.body.appendChild(notification)
  
  setTimeout(() => {
    notification.style.animation = "slideOut 0.3s ease-out"
    setTimeout(() => {
      notification.remove()
    }, 300)
  }, 3000)
}

// Agregar estilos CSS para animaciones
const style = document.createElement("style")
style.textContent = `
  @keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  
  @keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
  }
`
document.head.appendChild(style) 