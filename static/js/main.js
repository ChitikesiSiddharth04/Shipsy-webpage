// Main JavaScript for ML Experiments Tracker

// Utility Functions
const Utils = {
    // Show notification
    showNotification: function(message, type = 'info', duration = 3000) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, duration);
    },

    // Format date
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Validate form
    validateForm: function(formElement) {
        const inputs = formElement.querySelectorAll('input[required], textarea[required], select[required]');
        let isValid = true;
        const errors = [];

        inputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                errors.push(`${input.name} is required`);
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }
        });

        return { isValid, errors };
    }
};

// Dashboard Handler for dynamic filtering, pagination, and actions
const DashboardHandler = {
    init: function() {
        this.cacheElements();
        if (!this.filterForm) return;
        this.setupEventListeners();
        this.loadExperiments(1); // Initial load
    },

    cacheElements: function() {
        this.filterForm = document.getElementById('filterForm');
        this.searchInput = document.getElementById('search');
        this.filterSelects = this.filterForm ? this.filterForm.querySelectorAll('select') : [];
        this.experimentsList = document.getElementById('experiments-list');
        this.paginationContainer = document.getElementById('pagination-container');
    },

    setupEventListeners: function() {
        const debouncedLoad = Utils.debounce(() => this.loadExperiments(1), 300);
        this.searchInput.addEventListener('input', debouncedLoad);
        this.filterSelects.forEach(s => s.addEventListener('change', () => this.loadExperiments(1)));

        if (this.paginationContainer) {
            this.paginationContainer.addEventListener('click', e => {
                if (e.target.tagName === 'A' && e.target.dataset.page) {
                    e.preventDefault();
                    this.loadExperiments(parseInt(e.target.dataset.page, 10));
                }
            });
        }

        if (this.experimentsList) {
            this.experimentsList.addEventListener('click', e => {
                const deleteButton = e.target.closest('.delete-experiment-btn');
                if (deleteButton) {
                    e.preventDefault();
                    this.handleDelete(deleteButton);
                }
            });
        }
    },

    loadExperiments: function(page = 1) {
        const perPageSelect = document.getElementById('per_page');
        const perPage = perPageSelect ? perPageSelect.value : 5;
        const query = new URLSearchParams({ page: page, search: this.searchInput.value });
        this.filterSelects.forEach(s => s.value && query.append(s.name, s.value));

        fetch(`/api/filter_experiments?${query}`)
            .then(response => response.json())
            .then(data => {
                this.renderExperiments(data.experiments);
                this.renderPagination(data);
            })
            .catch(error => console.error('Error fetching experiments:', error));
    },

    renderExperiments: function(experiments) {
        if (!this.experimentsList) return;
        if (experiments.length === 0) {
            this.experimentsList.innerHTML = '<div class="col-12"><p class="text-center text-muted mt-4">No experiments found.</p></div>';
            return;
        }
        this.experimentsList.innerHTML = experiments.map((exp, index) => `
            <div class="col-md-6 col-lg-4 mb-4 fade-in-up" style="animation-delay: ${index * 0.1}s;">
                <div class="card experiment-card h-100">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="card-title mb-0 text-truncate"><a href="/experiment/${exp.id}" class="text-decoration-none">${exp.title}</a></h5>
                        <span class="badge status-badge status-${exp.status.toLowerCase().replace(' ', '-')}">${exp.status}</span>
                    </div>
                    <div class="card-body">
                        <p class="card-text text-muted text-truncate-3 mb-3">${exp.description}</p>
                        <div class="mb-2"><i class="fas fa-cogs text-info me-2"></i><strong>${exp.model_type}</strong></div>
                        <div><i class="fas fa-bullseye text-success me-2"></i>Accuracy: <strong>${(exp.accuracy * 100).toFixed(2)}%</strong></div>
                    </div>
                    <div class="card-footer bg-transparent">
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted"><i class="fas fa-calendar-alt me-1"></i>${Utils.formatDate(exp.created_at)}</small>
                            <div class="btn-group">
                                <a href="/experiment/${exp.id}/edit" class="btn btn-sm btn-outline-secondary"><i class="fas fa-edit"></i></a>
                                <a href="/experiment/${exp.id}" class="btn btn-sm btn-outline-primary"><i class="fas fa-eye"></i></a>
                                <button class="btn btn-sm btn-outline-danger delete-experiment-btn" data-id="${exp.id}" data-title="${exp.title}"><i class="fas fa-trash-alt"></i> Delete</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    },

    handleDelete: function(button) {
        const experimentId = button.dataset.id;
        const experimentTitle = button.dataset.title;

        const modalElement = document.getElementById('deleteConfirmationModal');
        const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
        const deleteModal = new bootstrap.Modal(modalElement);

        const modalBody = modalElement.querySelector('.modal-body');
        modalBody.textContent = `Are you sure you want to delete the experiment: "${experimentTitle}"?`;

        const deleteHandler = () => {
            console.log('Sending DELETE request to:', `/experiment/${experimentId}/delete`);
            fetch(`/experiment/${experimentId}/delete`, {
                method: 'DELETE',
            })
            .then(response => response.json())
            .then(data => {
                console.log('Parsed JSON data:', data);
                if (data.success) {
                    this.loadExperiments();
                    Utils.showNotification(data.message, 'success');
                } else {
                    Utils.showNotification(data.message, 'error');
                }
            })
            .catch(error => console.error('Error deleting experiment:', error))
            .finally(() => {
                deleteModal.hide();
            });
        };

        confirmDeleteBtn.addEventListener('click', deleteHandler, { once: true });

        modalElement.addEventListener('hidden.bs.modal', () => {
            confirmDeleteBtn.removeEventListener('click', deleteHandler);
        }, { once: true });

        deleteModal.show();
    },

    renderPagination: function(data) {
        if (!this.paginationContainer || data.pages <= 1) {
            if(this.paginationContainer) this.paginationContainer.innerHTML = '';
            return;
        }
        let html = '<ul class="pagination justify-content-center">';
        html += `<li class="page-item ${!data.has_prev ? 'disabled' : ''}"><a class="page-link" href="#" data-page="${data.page - 1}">Previous</a></li>`;
        for (let i = 1; i <= data.pages; i++) {
            html += `<li class="page-item ${i === data.page ? 'active' : ''}"><a class="page-link" href="#" data-page="${i}">${i}</a></li>`;
        }
        html += `<li class="page-item ${!data.has_next ? 'disabled' : ''}"><a class="page-link" href="#" data-page="${data.page + 1}">Next</a></li>`;
        html += '</ul>';
        this.paginationContainer.innerHTML = html;
    },

    handleDelete: function(button) {
        const experimentId = button.dataset.experimentId;
        const experimentTitle = button.dataset.experimentTitle;
        if (confirm(`Are you sure you want to delete "${experimentTitle}"?`)) {
            const form = document.getElementById(`delete-form-${experimentId}`);
            if (form) {
                form.submit();
            }
        }
    }
};

// Experiment Page Handler
const ExperimentHandler = {
    init: function() {
        const deleteBtn = document.getElementById('delete-experiment-btn');
        if (deleteBtn) {
            deleteBtn.addEventListener('click', (e) => {
                e.preventDefault();
                const experimentTitle = e.currentTarget.dataset.experimentTitle;
                if (confirm(`Are you sure you want to delete "${experimentTitle}"?`)) {
                    document.getElementById('delete-experiment-form').submit();
                }
            });
        }
    }
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('experiments-list')) {
        DashboardHandler.init();
    }
    if (document.body.classList.contains('experiment-details-page')) {
        ExperimentHandler.init();
    }
});

// Global event listeners
function setupGlobalEventListeners() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    });

    // Add loading states to buttons
    const buttons = document.querySelectorAll('button[type="submit"]');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        });
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// Enhanced Animations
function setupEnhancedAnimations() {
    // Animate cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all cards
    document.querySelectorAll('.card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // Animate progress bars
    document.querySelectorAll('.progress-bar').forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 500);
    });
}

// Enhanced Interactions
function setupEnhancedInteractions() {
    // Enhanced tooltips
    document.querySelectorAll('.tooltip-custom').forEach(element => {
        element.addEventListener('mouseenter', (e) => {
            const tooltip = e.target.getAttribute('data-tooltip');
            if (tooltip) {
                showCustomTooltip(e, tooltip);
            }
        });
    });

    // Enhanced search with debouncing
    const searchInput = document.getElementById('search');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // Add loading state
                const form = document.getElementById('filterForm');
                if (form) {
                    form.classList.add('loading');
                    setTimeout(() => {
                        form.submit();
                    }, 300);
                }
            }, 500);
        });
    }

    // Enhanced filter interactions
    document.querySelectorAll('#filterForm select').forEach(select => {
        select.addEventListener('change', () => {
            const form = document.getElementById('filterForm');
            if (form) {
                form.classList.add('loading');
                setTimeout(() => {
                    form.submit();
                }, 300);
            }
        });
    });

    // Enhanced button interactions
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('mouseenter', (e) => {
            e.target.style.transform = 'translateY(-2px) scale(1.02)';
        });
        
        button.addEventListener('mouseleave', (e) => {
            e.target.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Enhanced card interactions
    document.querySelectorAll('.experiment-card').forEach(card => {
        card.addEventListener('mouseenter', (e) => {
            e.target.style.transform = 'translateY(-8px) scale(1.02)';
            e.target.style.boxShadow = '0 20px 25px -5px rgba(0, 0, 0, 0.1)';
        });
        
        card.addEventListener('mouseleave', (e) => {
            e.target.style.transform = 'translateY(0) scale(1)';
            e.target.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1)';
        });
    });
}

// Custom tooltip function
function showCustomTooltip(event, text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.textContent = text;
    tooltip.style.cssText = `
        position: absolute;
        background: #1e293b;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-size: 0.875rem;
        z-index: 1000;
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    
    document.body.appendChild(tooltip);
    
    const rect = event.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
    
    setTimeout(() => {
        tooltip.style.opacity = '1';
    }, 10);
    
    event.target.addEventListener('mouseleave', () => {
        tooltip.remove();
    });
} 