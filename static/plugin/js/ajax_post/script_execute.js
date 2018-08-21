$("#script_execute").on("click",function(){
    var minion = $("#select2-hostname-container").text();
    var script_name = $("#script_name").text();
    if(minion != ""){
        $.ajax({
            type: "post",
            url: "http://127.0.0.1:8000/deploy/scripts/execute/",
            data: {
                "target": minion,
                "script_name": script_name
            },
            success: function (rst) {
                var info = rst.execute_res.return[0];
                for(var key in info){
                    var dom = $('<div style="margin-bottom: 20px;"><p style="font-weight: bold">' + key + '</p></div>');
                    var domli = $('<div>&nbsp;&nbsp;&nbsp;<span>stdout</span>:<br/><span>' + info[key].stdout.toString().replace(/\n/g,"<br/>") + '</span>');
                    dom.append(domli);
                    $("#execute_result").html(dom);
                }
            }
        })
    }
})