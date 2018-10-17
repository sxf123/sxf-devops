$("#execute_file").on("click",function () {
    var id = $("#upload_file_id").val();
    $.ajax({
        type: "post",
        url: "/deploy/upload/file/execute/" + id + "/",
        data: {
            "id": id
        },
        success: function(res) {
            window.location.href="/deploy/execute/file/res/" + res.id + "/";
        }
    });
});