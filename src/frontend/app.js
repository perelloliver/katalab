const state = {
    companyFiles: [],
    employeeFiles: [],
    sessionId: null,
    plan: null
};

const dom = {
    uploadSection: document.getElementById('upload-section'),
    processingSection: document.getElementById('processing-section'),
    planSection: document.getElementById('plan-section'),
    successSection: document.getElementById('success-section'),

    companyUploadArea: document.getElementById('company-upload-area'),
    employeeUploadArea: document.getElementById('employee-upload-area'),
    companyFileInput: document.getElementById('company-file-input'),
    employeeFileInput: document.getElementById('employee-file-input'),

    companyFileList: document.getElementById('company-file-list'),
    employeeFileList: document.getElementById('employee-file-list'),

    nTasksInput: document.getElementById('n-tasks-input'),
    uploadBtn: document.getElementById('upload-btn'),

    processingText: document.getElementById('processing-text'),
    planContent: document.getElementById('plan-content'),
    feedbackInput: document.getElementById('feedback-input'),
    regenerateBtn: document.getElementById('regenerate-btn'),
    approveBtn: document.getElementById('approve-btn'),
    downloadBtn: document.getElementById('download-btn')
};

// Event Listeners for Company Upload
dom.companyUploadArea.addEventListener('click', () => dom.companyFileInput.click());
dom.companyUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dom.companyUploadArea.classList.add('dragover');
});
dom.companyUploadArea.addEventListener('dragleave', () => {
    dom.companyUploadArea.classList.remove('dragover');
});
dom.companyUploadArea.addEventListener('drop', (e) => handleDrop(e, 'company'));
dom.companyFileInput.addEventListener('change', (e) => handleFileSelect(e, 'company'));

// Event Listeners for Employee Upload
dom.employeeUploadArea.addEventListener('click', () => dom.employeeFileInput.click());
dom.employeeUploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dom.employeeUploadArea.classList.add('dragover');
});
dom.employeeUploadArea.addEventListener('dragleave', () => {
    dom.employeeUploadArea.classList.remove('dragover');
});
dom.employeeUploadArea.addEventListener('drop', (e) => handleDrop(e, 'employee'));
dom.employeeFileInput.addEventListener('change', (e) => handleFileSelect(e, 'employee'));

// Other Event Listeners
dom.uploadBtn.addEventListener('click', uploadFiles);
dom.regenerateBtn.addEventListener('click', regeneratePlan);
dom.approveBtn.addEventListener('click', buildRepo);

function handleDrop(e, type) {
    e.preventDefault();
    const uploadArea = type === 'company' ? dom.companyUploadArea : dom.employeeUploadArea;
    uploadArea.classList.remove('dragover');
    const files = Array.from(e.dataTransfer.files);
    addFiles(files, type);
}

function handleFileSelect(e, type) {
    const files = Array.from(e.target.files);
    addFiles(files, type);
    e.target.value = '';
}

function addFiles(files, type) {
    if (type === 'company') {
        state.companyFiles = [...state.companyFiles, ...files];
        renderFileList('company');
    } else {
        state.employeeFiles = [...state.employeeFiles, ...files];
        renderFileList('employee');
    }
    updateUploadButton();
}

function renderFileList(type) {
    const files = type === 'company' ? state.companyFiles : state.employeeFiles;
    const listElement = type === 'company' ? dom.companyFileList : dom.employeeFileList;

    if (files.length === 0) {
        listElement.innerHTML = '';
        return;
    }

    listElement.innerHTML = files.map(file => `
        <div class="file-item">
            <span>${file.name}</span>
            <span style="color: #999;">${(file.size / 1024).toFixed(1)} KB</span>
        </div>
    `).join('');
}

function updateUploadButton() {
    const hasCompany = state.companyFiles.length > 0;
    const hasEmployee = state.employeeFiles.length > 0;
    dom.uploadBtn.disabled = !(hasCompany && hasEmployee);
}

async function uploadFiles() {
    showSection('processing-section');
    dom.processingText.textContent = "Parsing documents and generating plan...";

    const formData = new FormData();
    state.companyFiles.forEach(file => formData.append('company_files', file));
    state.employeeFiles.forEach(file => formData.append('employee_files', file));

    const nTasks = parseInt(dom.nTasksInput.value) || 1;

    try {
        const response = await fetch(`/api/init?n_tasks=${nTasks}`, {
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
                ${p.tasks.map((t, i) => `
                    <li class="task-item">
                        <div class="task-title">${i + 1}. ${t.name}</div>
                        <div class="task-desc">${t.description}</div>
                        <div class="task-desc" style="margin-top:0.5rem;">Files: ${t.files.join(', ')}</div>
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
        dom.feedbackInput.value = '';

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
            buffer = lines.pop();

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
    [dom.uploadSection, dom.processingSection, dom.planSection, dom.successSection].forEach(el => {
        el.classList.add('hidden');
    });
    document.getElementById(id).classList.remove('hidden');
}
