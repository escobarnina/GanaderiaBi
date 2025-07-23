/**
 * ============================================================================
 * JAVASCRIPT PERSONALIZADO PARA EL ADMIN DE DJANGO
 * Sistema de Inteligencia de Negocios Ganadero
 * ============================================================================
 */

// Esperar a que el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    
    // Configuración de colores para estados
    const STATUS_COLORS = {
        'APROBADO': '#28a745',
        'PENDIENTE': '#ffc107', 
        'EN_PROCESO': '#17a2b8',
        'RECHAZADO': '#dc3545',
        'ALTA': '#28a745',
        'MEDIA': '#ffc107',
        'BAJA': '#dc3545'
    };

    // Función para aplicar colores a estados
    function applyStatusColors() {
        const statusElements = document.querySelectorAll('[data-status]');
        statusElements.forEach(element => {
            const status = element.getAttribute('data-status');
            const color = STATUS_COLORS[status] || '#6c757d';
            element.style.color = color;
            element.style.fontWeight = 'bold';
        });
    }

    // Función para mejorar las tablas
    function enhanceTables() {
        const tables = document.querySelectorAll('#content-main table');
        tables.forEach(table => {
            // Agregar clases para mejor estilo
            table.classList.add('table-enhanced');
            
            // Agregar tooltips a las celdas
            const cells = table.querySelectorAll('td[title]');
            cells.forEach(cell => {
                cell.classList.add('tooltip');
                cell.setAttribute('data-tooltip', cell.getAttribute('title'));
            });
        });
    }

    // Función para mejorar los formularios
    function enhanceForms() {
        const inputs = document.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            // Agregar efectos de focus
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('focused');
            });
        });
    }

    // Función para agregar animaciones
    function addAnimations() {
        const modules = document.querySelectorAll('.module');
        modules.forEach((module, index) => {
            module.style.animationDelay = `${index * 0.1}s`;
        });
    }

    // Función para mejorar los botones de acción
    function enhanceActionButtons() {
        const actionButtons = document.querySelectorAll('.object-tools a, .submit-row input');
        actionButtons.forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
    }

    // Función para agregar contadores dinámicos
    function addDynamicCounters() {
        const counters = document.querySelectorAll('[data-counter]');
        counters.forEach(counter => {
            const target = counter.getAttribute('data-counter');
            const element = document.querySelector(target);
            if (element) {
                const count = element.textContent || '0';
                counter.textContent = count;
            }
        });
    }

    // Función para mejorar la navegación
    function enhanceNavigation() {
        const navItems = document.querySelectorAll('#nav-sidebar a');
        navItems.forEach(item => {
            item.addEventListener('mouseenter', function() {
                this.style.backgroundColor = 'rgba(102, 126, 234, 0.1)';
            });
            
            item.addEventListener('mouseleave', function() {
                this.style.backgroundColor = '';
            });
        });
    }

    // Función para agregar notificaciones
    function addNotifications() {
        // Crear sistema de notificaciones
        const notificationContainer = document.createElement('div');
        notificationContainer.id = 'notification-container';
        notificationContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            max-width: 300px;
        `;
        document.body.appendChild(notificationContainer);
    }

    // Función para mostrar notificaciones
    window.showNotification = function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#17a2b8'};
            color: white;
            padding: 1rem;
            margin-bottom: 0.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            animation: slideIn 0.3s ease-out;
        `;
        notification.textContent = message;
        
        const container = document.getElementById('notification-container');
        if (container) {
            container.appendChild(notification);
            
            // Auto-remover después de 5 segundos
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease-out';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            }, 5000);
        }
    };

    // Función para agregar filtros dinámicos
    function addDynamicFilters() {
        const filterSelects = document.querySelectorAll('.changelist-form select[name*="filter"]');
        filterSelects.forEach(select => {
            select.addEventListener('change', function() {
                // Agregar indicador visual de filtro activo
                if (this.value) {
                    this.style.borderColor = '#667eea';
                    this.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)';
                } else {
                    this.style.borderColor = '';
                    this.style.boxShadow = '';
                }
            });
        });
    }

    // Función para mejorar la búsqueda
    function enhanceSearch() {
        const searchInput = document.querySelector('#searchbar');
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                if (this.value.length > 0) {
                    this.style.borderColor = '#667eea';
                    this.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)';
                } else {
                    this.style.borderColor = '';
                    this.style.boxShadow = '';
                }
            });
        }
    }

    // Función para agregar shortcuts de teclado
    function addKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + S para guardar
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                const saveButton = document.querySelector('input[type="submit"][value="Save"]');
                if (saveButton) {
                    saveButton.click();
                }
            }
            
            // Ctrl/Cmd + N para nuevo
            if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
                e.preventDefault();
                const addButton = document.querySelector('.object-tools a[href*="add"]');
                if (addButton) {
                    window.location.href = addButton.href;
                }
            }
        });
    }

    // Función para agregar CSS dinámico
    function addDynamicCSS() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateX(100%);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            @keyframes slideOut {
                from {
                    opacity: 1;
                    transform: translateX(0);
                }
                to {
                    opacity: 0;
                    transform: translateX(100%);
                }
            }
            
            .table-enhanced {
                border-collapse: separate;
                border-spacing: 0;
            }
            
            .focused {
                border-color: #667eea !important;
            }
            
            .notification {
                transition: all 0.3s ease;
            }
        `;
        document.head.appendChild(style);
    }

    // Inicializar todas las mejoras
    function init() {
        addDynamicCSS();
        applyStatusColors();
        enhanceTables();
        enhanceForms();
        addAnimations();
        enhanceActionButtons();
        addDynamicCounters();
        enhanceNavigation();
        addNotifications();
        addDynamicFilters();
        enhanceSearch();
        addKeyboardShortcuts();
        
        // Mostrar notificación de bienvenida
        if (window.location.pathname === '/admin/') {
            setTimeout(() => {
                window.showNotification('🐄 ¡Bienvenido al Sistema de Inteligencia de Negocios Ganadero!', 'success');
            }, 1000);
        }
    }

    // Ejecutar inicialización
    init();
});

// Exportar funciones para uso global
window.GanaderiaBI = {
    showNotification: window.showNotification,
    STATUS_COLORS: {
        'APROBADO': '#28a745',
        'PENDIENTE': '#ffc107', 
        'EN_PROCESO': '#17a2b8',
        'RECHAZADO': '#dc3545',
        'ALTA': '#28a745',
        'MEDIA': '#ffc107',
        'BAJA': '#dc3545'
    }
}; 