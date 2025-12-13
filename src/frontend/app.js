const state = {
    files: [],
    sessionId: null,
    plan: null,
    isProcessing: false
};

const dom = {
    uploadSection: document.getElementById('upload-section'),
    processingSection: document.getElementById('processing-section'),
    planSection: document.getElementById('plan-section'),
    buildSection: document.getElementById('build-section'),
    successSection: document.getElementById('success-section'),
    fileInput: document.getElementById('file-input'),
    uploadArea: document.getElementById('upload-area'),
    fileList: document.getElementById('file-list'),
    uploadBtn: document.getElementById('upload-btn'),
    processingText: document.getElementById('processing-text'),
    planContent: document.getElementById('plan-content'),
    feedbackInput: document.getElementById('feedback-input'),
    regenerateBtn: document.getElementById('regenerate-btn'),
    approveBtn: document.getElementById('approve-btn'),
    downloadBtn: document.getElementById('download-btn')
};

// Event Listeners
dom.uploadArea.addEventListener('click', () => dom.fileInput.click());
dom.uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dom.uploadArea.classList.add('dragover');
});
dom.uploadArea.addEventListener('dragleave', () => dom.uploadArea.classList.remove('dragover'));
dom.uploadArea.addEventListener('drop', handleDrop);
dom.fileInput.addEventListener('change', handleFileSelect);
dom.uploadBtn.addEventListener('click', uploadFiles);
dom.regenerateBtn.addEventListener('click', regeneratePlan);
dom.approveBtn.addEventListener('click', buildRepo);

function handleDrop(e) {
    e.preventDefault();
    dom.uploadArea.classList.remove('dragover');
    const droppedFiles = Array.from(e.dataTransfer.files);
    addFiles(droppedFiles);
}

function handleFileSelect(e) {
    const selectedFiles = Array.from(e.target.files);
    addFiles(selectedFiles);
}

function addFiles(newFiles) {
    state.files = [...state.files, ...newFiles];
    renderFileList();
    dom.uploadBtn.disabled = state.files.length === 0;
}

function renderFileList() {
    dom.fileList.innerHTML = state.files.map(file => `
        <div class="file-item">
            <span>${file.name}</span>
            <span style="font-size: 0.8rem; color: var(--text-muted)">${(file.size / 1024).toFixed(1)} KB</span>
        </div>
    `).join('');
}

async function uploadFiles() {
    showSection('processing-section');
    dom.processingText.textContent = "Parsing documents and generating plan...";

    const formData = new FormData();
    state.files.forEach(file => formData.append('files', file));

    try {
        const response = await fetch('/api/init', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Upload failed');

        const data = await response.json();
        state.sessionId = data.session_id;
        state.plan = data.plan;

        renderPlan();
        showSection('plan-section');
    } catch (error) {
        console.error(error);
        alert('An error occurred during upload/parsing.');
        showSection('upload-section');
    }
}

function renderPlan() {
    const p = state.plan;
    dom.planContent.innerHTML = `
        <div class="info-group">
            <div class="info-label">Title</div>
            <div class="info-value">${p.title}</div>
        </div>
        <div class="info-group">
            <div class="info-label">Description</div>
            <div class="info-value">${p.description}</div>
        </div>
        <div class="info-group">
            <div class="info-label">Tasks (${p.tasks.length})</div>
            <ul class="task-list">
                ${p.tasks.map(t => `
                    <li class="task-item">
                        <div class="task-title">${t.name}</div>
                        <div class="task-desc">${t.description}</div>
                        <div class="task-desc" style="margin-top:0.5rem; font-size:0.8rem">Files: ${t.files.join(', ')}</div>
                    </li>
                `).join('')}
            </ul>
        </div>
    `;
}

async function regeneratePlan() {
    const feedback = dom.feedbackInput.value;
    if (!feedback) return;

    showSection('processing-section');
    dom.processingText.textContent = "Refining plan based on feedback...";

    try {
        const response = await fetch('/api/plan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: state.sessionId,
                feedback: feedback
            })
        });

        if (!response.ok) throw new Error('Planning failed');

        const newPlan = await response.json();
        state.plan = newPlan;
        dom.feedbackInput.value = ''; // Clear feedback

        renderPlan();
        showSection('plan-section');
    } catch (error) {
        console.error(error);
        alert('Failed to regenerate plan.');
        showSection('plan-section');
    }
}

async function buildRepo() {
    showSection('processing-section');
    dom.processingText.textContent = "Initializing build...";

    try {
        const response = await fetch('/api/build', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: state.sessionId })
        });

        if (!response.ok) throw new Error('Build failed to start');

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop(); // Keep incomplete chunk

            for (const line of lines) {
                if (!line.trim()) continue;
                try {
                    const event = JSON.parse(line);
                    handleBuildEvent(event);
                } catch (e) {
                    console.error("Error parsing stream line:", e, line);
                }
            }
        }

    } catch (error) {
        console.error(error);
        alert('Failed to build repository.');
        showSection('plan-section');
    }
}

function handleBuildEvent(event) {
    if (event.type === 'log') {
        dom.processingText.textContent = event.message;
    } else if (event.type === 'complete') {
        dom.downloadBtn.parentElement.href = event.download_url;
        showSection('success-section');
    } else if (event.type === 'error') {
        alert("Error during build: " + event.message);
        showSection('plan-section');
    }
}

function showSection(id) {
    // Hide all sections
    Object.values(dom).forEach(el => {
        if (el && el.id && el.id.includes('section')) {
            el.classList.add('hidden');
        }
    });
    // Show target
    document.getElementById(id).classList.remove('hidden');
}
