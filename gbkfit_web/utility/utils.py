#==============================================================================
#
# This code was developed as part of the Astronomy Data and Computing Services
# (ADACS; https:#adacs.org.au) 2017B Software Support program.
#
# Written by: Dany Vohl, Lewis Lakerink, Shibli Saleheen
# Date:       December 2017
#
# It is distributed under the MIT (Expat) License (see https:#opensource.org/):
#
# Copyright (c) 2017 Astronomy Data and Computing Services (ADACS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#==============================================================================

import base64
import logging

from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from six.moves.urllib.parse import quote_plus, unquote_plus, parse_qsl

from os import path, makedirs

logger = logging.getLogger(__name__)


def url_quote(raw):
    utf8 = quote_plus(raw).encode('utf8')
    return base64.b16encode(utf8).decode('utf8')


def url_unquote(enc):
    unquoted = unquote_plus(base64.b16decode(enc).decode('utf8'))
    return unquoted


def get_absolute_site_url(request=None):
    """
    Finds the site url that will be used to generate links
    :param request: A Django request object
    :return: String of the absolute url
    """

    # check whether forcefully using a specific url from the settings
    if settings.SITE_URL != '':
        return settings.SITE_URL

    # If no request, an absolute url cannot be generated
    if not request:
        return None

    # find the site name and protocol
    site_name = request.get_host()
    if request.is_secure():
        protocol = 'https'
    else:
        try:
            # Look for protocol forcefully defined in the settings
            protocol = settings.HTTP_PROTOCOL
        except AttributeError:
            protocol = 'http'
    return protocol + '://' + site_name


def get_token(information, validity=None):
    """
    Stores the information in the database and generates a corresponding token
    :param information: information that needs to be stored and corresponding token to be generated
    :param validity: for how long the token will be valid (in seconds)
    :return: token to be encoded in the url
    """
    if validity:
        now = timezone.localtime(timezone.now())
        expiry = now + timedelta(seconds=validity)
    else:
        expiry = None
    try:
        from gbkfit_web.models import Verification
        verification = Verification.objects.create(information=information, expiry=expiry)
        return url_quote('id=' + verification.id.__str__())
    except:
        logger.info("Failure generating Verification token with {}".format(information))
        raise


def get_information(token):
    """
    Retrieves the information from the database for a particular token

    :param token: encoded token from email
    :return: the actual information
    """
    now = timezone.localtime(timezone.now())
    try:
        params = dict(parse_qsl(url_unquote(token)))
        from gbkfit_web.models import Verification
        verification = Verification.objects.get(id=params.get('id'), expiry__gte=now)
        if verification.verified:
            raise ValueError('Already verified')
        else:
            verification.verified = True
            verification.save()
        return verification.information
    except Verification.DoesNotExist:
        raise ValueError('Invalid or expired verification code')
    except Exception as e:
        logger.exception(e)  # should notify admins via email
        raise

def check_path(my_path):
    """
    Check if path ends with a slash ('/'). Else, it adds it.

    :param path: path
    :return: functional path
    """
    if len(my_path) > 0 and my_path[-1] != '/':
        my_path = my_path + '/'

    if not path.exists(path):
        makedirs(path)

    return path

def set_dict_indices(my_array):
    """
    Creates a dictionary based on values in my_array, and links each of them to an indice.

    :param my_array: An array (e.g. [a,b,c])
    :return: A dictionary (e.g. {a:0, b:1, c:2})
    """
    my_dict = {}
    i = 0
    for value in my_array:
        my_dict[value] = i
        i += 1

    return my_dict

def make_image(job_json, result_json, data_file, mask_file, model_file, residual_file, output_file):
    """
    Modified version of code provided by George. Not yet tested.

    :param job_json: json file used to launch gbkfit_app_cli
    :param result_json: resulting json file generated by gbkfit_app_cli
    :param data_file: data fits file outputed by gbkfit_app_cli
    :param mask_file: mask fits file outputed by gbkfit_app_cli
    :param model_file: model fits file outputed by gbkfit_app_cli
    :param residual_file: residual fits file outputed by gbkfit_app_cli
    :param output_file: output image file
    :return: nothing.
    """
    import json
    import math
    import numpy as np
    from astropy.io import fits
    from matplotlib import pyplot as plt
    from matplotlib import rc
    from matplotlib import gridspec
    from matplotlib import patches
    from mpl_toolkits.axes_grid1 import inset_locator

    rc('font', size=12)
    rc('axes', titlesize=14)
    rc('axes', labelsize=14)

    # Figure constants
    FIG_FILE_DPI = 150
    FIG_PLOT_DPI = 150
    FIG_SIZE_UNIT = 1.0
    FIG_SIZE_X = 9.5
    FIG_SIZE_Y = 6.0
    CBAR_AXES_LABEL_FONT_SIZE = FIG_SIZE_UNIT * 20.0
    CBAR_AXES_TICKS_FONT_SIZE = FIG_SIZE_UNIT * 22.0
    SUBPLOT_TITLE_FONT_SIZE = FIG_SIZE_UNIT * 32.0

    # Read configuration file. It assumes that it is located in the results-dir.
    config = json.load(open(job_json), 'r')
    psf_fwhm_x = config['psf']['fwhm_x']
    psf_fwhm_y = config['psf']['fwhm_y']
    psf_pa = config['psf']['pa']
    step_x = config['dmodel']['step'][0]
    step_y = config['dmodel']['step'][1]

    # Read results file. It assumes that it is located in the results results-dir.
    vsys = None
    results = json.load(open(result_json), 'r')
    params = results['modes'][0]['parameters']
    for param in params:
        if param['name'] == 'vsys':
            vsys = param['value']

    # Load data, model, and residual maps
    map_dat = fits.getdata(data_file)
    map_msk = fits.getdata(mask_file)
    map_mdl = fits.getdata(model_file)
    map_res = fits.getdata(residual_file)


    # Crop the unused space around the data.
    # This is an optional step to improve the clarity of the figure.
    # Currently this is tailored for the SAMI data and it is blindly cropping pixels.
    # A better solution would be to use the mask images and decide where to crop.
    # TODO: crop.
    # map_dat = map_dat[5:45, 5:45]
    # map_msk = map_msk[5:45, 5:45]
    # map_mdl = map_mdl[5:45, 5:45]
    # map_res = map_res[5:45, 5:45]

    # Remove velocity offset completely
    map_dat -= vsys
    map_mdl -= vsys

    # Apply mask to model maps
    map_mdl[np.where(map_msk == 0)] = np.NaN

    # Calculate absolute min/max
    map_max = np.nanmax(np.fabs(map_mdl)) * 1.05
    map_max = int(math.ceil(map_max / 10.0)) * 10
    map_min = -map_max

    # Create main figure
    fig = plt.figure(figsize=(FIG_SIZE_X, FIG_SIZE_Y), dpi=FIG_PLOT_DPI)

    # Setup grid
    gs = gridspec.GridSpec(1, 4, wspace=0.0, hspace=0.0, height_ratios=[10], width_ratios=[10, 10, 10, 1])

    # Setup axes
    ax00 = fig.add_subplot(gs[0])
    ax01 = fig.add_subplot(gs[1])
    ax02 = fig.add_subplot(gs[2])
    ax03 = fig.add_subplot(gs[3])

    ax03.set_frame_on(False)
    ax03.patch.set_visible(False)
    ax03.get_xaxis().set_ticks([])
    ax03.get_yaxis().set_ticks([])

    ax00.tick_params(labelbottom=False, labelleft=False, labelright=False)
    ax01.tick_params(labelbottom=False, labelleft=False, labelright=False)
    ax02.tick_params(labelbottom=False, labelleft=False, labelright=False)
    ax03.tick_params(labelbottom=False, labelleft=False, labelright=False)

    data_size_x = map_dat.shape[1]
    data_size_y = map_dat.shape[0]

    ax00.set_xticks([0.25 * data_size_x, 0.5 * data_size_x, 0.75 * data_size_x])
    ax01.set_xticks([0.25 * data_size_x, 0.5 * data_size_x, 0.75 * data_size_x])
    ax02.set_xticks([0.25 * data_size_x, 0.5 * data_size_x, 0.75 * data_size_x])

    ax00.set_yticks([0.25 * data_size_y, 0.5 * data_size_y, 0.75 * data_size_y])
    ax01.set_yticks([0.25 * data_size_y, 0.5 * data_size_y, 0.75 * data_size_y])
    ax02.set_yticks([0.25 * data_size_y, 0.5 * data_size_y, 0.75 * data_size_y])

    cmap = 'RdBu_r'
    im00 = ax00.imshow(map_dat, aspect='auto', interpolation='none', cmap=cmap, vmin=map_min, vmax=map_max)
    im01 = ax01.imshow(map_mdl, aspect='auto', interpolation='none', cmap=cmap, vmin=map_min, vmax=map_max)
    im02 = ax02.imshow(map_res, aspect='auto', interpolation='none', cmap=cmap, vmin=map_min, vmax=map_max)

    ax00.invert_yaxis()
    ax01.invert_yaxis()
    ax02.invert_yaxis()

    # Add column titles
    ax00.set_title(r'\textbf{Data}', fontsize=SUBPLOT_TITLE_FONT_SIZE)
    ax01.set_title(r'\textbf{Model}', fontsize=SUBPLOT_TITLE_FONT_SIZE)
    ax02.set_title(r'\textbf{Residual}', fontsize=SUBPLOT_TITLE_FONT_SIZE)

    # Add row titles
    ax00.set_ylabel('Velocity', fontsize=SUBPLOT_TITLE_FONT_SIZE)

    # Setup color bars
    # Yes, the code is too comples for just a color bar.
    # I was trying to make it look pretty. :)
    cax0 = inset_locator.inset_axes(
        ax03,
        width='100%',
        height='90%',
        loc=5,
        bbox_to_anchor=(0.0, 0.0, 1.0, 1.0),
        bbox_transform=ax03.transAxes,
        borderpad=0)

    fig.colorbar(im01, cax=cax0, orientation='vertical')
    cax0.set_ylabel('km~s$^{-1}$', fontsize=CBAR_AXES_LABEL_FONT_SIZE)
    cax0.yaxis.set_label_coords(3.4, 0.5)
    cax0.tick_params(labelsize=CBAR_AXES_TICKS_FONT_SIZE)

    # Setup PSF patches
    psf_patch_size_x = psf_fwhm_x / step_x
    psf_patch_size_y = psf_fwhm_y / step_y
    psf_patch_position = (psf_patch_size_x / 2, psf_patch_size_y / 2)
    psf_patch_angle = psf_pa
    psf_patch_0 = patches.Ellipse(psf_patch_position, psf_patch_size_x, psf_patch_size_y, psf_patch_angle,
                                  color='0.50', alpha=0.5)

    ax00.add_artist(psf_patch_0)

    fig.savefig(output_file, bbox_inches='tight', dpi=FIG_FILE_DPI)


def file_to_b64(file_path):
    return base64.b64encode(open(file_path, 'rb').read()).decode('ascii')
