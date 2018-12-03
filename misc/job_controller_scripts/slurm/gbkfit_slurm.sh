#!/bin/bash
#SBATCH -o slurm-%%j.out
#SBATCH -e slurm-%%j.err
#SBATCH --nodes=%(nodes)d
#SBATCH --ntasks-per-node=%(tasks_per_node)d
#SBATCH --mem-per-cpu=%(mem)dM
#SBATCH --time=%(wt_hours)02d:%(wt_minutes)02d:%(wt_seconds)02d
#SBATCH --job-name=%(job_name)s

# Load GBKFit required modules
module load gnu/2018.0
module load boost/1.67.0-python-2.7.14
module load cfitsio/3.450
module load multinest/3.10
module load cuda/9.2.88

# Make sure the output directory exists
mkdir -p %(job_output_directory)s

# Start gbkfit with the specified parameter file and output location
set +e
/fred/oz075/gbkfit/gbkfit/bin/gbkfit_app_cli --config %(job_parameter_file)s --output %(job_output_directory)s
ret_code=$?
set -e

# Load python 2 module for running the make image script
module load python/2.7.14

# Activate the image generation venv
. /fred/oz075/gbkfit/make_image/venv/bin/activate

# Generate the images
python /fred/oz075/gbkfit/make_image/make_image.py %(working_directory)s

# Finally tar up all output in to one file
tar cf gbkfit_job_%(ui_job_id)d.tar.gz *

# Return the original result from gbkfit
exit $ret_code