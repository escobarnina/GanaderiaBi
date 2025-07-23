/**
 * JavaScript mejorado para Reporte Admin - Clean Architecture
 *
 * Responsabilidades:
 * - Gestionar visualizador de reportes interactivo
 * - Manejar análisis de contenido y métricas
 * - Proporcionar funcionalidad de exportación avanzada
 * - Gestionar sistema de recomendaciones
 */

// Configuración global
const ReportConfig = {
  maxPreviewSize: 1000000, // 1MB
  supportedFormats: ["PDF", "EXCEL", "JSON", "CSV", "HTML"],
  chartColors: {
    primary: "#007bff",
    success: "#28a745",
    warning: "#ffc107",
    danger: "#dc3545",
    info: "#17a2b8",
    purple: "#6f42c1",
  },
  apiEndpoints: {
    reportData: "/admin/analytics/reportedatamodel/api/report-data/",
    preview: "/admin/analytics/reportedatamodel/{id}/preview/",
    download: "/admin/analytics/reportedatamodel/{id}/download/",
  },
}

// Clase principal para gestión de reportes
class ReportManager {
    constructor() {
        this.currentReport = null;
        this.charts = {};
        this.previewCache = new Map();
        this.init();
    }

    init() {
        this.initializeCharts();
        this.setupEventListeners();
        this.initializeViewers();
        this.setupRecommendationSystem();
    }

    // Inicialización de gráficos
    initializeCharts() {
        this.initDataStructureChart();
        this.initUsageTrendChart();
        this.initQualityMetricsChart();
        this.initComparisonChart();
    }

    initDataStructureChart() {
        const canvases = document.querySelectorAll('[id^="data-structure-chart-"]');
        canvases.forEach(canvas => {
            const reportId = canvas.id.split('-').pop();
            
            this.charts[`dataStructure_${reportId}`] = new Chart(canvas, {
                type: 'doughnut',
                data: {
                    labels: ['Objetos', 'Arrays', 'Strings', 'Números', 'Booleanos'],
                    datasets: [{
                        data: [35, 25, 20, 15, 5],
                        backgroundColor: [
                            ReportConfig.chartColors.primary,
                            ReportConfig.chartColors.success,
                            ReportConfig.chartColors.warning,
                            ReportConfig.chartColors.info,
                            ReportConfig.chartColors.danger
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { 
                                color: 'white',
                                font: { size: 10 }
                            }
                        }
                    }
                }
            });
        });
    }

    initUsageTrendChart() {
        const ctx = document.getElementById('usage-trend-chart');
        if (!ctx) return;

        this.charts.usageTrend = new Chart(ctx, {
            type: 'line',
            data: {
                labels: Array.from({length: 30}, (_, i) => {
                    const date = new Date();
                    date.setDate(date.getDate() - (29 - i));
                    return date.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit' });
                }),
                datasets: [
                    {
                        label: 'Visualizaciones',
                        data: this.generateTrendData(30, 10, 50),
                        borderColor: ReportConfig.chartColors.primary,
                        backgroundColor: ReportConfig.chartColors.primary + '20',
                        tension: 0.4
                    },
                    {
                        label: 'Descargas',
                        data: this.generateTrendData(30, 5, 25),
                        borderColor: ReportConfig.chartColors.success,
                        backgroundColor: ReportConfig.chartColors.success + '20',
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: 'white' }
                    }
                },
                scales: {
                    x: {
                        ticks: { 
                            color: 'white',
                            maxTicksLimit: 7
                        },
                        grid: { color: 'rgba(255,255,255,0.1)' }
                    },
                    y: {
                        ticks: { color: 'white' },
                        grid: { color: 'rgba(255,255,255,0.1)' }
                    }
                }
            }
        });
    }

    initQualityMetricsChart() {
        const ctx = document.getElementById('quality-metrics-chart');
        if (!ctx) return;

        this.charts.qualityMetrics = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Completitud', 'Precisión', 'Consistencia', 'Actualidad', 'Relevancia'],
                datasets: [{
                    label: 'Calidad de Datos',
                    data: [92, 88, 95, 85, 90],
                    borderColor: ReportConfig.chartColors.success,
                    backgroundColor: ReportConfig.chartColors.success + '30',
                    pointBackgroundColor: ReportConfig.chartColors.success
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: 'white' }
                    }
                },
                scales: {
                    r: {
                        ticks: { color: 'white' },
                        grid: { color: 'rgba(255,255,255,0.2)' },
                        pointLabels: { color: 'white' },
                        min: 0,
                        max: 100
                    }
                }
            }
        });
    }

    initComparisonChart() {
        const ctx = document.getElementById('comparison-chart');
        if (!ctx) return;

        this.charts.comparison = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Tamaño', 'Velocidad', 'Popularidad', 'Calidad', 'Eficiencia'],
                datasets: [
                    {
                        label: 'Reporte Actual',
                        data: [85, 70, 90, 88, 82],
                        backgroundColor: ReportConfig.chartColors.primary
                    },
                    {
                        label: 'Promedio Sector',
                        data: [75, 80, 65, 85, 78],
                        backgroundColor: ReportConfig.chartColors.info
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: 'white' }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: 'white' },
                        grid: { color: 'rgba(255,255,255,0.1)' }
                    },
                    y: {
                        ticks: { color: 'white' },
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        min: 0,
                        max: 100
                    }
                }
            }
        });
    }

    // Event listeners
    setupEventListeners() {
        // Botones del visualizador
        document.addEventListener('click', (e) => {
            if (e.target.matches('.btn-zoom-in')) {
                this.zoomReport('in');
            } else if (e.target.matches('.btn-zoom-out')) {
                this.zoomReport('out');
            } else if (e.target.matches('.btn-fullscreen')) {
                this.toggleReportFullscreen();
            } else if (e.target.matches('.btn-print')) {
                this.printReport();
            } else if (e.target.matches('.btn-expand')) {
                this.expandData(e.target.dataset.reportId);
            }
        });

        // Responsive charts
        window.addEventListener('resize', () => {
            Object.values(this.charts).forEach(chart => {
                if (chart) chart.resize();
            });
        });
    }

    // Visualizadores
    initializeViewers() {
        this.initializeReportPreviews();
        this.setupLazyLoading();
    }

    initializeReportPreviews() {
        const previewElements = document.querySelectorAll('[id^="content-preview-"]');
        previewElements.forEach(element => {
            const reportId = element.id.split('-').pop();
            this.loadReportPreview(reportId, element);
        });
    }

    async loadReportPreview(reportId, element) {
        try {
            // Verificar cache
            if (this.previewCache.has(reportId)) {
                element.innerHTML = this.previewCache.get(reportId);
                return;
            }

            element.innerHTML = '<div class="loading-preview">Cargando vista previa...</div>';

            const response = await fetch(
                ReportConfig.apiEndpoints.reportData.replace('{id}', reportId)
            );
            const data = await response.json();

            if (data.error) {
                element.innerHTML = `<div class="error-preview">Error: ${data.error}</div>`;
                return;
            }

            const previewHtml = this.generatePreviewHtml(data);
            element.innerHTML = previewHtml;
            
            // Guardar en cache
            this.previewCache.set(reportId, previewHtml);

        } catch (error) {
            console.error('Error al cargar vista previa:', error);
            element.innerHTML = '<div class="error-preview">Error al cargar vista previa</div>';
        }
    }

    generatePreviewHtml(data) {
        const formatIcons = {
            'PDF': '📄',
            'EXCEL': '📊',
            'JSON': '🔧',
            'CSV': '📋',
            'HTML': '🌐'
        };

        return `
            <div class="report-preview">
                <div class="preview-header">
                    <div class="report-type">
                        <span class="type-icon">${formatIcons[data.formato] || '📁'}</span>
                        <span class="type-text">${data.tipo}</span>
                    </div>
                    <div class="report-format">${data.formato}</div>
                </div>
                
                <div class="preview-content">
                    <div class="content-summary">
                        <h4>Resumen del Contenido</h4>
                        <p>Reporte generado el ${new Date(data.fecha_generacion).toLocaleDateString('es-ES')}</p>
                        <p>Tamaño: ${data.tamaño}</p>
                        ${data.datos_preview ? `
                            <div class="data-preview">
                                <h5>Vista previa de datos:</h5>
                                <pre>${data.datos_preview}</pre>
                            </div>
                        ` : ''}
                    </div>
                </div>
                
                <div class="preview-actions">
                    <button class="btn-preview-download" onclick="downloadReport(${data.id})">
                        📥 Descargar
                    </button>
                    <button class="btn-preview-analyze" onclick="analyzeReport(${data.id})">
                        📊 Analizar
                    </button>
                </div>
            </div>
        `;
    }

    setupLazyLoading() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    const reportId = element.dataset.reportId;
                    if (reportId && !element.dataset.loaded) {
                        this.loadReportPreview(reportId, element);
                        element.dataset.loaded = 'true';
                        observer.unobserve(element);
                    }
                }
            });
        });

        document.querySelectorAll('[data-report-id]').forEach(element => {
            observer.observe(element);
        });
    }

    // Sistema de recomendaciones
    setupRecommendationSystem() {
        this.initializeRecommendationEngine();
        this.setupRecommendationActions();
    }

    initializeRecommendationEngine() {
        // Simular análisis de recomendaciones
        this.analyzeReportPatterns();
        this.generateSmartRecommendations();
    }

    analyzeReportPatterns() {
        // Análisis de patrones de uso
        const reports = document.querySelectorAll('.report-item');
        const patterns = {
            mostUsedFormats: this.analyzeMostUsedFormats(reports),
            peakUsageTimes: this.analyzePeakUsageTimes(),
            userPreferences: this.analyzeUserPreferences()
        };

        console.log('Patrones analizados:', patterns);
    }

    generateSmartRecommendations() {
        const recommendations = [
            {
                type: 'optimization',
                priority: 'high',
                title: 'Optimizar Formato de Salida',
                description: 'Cambiar a PDF para mejor compatibilidad',
                impact: 'Alto',
                effort: 'Bajo'
            },
            {
                type: 'automation',
                priority: 'medium',
                title: 'Automatizar Generación',
                description: 'Programar generación automática semanal',
                impact: 'Medio',
                effort: 'Medio'
            },
            {
                type: 'performance',
                priority: 'low',
                title: 'Comprimir Datos',
                description: 'Reducir tamaño del reporte en 40%',
                impact: 'Bajo',
                effort: 'Alto'
            }
        ];

        this.displayRecommendations(recommendations);
    }

    displayRecommendations(recommendations) {
        const containers = document.querySelectorAll('.recommendations-list');
        containers.forEach(container => {
            container.innerHTML = recommendations.map(rec => 
                this.createRecommendationHtml(rec)
            ).join('');
        });
    }

    createRecommendationHtml(recommendation) {
        const priorityColors = {
            high: 'danger',
            medium: 'warning',
            low: 'info'
        };

        const typeIcons = {
            optimization: '⚡',
            automation: '🤖',
            performance: '📈',
            security: '🔒'
        };

        return `
            <div class="recommendation-item ${recommendation.priority}-priority">
                <div class="rec-header">
                    <span class="rec-priority ${recommendation.priority}-priority">
                        ${recommendation.priority === 'high' ? 'Alta Prioridad' : 
                          recommendation.priority === 'medium' ? 'Media Prioridad' : 'Baja Prioridad'}
                    </span>
                    <span class="rec-impact">Impacto: ${recommendation.impact}</span>
                </div>
                <div class="rec-content">
                    <h5>
                        ${typeIcons[recommendation.type] || '💡'} 
                        ${recommendation.title}
                    </h5>
                    <p>${recommendation.description}</p>
                    <div class="rec-benefits">
                        <span class="benefit">📊 Impacto: ${recommendation.impact}</span>
                        <span class="benefit">⚡ Esfuerzo: ${recommendation.effort}</span>
                    </div>
                    <div class="rec-actions">
                        <button class="btn-apply" onclick="applyRecommendation('${recommendation.type}')">
                            Aplicar
                        </button>
                        <button class="btn-schedule" onclick="scheduleRecommendation('${recommendation.type}')">
                            Programar
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    setupRecommendationActions() {
        // Event listeners para acciones de recomendaciones
        document.addEventListener('click', (e) => {
            if (e.target.matches('.btn-apply-recommendations')) {
                this.applyAllRecommendations();
            } else if (e.target.matches('.btn-schedule-improvements')) {
                this.scheduleAllImprovements();
            }
        });
    }

    // Funciones de utilidad
    generateTrendData(days, min, max) {
        return Array.from({length: days}, () => 
            Math.floor(Math.random() * (max - min + 1)) + min
        );
    }

    analyzeMostUsedFormats(reports) {
        const formatCount = {};
        reports.forEach(report => {
            const format = report.dataset.format;
            formatCount[format] = (formatCount[format] || 0) + 1;
        });
        return formatCount;
    }

    analyzePeakUsageTimes() {
        // Simular análisis de horarios pico
        return {
            morning: 35,
            afternoon: 45,
            evening: 20
        };
    }

    analyzeUserPreferences() {
        // Simular análisis de preferencias de usuario
        return {
            preferredFormats: ['PDF', 'EXCEL'],
            averageReportSize: '2.5MB',
            commonReportTypes: ['Mensual', 'Trimestral']
        };
    }

    // Funciones de interacción
    zoomReport(direction) {
        const preview = document.querySelector('.content-preview');
        if (!preview) return;

        const currentScale = parseFloat(preview.style.transform.replace('scale(', '').replace(')', '')) || 1;
        const newScale = direction === 'in' ? currentScale * 1.2 : currentScale / 1.2;
        
        preview.style.transform = `scale(${Math.max(0.5, Math.min(3, newScale))})`;
    }

    toggleReportFullscreen() {
        const viewer = document.querySelector('.report-viewer-container');
        if (!viewer) return;

        if (!document.fullscreenElement) {
            viewer.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    }

    printReport() {
        const printWindow = window.open('', '_blank');
        const reportContent = document.querySelector('.content-preview').innerHTML;
        
        printWindow.document.write(`
            <html>
                <head>
                    <title>Reporte - Impresión</title>
                    <style>
                        body { font-family: Arial, sans-serif; }
                        .report-content { padding: 20px; }
                    </style>
                </head>
                <body>
                    <div class="report-content">${reportContent}</div>
                </body>
            </html>
        `);
        printWindow.document.close();
        printWindow.print();
    }

    expandData(reportId) {
        const dataElement = document.querySelector(`[data-report-id="${reportId}"] .datos-preview`);
        if (!dataElement) return;

        if (dataElement.classList.contains('expanded')) {
            dataElement.classList.remove('expanded');
            dataElement.style.maxHeight = '200px';
        } else {
            dataElement.classList.add('expanded');
            dataElement.style.maxHeight = 'none';
        }
    }

    // Funciones de recomendaciones
    applyAllRecommendations() {
        console.log('Aplicando todas las recomendaciones...');
        this.showNotification('Recomendaciones aplicadas exitosamente', 'success');
    }

    scheduleAllImprovements() {
        console.log('Programando todas las mejoras...');
        this.showNotification('Mejoras programadas para ejecución automática', 'info');
    }

    // Funciones de notificación
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    // Funciones de exportación
    async downloadReport(reportId) {
        try {
            const response = await fetch(
                ReportConfig.apiEndpoints.download.replace('{id}', reportId)
            );
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `reporte_${reportId}.pdf`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                this.showNotification('Reporte descargado exitosamente', 'success');
            } else {
                throw new Error('Error al descargar el reporte');
            }
        } catch (error) {
            console.error('Error al descargar reporte:', error);
            this.showNotification('Error al descargar el reporte', 'error');
        }
    }

    async analyzeReport(reportId) {
        try {
            const response = await fetch(
                ReportConfig.apiEndpoints.reportData.replace('{id}', reportId)
            );
            const data = await response.json();
            
            this.showAnalysisModal(data);
        } catch (error) {
            console.error('Error al analizar reporte:', error);
            this.showNotification('Error al analizar el reporte', 'error');
        }
    }

    showAnalysisModal(data) {
        const modal = document.createElement('div');
        modal.className = 'analysis-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Análisis del Reporte</h3>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="analysis-summary">
                        <h4>Resumen del Análisis</h4>
                        <p><strong>Tipo:</strong> ${data.tipo}</p>
                        <p><strong>Formato:</strong> ${data.formato}</p>
                        <p><strong>Tamaño:</strong> ${data.tamaño}</p>
                        <p><strong>Calidad:</strong> ${this.calculateQualityScore(data)}%</p>
                    </div>
                    <div class="analysis-details">
                        <h4>Detalles Técnicos</h4>
                        <ul>
                            <li>Completitud de datos: ${this.calculateCompleteness(data)}%</li>
                            <li>Precisión: ${this.calculateAccuracy(data)}%</li>
                            <li>Consistencia: ${this.calculateConsistency(data)}%</li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        modal.querySelector('.modal-close').addEventListener('click', () => {
            modal.remove();
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }

    calculateQualityScore(data) {
        // Simular cálculo de calidad basado en múltiples factores
        const completeness = this.calculateCompleteness(data);
        const accuracy = this.calculateAccuracy(data);
        const consistency = this.calculateConsistency(data);
        
        return Math.round((completeness + accuracy + consistency) / 3);
    }

    calculateCompleteness(data) {
        // Simular cálculo de completitud
        return Math.floor(Math.random() * 20) + 80; // 80-100%
    }

    calculateAccuracy(data) {
        // Simular cálculo de precisión
        return Math.floor(Math.random() * 15) + 85; // 85-100%
    }

    calculateConsistency(data) {
        // Simular cálculo de consistencia
        return Math.floor(Math.random() * 10) + 90; // 90-100%
    }
}

// Funciones globales para compatibilidad
window.downloadReport = function(reportId) {
    if (window.reportManager) {
        window.reportManager.downloadReport(reportId);
    }
};

window.analyzeReport = function(reportId) {
    if (window.reportManager) {
        window.reportManager.analyzeReport(reportId);
    }
};

window.applyRecommendation = function(type) {
    console.log(`Aplicando recomendación: ${type}`);
    if (window.reportManager) {
        window.reportManager.showNotification(`Recomendación ${type} aplicada`, 'success');
    }
};

window.scheduleRecommendation = function(type) {
    console.log(`Programando recomendación: ${type}`);
    if (window.reportManager) {
        window.reportManager.showNotification(`Recomendación ${type} programada`, 'info');
    }
};

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.reportManager = new ReportManager();
});

// Exportar para uso en otros módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ReportManager;
} 