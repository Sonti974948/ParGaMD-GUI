#!/usr/bin/env python3
"""
ParGaMD UI - Web interface for setting up and monitoring ParGaMD experiments
"""

import os
import json
import subprocess
import threading
import time
from datetime import datetime
import os
from io import BytesIO
import zipfile
from flask import Flask, render_template, request, jsonify, send_file, session
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
import tempfile
import shutil
from jinja2 import Template
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pargamd-ui-secret-key-2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

socketio = SocketIO(app, cors_allowed_origins="*")

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global variables for job monitoring (SSH removed)
job_status = {}
experiment_configs = {}

class ParGaMDConfigGenerator:
    """Generate configuration files for ParGaMD experiments"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """Load Jinja2 templates for configuration files"""
        return {
            'west_cfg': self._get_west_cfg_template(),
            'env_sh': self._get_env_sh_template(),
            'runseg_sh': self._get_runseg_sh_template(),
            'run_cmd_sh': self._get_run_cmd_sh_template(),
            'run_we_sh': self._get_run_we_sh_template()
        }
    
    def _get_west_cfg_template(self):
        return Template("""# The master WEST configuration file for a simulation.
# vi: set filetype=yaml :
---
west: 
  system:
    driver: westpa.core.systems.WESTSystem
    system_options:
      # Dimensionality of your progress coordinate
      pcoord_ndim: 2
      # Number of data points per iteration
      # Needs to be pcoord_len >= 2 (minimum of parent, last frame) to work with most analysis tools
      pcoord_len: {{ pcoord_len }}
      # Data type for your progress coordinate 
      pcoord_dtype: !!python/name:numpy.float32
      bins:
        type: RectilinearBinMapper
        # The edges of the bins 
        boundaries:         
          - {{ pc1_bins }}
          - {{ pc2_bins }}
      # Number walkers per bin
      bin_target_counts: {{ bin_target_counts }}
  propagation:
    max_total_iterations: {{ max_total_iterations }}
    max_run_wallclock:    47:30:00
    propagator:           executable
    gen_istates:          false
  data:
    west_data_file: west.h5
    datasets:
      - name:        pcoord
        scaleoffset: 4
      - name:        coord
        dtype:       float32
        scaleoffset: 3
    data_refs:
      segment:       $WEST_SIM_ROOT/traj_segs/{segment.n_iter:06d}/{segment.seg_id:06d}
      basis_state:   $WEST_SIM_ROOT/bstates/{basis_state.auxref}
      initial_state: $WEST_SIM_ROOT/istates/{initial_state.iter_created}/{initial_state.state_id}.rst
  plugins:
  executable:
    environ:
      PROPAGATION_DEBUG: 1
    datasets:
      - name:    coord
        enabled: false
    propagator:
      executable: $WEST_SIM_ROOT/westpa_scripts/runseg.sh
      stdout:     $WEST_SIM_ROOT/seg_logs/{segment.n_iter:06d}-{segment.seg_id:06d}.log
      stderr:     stdout
      stdin:      null
      cwd:        null
      environ:
        SEG_DEBUG: 1
    get_pcoord:
      executable: $WEST_SIM_ROOT/westpa_scripts/get_pcoord.sh
      stdout:     /dev/null 
      stderr:     stdout
    gen_istate:
      executable: $WEST_SIM_ROOT/westpa_scripts/gen_istate.sh
      stdout:     /dev/null 
      stderr:     stdout
    post_iteration:
      enabled:    true
      executable: $WEST_SIM_ROOT/westpa_scripts/post_iter.sh
      stderr:     stdout
    pre_iteration:
      enabled:    false
      executable: $WEST_SIM_ROOT/westpa_scripts/pre_iter.sh
      stderr:     stdout
""")
    
    def _get_env_sh_template(self):
        return Template("""#!/bin/bash

source ~/.bash_profile
module purge
module load shared
module load gpu/0.15.4
module load slurm
module load openmpi/4.0.4
module load cuda/11.0.2
module load amber/20-patch15
conda activate westpa-2.0

export PATH=$PATH:$HOME/bin
export PYTHONPATH=$HOME/miniconda3/envs/westpa-2.0/bin/python
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH

# Explicitly name our simulation root directory
if [[ -z "$WEST_SIM_ROOT" ]]; then
    export WEST_SIM_ROOT="$PWD"
fi

export SIM_NAME=$(basename $WEST_SIM_ROOT)
echo "simulation $SIM_NAME root is $WEST_SIM_ROOT"

# Set up environment for dynamics
source $AMBERHOME/amber.sh

# Set runtime commands (this is said to be easier on the filesystem)
export NODELOC="${WEST_SIM_ROOT:-$PWD}"
export USE_LOCAL_SCRATCH=1

export WM_ZMQ_MASTER_HEARTBEAT=100
export WM_ZMQ_WORKER_HEARTBEAT=100
export WM_ZMQ_TIMEOUT_FACTOR=300
export BASH=$SWROOT/bin/bash
export PERL=$SWROOT/usr/bin/perl
export ZSH=$SWROOT/bin/zsh
export IFCONFIG=$SWROOT/bin/ifconfig
export CUT=$SWROOT/usr/bin/cut
export TR=$SWROOT/usr/bin/tr
export LN=$SWROOT/bin/ln
export CP=$SWROOT/bin/cp
export RM=$SWROOT/bin/rm
export SED=$SWROOT/bin/sed
export CAT=$SWROOT/bin/cat
export HEAD=$SWROOT/bin/head
export TAR=$SWROOT/bin/tar
export AWK=$SWROOT/usr/bin/awk
export PASTE=$SWROOT/usr/bin/paste
export GREP=$SWROOT/bin/grep
export SORT=$SWROOT/usr/bin/sort
export UNIQ=$SWROOT/usr/bin/uniq
export HEAD=$SWROOT/usr/bin/head
export MKDIR=$SWROOT/bin/mkdir
export ECHO=$SWROOT/bin/echo
export DATE=$SWROOT/bin/date
export SANDER=$AMBERHOME/bin/sander
export PMEMD=$AMBERHOME/bin/pmemd.cuda
export CPPTRAJ=$AMBERHOME/bin/cpptraj
""")
    
    def _get_runseg_sh_template(self):
        return Template("""#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

cd $WEST_SIM_ROOT
mkdir -pv $WEST_CURRENT_SEG_DATA_REF
cd $WEST_CURRENT_SEG_DATA_REF

ln -sv $WEST_SIM_ROOT/common_files/{{ protein_name }}.prmtop .
ln -sv $WEST_SIM_ROOT/common_files/gamd-restart.dat .

if [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_CONTINUES" ]; then
  sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/md.in > md.in
  ln -sv $WEST_PARENT_DATA_REF/seg.rst ./parent.rst
elif [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_NEWTRAJ" ]; then
  sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/md_init.in > md.in
  ln -sv $WEST_PARENT_DATA_REF ./parent.rst
fi

{% if enable_gpu_parallelization %}
export CUDA_DEVICES=(`echo $CUDA_VISIBLE_DEVICES_ALLOCATED | tr , ' '`)
export CUDA_VISIBLE_DEVICES=${CUDA_DEVICES[$WM_PROCESS_INDEX]}

echo "RUNSEG.SH: CUDA_VISIBLE_DEVICES_ALLOCATED = " $CUDA_VISIBLE_DEVICES_ALLOCATED
echo "RUNSEG.SH: WM_PROCESS_INDEX = " $WM_PROCESS_INDEX
echo "RUNSEG.SH: CUDA_VISIBLE_DEVICES = " $CUDA_VISIBLE_DEVICES
{% endif %}

while ! grep -q "Final Performance Info" seg.log; do
	$PMEMD -O -i md.in   -p {{ protein_name }}.prmtop  -c parent.rst \\
          -r seg.rst -x seg.nc      -o seg.log    -inf seg.nfo -gamd gamd.log
done

RMSD=rmsd.dat
RG=rg.dat
COMMAND="         parm {{ protein_name }}.prmtop\\n"
COMMAND="${COMMAND} trajin $WEST_CURRENT_SEG_DATA_REF/parent.rst\\n"
COMMAND="${COMMAND} trajin $WEST_CURRENT_SEG_DATA_REF/seg.nc\\n"
COMMAND="${COMMAND} reference $WEST_SIM_ROOT/common_files/{{ protein_name }}.pdb\\n"
COMMAND="${COMMAND} rms ca-rmsd @CA reference out $RMSD mass\\n"
COMMAND="${COMMAND} radgyr ca-rg @CA  out $RG  mass\\n"
COMMAND="${COMMAND} go\\n"

echo -e $COMMAND | $CPPTRAJ
#cat $RMSD > rmsd.dat
#cat $RG > rg.dat
paste <(cat rmsd.dat | tail -n +2 | awk {'print $2'}) <(cat rg.dat | tail -n +2 | awk {'print $2'})>$WEST_PCOORD_RETURN
#cat $TEMP | tail -n +2 | awk '{print $2}' > $WEST_PCOORD_RETURN
#paste <(cat $TEMP | tail -n 1 | awk {'print $2'}) <(cat $RG | tail -n 1 | awk {'print $2'})>$WEST_PCOORD_RETURN
#cat $TEMP >pcoord.dat
# Clean up
rm -f $TEMP md.in seg.nfo seg.pdb
""")
    
    def _get_run_cmd_sh_template(self):
        return Template("""#!/bin/bash
#SBATCH --job-name="{{ protein_name }}_GaMD"
#SBATCH --output="job.out"
#SBATCH --partition=gpu-shared
#SBATCH --nodes=1
#SBATCH --gpus=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=50G
#SBATCH --account={{ account }}
#SBATCH --no-requeue
#SBATCH --mail-user={{ email }}
#SBATCH --mail-type=ALL
#SBATCH -t 48:00:00

module purge
module load shared
module load gpu/0.15.4
module load slurm
module load openmpi/4.0.4
module load cuda/11.0.2
module load amber/20

export PATH=$PATH:$HOME/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
source $AMBERHOME/amber.sh
pmemd.cuda -O -i md.in -o md.out -p {{ protein_name }}.prmtop -c {{ protein_name }}.rst -r md_cmd.rst -x md.nc
""")
    
    def _get_run_we_sh_template(self):
        return Template("""#!/bin/bash
#SBATCH --job-name="{{ protein_name }}_WE_run"
#SBATCH --output="job.out"
#SBATCH --partition=gpu-shared
#SBATCH --nodes=1
#SBATCH --gpus=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=50G
#SBATCH --account={{ account }}
#SBATCH --no-requeue
#SBATCH --mail-user={{ email }}
#SBATCH --mail-type=ALL
#SBATCH -t 48:00:00

set -x
cd $SLURM_SUBMIT_DIR
source ~/.bashrc
module purge
module load shared
module load gpu/0.15.4
module load slurm
module load openmpi/4.0.4
module load cuda/11.0.2
module load amber/20-patch15
conda activate westpa-2.0

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export WEST_SIM_ROOT=$SLURM_SUBMIT_DIR
cd $WEST_SIM_ROOT
export PYTHONPATH=$HOME/miniconda3/envs/westpa-2.0/bin/python

./init.sh
echo "init.sh ran"
source env.sh || exit 1
env | sort
SERVER_INFO=$WEST_SIM_ROOT/west_zmq_info.json

#TODO: set num_gpu_per_node
num_gpu_per_node=1
rm -rf nodefilelist.txt
scontrol show hostname $SLURM_JOB_NODELIST > nodefilelist.txt

# start server
#w_truncate -n 11
#rm -rf traj_segs/000011
#rm -rf seg_logs/000011*
w_run --work-manager=zmq --n-workers=0 --zmq-mode=master --zmq-write-host-info=$SERVER_INFO --zmq-comm-mode=tcp &> west-$SLURM_JOBID-local.log &

# wait on host info file up to 1 min
for ((n=0; n<60; n++)); do
    if [ -e $SERVER_INFO ] ; then
        echo "== server info file $SERVER_INFO =="
        cat $SERVER_INFO
        break
    fi
    sleep 1
done

# exit if host info file doesn't appear in one minute
if ! [ -e $SERVER_INFO ] ; then
    echo 'server failed to start'
    exit 1
fi
export CUDA_VISIBLE_DEVICES=0
echo$CUDA_VISIBLE_DEVICES
for node in $(cat nodefilelist.txt); do
    ssh -o StrictHostKeyChecking=no $node $PWD/node.sh $SLURM_SUBMIT_DIR $SLURM_JOBID $node $CUDA_VISIBLE_DEVICES --work-manager=zmq --n-workers=$num_gpu_per_node --zmq-mode=client --zmq-read-host-info=$SERVER_INFO --zmq-comm-mode=tcp &
done
wait
""")
    
    def generate_bin_boundaries(self, min_val, max_val, step_size, include_infinite_bounds=True):
        """Generate bin boundaries for progress coordinates"""
        # Coerce to numeric types
        min_val = float(min_val)
        max_val = float(max_val)
        step_size = float(step_size)
        if step_size <= 0:
            step_size = 0.1
        boundaries = []
        if include_infinite_bounds:
            # Use strings for infinities; YAML will render them quoted
            boundaries.append('-inf')
        current = min_val
        # Avoid floating accumulation errors by using integer steps
        num_steps = int(round((max_val - min_val) / step_size))
        for i in range(num_steps + 1):
            value = min_val + i * step_size
            # Keep numeric entries as floats (not strings) for proper YAML formatting
            boundaries.append(float(f"{value:.6g}"))
        if include_infinite_bounds:
            boundaries.append('inf')
        return boundaries
    
    def generate_configs(self, params):
        """Generate all configuration files based on user parameters"""
        configs = {}
        
        include_inf = bool(params.get('include_infinite_bounds', True))
        # Generate bin boundaries
        pc1_bins = self.generate_bin_boundaries(
            params['pc1_min'], params['pc1_max'], params['pc1_step'], include_inf
        )
        pc2_bins = self.generate_bin_boundaries(
            params['pc2_min'], params['pc2_max'], params['pc2_step'], include_inf
        )
        
        # Calculate pcoord_len based on nstlim and ntpr
        nstlim = int(params['nstlim'])
        ntpr = int(params['ntpr'])
        if ntpr <= 0:
            ntpr = 1
        pcoord_len = (nstlim // ntpr) + 1
        
        # Generate west.cfg
        configs['west.cfg'] = self.templates['west_cfg'].render(
            pcoord_len=pcoord_len,
            pc1_bins=pc1_bins,
            pc2_bins=pc2_bins,
            bin_target_counts=int(params['bin_target_counts']),
            max_total_iterations=int(params['max_total_iterations'])
        )
        
        # Generate env.sh (SSH-free; uses $PWD/WEST_SIM_ROOT)
        configs['env.sh'] = self.templates['env_sh'].render()
        
        # Generate runseg.sh
        configs['westpa_scripts/runseg.sh'] = self.templates['runseg_sh'].render(
            protein_name=params['protein_name'],
            enable_gpu_parallelization=params['enable_gpu_parallelization']
        )
        
        # Generate run_cmd.sh
        configs['cMD/run_cmd.sh'] = self.templates['run_cmd_sh'].render(
            protein_name=params['protein_name'],
            account=params['account'],
            email=params['email']
        )
        
        # Generate run_we.sh
        configs['run_we.sh'] = self.templates['run_we_sh'].render(
            protein_name=params['protein_name'],
            account=params['account'],
            email=params['email']
        )
        
        return configs

# Initialize global objects
config_generator = ParGaMDConfigGenerator()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/save_config', methods=['POST'])
def save_config():
    """Save experiment configuration"""
    try:
        config = request.json
        config_id = str(uuid.uuid4())
        experiment_configs[config_id] = config
        return jsonify({'success': True, 'config_id': config_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/download_configs_zip', methods=['POST'])
def download_configs_zip():
    """Generate all configuration files and return as a ZIP download with full directories"""
    try:
        data = request.json or {}
        params = data.get('params', {})

        if 'include_infinite_bounds' not in params:
            params['include_infinite_bounds'] = True

        # Render all templated configs (these should overwrite any static counterparts)
        configs = config_generator.generate_configs(params)
        generated_paths = set(p.replace('\\', '/') for p in configs.keys())

        include_dirs = ['cMD', 'common_files', 'bstates', 'westpa_scripts']
        include_root_files = [
            'west.cfg', 'run_WE.sh', 'env.sh',
            'node.sh', 'init.sh', 'run_data.sh', 'data_extract.py',
            'nodefilelist.txt', 'simtime.py', 'tstate.file'
        ]

        mem_zip = BytesIO()
        with zipfile.ZipFile(mem_zip, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
            # Add directories recursively, skipping files that will be provided by templates
            for directory in include_dirs:
                if not os.path.isdir(directory):
                    continue
                for root, _dirs, files in os.walk(directory):
                    for fname in files:
                        abs_path = os.path.join(root, fname)
                        rel_path = abs_path.replace('\\', '/')
                        # Skip files that will be supplied by generated configs (e.g., runseg.sh, run_cmd.sh)
                        if rel_path in generated_paths:
                            continue
                        zf.write(abs_path, arcname=rel_path)

            # Add specified root files that exist (skip those provided as generated configs)
            for rf in include_root_files:
                rel_path = rf.replace('\\', '/')
                if rel_path in generated_paths:
                    continue
                if os.path.isfile(rf):
                    zf.write(rf, arcname=rel_path)

            # Finally, write generated configs (these overwrite any static ones by name)
            for path, content in configs.items():
                zf.writestr(path, content)

        mem_zip.seek(0)
        return send_file(
            mem_zip,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f"ParGaMD_full_WE_bundle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/load_config', methods=['POST'])
def load_config():
    """Load saved experiment configuration"""
    try:
        config_id = request.json['config_id']
        if config_id in experiment_configs:
            return jsonify({'success': True, 'config': experiment_configs[config_id]})
        else:
            return jsonify({'success': False, 'error': 'Configuration not found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/upload_files', methods=['POST'])
def upload_files():
    """Handle file uploads"""
    try:
        # Check which file is being uploaded
        if 'pdb_file' in request.files:
            file = request.files['pdb_file']
            file_type = 'pdb_file'
        elif 'prmtop_file' in request.files:
            file = request.files['prmtop_file']
            file_type = 'prmtop_file'
        else:
            return jsonify({'success': False, 'error': 'No file provided'})
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        return jsonify({
            'success': True,
            'file_path': file_path,
            'filename': filename,
            'file_type': file_type
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/setup_experiment', methods=['POST'])
def setup_experiment():
    return jsonify({'success': False, 'error': 'SSH/job submission temporarily disabled in this build'})
def monitor_jobs(*args, **kwargs):
    return

@app.route('/api/generate_config_preview', methods=['POST'])
def generate_config_preview():
    """Generate configuration file preview"""
    try:
        data = request.json
        filename = data['filename']
        params = data['params']
        # Map simple names to full template keys
        name_map = {
            'runseg.sh': 'westpa_scripts/runseg.sh',
            'run_cmd.sh': 'cMD/run_cmd.sh',
            'west.cfg': 'west.cfg',
            'env.sh': 'env.sh',
            'run_we.sh': 'run_we.sh',
        }
        key = name_map.get(filename, filename)

        # Render only requested file to avoid missing param errors
        tpls = config_generator.templates
        include_inf = bool(params.get('include_infinite_bounds', True))

        if key == 'west.cfg':
            nstlim = int(params.get('nstlim', 50000))
            ntpr = int(params.get('ntpr', 500)) or 1
            pcoord_len = (nstlim // ntpr) + 1
            pc1_bins = config_generator.generate_bin_boundaries(
                params.get('pc1_min', 0.0), params.get('pc1_max', 8.0), params.get('pc1_step', 0.2), include_inf
            )
            pc2_bins = config_generator.generate_bin_boundaries(
                params.get('pc2_min', 0.0), params.get('pc2_max', 8.0), params.get('pc2_step', 0.2), include_inf
            )
            content = tpls['west_cfg'].render(
                pcoord_len=pcoord_len,
                pc1_bins=pc1_bins,
                pc2_bins=pc2_bins,
                bin_target_counts=int(params.get('bin_target_counts', 4)),
                max_total_iterations=int(params.get('max_total_iterations', 1000))
            )
        elif key == 'env.sh':
            content = tpls['env_sh'].render()
        elif key == 'westpa_scripts/runseg.sh':
            content = tpls['runseg_sh'].render(
                protein_name=params.get('protein_name', 'protein'),
                enable_gpu_parallelization=bool(params.get('enable_gpu_parallelization', False))
            )
        elif key == 'cMD/run_cmd.sh':
            content = tpls['run_cmd_sh'].render(
                protein_name=params.get('protein_name', 'protein'),
                account=params.get('account', 'account'),
                email=params.get('email', 'user@example.com')
            )
        elif key == 'run_we.sh':
            content = tpls['run_we_sh'].render(
                protein_name=params.get('protein_name', 'protein'),
                account=params.get('account', 'account'),
                email=params.get('email', 'user@example.com')
            )
        else:
            return jsonify({'success': False, 'error': f'Configuration file {filename} not found'})

        return jsonify({'success': True, 'content': content})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get_job_status', methods=['POST'])
def get_job_status():
    return jsonify({'success': False, 'error': 'SSH/job submission disabled in this build'})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
