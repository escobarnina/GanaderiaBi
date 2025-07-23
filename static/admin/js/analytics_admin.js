// JavaScript personalizado para el admin de analytics

document.addEventListener("DOMContentLoaded", () => {
  // Inicializar funcionalidades del admin
  initAnalyticsAdmin()
})

function initAnalyticsAdmin() {
  // Configurar tooltips
  setupTooltips()

  // Configurar actualizaciones automáticas
  setupAutoRefresh()

  // Configurar confirmaciones para acciones masivas
  setupActionConfirmations()

  // Configurar filtros avanzados
  setupAdvancedFilters()

  // Configurar gráficos
  setupCharts()
}

function setupTooltips() {
  // Agregar tooltips a elementos con información adicional
  const elements = document.querySelectorAll("[data-tooltip]")
  elements.forEach((element) => {
    element.title = element.getAttribute("data-tooltip")
  })
}

function setupAutoRefresh() {
  // Auto-refresh para el dashboard cada 30 segundos
  if (window.location.pathname.includes("dashboarddata")) {
    setInterval(() => {
      refreshDashboardMetrics()
    }, 30000)
  }
}

function refreshDashboardMetrics() {
  // Actualizar métricas del dashboard via AJAX
  fetch("/admin/analytics/dashboarddata/metricas-api/")
    .then((response) => response.json())
    .then((data) => {
      updateDashboardDisplay(data)
    })
    .catch((error) => {
      console.error("Error actualizando métricas:", error)
    })
}

function updateDashboardDisplay(data) {
  // Actualizar elementos del dashboard con nuevos datos
  const elements = {
    "total-marcas": data.total_marcas_activas,
    "marcas-hoy": data.marcas_procesadas_hoy,
    "logos-hoy": data.logos_generados_hoy,
    "eficiencia": data.eficiencia_sistema + "%",
  }

  Object.keys(elements).forEach((id) => {
    const element = document.getElementById(id)
    if (element) {
      element.textContent = elements[id]
    }
  })
}

function setupActionConfirmations() {
  // Confirmar acciones masivas importantes
  const dangerousActions = ["rechazar_marcas", "delete_selected"]

  dangerousActions.forEach((action) => {
    const button = document.querySelector(`option[value="${action}"]`)
    if (button) {
      button.addEventListener("click", (e) => {
        if (!confirm("¿Está seguro de realizar esta acción?")) {
          e.preventDefault()
          return false
        }
      })
    }
  })
}

// Función para regenerar reportes (llamada desde el template)
function regenerarReporte(reporteId) {
  if (confirm("¿Desea regenerar este reporte?")) {
    // Aquí iría la lógica AJAX para regenerar el reporte
    fetch(`/admin/analytics/reportedata/${reporteId}/regenerar/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Reporte marcado para regeneración")
          location.reload()
        } else {
          alert("Error al regenerar reporte: " + data.error)
        }
      })
      .catch((error) => {
        console.error("Error:", error)
        alert("Error al regenerar reporte")
      })
  }
}

// Función auxiliar para obtener el token CSRF
function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

// Funciones para filtros avanzados
function setupAdvancedFilters() {
  // Configurar filtros en cascada (departamento -> municipio)
  const departamentoSelect = document.getElementById("id_departamento")
  const municipioSelect = document.getElementById("id_municipio")

  if (departamentoSelect && municipioSelect) {
    departamentoSelect.addEventListener("change", function () {
      updateMunicipios(this.value, municipioSelect)
    })
  }
}

function updateMunicipios(departamento, municipioSelect) {
  // Actualizar opciones de municipio basado en departamento seleccionado
  fetch(`/api/municipios/?departamento=${departamento}`)
    .then((response) => response.json())
    .then((data) => {
      municipioSelect.innerHTML = '<option value="">---------</option>'
      data.municipios.forEach((municipio) => {
        const option = document.createElement("option")
        option.value = municipio.codigo
        option.textContent = municipio.nombre
        municipioSelect.appendChild(option)
      })
    })
    .catch((error) => {
      console.error("Error cargando municipios:", error)
    })
}

// Configurar gráficos si Chart.js está disponible
function setupCharts() {
  if (typeof Chart !== "undefined") {
    setupKPICharts()
    setupDashboardCharts()
  }
}

function setupKPICharts() {
  const ctx = document.getElementById("kpiChart")
  if (ctx) {
    new Chart(ctx, {
      type: "line",
      data: {
        labels: [], // Se llenarían con datos reales
        datasets: [
          {
            label: "Eficiencia de Aprobación",
            data: [],
            borderColor: "#007bff",
            backgroundColor: "rgba(0, 123, 255, 0.1)",
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
          },
        },
      },
    })
  }
}

function setupDashboardCharts() {
  const ctx = document.getElementById("dashboardChart")
  if (ctx) {
    new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: ["Aprobadas", "Pendientes", "En Proceso", "Rechazadas"],
        datasets: [
          {
            data: [], // Se llenarían con datos reales
            backgroundColor: ["#28a745", "#ffc107", "#17a2b8", "#dc3545"],
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    })
  }
}

// Funciones adicionales para analytics

// Función para exportar datos
function exportarDatos(formato) {
  const url = new URL(window.location.href)
  url.searchParams.set('export', formato)
  window.location.href = url.toString()
}

// Función para aplicar filtros avanzados
function aplicarFiltrosAvanzados() {
  const form = document.getElementById('filtros-avanzados')
  if (form) {
    form.submit()
  }
}

// Función para limpiar filtros
function limpiarFiltros() {
  const inputs = document.querySelectorAll('input[type="text"], select')
  inputs.forEach(input => {
    if (input.type === 'text') {
      input.value = ''
    } else if (input.tagName === 'SELECT') {
      input.selectedIndex = 0
    }
  })
  
  // Recargar la página sin filtros
  window.location.href = window.location.pathname
}

// Función para mostrar/ocultar filtros avanzados
function toggleFiltrosAvanzados() {
  const filtros = document.getElementById('filtros-avanzados')
  if (filtros) {
    filtros.style.display = filtros.style.display === 'none' ? 'block' : 'none'
  }
}

// Función para validar formularios
function validarFormulario(form) {
  const requiredFields = form.querySelectorAll('[required]')
  let isValid = true
  
  requiredFields.forEach(field => {
    if (!field.value.trim()) {
      field.style.borderColor = '#dc3545'
      isValid = false
    } else {
      field.style.borderColor = '#28a745'
    }
  })
  
  return isValid
}

// Función para mostrar notificaciones
function mostrarNotificacion(mensaje, tipo = 'info') {
  const notification = document.createElement('div')
  notification.className = `alert alert-${tipo}`
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10000;
    padding: 15px;
    border-radius: 4px;
    color: white;
    font-weight: bold;
  `
  
  const colors = {
    success: '#28a745',
    error: '#dc3545',
    warning: '#ffc107',
    info: '#17a2b8'
  }
  
  notification.style.backgroundColor = colors[tipo] || colors.info
  notification.textContent = mensaje
  
  document.body.appendChild(notification)
  
  setTimeout(() => {
    notification.remove()
  }, 3000)
}

// Función para actualizar contadores en tiempo real
function actualizarContadores() {
  const contadores = document.querySelectorAll('[data-counter]')
  contadores.forEach(contador => {
    const url = contador.getAttribute('data-counter')
    fetch(url)
      .then(response => response.json())
      .then(data => {
        contador.textContent = data.count
      })
      .catch(error => {
        console.error('Error actualizando contador:', error)
      })
  })
}

// Configurar actualizaciones automáticas de contadores
if (document.querySelector('[data-counter]')) {
  setInterval(actualizarContadores, 60000) // Actualizar cada minuto
}

// Función para manejar acciones masivas
function ejecutarAccionMasiva(accion) {
  const checkboxes = document.querySelectorAll('input[name="_selected_action"]:checked')
  if (checkboxes.length === 0) {
    mostrarNotificacion('Debe seleccionar al menos un elemento', 'warning')
    return
  }
  
  if (confirm(`¿Está seguro de ejecutar la acción "${accion}" en ${checkboxes.length} elementos?`)) {
    const form = document.createElement('form')
    form.method = 'POST'
    form.action = window.location.href
    
    const actionInput = document.createElement('input')
    actionInput.type = 'hidden'
    actionInput.name = 'action'
    actionInput.value = accion
    form.appendChild(actionInput)
    
    checkboxes.forEach(checkbox => {
      const input = document.createElement('input')
      input.type = 'hidden'
      input.name = '_selected_action'
      input.value = checkbox.value
      form.appendChild(input)
    })
    
    // Agregar CSRF token
    const csrfInput = document.createElement('input')
    csrfInput.type = 'hidden'
    csrfInput.name = 'csrfmiddlewaretoken'
    csrfInput.value = getCookie('csrftoken')
    form.appendChild(csrfInput)
    
    document.body.appendChild(form)
    form.submit()
  }
}

// Función para ordenar tablas
function ordenarTabla(columna) {
  const tabla = document.querySelector('table')
  const tbody = tabla.querySelector('tbody')
  const filas = Array.from(tbody.querySelectorAll('tr'))
  
  filas.sort((a, b) => {
    const valorA = a.cells[columna].textContent.trim()
    const valorB = b.cells[columna].textContent.trim()
    
    // Intentar ordenar como números si es posible
    const numA = parseFloat(valorA)
    const numB = parseFloat(valorB)
    
    if (!isNaN(numA) && !isNaN(numB)) {
      return numA - numB
    }
    
    return valorA.localeCompare(valorB)
  })
  
  // Limpiar y reinsertar filas ordenadas
  filas.forEach(fila => tbody.appendChild(fila))
}

// Función para buscar en tablas
function buscarEnTabla(termino) {
  const tabla = document.querySelector('table')
  const filas = tabla.querySelectorAll('tbody tr')
  
  filas.forEach(fila => {
    const texto = fila.textContent.toLowerCase()
    const coincide = texto.includes(termino.toLowerCase())
    fila.style.display = coincide ? '' : 'none'
  })
}

// Configurar búsqueda en tiempo real
const searchInput = document.getElementById('buscar-tabla')
if (searchInput) {
  searchInput.addEventListener('input', (e) => {
    buscarEnTabla(e.target.value)
  })
} 