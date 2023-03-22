const fileInput = document.getElementById('fileInput');
const reportText = document.getElementById('reportText');
const submitBtn = document.getElementById('submitBtn');
const spinner = document.getElementById('spinner');
const jsonOutput = document.getElementById('jsonOutput');
const downloadBtn = document.getElementById('downloadBtn');

fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = () => {
        reportText.value = reader.result;
    };
    reader.readAsText(file);
});

submitBtn.addEventListener('click', async () => {
    event.preventDefault(); // Add this line to prevent the form from being submitted
    const apiKey = document.getElementById('api_key').value;
    const report = reportText.value;
    if (apiKey && report) {
        spinner.style.display = 'block';
        const formData = new FormData();
        formData.append('api_key', apiKey);
        formData.append('report', report);
        const response = await fetch('/process', {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json',
            },
        });
        const structuredReport = await response.json();
        jsonOutput.textContent = JSON.stringify(structuredReport, null, 2);
        downloadBtn.href = 'data:application/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(structuredReport));
        spinner.style.display = 'none';
        jsonOutput.style.display = 'block';
        downloadBtn.style.display = 'block';
    } else {
        alert('Please enter an API key and report text');
    }
});
