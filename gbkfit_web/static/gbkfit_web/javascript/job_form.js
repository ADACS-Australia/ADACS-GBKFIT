$(document).ready(function() {

    // Job start hide/show job name field:
    $('#id_name').addClass('form-control');
    $('body').on('change', '#id_job',
        function() {
            if ($('#id_job').find(":selected").text() != 'New')
            {
                $('.div-job_name').addClass('hidden');
            }
            else{
                $('.div-job_name').removeClass('hidden');
            }
        });

    // DModel hide/show fields on change.
    check_dmodel_type();
    $('body').on('change', '#id_dmodel_type',
        function() {
            check_dmodel_type();
        });

    function check_dmodel_type() {
        if ($('#id_dmodel_type').find(":selected").text() == 'mmnt_omp' ||
            $('#id_dmodel_type').find(":selected").text() == 'mmnt_cuda' ||
            $('#id_dmodel_type').find(":selected").text() == 'mmaps_omp' ||
            $('#id_dmodel_type').find(":selected").text() == 'mmaps_cuda')
        {
            $('.div-method').removeClass('hidden');
            $('.div-step_z').addClass('hidden');
            $('.div-scale_z').addClass('hidden');
        }
        else{
            $('.div-method').addClass('hidden');
            $('.div-step_z').removeClass('hidden');
            $('.div-scale_z').removeClass('hidden')
        };
    }

    // PSF hide/show fields on change.
    check_psf_type();
    $('body').on('change', '#id_psf_type',
        function() {
            check_psf_type();
        });

    function check_psf_type() {
        if ($('#id_psf_type').find(":selected").text() == 'moffat')
        {
            $('.div-beta').removeClass('hidden');
        }
        else{
            $('.div-beta').addClass('hidden');
        }
    }

    // LSF hide/show fields on change.
    check_lsf_type();
    $('body').on('change', '#id_lsf_type',
        function() {
            check_lsf_type();
        });

    function check_lsf_type() {
        if ($('#id_lsf_type').find(":selected").text() == 'moffat')
        {
            $('.div-beta').removeClass('hidden');
        }
        else{
            $('.div-beta').addClass('hidden');
        }
    }

    // Fitter hide/show fields on change.
    check_fitter_type();
    $('body').on('change', '#id_fitter_type',
        function() {
            check_fitter_type();
        });

    function check_fitter_type() {
        if ($('#id_fitter_type').find(":selected").text() == 'mpfit') {
            $('.div-mpfit').removeClass('hidden');
            $('.div-multinest').addClass('hidden');
        }
        else{
            $('.div-mpfit').addClass('hidden');
            $('.div-multinest').removeClass('hidden');
        };
    }

    // Galaxy model change
    check_vel_profile();
    $('body').on('change', '#id_vel_profile',
        function() {
           check_vel_profile();
        });

    function check_vel_profile() {
        if ($('#id_vel_profile').find(":selected").text() == 'exponential')
        {
            $('.div-rt_flat').addClass('hidden');
            $('.div-vt_flat').addClass('hidden');

            $('.div-rt_boissier').addClass('hidden');
            $('.div-vt_boissier').addClass('hidden');

            $('.div-rt_arctan').addClass('hidden');
            $('.div-vt_arctan').addClass('hidden');

            $('.div-rt_epinat').addClass('hidden');
            $('.div-vt_epinat').addClass('hidden');
            $('.div-a_epinat').addClass('hidden');
            $('.div-b_epinat').addClass('hidden');
        }

        if ($('#id_vel_profile').find(":selected").text() == 'flat')
        {
            $('.div-rt_flat').removeClass('hidden');
            $('.div-vt_flat').removeClass('hidden');

            $('.div-rt_boissier').addClass('hidden');
            $('.div-vt_boissier').addClass('hidden');

            $('.div-rt_arctan').addClass('hidden');
            $('.div-vt_arctan').addClass('hidden');

            $('.div-rt_epinat').addClass('hidden');
            $('.div-vt_epinat').addClass('hidden');
            $('.div-a_epinat').addClass('hidden');
            $('.div-b_epinat').addClass('hidden');
        }

        if ($('#id_vel_profile').find(":selected").text() == 'boissier') {
            $('.div-rt_flat').addClass('hidden');
            $('.div-vt_flat').addClass('hidden');

            $('.div-rt_boissier').removeClass('hidden');
            $('.div-vt_boissier').removeClass('hidden');

            $('.div-rt_arctan').addClass('hidden');
            $('.div-vt_arctan').addClass('hidden');

            $('.div-rt_epinat').addClass('hidden');
            $('.div-vt_epinat').addClass('hidden');
            $('.div-a_epinat').addClass('hidden');
            $('.div-b_epinat').addClass('hidden');
        }

        if ($('#id_vel_profile').find(":selected").text() == 'arctan') {
            $('.div-rt_flat').addClass('hidden');
            $('.div-vt_flat').addClass('hidden');

            $('.div-rt_boissier').addClass('hidden');
            $('.div-vt_boissier').addClass('hidden');

            $('.div-rt_arctan').removeClass('hidden');
            $('.div-vt_arctan').removeClass('hidden');

            $('.div-rt_epinat').addClass('hidden');
            $('.div-vt_epinat').addClass('hidden');
            $('.div-a_epinat').addClass('hidden');
            $('.div-b_epinat').addClass('hidden');
        }

        if ($('#id_vel_profile').find(":selected").text() == 'epinat') {
            $('.div-rt_flat').addClass('hidden');
            $('.div-vt_flat').addClass('hidden');

            $('.div-rt_boissier').addClass('hidden');
            $('.div-vt_boissier').addClass('hidden');

            $('.div-rt_arctan').addClass('hidden');
            $('.div-vt_arctan').addClass('hidden');

            $('.div-rt_epinat').removeClass('hidden');
            $('.div-vt_epinat').removeClass('hidden');
            $('.div-a_epinat').removeClass('hidden');
            $('.div-b_epinat').removeClass('hidden');
        }
    }

    // Confirm job deletion
    $('body').on('click', '.delete_job',
        function(e) {
            var $a_job = $(this.id);

            console.log(this.id);
            console.log($(this));
            var $job_id = $(this).job_id;

//            var $form = $(this).closest('form');
            e.preventDefault();
            $('#confirm').modal({
              backdrop: 'static',
              keyboard: false
            })
            .one('click', '#delete', function(e) {
                $a_job.trigger();
            });
        });


    // Delete a job
    $('body').on('click', '.delete_job',
        function() {
            var job_id = $(this).attr('job_id');
            var job_name = $(this).attr('job_name');

            bootbox.confirm({
                title: "Delete Job " + job_id + "?",
                message: "Do you want to delete Job " + job_id + ": `" + job_name + "'?",
                buttons: {
                    cancel: {
                        label: '<i class="fa fa-times"></i> Cancel'
                    },
                    confirm: {
                        label: '<i class="fa fa-check"></i> Confirm'
                    }
                },
                callback: function (result) {
                    if (result == true) {
                        $.ajax({
                            type: "POST",
                            url: "/jobs/" + job_id + "/delete",
                            data: {
                                csrfmiddlewaretoken: csrftoken,
                                id: job_id,
                                name: job_name
                            },
                            dataType: "json",
                            success: function(response){
                                $( "#table_jobs" ).load( "/jobs/ #table_jobs" );
                            }
                        });
                    }
                }
            });
        });

});