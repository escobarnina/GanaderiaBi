/**
 * Componente Chart simple como placeholder
 * Para ser reemplazado con Chart.js o similar en producción
 */

export const Chart = () => {
  return {
    // Método para crear un gráfico
    create: function(canvas, config) {
      console.log('Chart placeholder creado:', config)
      
      // Crear un div placeholder
      const placeholder = document.createElement('div')
      placeholder.className = 'chart-placeholder'
      placeholder.style.cssText = `
        width: 100%;
        height: 300px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 2px dashed #dee2e6;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #6c757d;
        font-size: 14px;
        font-weight: 600;
      `
      placeholder.innerHTML = `
        <div style="text-align: center;">
          <div style="font-size: 48px; margin-bottom: 10px;">📊</div>
          <div>Gráfico: ${config.type || 'Gráfico'}</div>
          <div style="font-size: 12px; margin-top: 5px;">Chart.js placeholder</div>
        </div>
      `
      
      // Reemplazar el canvas con el placeholder
      if (canvas.parentNode) {
        canvas.parentNode.replaceChild(placeholder, canvas)
      }
      
      return {
        // Método para actualizar el gráfico
        update: function(mode = 'default') {
          console.log('Actualizando gráfico:', mode)
          // Aquí se actualizaría el gráfico real
        },
        
        // Método para destruir el gráfico
        destroy: function() {
          console.log('Destruyendo gráfico')
          if (placeholder.parentNode) {
            placeholder.parentNode.removeChild(placeholder)
          }
        }
      }
    }
  }
}

// Función global para crear gráficos
window.Chart = function(canvas, config) {
  const chartComponent = Chart()
  return chartComponent.create(canvas, config)
}

// Función para inicializar gráficos específicos
function initChart(canvasId, config) {
  const canvas = document.getElementById(canvasId)
  if (!canvas) {
    console.warn(`Canvas con id '${canvasId}' no encontrado`)
    return null
  }
  
  return new window.Chart(canvas, config)
}

// Exportar para uso global
window.initChart = initChart 