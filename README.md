# ParGaMD GUI

A modern web-based graphical user interface for setting up and configuring ParGaMD (Parallelizable Gaussian Accelerated Molecular Dynamics) experiments. This tool streamlines the process of configuring molecular dynamics simulations by providing an intuitive interface for parameter management and configuration file generation.

## 🚀 Features

### Core Functionality
- **Interactive Parameter Configuration**: Set up all ParGaMD simulation parameters through a user-friendly web interface
- **Dynamic Configuration Generation**: Automatically generate all required configuration files with proper formatting
- **Real-time Preview**: Preview generated configuration files before downloading
- **Complete Bundle Export**: Download all necessary files and directories as a ZIP archive
- **Template Management**: Save and load parameter configurations for reuse

### Parameter Management
- **Progress Coordinate Configuration**: Define minimum, maximum, and step sizes for both CVs (Collective Variables)
- **Infinite Bounds Support**: Optional inclusion of `-inf` and `inf` as outer bin boundaries to prevent simulation errors
- **GPU Parallelization Control**: Toggle GPU parallelization features in runseg.sh
- **WE Parameters**: Configure bin target counts and maximum iterations
- **MD Parameters**: Set nstlim, ntpr, and other molecular dynamics parameters
- **File Upload**: Upload PDB and PRMTOP files for protein structure input

### Generated Files
The GUI generates the following configuration files:
- `west.cfg` - WESTPA configuration with dynamic bin boundaries
- `env.sh` - Environment setup with dynamic path configuration
- `runseg.sh` - Segment execution script with optional GPU parallelization
- `run_cmd.sh` - Conventional MD execution script
- `run_WE.sh` - Weighted Ensemble execution script

### Included Directories
The ZIP export includes complete directory structure:
- `cMD/` - Conventional MD files and scripts
- `common_files/` - Shared files and templates
- `bstates/` - Basis state files
- `westpa_scripts/` - WESTPA execution scripts

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sonti974948/ParGaMD-GUI.git
   cd ParGaMD-GUI
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python ui_app.py
   ```

4. **Access the GUI**:
   Open your web browser and navigate to `http://localhost:5000`

## 🎯 Usage Guide

### Step 1: Basic Information
- Enter protein name (used in file naming)
- Provide account and email information for SLURM job submission
- Set job time limit (default: 48 hours)

### Step 2: File Upload
- Upload your PDB file (protein structure)
- Upload your PRMTOP file (topology)
- Files are validated and stored for configuration generation

### Step 3: WE Parameters
- **Progress Coordinate 1 (PC1)**: Set minimum, maximum, and step size
- **Progress Coordinate 2 (PC2)**: Set minimum, maximum, and step size
- **Include Infinite Bounds**: Toggle to add `-inf` and `inf` as outer boundaries
- **Bin Target Counts**: Number of walkers per bin
- **Max Total Iterations**: Maximum number of WE iterations

### Step 4: MD Parameters
- **nstlim**: Number of MD steps
- **ntpr**: Frequency of trajectory output
- **Enable GPU Parallelization**: Toggle GPU features in runseg.sh

### Step 5: Review & Generate
- Preview all generated configuration files
- Switch between different files using the dropdown
- Verify parameter settings and file content

### Step 6: Download
- Click "Download All as ZIP" to get the complete ParGaMD bundle
- The ZIP contains all necessary files and directories for running simulations

## 📁 Project Structure

```
ParGaMD-GUI/
├── ui_app.py              # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main UI template
├── static/
│   └── js/
│       └── main.js       # Frontend JavaScript logic
├── uploads/              # Temporary file storage
├── README.md            # This documentation
└── UI_README.md         # Detailed UI documentation
```

## 🔧 Configuration Details

### west.cfg
- Dynamic bin boundaries based on user input
- Configurable progress coordinate dimensionality
- Automatic pcoord_len calculation based on MD parameters
- Support for infinite bounds to prevent simulation errors

### env.sh
- Dynamic NODELOC setting using `${WEST_SIM_ROOT:-$PWD}`
- Complete environment setup for AMBER/WESTPA
- All necessary PATH and environment variable exports

### runseg.sh
- Conditional GPU parallelization based on user preference
- Complete MD simulation workflow
- Progress coordinate calculation using CPPTRAJ
- Proper file linking and cleanup

### run_WE.sh
- SLURM job submission script
- ZMQ-based parallel execution setup
- Node management and communication

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Kill existing process on port 5000
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```

2. **File Upload Issues**:
   - Ensure files are valid PDB/PRMTOP format
   - Check file permissions
   - Verify file size limits

3. **Configuration Preview Not Loading**:
   - Refresh the browser page
   - Check browser console for JavaScript errors
   - Verify all required parameters are filled

4. **ZIP Download Issues**:
   - Ensure all directories exist in the project
   - Check file permissions for directory access
   - Verify sufficient disk space

### Debug Mode
Run the application in debug mode for detailed error messages:
```bash
export FLASK_ENV=development
python ui_app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ParGaMD**: Parallelizable Gaussian Accelerated Molecular Dynamics framework
- **WESTPA**: Weighted Ensemble Simulation Toolkit
- **AMBER**: Assisted Model Building with Energy Refinement
- **Flask**: Python web framework
- **Bootstrap**: CSS framework for responsive design

## 📞 Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Contact the development team
- Check the troubleshooting section above

## 🔄 Version History

- **v1.0.0**: Initial release with basic ParGaMD configuration
- **v1.1.0**: Added infinite bounds support and complete file preview
- **v1.2.0**: Enhanced ZIP export with full directory structure
- **v1.3.0**: Improved UI/UX and error handling

---

**Note**: This GUI is designed to work with ParGaMD simulations and requires proper setup of AMBER, WESTPA, and related dependencies on your HPC cluster.


