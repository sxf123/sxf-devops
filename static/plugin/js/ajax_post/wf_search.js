$("#search_wf").on("click",function() {
    var artifactId = $("#search_artifact").val();
    var service_type = $("#search_service_type").val();
    if(artifactId != "" && search_type != ""){
        $.ajax({
            type: "post",
            url: "http://127.0.0.1:8000/dxwf/mavenproj/",
            data: {
                "artifactId": artifactId,
                "service_type": service_type
            },
            success: function(rst) {
            console.log(rst);
                $("#hosttable").find("tr").remove();
                if (rst && rst.length > 0) {
                    for (var i = 0; i < rst.length; i++) {
                        var newTr = '<tr>';
                        newTr += '	<td>' + rst[i].fields.artifactId + '</td>';
                        newTr += '	<td>' + rst[i].fields.groupId + '</td>';
                        newTr += '	<td>' + rst[i].fields.create_time + '</td>';
                        newTr += '	<td>';
                        newTr += '		<a href="javascript:;">';
                        newTr += '			<button class="btn btn-success btn-sm">模 块</button>';
                        newTr += '		</a>';
                        newTr += '		<a href="/dxwf/mavenproj/download/' + rst[i].fields.artifactId + '">';
                        newTr += '			<button class="btn btn-warning btn-sm edit_btn" data-toggle="modal" data-target="#edit_project">下 载</button>';
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