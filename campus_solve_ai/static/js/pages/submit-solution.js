(function () {
    // Loading state on submit
    const form = document.getElementById('ssForm');
    const submitBtn = document.getElementById('ssSubmit');

    if (form && submitBtn) {
        form.addEventListener('submit', function () {
            submitBtn.disabled = true;
            submitBtn.innerHTML = `
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <span>SubmittingÃ¢â‚¬Â¦</span>
            `;
        });
    }
})();
