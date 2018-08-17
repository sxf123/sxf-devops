$('#search_project').on('click', function(){
  var projectName = $('#input_proname').val(),
      stageName = $('#select_stage').val();
  console.log(projectName, stageName)
});
// 编辑按钮
// $('.table1').on('click', '.edit_btn', function(){
//   $('#edit_project').attr('index',$(this).parents('tr').index());
//   var proName = $(this).parents('tr').find('td[valname="pro_name"]').html(),
//       departmentName = $(this).parents('tr').find('td[valname="department_name"]').attr('value'),
//       stageName = $(this).parents('tr').find('td[valname="stage_name"]').attr('value'),
//       chargeName = $(this).parents('tr').find('td[valname="charge_name"]').html(),
//       describeText = $(this).parents('tr').find('td[valname="describe_text"]').html();
//
//   $('#edit_project #pro_name').val(proName)
//   $('#edit_project #department_name').val(departmentName)
//   $('#edit_project #stage_name').val(stageName)
//   $('#edit_project #charge_name').val(chargeName)
//   $('#edit_project #describe_text').val(describeText)
// });
// 删除按钮
// $('.table1').on('click', '.del_btn', function(){
//   var index = $(this).parents('tr').index();
//   console.log(index)
//   $('#del_project').attr('index', index);
// })
// modal 项目编辑 确定按钮(编辑、新增)
// $('#add_edit_ok').on('click',function(){
//   var proName = $('#edit_project #pro_name').val(),
//       departmentName = $('#edit_project #department_name').val(),
//       stageName = $('#edit_project #stage_name').val(),
//       chargeName = $('#edit_project #charge_name').val(),
//       describeText = $('#edit_project #describe_text').val(),
//       time = new Date(), year = time.getFullYear(),
//       month = fillZero(time.getMonth()+1), day = fillZero(time.getDate()),
//       hour = fillZero(time.getHours()), minutes = fillZero(time.getMinutes()), seconds = fillZero(time.getSeconds()),
//       createTime = year+'-'+month+'-'+day+' '+hour+':'+minutes+':'+seconds;
//   var index = $('#edit_project').attr('index');
//   if(index){ // 编辑
//     $('.table1 tbody tr').eq(index).find('td[valname="pro_name"]').html(proName)
//     $('.table1 tbody tr').eq(index).find('td[valname="department_name"]').html(departmentName)
//     $('.table1 tbody tr').eq(index).find('td[valname="stage_name"]').html(stageName)
//     $('.table1 tbody tr').eq(index).find('td[valname="charge_name"]').html(chargeName)
//     $('.table1 tbody tr').eq(index).find('td[valname="describe_text"]').html(describeText)
//     $('.table1 tbody tr').eq(index).find('td[valname="create_time"]').html(createTime)
//   }else{ // 新增
//     var newTr = '<tr>'+
//                   '<td>' + $('table tbody tr').length + 1 +'</td>' +
//                   '<td valname="pro_name">' + proName + '</td>' +
//                   '<td valname="department_name" value="01">'+ departmentName +'</td>'+
//                   '<td valname="stage_name" value="01">' + stageName + '</td>'+
//                   '<td valname="charge_name">' + chargeName + '</td>'+
//                   '<td valname="describe_text">' + describeText + '</td>'+
//                   '<td valname="create_time">' + createTime + '</td>'+
//                   '<td class="text-center">'+
//                     '<button class="btn btn-sm btn-success">模 块</button> '+
//                     '<button class="btn btn-sm btn-warning edit_btn" data-toggle="modal" data-target="#edit_project">编 辑</button> '+
//                     '<button class="btn btn-sm btn-danger" data-toggle="modal" data-target="#del_project">删 除</button>'+
//                   '</td>'+
//                 '</tr>';
//     $('.table1 tbody').append(newTr);
//   }
// });
// modal 删除项目 确定按钮
// $('#del_ok').on('click',function(){
//   var index = $('#del_project').attr('index');
//   $('table tbody tr').eq(index).remove();
// });

// $('#edit_project').on('hide.bs.modal', function () {
//   // 执行一些动作...
//   $('#edit_project #pro_name').val('')
//   $('#edit_project #department_name').val('')
//   $('#edit_project #stage_name').val('')
//   $('#edit_project #charge_name').val('')
//   $('#edit_project #describe_text').val('')
//   $('#edit_project').removeAttr('index')
// });

function fillZero(num) {
  return num<10 ? '0'+num : num 
}