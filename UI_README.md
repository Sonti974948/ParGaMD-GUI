# ParGaMD UI - Web Interface for ParGaMD Experiments

A modern web-based user interface for setting up and monitoring ParGaMD (Parallelizable Gaussian Accelerated Molecular Dynamics) experiments on HPC clusters.

## Features

### 🚀 **Easy Experiment Setup**
- **Multi-step Wizard**: Guided setup through 6 intuitive steps
- **Dynamic Configuration Generation**: Automatically generates all required config files
- **File Upload**: Drag-and-drop interface for PDB and PRMTOP files
- **Parameter Templates**: Save and load experiment configurations

### 🔧 **Smart Configuration Management**
- **GPU Parallelization Toggle**: Enable/disable multi-GPU support with a single click
- **Progress Coordinate Setup**: Easy configuration of RMSD and Radius of Gyration boundaries
- **WE Parameters**: Configure walkers, iterations, and MD parameters
- **Real-time Preview**: Preview generated configuration files before submission

### 🔐 **Secure Cluster Integration**
- **SSH Authentication**: Support for both password and SSH key authentication
- **Automatic File Transfer**: Upload files directly to HPC cluster
- **Job Submission**: Automatically submit cGaMD and ParGaMD jobs
- **Local Terminal Integration**: Open terminal with pre-filled SSH command

### 📊 **Real-time Monitoring**
- **Job Status Tracking**: Monitor cGaMD and WE job progress
- **Iteration Progress**: Real-time updates on WE simulation iterations
- **WebSocket Communication**: Live updates without page refresh
- **Error Handling**: Clear error messages and status updates

## Installation

### Prerequisites
- Python 3.8 or higher
- Access to an HPC cluster with SLURM scheduler
- AMBER molecular dynamics software
- WESTPA framework

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ParGaMD
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the UI**:
   ```bash
   python ui_app.py
   ```

4. **Access the interface**:
   Open your web browser and navigate to `http://localhost:5000`

## Usage Guide

### Step 1: System Setup
- **SSH Connection**: Enter your cluster hostname, username, and authentication method
- **Experiment Directory**: Specify the execution directory on the cluster
- **SLURM Account**: Enter your SLURM account and email for notifications

### Step 2: Molecular System
- **Protein Name**: Enter a name for your protein (e.g., "chignolin")
- **File Upload**: Upload your PDB and PRMTOP files using drag-and-drop or file browser

### Step 3: WE Parameters
- **Basic Parameters**:
  - **Walkers per Bin**: Number of walkers per progress coordinate bin (default: 4)
  - **Maximum Iterations**: Total number of WE iterations (default: 1000)
  - **MD Steps**: Number of molecular dynamics steps per iteration (default: 50000)
  - **Print Frequency**: Frequency of output writing (default: 500)

- **Progress Coordinates**:
  - **PC1 (RMSD)**: Configure minimum, maximum, and step size for RMSD
  - **PC2 (Radius of Gyration)**: Configure minimum, maximum, and step size for Rg

### Step 4: GPU Options
- **Multi-GPU Parallelization**: Toggle to enable/disable multi-GPU support
  - When **enabled**: Uses multiple GPUs for parallel processing
  - When **disabled**: GPU parallelization code is commented out for single-GPU systems

### Step 5: Review & Generate
- **Configuration Summary**: Review all your settings
- **File Preview**: Preview generated configuration files
- **Save/Load**: Save your configuration or load a previously saved one

### Step 6: Monitor
- **Start Experiment**: Begin the ParGaMD simulation
- **Job Monitoring**: Track cGaMD and WE job progress
- **Terminal Access**: Open local terminal with SSH connection
- **Progress Tracking**: Monitor WE iteration progress in real-time

## Configuration Files Generated

The UI automatically generates the following configuration files:

1. **`west.cfg`**: WESTPA configuration with progress coordinates and bin setup
2. **`env.sh`**: Environment setup script with paths and module loading
3. **`westpa_scripts/runseg.sh`**: Segment execution script with GPU options
4. **`cMD/run_cmd.sh`**: cGaMD job submission script
5. **`run_we.sh`**: WE job submission script

## Workflow

1. **cGaMD Phase**: The system first runs conventional GaMD to obtain acceleration parameters
2. **File Transfer**: PDB/PRMTOP files and configurations are uploaded to the cluster
3. **Job Submission**: cGaMD job is submitted automatically
4. **Monitoring**: System monitors cGaMD completion
5. **WE Phase**: When cGaMD completes, WE job is automatically submitted
6. **Progress Tracking**: Real-time monitoring of WE iterations and completion

## Security Features

- **No Credential Storage**: SSH credentials are never stored on disk
- **Secure File Upload**: Files are temporarily stored and then transferred to cluster
- **Session Management**: Each experiment gets a unique session ID
- **Error Handling**: Secure error reporting without exposing sensitive information

## Troubleshooting

### Common Issues

1. **SSH Connection Failed**
   - Verify hostname and username
   - Check SSH key permissions (if using key authentication)
   - Ensure cluster is accessible from your network

2. **File Upload Errors**
   - Check file sizes (max 100MB per file)
   - Verify file formats (.pdb, .prmtop)
   - Ensure sufficient disk space

3. **Job Submission Errors**
   - Verify SLURM account and partition
   - Check cluster resource availability
   - Review job script permissions

4. **Configuration Generation Errors**
   - Validate all required parameters
   - Check progress coordinate boundaries
   - Ensure protein name doesn't contain special characters

### Getting Help

- Check the job logs on the cluster for detailed error messages
- Use the terminal access feature to manually inspect the experiment directory
- Review the generated configuration files for any issues

## Advanced Features

### Parameter Templates
- Save frequently used configurations
- Share configurations with team members
- Quick setup for similar experiments

### Real-time Monitoring
- WebSocket-based live updates
- No need to refresh the page
- Automatic job status detection

### GPU Optimization
- Automatic detection of GPU parallelization needs
- Configurable GPU device allocation
- Error-free single-GPU operation

## Contributing

To contribute to the ParGaMD UI:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the same license as the main ParGaMD repository.

## Support

For support and questions:
- Check the troubleshooting section
- Review the generated configuration files
- Contact the development team

---

**Note**: This UI is designed to work with the existing ParGaMD framework. Ensure you have the proper AMBER and WESTPA installations on your HPC cluster before using this interface.
