$("#mid_install").on("click",function () {
    var host = $("#select2-select_host-container").text();
    if(host != ""){
        $.ajax({
            type: "post",
            url: "http://127.0.0.1:8000/cmdb/middleware/install/",
            data: {
                "target": host,
                "target_type": "glob",
                "midware":"nginx",
            },
            success: function (rst) {
                var info = rst.install_res.return[0][host];
                for(var key in info){
                    var dom = $('<div style="margin-bottom: 20px;"><p style="font-weight: bold">'+key+'</p>{</div>');
                    for (var k in info[key]){
                        var domli = $('<div>&nbsp;&nbsp;&nbsp;<span>'+[k]+'</span>：<span>'+info[key][k]+'</span></div>');
                        dom.append(domli)
                    }
                    dom.append("}");
                    $('#host-info').append(dom);
                }
            }
        })
    }
})