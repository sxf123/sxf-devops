$("#rdsinstance").on("select2:select",function (e) {
    console.log(e.params.data.text);
    var rdsinstance = e.params.data.text;
    label = '<div class="form-group" id="' + rdsinstance + '_form"><div class="col-xs-6"><label id="' + rdsinstance + '_label">' + rdsinstance + '</label><select multiple="multiple" class="form-control" id="' + rdsinstance + '" name="' + rdsinstance + '" required><option></option></select></div></div>';
    $("#rdsinstance_form").after(label);
    $.ajax({
        url: "/deploy/task/rdsschema/select/",
        type: "POST",
        data: {
            "rdsinstance": rdsinstance
        },
        success: function (rst) {
            var id = "#" + rdsinstance
            $(id).select2({
                data: rst.rdsschema,
                placeholder: "请选择",
                language: "zh-CN",
                allowClear: false,
            });
        }
    });
    $("#rdsinstance").on("select2:unselect",function (e) {
        $("#" + e.params.data.text + "_form").remove();
    });
    $("#" + rdsinstance).on("select2:select",function (e) {
        var rdsschema = e.params.data.text;
        label = '<div class="form-group" id="' + rdsschema + '_form"><div class="col-xs-6"><label id="' + rdsschema + '_label">' + rdsschema + '</label><input type="file" class="file" name="' + rdsschema + '" id="' + rdsschema + '" data-show-preview="false" data-show-upload="false" required/></div></div>';
        $("#" + rdsinstance + "_form").after(label);
        $("#" + rdsschema).fileinput({
            language: "zh",
            showUpload: true,
        })
    });
    $("#" + rdsinstance).on("select2:unselect",function (e) {
        var rdsschema = e.params.data.text;
        $("#" + rdsschema + "_form").remove();
    });
});

$("#need_test").on("select2:select",function (e) {
    var need_test = e.params.data.id;
    if(need_test == "yes") {
        label = '<div class="form-group" id="verify_person_form"><div class="col-xs-6"><label id="verify_person_label">升级后功能验证人员<span style="color:#F00;;">(不能为空)</span></label><select multiple="multiple" class="form-control select2" id="verify_person" name="verify_person" required><option></option></select></div></div>';
        $("#need_test_form").after(label);
        $.ajax({
            url: "/deploy/task/verifyperson/select/",
            type: "POST",
            data: {
                "need_test": need_test
            },
            success: function (rst) {
                $("#verify_person").select2({
                    data: rst.verify_person,
                    placeholder: "请选择",
                    languate: "zh-CN",
                    allowClear: false
                })
            }
        });
    }else if(need_test == "no") {
        if($("#verify_person_form").length > 0){
            $("#verify_person_form").remove();
        }
    }
})