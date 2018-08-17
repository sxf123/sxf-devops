$("#host_update").on("click",function(){
    var hostname =
    $.ajax({
        type: "post",
        url: "http://127.0.0.1:8000/cmdb/hostinfo/update/",
        data: {
            "hostname": hostname
        },
        success: function (res) {
            console.log(rst);
        }
    })
})