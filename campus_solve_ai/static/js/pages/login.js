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
    const inputs = document.querySelectorAll('.field input');
    inputs.forEach(function (input) {
        if (input.value && input.value.length) input.classList.add('has-value');
        input.addEventListener('input', function () {
            this.classList.toggle('has-value', this.value.length > 0);
        });
    });

    // ==== Add placeholders for floating labels (required) ====
    // Ensures :placeholder-shown selector works. The label visually replaces the placeholder.
    inputs.forEach(function (input) {
        if (!input.hasAttribute('placeholder')) {
            input.setAttribute('placeholder', ' ');
        }
    });

    // ==== Smooth submit state ====
    const form = document.querySelector('.auth-form-panel form');
    if (form) {
        form.addEventListener('submit', function () {
            const btn = form.querySelector('.btn-auth');
            if (!btn) return;
            btn.disabled = true;
            btn.innerHTML = `
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <span>Signing inÃ¢â‚¬Â¦</span>
            `;
        });
    }
})();
