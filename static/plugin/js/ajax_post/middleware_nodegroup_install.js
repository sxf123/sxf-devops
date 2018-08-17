$("#mid_mutiple_install").on("click",function () {
    var nodegroup = $("#select2-select_nodegroup-container").text();
    if(nodegroup != ""){
        $.ajax({
            type: "post",
            url: "http://127.0.0.1:8000/cmdb/middleware/nodegroup/",
            data: {
                "target": nodegroup,
                "target_type": "nodegroup"
            },
            success: function (rst) {
                console.log(rst);
            }
        })
    }
})