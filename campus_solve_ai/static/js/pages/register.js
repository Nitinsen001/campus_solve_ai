(function () {
    // ==== Password visibility toggle ====
    document.querySelectorAll('.toggle-pass').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const input = document.getElementById(this.dataset.target);
            if (!input) return;
            const icon = this.querySelector('i');
            const isPass = input.type === 'password';
            input.type = isPass ? 'text' : 'password';
            icon.classList.toggle('bi-eye', !isPass);
            icon.classList.toggle('bi-eye-slash', isPass);
        });
    });

    // ==== Mark inputs as has-value for floating label ====
    const inputs = document.querySelectorAll('.field input, .field select');
    inputs.forEach(function (input) {
        if (input.value && input.value.length) input.classList.add('has-value');
        input.addEventListener('input', function () {
            this.classList.toggle('has-value', this.value.length > 0);
        });
        input.addEventListener('change', function () {
            this.classList.toggle('has-value', this.value.length > 0);
        });
        if (!input.hasAttribute('placeholder')) {
            input.setAttribute('placeholder', ' ');
        }
    });

    // ==== Password strength meter ====
    const pwInput = document.querySelector('input[name="password1"], input[name="password"]');
    const meter = document.getElementById('pwStrength');

    if (pwInput && meter) {
        const strengthText = meter.querySelector('.strength-text');
        const hint = meter.querySelector('.strength-hint');

        pwInput.addEventListener('input', function () {
            const val = this.value;

            if (!val.length) {
                meter.classList.remove('is-visible');
                meter.removeAttribute('data-level');
                hint.style.display = '';
                return;
            }

            meter.classList.add('is-visible');
            hint.style.display = 'none';

            let score = 0;
            if (val.length >= 8) score++;
            if (/[A-Z]/.test(val) && /[a-z]/.test(val)) score++;
            if (/\d/.test(val)) score++;
            if (/[^A-Za-z0-9]/.test(val)) score++;

            // Ensure at least level 1 when user types something
            score = Math.max(1, score);
            meter.setAttribute('data-level', score);

            const labels = ['', 'Weak password', 'Fair password', 'Good password', 'Strong password'];
            strengthText.textContent = labels[score];
        });
    }

    // ==== Smooth submit state ====
    const form = document.getElementById('registerForm');
    if (form) {
        form.addEventListener('submit', function () {
            const btn = form.querySelector('.btn-auth');
            if (!btn) return;
            btn.disabled = true;
            btn.innerHTML = `
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <span>Creating accountÃ¢â‚¬Â¦</span>
            `;
        });
    }
})();
