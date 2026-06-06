const dropZone = document.querySelector('.drop-zone');
const imageInput = document.getElementById('imageInput');
const scanBtn = document.getElementById('scanBtn');
const imagePreview = document.getElementById('imagePreview');
const dropZoneText = document.getElementById('dropZoneText');

const resultSection = document.getElementById('resultSection');
const statusBadge = document.getElementById('statusBadge');
const resName = document.getElementById('resName');
const resPurpose = document.getElementById('resPurpose');
const resDosage = document.getElementById('resDosage');
const resSdg = document.getElementById('resSdg');

let selectedFile = null;

// Handle click trigger for file upload zone
dropZone.addEventListener('click', () => imageInput.click());

// Handle file selections
imageInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelection(e.target.files[0]);
    }
});

function handleFileSelection(file) {
    selectedFile = file;
    scanBtn.disabled = false;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        imagePreview.src = e.target.result;
        imagePreview.style.display = 'block';
        dropZoneText.style.display = 'none';
    }
    reader.readAsDataURL(file);
}

// Request and Response parsing pipeline 
scanBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    scanBtn.innerText = "Analyzing Code/Image Pattern...";
    scanBtn.disabled = true;

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
        // CHANGED: Routed to localhost to match Live Server origin routing contexts
        const response = await fetch('http://localhost:5000/api/verify-package', {
            method: 'POST',
            body: formData,
            mode: 'cors' // Forces browser to track cross-origin network pipeline rules
        });

        const result = await response.json();
        renderResults(result);
    } catch (error) {
        console.error("Transmission Error Details:", error);
        alert("Could not connect to the backend server. Please make sure Flask is running on http://localhost:5000.");
        scanBtn.innerText = "Analyze Verification Status";
        scanBtn.disabled = false;
    }
});

function renderResults(res) {
    scanBtn.innerText = "Analyze Verification Status";
    scanBtn.disabled = false;
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth' });

    if (res.success) {
        statusBadge.className = "badge success";
        statusBadge.innerText = `🟢 VERIFIED: ${res.detected_label}`;
        resName.innerText = res.data.name;
        resPurpose.innerText = res.data.purpose;
        resDosage.innerText = res.data.standard_dosage;
        resSdg.innerText = res.data.sdg3_alignment;
    } else {
        statusBadge.className = "badge error";
        statusBadge.innerText = `⚠️ WARNING: ${res.detected_label}`;
        resName.innerText = "UNKNOWN LABEL";
        resPurpose.innerText = "N/A - Critical security block triggered.";
        resDosage.innerText = "DO NOT INGEST. Run safety batch diagnostics tracking.";
        resSdg.innerText = res.sdg3_alignment;
    }
}
