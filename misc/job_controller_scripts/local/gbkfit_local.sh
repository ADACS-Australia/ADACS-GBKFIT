#!/bin/bash

# Make sure the output directory exists
mkdir -p %(job_output_directory)s

# Start gbkfit with the specified parameter file and output location
set +e
LD_LIBRARY_PATH=/home/lewis/gbkfit/bin/lib ~/gbkfit/bin/bin/gbkfit_app_cli --config %(job_parameter_file)s --output %(job_output_directory)s
ret_code=$?
set -e

# Activate the image generation venv
. /home/lewis/gbkfit/bin/make_image/venv/bin/activate

# Generate the images
python /home/lewis/gbkfit/bin/make_image/make_image.py %(working_directory)s

# Finally tar up all output in to one file
tar cf gbkfit_job_%(ui_job_id)d.tar.gz *

# Return the original result from gbkfit
exit $ret_code