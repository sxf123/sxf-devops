$("#search_domainname").on("click",function(){
    var search_dns = $("#search_dns").val();
    var search_ip_address = $("#select2-search_ip_address-container").text();
    console.log(search_dns);
    console.log(search_ip_address);
    if(search_dns != "" && search_ip_address != ""){
        $.ajax({
            type: "post",
            url: "http://127.0.0.1:8000/cmdb/domainname/",
            data: {
                "search_dns": search_dns,
                "search_ip_address": search_ip_address
            },
            success: function(res){
                $("#domainnametable").find("tr").remove();
                if(res && res.length > 0){
                    for(var i=0; i < res.length; i++){
                        console.log(res[i]);
                        var newTr = "<tr>";
                        newTr += "   <td>" + res[i].fields.dns + "</td>";
                        newTr += "   <td>" + res[i].fields.ip + "</td>";
                        newTr += "   <td>" + res[i].fields.project_module + "</td>";
                        newTr += "   <td>" + res[i].fields.project_module_url + "</td>";
                        newTr += "   <td>"
                        newTr += '      <a href="javascript::">';
                        newTr += '          <button class="btn btn-success btn-sm">模块</button>';
                        newTr += '      </a>';
                        newTr += '      <a href="/cmdb/domainname/update/' + res[i].pk + '/">';
                        newTr += '          <button class="btn btn-warning btn-sm edit_btn">修改</button>';
                        newTr += '      </a>';
                        newTr += '      <a href="/cmdb/domainname/delete/' + res[i].pk +'/">';
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