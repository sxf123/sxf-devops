$("#search_database").on("click",function() {
    var search_schema = $("#search_schema").val();
    var search_db_type = $("#search_db_type").val();
    if(hostname != "" && environment != ""){
        $.ajax({
            type: "post",
            url: "http://127.0.0.1:8000/cmdb/host/",
            data: {
                "hostname": search_schema,
                "environment": search_db_type
            },
            success: function(rst) {
            console.log(rst);
                $("#hosttable").find("tr").remove();
                if (rst && rst.length > 0) {
                    for (var i = 0; i < rst.length; i++) {
                        var newTr = '<tr>';
                        newTr += '	<td>' + rst[i].fields.schema + '</td>';
                        newTr += '	<td>' + rst[i].fields.db_type + '</td>';
                        newTr += '	<td>' + rst[i].fields.osrelease + '</td>';
                        newTr += '	<td>' + rst[i].fields.os + '</td>';
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
            error: function() {}
        });
    }else{
        $('#host_tip').show();
        var timer = setTimeout(function() {
            $('#host_tip').hide();
            clearTimeout(timer)
        },2000)
    }
});