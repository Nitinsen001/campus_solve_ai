/* ==========================================================
   GLOBAL CHART CONFIG
   ========================================================== */
if (window.Chart) {
    Chart.defaults.font.family = "'Plus Jakarta Sans', system-ui, sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.color = '#616161';
}

/* ==========================================================
   GRADIENT HELPERS
   ========================================================== */
function makeGradient(ctx, c1, c2) {
    const g = ctx.createLinearGradient(0, 0, 0, 260);
    g.addColorStop(0, c1);
    g.addColorStop(1, c2);
    return g;
}

/* ==========================================================
   CUSTOM TOOLTIP STYLE
   ========================================================== */
const tooltipStyle = {
    backgroundColor: 'rgba(0, 0, 0, 0.12)',
    titleColor: '#FFFFFF',
    bodyColor: '#616161',
    padding: 12,
    cornerRadius: 10,
    displayColors: true,
    boxPadding: 6,
    titleFont: { weight: '700', size: 13 },
    bodyFont: { weight: '500', size: 12 },
    borderColor: 'rgba(97, 97, 97, 0.4)',
    borderWidth: 1
};

/* ==========================================================
   1. PROBLEMS BY CATEGORY Ã¢â‚¬â€ BAR
   ========================================================== */
(function () {
    const el = document.getElementById('categoryChart');
    if (!el) return;
    const data = window.CAMPUS_ANALYTICS.categoryData;
    const ctx = el.getContext('2d');
    const grad = makeGradient(ctx, '#212121', '#616161');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.category),
            datasets: [{
                label: 'Problems',
                data: data.map(d => d.count),
                backgroundColor: grad,
                hoverBackgroundColor: makeGradient(ctx, '#E0E0E0', '#212121'),
                borderRadius: 8,
                borderSkipped: false,
                maxBarThickness: 44,
                barPercentage: 0.7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: tooltipStyle
            },
            scales: {
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { font: { weight: '600' }, color: '#616161' }
                },
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(0, 0, 0, 0.15)', drawBorder: false },
                    border: { display: false },
                    ticks: { font: { weight: '500' }, color: '#616161', stepSize: 1, precision: 0 }
                }
            },
            animation: { duration: 900, easing: 'easeOutQuart' }
        }
    });
})();

/* ==========================================================
   2. PRIORITY DISTRIBUTION Ã¢â‚¬â€ DOUGHNUT
   ========================================================== */
(function () {
    const el = document.getElementById('priorityChart');
    if (!el) return;
    const data = window.CAMPUS_ANALYTICS.priorityData;

    new Chart(el, {
        type: 'doughnut',
        data: {
            labels: data.map(d => d.priority),
            datasets: [{
                data: data.map(d => d.count),
                backgroundColor: [
                    'rgba(239, 68, 68, 0.9)',
                    'rgba(245, 158, 11, 0.9)',
                    'rgba(0, 0, 0, 0.2)',
                    'rgba(100, 116, 139, 0.9)'
                ],
                hoverBackgroundColor: [
                    '#ef4444', '#f59e0b', '#212121', '#616161'
                ],
                borderColor: '#FFFFFF',
                borderWidth: 3,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '68%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 16,
                        usePointStyle: true,
                        pointStyle: 'circle',
                        font: { weight: '600', size: 12 },
                        color: '#616161'
                    }
                },
                tooltip: tooltipStyle
            },
            animation: { duration: 1000, easing: 'easeOutQuart' }
        }
    });
})();

/* ==========================================================
   3. MONTHLY TRENDS Ã¢â‚¬â€ LINE with gradient fill
   ========================================================== */
(function () {
    const el = document.getElementById('monthlyChart');
    if (!el) return;
    const labels = window.CAMPUS_ANALYTICS.monthlyLabels;
    const values = window.CAMPUS_ANALYTICS.monthlyValues;
    const ctx = el.getContext('2d');

    const lineGrad = ctx.createLinearGradient(0, 0, 0, 300);
    lineGrad.addColorStop(0, 'rgba(0, 0, 0, 0.175)');
    lineGrad.addColorStop(1, 'rgba(0, 0, 0, 0.01)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Problems',
                data: values,
                borderColor: '#212121',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                backgroundColor: lineGrad,
                pointBackgroundColor: '#FFFFFF',
                pointBorderColor: '#212121',
                pointBorderWidth: 3,
                pointRadius: 4,
                pointHoverRadius: 7,
                pointHoverBackgroundColor: '#212121',
                pointHoverBorderColor: '#FFFFFF'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: tooltipStyle
            },
            scales: {
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { font: { weight: '600' }, color: '#616161' }
                },
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(0, 0, 0, 0.15)', drawBorder: false },
                    border: { display: false },
                    ticks: { font: { weight: '500' }, color: '#616161', precision: 0 }
                }
            },
            animation: { duration: 1200, easing: 'easeOutQuart' },
            interaction: { intersect: false, mode: 'index' }
        }
    });
})();

/* ==========================================================
   4. CAMPUS HOTSPOTS - HORIZONTAL BAR
   ========================================================== */
(function () {
    const el = document.getElementById('locationChart');
    if (!el) return;
    const data = window.CAMPUS_ANALYTICS.locationData;

    new Chart(el, {
        type: 'bar',
        data: {
            labels: data.map(d => d.location || 'Unknown'),
            datasets: [{
                label: 'Approved problems',
                data: data.map(d => d.count),
                backgroundColor: 'rgba(0, 0, 0, 0.2)',
                hoverBackgroundColor: '#E0E0E0',
                borderRadius: 6,
                borderSkipped: false,
                barThickness: 20
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: tooltipStyle },
            scales: {
                x: { beginAtZero: true, grid: { color: 'rgba(0, 0, 0, 0.15)' }, ticks: { precision: 0 } },
                y: { grid: { display: false }, ticks: { color: '#616161', font: { weight: '600' } } }
            },
            animation: { duration: 900, easing: 'easeOutQuart' }
        }
    });
})();

/* ==========================================================
   5. RESOLUTION FUNNEL - STATUS MIX
   ========================================================== */
(function () {
    const el = document.getElementById('statusChart');
    if (!el) return;
    const data = window.CAMPUS_ANALYTICS.statusData;
    const statusOrder = ['PENDING', 'APPROVED', 'Open', 'Under Review', 'Solution Available', 'Resolved', 'Closed', 'REJECTED'];
    const byStatus = Object.fromEntries(data.map(d => [d.status, d.count]));
    const labels = statusOrder.filter(status => byStatus[status]);

    new Chart(el, {
        type: 'bar',
        data: {
            labels: labels.map(status => status.replace('_', ' ')),
            datasets: [{
                label: 'Problems',
                data: labels.map(status => byStatus[status]),
                backgroundColor: ['#f59e0b', '#212121', '#616161', '#212121', '#212121', '#616161', '#212121', '#ef4444'],
                borderRadius: 7,
                borderSkipped: false,
                maxBarThickness: 38
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false }, tooltip: tooltipStyle },
            scales: {
                x: { grid: { display: false }, ticks: { color: '#616161', font: { weight: '600' }, maxRotation: 35 } },
                y: { beginAtZero: true, grid: { color: 'rgba(0, 0, 0, 0.15)' }, ticks: { precision: 0 } }
            },
            animation: { duration: 1000, easing: 'easeOutQuart' }
        }
    });
})();

/* ==========================================================
   6. KPI SPARKLINES Ã¢â‚¬â€ tiny decorative line charts
   ========================================================== */
(function () {
    const sparkConfigs = [
        { id: 'spark1', color: '#212121' },
        { id: 'spark2', color: '#212121' },
        { id: 'spark3', color: '#616161' },
        { id: 'spark4', color: '#f59e0b' },
        { id: 'spark5', color: '#616161' },
        { id: 'spark6', color: '#212121' }
    ];

    function seed(seedVal) {
        // deterministic pseudo-random sequence per card
        let s = seedVal;
        return function () {
            s = (s * 9301 + 49297) % 233280;
            return s / 233280;
        };
    }

    sparkConfigs.forEach(function (cfg, idx) {
        const el = document.getElementById(cfg.id);
        if (!el) return;
        const rnd = seed(40 + idx * 17);
        const points = Array.from({ length: 12 }, function () {
            return Math.round(20 + rnd() * 80);
        });
        const ctx = el.getContext('2d');
        const grad = ctx.createLinearGradient(0, 0, 0, 40);
        grad.addColorStop(0, cfg.color + '55');
        grad.addColorStop(1, cfg.color + '00');

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: points.map(function (_, i) { return i; }),
                datasets: [{
                    data: points,
                    borderColor: cfg.color,
                    borderWidth: 2,
                    tension: 0.4,
                    pointRadius: 0,
                    fill: true,
                    backgroundColor: grad
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: { enabled: false } },
                scales: {
                    x: { display: false },
                    y: { display: false }
                },
                elements: { line: { capBezierPoints: true } },
                animation: { duration: 1200, easing: 'easeOutQuart' }
            }
        });
    });
})();
