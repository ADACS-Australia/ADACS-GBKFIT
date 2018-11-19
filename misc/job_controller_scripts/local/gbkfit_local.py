import base64
import json
import logging
import os
import shutil
import uuid

from scheduler.local import Local


class Gbkfit(Local):
    def __init__(self, settings, ui_id, job_id):
        """
        Initialises the local scheduler class for Gbkfit

        :param settings: The settings from settings.py
        :param ui_id: The UI id of the job
        :param job_id: The Slurm id of the Job
        """
        # Call the original constructor
        super().__init__(settings, ui_id, job_id)

        # Set the local template
        self.local_template = 'settings/gbkfit_local.sh'
        # Set our job parameter path
        self.job_parameter_file = os.path.join(self.get_working_directory(), 'json_params.json')
        # Set the job output directory
        self.job_output_directory = os.path.join(self.get_working_directory(), 'output')
        # Set the job input file directory
        self.job_input_directory = os.path.join(self.get_working_directory(), 'input')

    def generate_template_dict(self):
        """
        Called before a job is submitted before writing the local script

        We add in our custom local arguments

        :return: A dict of key/value pairs used in the local script template
        """
        # Get the existing parameters
        params = super().generate_template_dict()

        # Add our custom parameters
        params['job_parameter_file'] = self.job_parameter_file
        params['job_output_directory'] = self.job_output_directory
        params['working_directory'] = self.get_working_directory()

        # Return the updated params
        return params

    def submit(self, job_parameters):
        """
        Called when a job is submitted

        :param job_parameters: The parameters for this job, this is a string representing a json dump
        :return: The super call return to submit
        """

        # First we have to iterate over each dataset in the job parameters as they are sent as base64 encoded blobs,
        # then save them to their respective location
        # Iterate over the datasets
        for dataset in job_parameters['datasets']:
            # Get the dataset type
            dtype = dataset['type']
            # Get the output filename
            filename = os.path.join(self.job_input_directory, dtype, 'data', dataset['data']['filename'])
            # Decode the data
            filedata = base64.b64decode(dataset['data']['data'])
            # Save the data
            logging.info("Saving data file for {} to {}...".format(dtype, filename))
            os.makedirs(os.path.dirname(filename), 0o770, True)
            open(filename, 'wb').write(filedata)
            # Update the parameters with the path to the data file
            dataset['data'] = filename

            # Check if there is an error dataset
            if 'error' in dataset:
                # Get the output filename
                filename = os.path.join(self.job_input_directory, dtype, 'error', dataset['error']['filename'])
                # Decode the data
                filedata = base64.b64decode(dataset['error']['data'])
                # Save the data
                logging.info("Saving error file for {} to {}...".format(dtype, filename))
                os.makedirs(os.path.dirname(filename), 0o770, True)
                open(filename, 'wb').write(filedata)
                # Update the parameters with the path to the data file
                dataset['error'] = filename

            # Check if there is a mask dataset
            if 'mask' in dataset:
                # Get the output filename
                filename = os.path.join(self.job_input_directory, dtype, 'mask', dataset['mask']['filename'])
                # Decode the data
                filedata = base64.b64decode(dataset['mask']['data'])
                # Save the data
                logging.info("Saving mask file for {} to {}...".format(dtype, filename))
                os.makedirs(os.path.dirname(filename), 0o770, True)
                open(filename, 'wb').write(filedata)
                # Update the parameters with the path to the data file
                dataset['mask'] = filename

        logging.info(job_parameters)

        # Write the job parameters to a file
        json.dump(job_parameters, open(self.job_parameter_file, 'w'))

        # Run the job
        return super().submit(job_parameters)