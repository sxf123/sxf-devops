$("#search_ippool").on("click",function(){
    var search_ip_address = $("#search_ip_address").val();
    var search_ip_type = $("#search_ip_type").val();
    if(search_ip_address != "" && search_ip_type != ""){
        $.ajax({
            type: "post",
            url: "http://127.0.0.1:8000/cmdb/ippool/",
            data: {
                "search_ip_address": search_ip_address,
                "search_ip_type": search_ip_type
            },
            success: function(rst){
                $("#ippooltable").find("tr").remove();
                if(rst && rst.length > 0){
                    for(var i=0; i < rst.length; i++){
                        var newTr = "<tr>";
                        newTr += "  <td>" + rst[i].fields.ip_address + "</td>";
                        newTr += "  <td>" + rst[i].fields.gateway + "</td>";
                        newTr += "  <td>" + rst[i].fields.ip_segment + "</td>";
                        newTr += "  <td>" + rst[i].fields.ip_type + "</td>";
                        newTr += "  <td>";
                        newTr += '      <a href="javascript::">';
                        newTr += '          <button class="btn btn-success btn-sm">模块</button>';
                        newTr += '      </a>';
                        newTr += '      <a href="/cmdb/ippool/update/' + rst[i].pk + '/">';
                        newTr += '          <button class="btn btn-warning btn-sm edit_btn">修改</button>';
                        newTr += '      </a>';
                        newTr += '      <a href="/cmdb/ippool/delete/' + rst[i].pk +'/">';
                        newTr += '          <button class="btn btn-danger btn-sm del_btn">删除</button>';
                        newTr += '      </a>';
                        newTr += '   </td>';
                        newTr += '</tr>';
                        $('.table1 tbody').append(newTr);
                    }
                }
            }
        })
    }
})