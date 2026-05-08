document.addEventListener('DOMContentLoaded', () => {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('file-input');
    const decodeBtn = document.getElementById('decode-btn');
    const resultDiv = document.getElementById('result');
    const output = document.getElementById('output');

    let currentFile = null;

    dropzone.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', (e) => {
        currentFile = e.target.files[0];
        decodeBtn.disabled = false;
        dropzone.innerHTML = `<p>Selected: ${currentFile.name}</p>`;
    });

    decodeBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        const formData = new FormData();
        formData.append('file', currentFile);

        const res = await fetch('/decode', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();

        resultDiv.style.display = 'block';
        if (data.success) {
            output.textContent = data.code;
        } else {
            output.innerHTML = `<span style="color:red">${data.error}</span>`;
        }
    });
});
```