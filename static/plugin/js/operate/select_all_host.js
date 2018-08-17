;$(function () {
    $('#checkAll').on('click',function () {
        if($(this).prop("checked")){
            $('table tbody').find('input').prop('checked',true)
        }else{
            $('table tbody').find('input').prop('checked',false)
        }
    })
    $('tbody input[type="checkbox"]').on('click',function () {
        if($(this).prop('checked')){
            $(this).attr('check','yes');
            if($( 'tbody input[check="yes"]').length ===$('tbody input[type="checkbox"]').length){
                $('#checkAll').prop('checked',true);
            }else{
                $('#checkAll').prop('checked',false);
            }
        }else{
            $(this).removeAttr('check');
            $('#checkAll').prop('checked',false);
        }
    });
})