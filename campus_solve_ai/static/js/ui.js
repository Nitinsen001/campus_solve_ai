/* ==========================================================================
   CampusSolve AI — Aurora v3 UI behaviours
   Progressive enhancement only: every feature degrades gracefully and
   nothing here is required for a page to work.
   ========================================================================== */
(function () {
    'use strict';

    var reduceMotion = window.matchMedia &&
        window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function $(sel, root) { return (root || document).querySelector(sel); }
    function $$(sel, root) {
        return Array.prototype.slice.call((root || document).querySelectorAll(sel));
    }

    /* ------------------------------------------------------------------
       1. Scroll progress bar + navbar state + back-to-top
       ------------------------------------------------------------------ */
    function initChrome() {
        var bar = $('#csProgress');
        var navbar = $('#mainNavbar');
        var fab = $('#csToTop');
        var ticking = false;

        function paint() {
            var doc = document.documentElement;
            var scrolled = window.pageYOffset || doc.scrollTop || 0;
            var max = (doc.scrollHeight - window.innerHeight) || 1;
            if (bar) {
                bar.style.transform = 'scaleX(' + Math.min(scrolled / max, 1) + ')';
            }
            if (navbar) {
                navbar.classList.toggle('is-scrolled', scrolled > 12);
            }
            if (fab) {
                fab.classList.toggle('is-visible', scrolled > 420);
            }
            ticking = false;
        }

        function onScroll() {
            if (!ticking) {
                ticking = true;
                window.requestAnimationFrame(paint);
            }
        }

        window.addEventListener('scroll', onScroll, { passive: true });
        window.addEventListener('resize', onScroll);
        paint();

        if (fab) {
            fab.addEventListener('click', function () {
                window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
            });
        }
    }

    /* ------------------------------------------------------------------
       2. Reveal on scroll
       ------------------------------------------------------------------ */
    var REVEAL_SELECTOR = [
        '.problem-card', '.pd-card', '.pd-hero', '.side-card', '.sp-card', '.ss-card',
        '.ms-card', '.mod-card', '.sm-card', '.stat-card', '.kpi-card', '.chart-card',
        '.section-card', '.info-card', '.stat-tile', '.pf-hero', '.ss-hero',
        '.sp-hero', '.ms-hero', '.mod-hero', '.sm-hero', '.analytics-hero', '.profile-hero'
    ].join(',');

    function initReveal() {
        var nodes = $$(REVEAL_SELECTOR);
        if (!nodes.length) { return; }

        if (reduceMotion || !('IntersectionObserver' in window)) {
            nodes.forEach(function (n) { n.classList.add('cs-reveal', 'cs-in'); });
            return;
        }

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('cs-in');
                    observer.unobserve(entry.target);
                }
            });
        }, { rootMargin: '0px 0px -8% 0px', threshold: 0.04 });

        nodes.forEach(function (node, i) {
            node.classList.add('cs-reveal');
            node.style.transitionDelay = Math.min(i % 6, 5) * 55 + 'ms';
            observer.observe(node);
        });
    }

    /* ------------------------------------------------------------------
       3. Animated statistics counters
       ------------------------------------------------------------------ */
    var COUNT_SELECTOR = [
        '.stat-value', '.kpi-value', '.tile-value', '.metric-value',
        '.mod-hero-stat .stat-num', '.sm-hero-stat .stat-num',
        '.header-stat-badge .stat-value'
    ].join(',');

    function animateCount(node) {
        var raw = (node.textContent || '').trim();
        if (!/^\d+(\.\d+)?$/.test(raw)) { return; }
        var target = parseFloat(raw);
        var decimals = (raw.split('.')[1] || '').length;
        if (target === 0) { return; }

        var start = null;

        function step(ts) {
            if (start === null) { start = ts; }
            var p = Math.min((ts - start) / 900, 1);
            var eased = 1 - Math.pow(1 - p, 3);
            node.textContent = (target * eased).toFixed(decimals);
            if (p < 1) {
                window.requestAnimationFrame(step);
            } else {
                node.textContent = raw;
            }
        }
        window.requestAnimationFrame(step);
    }

    function initCounters() {
        if (reduceMotion || !('IntersectionObserver' in window)) { return; }
        var nodes = $$(COUNT_SELECTOR);
        if (!nodes.length) { return; }

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    animateCount(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });

        nodes.forEach(function (n) { observer.observe(n); });
    }
    /* ------------------------------------------------------------------
       4. Toast stack (Django flash messages)
       ------------------------------------------------------------------ */
    function dismissToast(toast) {
        if (!toast || toast.classList.contains('cs-out')) { return; }
        toast.classList.add('cs-out');
        window.setTimeout(function () {
            if (toast.parentNode) { toast.parentNode.removeChild(toast); }
        }, 320);
    }

    function initToasts() {
        $$('.cs-toast').forEach(function (toast, i) {
            var delay = toast.getAttribute('data-cs-timeout');
            delay = delay ? parseInt(delay, 10) : 6400;
            toast.style.animationDelay = (i * 70) + 'ms';

            var closer = $('.cs-toast-close', toast);
            if (closer) {
                closer.addEventListener('click', function () { dismissToast(toast); });
            }
            if (delay > 0) {
                window.setTimeout(function () { dismissToast(toast); }, delay + i * 260);
            }
        });
    }

    /* ------------------------------------------------------------------
       5. Quick search: Ctrl/Cmd + K
       ------------------------------------------------------------------ */
    function initQuickSearch() {
        document.addEventListener('keydown', function (event) {
            var key = (event.key || '').toLowerCase();
            if ((event.ctrlKey || event.metaKey) && key === 'k') {
                var input = $('#csQuickSearch') || $('#pfFilterForm input[name="q"]');
                if (!input) { return; }
                event.preventDefault();
                input.focus();
                if (input.select) { input.select(); }
            }
            if (key === 'escape' && document.activeElement &&
                document.activeElement.id === 'csQuickSearch') {
                document.activeElement.blur();
            }
        });
    }

    /* ------------------------------------------------------------------
       6. Submit guards — no double posting, spinner feedback
       ------------------------------------------------------------------ */
    function initSubmitGuards() {
        $$('form').forEach(function (form) {
            if (form.hasAttribute('data-cs-plain')) { return; }
            form.addEventListener('submit', function () {
                if (form.dataset.csSubmitting === '1') { return false; }
                form.dataset.csSubmitting = '1';
                $$('button[type="submit"], input[type="submit"]', form).forEach(function (btn) {
                    btn.classList.add('is-loading');
                    btn.setAttribute('aria-busy', 'true');
                });
                return true;
            });
        });
    }

    /* ------------------------------------------------------------------
       7. Image lightbox for problem photos
       ------------------------------------------------------------------ */
    function initLightbox() {
        var targets = $$('.pd-image img, .mod-image img, .dz-thumb img');
        if (!targets.length) { return; }

        var overlay = document.createElement('div');
        overlay.className = 'cs-lightbox';
        overlay.setAttribute('role', 'dialog');
        overlay.setAttribute('aria-label', 'Image preview');
        overlay.innerHTML = '<button type="button" class="cs-lightbox-close" aria-label="Close">' +
            '<i class="bi bi-x-lg"></i></button><img alt="Problem photo preview">';
        document.body.appendChild(overlay);

        var img = $('img', overlay);
        var closeBtn = $('.cs-lightbox-close', overlay);
        function close() { overlay.classList.remove('is-open'); }

        targets.forEach(function (target) {
            target.style.cursor = 'zoom-in';
            target.addEventListener('click', function () {
                img.src = target.currentSrc || target.src;
                overlay.classList.add('is-open');
            });
        });

        closeBtn.addEventListener('click', close);
        overlay.addEventListener('click', function (event) {
            if (event.target === overlay) { close(); }
        });
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape') { close(); }
        });
    }
    /* ------------------------------------------------------------------
       8. Copy to clipboard ([data-cs-copy="value"])
       ------------------------------------------------------------------ */
    function initCopy() {
        $$('[data-cs-copy]').forEach(function (node) {
            node.addEventListener('click', function (event) {
                var value = node.getAttribute('data-cs-copy');
                if (!value || !navigator.clipboard) { return; }
                event.preventDefault();
                navigator.clipboard.writeText(value).then(function () {
                    node.classList.add('is-copied');
                    window.setTimeout(function () { node.classList.remove('is-copied'); }, 1400);
                });
            });
        });
    }

    /* ------------------------------------------------------------------
       9. Smooth in-page anchors
       ------------------------------------------------------------------ */
    function initAnchors() {
        $$('a[href^="#"]').forEach(function (link) {
            link.addEventListener('click', function (event) {
                var id = link.getAttribute('href');
                if (!id || id === '#' || link.hasAttribute('data-bs-toggle')) { return; }
                var target = document.getElementById(id.slice(1));
                if (!target) { return; }
                event.preventDefault();
                target.scrollIntoView({
                    behavior: reduceMotion ? 'auto' : 'smooth',
                    block: 'start'
                });
            });
        });
    }

    /* ------------------------------------------------------------------
       10. Bootstrap tooltips
       ------------------------------------------------------------------ */
    function initTooltips() {
        if (!window.bootstrap || !window.bootstrap.Tooltip) { return; }
        $$('[data-bs-toggle="tooltip"]').forEach(function (node) {
            if (!window.bootstrap.Tooltip.getInstance(node)) {
                new window.bootstrap.Tooltip(node);
            }
        });
    }

    /* ------------------------------------------------------------------
       boot
       ------------------------------------------------------------------ */
    function boot() {
        initChrome();
        initReveal();
        initCounters();
        initToasts();
        initQuickSearch();
        initSubmitGuards();
        initLightbox();
        initCopy();
        initAnchors();
        initTooltips();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();