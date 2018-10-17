$(function () {
    function initTableCheckbox() {
        var $thr = $("#func_table thead tr");
        var $checkAllTh = $('<th><input type="checkbox" id="checkAll" name="checkAll"/></th>');
        $thr.prepend($checkAllTh);
        var $checkAll = $thr.find("input");
        $checkAll.click(function(event){
            $tbr.find('input').prop('checked',$(this).prop('checked'));
            if($(this).prop('checked')) {
                $tbr.find('input').parent().parent().addClass("warning");
            }else {
                $tbr.find('input').parent().parent().removeClass("warning");
            }
            event.stopPropagation();
        });
        $checkAllTh.click(function () {
            $(this).find('input').click();
        });
        var $tbr = $('#func_table tbody tr');
        var checkItemId = $('<td><input type="checkbox" name="checkItem"/></td>');
        $tbr.prepend(checkItemId);
        $tbr.find('input').click(function (event) {
            $(this).parent().parent().toggleClass("warning");
            $checkAllTh.prop('checked',$tbr.find('input:checked').length == $tbr.length ? true : false);
            event.stopPropagation();
        });
        $tbr.click(function () {
            $(this).find('input').click();
        });
    }
    initTableCheckbox();
});

$("#ecs_init").on("click",function () {
    var vals = [];
    $("input[name='checkItem']:checkbox:checked").each(function () {
        var tablerow = $(this).parent().parent();
        var func_name = tablerow.children("td").eq(1).text();
        console.log(func_name);
        vals.push(func_name);
    });
    console.log(vals);
    if(vals.length <= 0){
        alert("请选择功能执行....");
    }else {
        var target = $("#minion_id").text();
        $.ajax({
            type: "post",
            url: "/cmdb/ecshost/install/",
            data: {
                "tgt": target,
                "func_list": vals
            },
            dataType: "json",
            traditional: true,
            success: function (rst) {
                window.location.href="/cmdb/ecshost/install/res/" + target + "/";
            }
        });
    }
});