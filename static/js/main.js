// ParGaMD UI - Main JavaScript File

class ParGaMDUIController {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 6;
        this.socket = io();
        this.sessionId = null;
        this.uploadedFiles = {};
        
        this.initializeEventListeners();
        this.initializeSocketListeners();
    }
    
    initializeEventListeners() {
        // Navigation
        document.getElementById('next-btn').addEventListener('click', () => this.nextStep());
        document.getElementById('prev-btn').addEventListener('click', () => this.prevStep());
        
        // SSH removed: no auth method listeners
        
        // File uploads
        this.setupFileUploads();
        
        // Configuration management
        document.getElementById('save-config-btn').addEventListener('click', () => this.saveConfiguration());
        document.getElementById('load-config-btn').addEventListener('click', () => this.showLoadConfigModal());
        document.getElementById('load-config-confirm').addEventListener('click', () => this.loadConfiguration());
        
        // Configuration preview
        document.getElementById('config-preview-select').addEventListener('change', (e) => {
            this.updateConfigPreview(e.target.value);
        });
        // Download ZIP
        const downloadBtn = document.getElementById('download-zip-btn');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => this.downloadConfigsZip());
        }
        
        // Experiment control
        document.getElementById('start-experiment-btn').addEventListener('click', () => this.startExperiment());
        // SSH removed: no terminal/copy actions
        
        // Form validation
        this.setupFormValidation();
    }
    
    initializeSocketListeners() {
        this.socket.on('job_status_update', (data) => {
            this.updateJobStatus(data);
        });
        
        this.socket.on('iteration_update', (data) => {
            this.updateIterationProgress(data);
        });
        
        this.socket.on('error', (data) => {
            this.showError(data.error);
        });
    }
    
    setupFileUploads() {
        // PDB file upload
        const pdbUploadArea = document.getElementById('pdb_upload_area');
        const pdbFileInput = document.getElementById('pdb_file');
        
        pdbUploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            pdbUploadArea.classList.add('dragover');
        });
        
        pdbUploadArea.addEventListener('dragleave', () => {
            pdbUploadArea.classList.remove('dragover');
        });
        
        pdbUploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            pdbUploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                pdbFileInput.files = files;
                this.handleFileUpload('pdb_file', files[0]);
            }
        });
        
        pdbFileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFileUpload('pdb_file', e.target.files[0]);
            }
        });
        
        // PRMTOP file upload
        const prmtopUploadArea = document.getElementById('prmtop_upload_area');
        const prmtopFileInput = document.getElementById('prmtop_file');
        
        prmtopUploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            prmtopUploadArea.classList.add('dragover');
        });
        
        prmtopUploadArea.addEventListener('dragleave', () => {
            prmtopUploadArea.classList.remove('dragover');
        });
        
        prmtopUploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            prmtopUploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                prmtopFileInput.files = files;
                this.handleFileUpload('prmtop_file', files[0]);
            }
        });
        
        prmtopFileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFileUpload('prmtop_file', e.target.files[0]);
            }
        });
    }
    
    setupFormValidation() {
        // Real-time validation for required fields
        const requiredFields = document.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            field.addEventListener('blur', () => {
                this.validateField(field);
            });
        });
    }
    
    validateField(field) {
        const isValid = field.checkValidity();
        if (!isValid) {
            field.classList.add('is-invalid');
        } else {
            field.classList.remove('is-invalid');
        }
        return isValid;
    }
    
    validateCurrentStep() {
        const currentSection = document.getElementById(`step-${this.currentStep}`);
        const requiredFields = currentSection.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });
        
        // Step-specific validation
        if (this.currentStep === 2) {
            if (!this.uploadedFiles.pdb_file || !this.uploadedFiles.prmtop_file) {
                this.showError('Please upload both PDB and PRMTOP files');
                isValid = false;
            }
        }
        
        return isValid;
    }
    
    nextStep() {
        if (!this.validateCurrentStep()) {
            return;
        }
        
        if (this.currentStep < this.totalSteps) {
            this.currentStep++;
            this.updateStepDisplay();
            
            // Special handling for step 5 (Review & Generate)
            if (this.currentStep === 5) {
                this.generateConfigurationPreview();
            }
        }
    }
    
    prevStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.updateStepDisplay();
        }
    }
    
    updateStepDisplay() {
        // Update step indicators
        document.querySelectorAll('.step').forEach((step, index) => {
            const stepNum = index + 1;
            step.classList.remove('active', 'completed');
            
            if (stepNum === this.currentStep) {
                step.classList.add('active');
            } else if (stepNum < this.currentStep) {
                step.classList.add('completed');
            }
        });
        
        // Update form sections
        document.querySelectorAll('.form-section').forEach((section, index) => {
            const stepNum = index + 1;
            section.classList.remove('active');
            
            if (stepNum === this.currentStep) {
                section.classList.add('active');
            }
        });
        
        // Update navigation buttons
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        
        prevBtn.style.display = this.currentStep > 1 ? 'block' : 'none';
        
        if (this.currentStep === this.totalSteps) {
            nextBtn.style.display = 'none';
        } else {
            nextBtn.style.display = 'block';
        }
    }
    
    // SSH removed
    
    async handleFileUpload(fileType, file) {
        const formData = new FormData();
        formData.append(fileType, file);
        
        try {
            const response = await fetch('/api/upload_files', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.uploadedFiles[fileType] = {
                    file_path: result.file_path,
                    filename: result.filename,
                    file_type: result.file_type
                };
                this.updateFileInfo(fileType, file.name, result);
                this.showSuccess(`${file.name} uploaded successfully`);
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError('File upload failed: ' + error.message);
        }
    }
    
    updateFileInfo(fileType, fileName, uploadResult) {
        const infoDiv = document.getElementById(`${fileType}_info`);
        infoDiv.innerHTML = `
            <div class="alert alert-success">
                <i class="fas fa-check-circle"></i> ${fileName} uploaded successfully
            </div>
        `;
    }
    
    generateConfigurationPreview() {
        const formData = this.getFormData();
        const configSummary = document.getElementById('config-summary');
        
        configSummary.innerHTML = `
            <div class="card">
                <div class="card-body">
                    <h6>System Setup</h6>
                    <ul class=\"list-unstyled\"> 
                        <li><strong>SLURM Account:</strong> ${formData.account}</li>
                        <li><strong>Email:</strong> ${formData.email}</li>
                    </ul>
                    
                    <h6>Molecular System</h6>
                    <ul class="list-unstyled">
                        <li><strong>Protein Name:</strong> ${formData.protein_name}</li>
                        <li><strong>PDB File:</strong> ${this.uploadedFiles.pdb_file?.filename || 'Not uploaded'}</li>
                        <li><strong>PRMTOP File:</strong> ${this.uploadedFiles.prmtop_file?.filename || 'Not uploaded'}</li>
                    </ul>
                    
                    <h6>WE Parameters</h6>
                    <ul class="list-unstyled">
                        <li><strong>Walkers per Bin:</strong> ${formData.bin_target_counts}</li>
                        <li><strong>Max Iterations:</strong> ${formData.max_total_iterations}</li>
                        <li><strong>PC1 (RMSD):</strong> ${formData.pc1_min} to ${formData.pc1_max} (step: ${formData.pc1_step})</li>
                        <li><strong>PC2 (Rg):</strong> ${formData.pc2_min} to ${formData.pc2_max} (step: ${formData.pc2_step})</li>
                    </ul>
                    
                    <h6>GPU Options</h6>
                    <ul class="list-unstyled">
                        <li><strong>Multi-GPU Parallelization:</strong> ${formData.enable_gpu_parallelization ? 'Enabled' : 'Disabled'}</li>
                    </ul>
                </div>
            </div>
        `;
        
        // Update config preview
        this.updateConfigPreview('west.cfg');
    }
    
    async updateConfigPreview(filename) {
        const formData = this.getFormData();
        // include include_infinite_bounds flag from UI
        formData.include_infinite_bounds = document.getElementById('include_infinite_bounds')?.checked ?? true;
        
        try {
            const response = await fetch('/api/generate_config_preview', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filename: filename,
                    params: formData
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                const previewDiv = document.getElementById('config-preview');
                previewDiv.innerHTML = `<pre><code>${result.content}</code></pre>`;
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError('Failed to generate config preview: ' + error.message);
        }
    }

    async downloadConfigsZip() {
        const formData = this.getFormData();
        formData.include_infinite_bounds = document.getElementById('include_infinite_bounds')?.checked ?? true;

        try {
            const response = await fetch('/api/download_configs_zip', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ params: formData })
            });

            if (!response.ok) {
                const text = await response.text();
                this.showError('Failed to download ZIP: ' + text);
                return;
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `ParGaMD_configs_${Date.now()}.zip`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            this.showError('Error downloading ZIP: ' + error.message);
        }
    }
    
    async saveConfiguration() {
        const formData = this.getFormData();
        
        try {
            const response = await fetch('/api/save_config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showSuccess(`Configuration saved with ID: ${result.config_id}`);
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError('Failed to save configuration: ' + error.message);
        }
    }
    
    showLoadConfigModal() {
        const modal = new bootstrap.Modal(document.getElementById('loadConfigModal'));
        modal.show();
    }
    
    async loadConfiguration() {
        const configId = document.getElementById('config-id-input').value;
        
        if (!configId) {
            this.showError('Please enter a configuration ID');
            return;
        }
        
        try {
            const response = await fetch('/api/load_config', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ config_id: configId })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.populateFormWithConfig(result.config);
                this.showSuccess('Configuration loaded successfully');
                
                const modal = bootstrap.Modal.getInstance(document.getElementById('loadConfigModal'));
                modal.hide();
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError('Failed to load configuration: ' + error.message);
        }
    }
    
    populateFormWithConfig(config) {
        // Populate form fields with loaded configuration
        Object.keys(config).forEach(key => {
            const field = document.getElementById(key);
            if (field) {
                if (field.type === 'checkbox') {
                    field.checked = config[key];
                } else {
                    field.value = config[key];
                }
            }
        });
        
        // Update step display to show current configuration
        this.generateConfigurationPreview();
    }
    
    async startExperiment() {
        const formData = this.getFormData();
        
        if (!this.validateExperimentSetup(formData)) {
            return;
        }
        
        try {
            // SSH disabled: show message only
            this.showError('Start is disabled: SSH/job submission is turned off in this build.');
            return;
            
            const result = await response.json();
            
            if (result.success) {
                this.sessionId = result.session_id;
                this.updateJobStatus({
                    status: 'cmd_running',
                    cmd_job_id: result.cmd_job_id
                });
                
                document.getElementById('ssh-command').value = result.ssh_command;
                document.getElementById('open-terminal-btn').style.display = 'block';
                
                this.showSuccess('Experiment started successfully! cGaMD job submitted.');
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError('Failed to start experiment: ' + error.message);
        }
    }
    
    validateExperimentSetup(formData) {
        // Check if all required files are uploaded
        if (!this.uploadedFiles.pdb_file || !this.uploadedFiles.prmtop_file) {
            this.showError('Please upload both PDB and PRMTOP files');
            return false;
        }
        
        // Check if required fields are filled (SSH removed)
        const requiredFields = ['account', 'email', 'protein_name'];
        for (const field of requiredFields) {
            if (!formData[field]) {
                this.showError(`Please fill in the ${field} field`);
                return false;
            }
        }
        
        return true;
    }
    
    updateJobStatus(data) {
        const statusDiv = document.getElementById('job-status');
        const progressContainer = document.getElementById('progress-container');
        
        let statusHtml = '';
        
        switch (data.status) {
            case 'cmd_running':
                statusHtml = `
                    <div class="alert alert-info">
                        <i class="fas fa-play-circle"></i> cGaMD simulation running (Job ID: ${data.cmd_job_id})
                    </div>
                `;
                break;
            case 'we_started':
                statusHtml = `
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle"></i> cGaMD completed successfully
                    </div>
                    <div class="alert alert-info">
                        <i class="fas fa-play-circle"></i> WE simulation started (Job ID: ${data.we_job_id})
                    </div>
                `;
                progressContainer.style.display = 'block';
                break;
            case 'we_running':
                statusHtml = `
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle"></i> cGaMD completed successfully
                    </div>
                    <div class="alert alert-info">
                        <i class="fas fa-play-circle"></i> WE simulation running (Job ID: ${data.we_job_id})
                    </div>
                `;
                progressContainer.style.display = 'block';
                break;
            case 'completed':
                statusHtml = `
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle"></i> Experiment completed successfully!
                    </div>
                `;
                break;
            default:
                statusHtml = `
                    <div class="alert alert-info">
                        <i class="fas fa-clock"></i> Ready to start experiment
                    </div>
                `;
        }
        
        statusDiv.innerHTML = statusHtml;
    }
    
    updateIterationProgress(data) {
        const progressBar = document.getElementById('iteration-progress');
        const iterationText = document.getElementById('iteration-text');
        
        const percentage = (data.current_iteration / data.max_iterations) * 100;
        progressBar.style.width = `${percentage}%`;
        progressBar.setAttribute('aria-valuenow', data.current_iteration);
        progressBar.setAttribute('aria-valuemax', data.max_iterations);
        
        iterationText.textContent = `Iteration ${data.current_iteration} / ${data.max_iterations}`;
    }
    
    // SSH removed
    
    getFormData() {
        const form = document.getElementById('experiment-form');
        const formData = new FormData(form);
        const data = {};
        
        for (const [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        // Handle checkbox
        data.enable_gpu_parallelization = document.getElementById('enable_gpu_parallelization').checked;
        
        // Handle file inputs
        const pdbFile = document.getElementById('pdb_file').files[0];
        const prmtopFile = document.getElementById('prmtop_file').files[0];
        if (pdbFile) data.pdb_file = pdbFile;
        if (prmtopFile) data.prmtop_file = prmtopFile;
        
        return data;
    }
    
    showError(message) {
        this.showMessage(message, 'error');
    }
    
    showSuccess(message) {
        this.showMessage(message, 'success');
    }
    
    showMessage(message, type) {
        const container = document.getElementById('message-container');
        const messageDiv = document.createElement('div');
        messageDiv.className = type === 'error' ? 'error-message' : 'success-message';
        messageDiv.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'check-circle'}"></i>
            ${message}
        `;
        
        container.appendChild(messageDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 5000);
    }
}

// Initialize the UI controller when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.pargamdUI = new ParGaMDUIController();
});
