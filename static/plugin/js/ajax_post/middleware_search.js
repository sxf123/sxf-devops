$("#search_middleware").on("click",function(){
    var mid_search_name = $("#mid_search_name").val();
    var mid_search_type = $("#mid_search_type").val();
    if(mid_search_name != "" && mid_search_type != ""){
        $.ajax({
            type:"post",
            url:"http://127.0.0.1:8000/cmdb/middleware/",
            data: {
                "mid_search_name":mid_search_name,
                "mid_search_type":mid_search_type
            },
            success: function (rst) {
                $("#hosttable").find("tr").remove();
                if(rst && rst.length > 0){
                    for(var i = 0;i < rst.length; i++){
                        var newTr = "<tr>";
                        newTr += "<td>" + rst[i].fields.mid_name + "</td>";
                        newTr += "<td>" + rst[i].fields.mid_type + "</td>";
                        newTr += "<td>" + rst[i].fields.mid_description + "</td>";
                        newTr += "<td>" + rst[i].fields.mid_version + "</td>";
                        newTr += '	<td>';
                        newTr += '		<a href="javascript:;">';
                        newTr += '			<button class="btn btn-success btn-sm">模 块</button>';
                        newTr += '		</a>';
                        newTr += '		<a href="javascript:;">';
                        newTr += '			<button class="btn btn-warning btn-sm edit_btn" data-toggle="modal" data-target="#edit_project">修 改</button>';
                        newTr += '		</a>';
                        newTr += '		<a href="javascript:;">';
                        newTr += '			<button class="btn btn-danger btn-sm del_btn" data-toggle="modal" data-target="#del_project">删 除</button>';
                        newTr += '		</a>';
                        newTr += '	</td>';
                        newTr += '</tr>';
                        $('.table1 tbody').append(newTr);
                    }
                }
            },
            error:function () {}
        });
    }
});