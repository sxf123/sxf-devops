$("#sqlupload_rdsinstance").on("select2:select",function (e) {
    var sqlupload_rdsinstance = e.params.data.text;
    label = '<div class="form-group" id="sqlupload_' + sqlupload_rdsinstance + '_form"><div class="col-xs-6"><label id="sqlupload_' + sqlupload_rdsinstance + '_label">' + sqlupload_rdsinstance + '</label><select multiple="multiple" class="form-control" id="sqlupload_' +sqlupload_rdsinstance + '" name="sqlupload_' + sqlupload_rdsinstance + '" required><option></option></select></div></div>';
    $("#sqlupload_rdsinstance_form").after(label);
    $.ajax({
        url: "/deploy/task/rdsschema/select/",
        type: "POST",
        data: {
            "rdsinstance": sqlupload_rdsinstance
        },
        success: function (rst) {
            var id = "#sqlupload_" + sqlupload_rdsinstance
            $(id).select2({
                data: rst.rdsschema,
                placeholder: "请选择",
                language: "zh-CN",
                allowClear: false
            });
        }
    });
    $("#sqlupload_rdsinstance").on("select2:unselect",function (e) {
       $("#sqlupload_" + e.params.data.text + "_form").remove();
    });
    $("#sqlupload_" + sqlupload_rdsinstance).on("select2:select",function(e) {
        var sqlupload_rdsschema = e.params.data.text;
        label = '<div class="form-group" id="sqlupload_' + sqlupload_rdsschema + '_form"><div class="col-xs-6"><label id="sqlupload_' + sqlupload_rdsschema + '_label">' + sqlupload_rdsschema + '</label><input type="file" class="file" name="sqlupload_' + sqlupload_rdsschema + '" id="sqlupload_' + sqlupload_rdsschema + '" data-show-preview="false" data-show-upload="false" required/></div></div>';
        $("#sqlupload_" + sqlupload_rdsinstance + "_form").after(label);
        $("#sqlupload_" + sqlupload_rdsschema).fileinput({
            language: "zh",
            showUpload: true
        })
    });
    $("#sqlupload_" + sqlupload_rdsinstance).on("select2:unselect",function (e) {
        var sqlupload_rdsschema = e.params.data.text;
        $("#sqlupload_" + sqlupload_rdsschema +"_form").remove();
    })
})