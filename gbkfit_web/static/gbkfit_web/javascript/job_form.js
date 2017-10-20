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
    $('body').on('change', '#id_dmodel_type',
        function() {
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
            }
        });

    // PSF hide/show fields on change.
    $('body').on('change', '#id_psf_type',
        function() {
            if ($('#id_psf_type').find(":selected").text() == 'moffat')
            {
                $('.div-beta').removeClass('hidden');
            }
            else{
                $('.div-beta').addClass('hidden');
            }
        });

    // LSF hide/show fields on change.
    $('body').on('change', '#id_lsf_type',
        function() {
            if ($('#id_lsf_type').find(":selected").text() == 'moffat')
            {
                $('.div-beta').removeClass('hidden');
            }
            else{
                $('.div-beta').addClass('hidden');
            }
        });

    // Fitter hide/show fields on change.
    $('.div-multinest').addClass('hidden');

    $('body').on('change', '#id_fitter_type',
        function() {
            if ($('#id_fitter_type').find(":selected").text() == 'mpfit')
            {
                $('.div-mpfit').removeClass('hidden');
                $('.div-multinest').addClass('hidden');
            }
            else{
                $('.div-mpfit').addClass('hidden');
                $('.div-multinest').removeClass('hidden');
            }
        });

    // Galaxy model change
    $('body').on('change', '#id_vel_profile',
        function() {
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
        });

//    $('body').on('click', '.nav li',
//        function() {
////            console.log($(this).attr('id').replace("li_", ""));
//            $.ajax({
//                 type:"POST",
//                 headers: { "X-CSRFToken": csrftoken},
//                 url:"/new_job/",
//                 data: {
//                    'active_tab': $(this).attr('id').replace("li_", "")
//                 }
//            });
//        });
});