(function () {
    const dropzone = document.getElementById('spDropzone');
    const fileInput = dropzone ? dropzone.querySelector('input[type="file"]') : null;
    const fileNameEl = document.getElementById('dzFileName');
    const fileSizeEl = document.getElementById('dzFileSize');
    const thumbEl = document.getElementById('dzThumb');

    if (dropzone && fileInput) {

        /* Mark dropzone as having a file */
        function handleFile(file) {
            if (!file) return;
            dropzone.classList.add('has-file');
            if (fileNameEl) fileNameEl.textContent = file.name;
            if (fileSizeEl) {
                const kb = (file.size / 1024).toFixed(1);
                fileSizeEl.textContent = kb > 1024 ? (kb / 1024).toFixed(2) + ' MB' : kb + ' KB';
            }
            // Thumbnail preview
            if (thumbEl && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    thumbEl.innerHTML = '<img src="' + e.target.result + '" alt="">';
                };
                reader.readAsDataURL(file);
            }
        }

        fileInput.addEventListener('change', function () {
            if (this.files && this.files[0]) handleFile(this.files[0]);
        });

        /* Drag & drop */
        ['dragenter', 'dragover'].forEach(function (evt) {
            dropzone.addEventListener(evt, function (e) {
                e.preventDefault();
                dropzone.classList.add('dragover');
            });
        });

        ['dragleave', 'drop'].forEach(function (evt) {
            dropzone.addEventListener(evt, function (e) {
                e.preventDefault();
                dropzone.classList.remove('dragover');
            });
        });

        dropzone.addEventListener('drop', function (e) {
            const files = e.dataTransfer && e.dataTransfer.files;
            if (files && files.length) {
                fileInput.files = files;
                handleFile(files[0]);
            }
        });
    }

    /* Loading state on submit */
    const form = document.getElementById('spForm');
    const submitBtn = document.getElementById('spSubmit');
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
