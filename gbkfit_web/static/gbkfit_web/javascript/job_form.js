$(document).ready(function() {

    $('.has-popover').popover({'trigger':'hover'});

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

    // ParameterSet hide/show fields on change.
    check_xo_fixed_type();
    $('body').on('click', '#id_xo_fixed',
        function() {
            check_xo_fixed_type();
        });

    function check_xo_fixed_type() {
        var myElem = document.getElementById('id_xo_wrap');
        if (myElem === null) var hide_value = false;
        else var hide_value = true;
            // MPFIT
        if($('#id_xo_fixed').is(':checked')) {
            if (hide_value)
                $('.div-xo_value').removeClass('hidden');
            $('.div-xo_min').addClass('hidden');
            $('.div-xo_max').addClass('hidden');
            $('.div-xo_wrap').addClass('hidden');
            $('.div-xo_step').addClass('hidden');
            $('.div-xo_relstep').addClass('hidden');
            $('.div-xo_side').addClass('hidden');
        }
        else {
            if (hide_value)
                $('.div-xo_value').addClass('hidden');
            $('.div-xo_min').removeClass('hidden');
            $('.div-xo_max').removeClass('hidden');
            $('.div-xo_wrap').removeClass('hidden');
            $('.div-xo_step').removeClass('hidden');
            $('.div-xo_relstep').removeClass('hidden');
            $('.div-xo_side').removeClass('hidden');
        }
    }
    
    check_yo_fixed_type();
    $('body').on('click', '#id_yo_fixed',
        function() {
            check_yo_fixed_type();
        });

    function check_yo_fixed_type() {
        var myElem = document.getElementById('id_yo_wrap');
        if (myElem === null) var hide_value = false;
        else var hide_value = true;
            // MPFIT
        if($('#id_yo_fixed').is(':checked')) {
            if (hide_value)
                $('.div-yo_value').removeClass('hidden');
            $('.div-yo_min').addClass('hidden');
            $('.div-yo_max').addClass('hidden');
            $('.div-yo_wrap').addClass('hidden');
            $('.div-yo_step').addClass('hidden');
            $('.div-yo_relstep').addClass('hidden');
            $('.div-yo_side').addClass('hidden');
        }
        else {
            if (hide_value)
                $('.div-yo_value').addClass('hidden');
            $('.div-yo_min').removeClass('hidden');
            $('.div-yo_max').removeClass('hidden');
            $('.div-yo_wrap').removeClass('hidden');
            $('.div-yo_step').removeClass('hidden');
            $('.div-yo_relstep').removeClass('hidden');
            $('.div-yo_side').removeClass('hidden');
        }
    }
    
    check_pa_fixed_type();
    $('body').on('click', '#id_pa_fixed',
        function() {
            check_pa_fixed_type();
        });

    function check_pa_fixed_type() {
        var myElem = document.getElementById('id_pa_wrap');
        if (myElem === null) var hide_value = false;
        else var hide_value = true;
            // MPFIT
        if($('#id_pa_fixed').is(':checked')) {
            if (hide_value)
                $('.div-pa_value').removeClass('hidden');
            $('.div-pa_min').addClass('hidden');
            $('.div-pa_max').addClass('hidden');
            $('.div-pa_wrap').addClass('hidden');
            $('.div-pa_step').addClass('hidden');
            $('.div-pa_relstep').addClass('hidden');
            $('.div-pa_side').addClass('hidden');
        }
        else {
            if (hide_value)
                $('.div-pa_value').addClass('hidden');
            $('.div-pa_min').removeClass('hidden');
            $('.div-pa_max').removeClass('hidden');
            $('.div-pa_wrap').removeClass('hidden');
            $('.div-pa_step').removeClass('hidden');
            $('.div-pa_relstep').removeClass('hidden');
            $('.div-pa_side').removeClass('hidden');
        }
    }
    
    check_incl_fixed_type();
    $('body').on('click', '#id_incl_fixed',
        function() {
            check_incl_fixed_type();
        });

    function check_incl_fixed_type() {
        var myElem = document.getElementById('id_incl_wrap');
        if (myElem === null) var hide_value = false;
        else var hide_value = true;
            // MPFIT
        if($('#id_incl_fixed').is(':checked')) {
            if (hide_value)
                $('.div-incl_value').removeClass('hidden');
            $('.div-incl_min').addClass('hidden');
            $('.div-incl_max').addClass('hidden');
            $('.div-incl_wrap').addClass('hidden');
            $('.div-incl_step').addClass('hidden');
            $('.div-incl_relstep').addClass('hidden');
            $('.div-incl_side').addClass('hidden');
        }
        else {
            if (hide_value)
                $('.div-incl_value').addClass('hidden');
            $('.div-incl_min').removeClass('hidden');
            $('.div-incl_max').removeClass('hidden');
            $('.div-incl_wrap').removeClass('hidden');
            $('.div-incl_step').removeClass('hidden');
            $('.div-incl_relstep').removeClass('hidden');
            $('.div-incl_side').removeClass('hidden');
        }
    }
    
    check_vsys_fixed_type();
    $('body').on('click', '#id_vsys_fixed',
        function() {
            check_vsys_fixed_type();
        });

    function check_vsys_fixed_type() {
        var myElem = document.getElementById('id_vsys_wrap');
        if (myElem === null) var hide_value = false;
        else var hide_value = true;
            // MPFIT
        if($('#id_vsys_fixed').is(':checked')) {
            if (hide_value)
                $('.div-vsys_value').removeClass('hidden');
            $('.div-vsys_min').addClass('hidden');
            $('.div-vsys_max').addClass('hidden');
            $('.div-vsys_wrap').addClass('hidden');
            $('.div-vsys_step').addClass('hidden');
            $('.div-vsys_relstep').addClass('hidden');
            $('.div-vsys_side').addClass('hidden');
        }
        else {
            if (hide_value)
                $('.div-vsys_value').addClass('hidden');
            $('.div-vsys_min').removeClass('hidden');
            $('.div-vsys_max').removeClass('hidden');
            $('.div-vsys_wrap').removeClass('hidden');
            $('.div-vsys_step').removeClass('hidden');
            $('.div-vsys_relstep').removeClass('hidden');
            $('.div-vsys_side').removeClass('hidden');
        }
    }
    
    check_vsig_fixed_type();
    $('body').on('click', '#id_vsig_fixed',
        function() {
            check_vsig_fixed_type();
        });

    function check_vsig_fixed_type() {
        var myElem = document.getElementById('id_vsig_wrap');
        if (myElem === null) var hide_value = false;
        else var hide_value = true;
            // MPFIT
        if($('#id_vsig_fixed').is(':checked')) {
            if (hide_value)
                $('.div-vsig_value').removeClass('hidden');
            $('.div-vsig_min').addClass('hidden');
            $('.div-vsig_max').addClass('hidden');
            $('.div-vsig_wrap').addClass('hidden');
            $('.div-vsig_step').addClass('hidden');
            $('.div-vsig_relstep').addClass('hidden');
            $('.div-vsig_side').addClass('hidden');
        }
        else {
            if (hide_value)
                $('.div-vsig_value').addClass('hidden');
            $('.div-vsig_min').removeClass('hidden');
            $('.div-vsig_max').removeClass('hidden');
            $('.div-vsig_wrap').removeClass('hidden');
            $('.div-vsig_step').removeClass('hidden');
            $('.div-vsig_relstep').removeClass('hidden');
            $('.div-vsig_side').removeClass('hidden');
        }
    }
    
    check_i0_fixed_type();
    $('body').on('click', '#id_i0_fixed',
        function() {
            check_i0_fixed_type();
        });

    function check_i0_fixed_type() {
        var myElem = document.getElementById('id_i0_wrap');
        if (myElem === null) var hide_value = false;
        else var hide_value = true;
            // MPFIT
        if($('#id_i0_fixed').is(':checked')) {
            if (hide_value)
                $('.div-i0_value').removeClass('hidden');
            $('.div-i0_min').addClass('hidden');
            $('.div-i0_max').addClass('hidden');
            $('.div-i0_wrap').addClass('hidden');
            $('.div-i0_step').addClass('hidden');
            $('.div-i0_relstep').addClass('hidden');
            $('.div-i0_side').addClass('hidden');
        }
        else {
            if (hide_value)
                $('.div-i0_value').addClass('hidden');
            $('.div-i0_min').removeClass('hidden');
            $('.div-i0_max').removeClass('hidden');
            $('.div-i0_wrap').removeClass('hidden');
            $('.div-i0_step').removeClass('hidden');
            $('.div-i0_relstep').removeClass('hidden');
            $('.div-i0_side').removeClass('hidden');
        }
    }
    
    check_r0_fixed_type();
    $('body').on('click', '#id_r0_fixed',
        function() {
            check_r0_fixed_type();
        });

    function check_r0_fixed_type() {
        var myElem = document.getElementById('id_r0_wrap');
        if (myElem === null) var hide_value = false;
        else var hide_value = true;
            // MPFIT
        if($('#id_r0_fixed').is(':checked')) {
            if (hide_value)
                $('.div-r0_value').removeClass('hidden');
            $('.div-r0_min').addClass('hidden');
            $('.div-r0_max').addClass('hidden');
            $('.div-r0_wrap').addClass('hidden');
            $('.div-r0_step').addClass('hidden');
            $('.div-r0_relstep').addClass('hidden');
            $('.div-r0_side').addClass('hidden');
        }
        else {
            if (hide_value)
                $('.div-r0_value').addClass('hidden');
            $('.div-r0_min').removeClass('hidden');
            $('.div-r0_max').removeClass('hidden');
            $('.div-r0_wrap').removeClass('hidden');
            $('.div-r0_step').removeClass('hidden');
            $('.div-r0_relstep').removeClass('hidden');
            $('.div-r0_side').removeClass('hidden');
        }
    }
    
    check_rt_fixed_type();
    $('body').on('click', '#id_rt_fixed',
        function() {
            check_rt_fixed_type();
        });

    function check_rt_fixed_type() {
        var myElem = document.getElementById('id_rt_wrap');
        if (myElem === null) var hide_value = false;
        else var hide_value = true;
            // MPFIT
        if($('#id_rt_fixed').is(':checked')) {
            if (hide_value)
                $('.div-rt_value').removeClass('hidden');
            $('.div-rt_min').addClass('hidden');
            $('.div-rt_max').addClass('hidden');
            $('.div-rt_wrap').addClass('hidden');
            $('.div-rt_step').addClass('hidden');
            $('.div-rt_relstep').addClass('hidden');
            $('.div-rt_side').addClass('hidden');
        }
        else {
            if (hide_value)
                $('.div-rt_value').addClass('hidden');
            $('.div-rt_min').removeClass('hidden');
            $('.div-rt_max').removeClass('hidden');
            $('.div-rt_wrap').removeClass('hidden');
            $('.div-rt_step').removeClass('hidden');
            $('.div-rt_relstep').removeClass('hidden');
            $('.div-rt_side').removeClass('hidden');
        }
    }
    
    check_vt_fixed_type();
    $('body').on('click', '#id_vt_fixed',
        function() {
            check_vt_fixed_type();
        });

    function check_vt_fixed_type() {
        var myElem = document.getElementById('id_vt_wrap');
        if (myElem === null) var hide_value = false;
        else var hide_value = true;
            // MPFIT
        if($('#id_vt_fixed').is(':checked')) {
            if (hide_value)
                $('.div-vt_value').removeClass('hidden');
            $('.div-vt_min').addClass('hidden');
            $('.div-vt_max').addClass('hidden');
            $('.div-vt_wrap').addClass('hidden');
            $('.div-vt_step').addClass('hidden');
            $('.div-vt_relstep').addClass('hidden');
            $('.div-vt_side').addClass('hidden');
        }
        else {
            if (hide_value)
                $('.div-vt_value').addClass('hidden');
            $('.div-vt_min').removeClass('hidden');
            $('.div-vt_max').removeClass('hidden');
            $('.div-vt_wrap').removeClass('hidden');
            $('.div-vt_step').removeClass('hidden');
            $('.div-vt_relstep').removeClass('hidden');
            $('.div-vt_side').removeClass('hidden');
        }
    }
    
    check_a_fixed_type();
    $('body').on('click', '#id_a_fixed',
        function() {
            check_a_fixed_type();
        });

    function check_a_fixed_type() {
        var myElem = document.getElementById('id_a_wrap');
        if (myElem === null) var hide_value = false;
        else var hide_value = true;
            // MPFIT
        if($('#id_a_fixed').is(':checked')) {
            if (hide_value)
                $('.div-a_value').removeClass('hidden');
            $('.div-a_min').addClass('hidden');
            $('.div-a_max').addClass('hidden');
            $('.div-a_wrap').addClass('hidden');
            $('.div-a_step').addClass('hidden');
            $('.div-a_relstep').addClass('hidden');
            $('.div-a_side').addClass('hidden');
        }
        else {
            if (hide_value)
                $('.div-a_value').addClass('hidden');
            $('.div-a_min').removeClass('hidden');
            $('.div-a_max').removeClass('hidden');
            $('.div-a_wrap').removeClass('hidden');
            $('.div-a_step').removeClass('hidden');
            $('.div-a_relstep').removeClass('hidden');
            $('.div-a_side').removeClass('hidden');
        }
    }

    check_b_fixed_type();
    $('body').on('click', '#id_b_fixed',
        function() {
            check_b_fixed_type();
        });

    function check_b_fixed_type() {
        var myElem = document.getElementById('id_b_wrap');
        if (myElem === null) var hide_value = false;
        else var hide_value = true;
            // MPFIT
        if($('#id_b_fixed').is(':checked')) {
            if (hide_value)
                $('.div-b_value').removeClass('hidden');
            $('.div-b_min').addClass('hidden');
            $('.div-b_max').addClass('hidden');
            $('.div-b_wrap').addClass('hidden');
            $('.div-b_step').addClass('hidden');
            $('.div-b_relstep').addClass('hidden');
            $('.div-b_side').addClass('hidden');
        }
        else {
            if (hide_value)
                $('.div-b_value').addClass('hidden');
            $('.div-b_min').removeClass('hidden');
            $('.div-b_max').removeClass('hidden');
            $('.div-b_wrap').removeClass('hidden');
            $('.div-b_step').removeClass('hidden');
            $('.div-b_relstep').removeClass('hidden');
            $('.div-b_side').removeClass('hidden');
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