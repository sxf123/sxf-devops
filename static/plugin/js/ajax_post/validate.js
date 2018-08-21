$(document).ready(function(){
    $("#project").focus(function () {
        $("#project_label").html('<label for="pro_name" id="project_label">项目名称</label>');
    })
    $("#project").blur(function () {
       if($("#select2-project-container").val() == ""){
           $("#project_label").html('<label for="pro_name" id="project_label">项目名称<span style="color: #F00;;">(不能为空)</span></label>');
       }else{
           $("#project_label").html('<label for="pro_name" id="project_label">项目名称</label>');
       }
    });
     $("#svn_path").focus(function () {
        $("#svn_path_label").html('<label for="pro_name" id="svn_path_label">svn地址</label>');
    })
    $("#svn_path").blur(function () {
       if($("#svn_path").val() == ""){
           $("#svn_path_label").html('<label for="pro_name" id="svn_path_label">svn地址<span style="color: #F00;;">(不能为空)</span></label>');
       }else{
           $("#svn_path_label").html('<label for="pro_name" id="svn_path_label">svn地址</label>');
       }
    });
    $("#principal").focus(function () {
       $("#principal_label").html('<label for="pro_name" id="principal_label">负责人</label>')
    });
    $("#principal").blur(function () {
        if($("#principal").val() == ""){
            $("#principal_label").html('<label for="stage_name" id="principal_label">负责人<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#principal_label").html('<label for="pro_name" id="principal_label">负责人</label>');
        }
    });
    $("#update_date").focus(function () {
       $("#update_date_label").html('<label for="pro_name" id="update_date_label">更新日期</label>')
    });
    $("#update_date").blur(function () {
        if($("#update_date").val() == ""){
            $("#update_date_label").html('<label for="stage_name" id="update_date_label">更新日期<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#update_date_label").html('<label for="pro_name" id="update_date_label">更新日期</label>');
        }
    });
    $("#update_project").focus(function () {
       $("#update_project_label").html('<label for="pro_name" id="update_project_label">升级项目</label>')
    });
    $("#update_project").blur(function () {
        if($("#update_project").val() == ""){
            $("#update_project_label").html('<label for="stage_name" id="update_project_label">升级项目<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#update_project_label").html('<label for="pro_name" id="update_project_label">升级项目</label>');
        }
    });
    $("#tag_date").focus(function () {
       $("#tag_date_label").html('<label for="pro_name" id="tag_date_label">tag日期</label>')
    });
    $("#tag_date").blur(function () {
        if($("#tag_date").val() == ""){
            $("#tag_date_label").html('<label for="stage_name" id="tag_date_label">tag日期<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#tag_date_label").html('<label for="pro_name" id="tag_date_label">tag日期</label>');
        }
    });
    $("#tag_version").focus(function () {
       $("#tag_version_label").html('<label for="pro_name" id="tag_version_label">tag版本</label>')
    });
    $("#tag_version").blur(function () {
        if($("#tag_version").val() == ""){
            $("#tag_version_label").html('<label for="stage_name" id="tag_version_label">tag版本<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#tag_version_label").html('<label for="pro_name" id="tag_version_label">tag版本</label>');
        }
    });
    $("#desc").focus(function () {
       $("#desc_label").html('<label for="pro_name" id="desc_label">版本简要说明</label>')
    });
    $("#desc").blur(function () {
        if($("#desc").val() == ""){
            $("#desc_label").html('<label for="stage_name" id="desc_label">版本简要说明<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#desc_label").html('<label for="pro_name" id="desc_label">版本简要说明</label>');
        }
    });
    $("#bug_fix").focus(function () {
        $("#bug_fix_label").html('<label for="pro_name" id="bug_fix_label">修改的缺陷</label>')
    });
    $("#bug_fix").blur(function () {
        if($("#bug_fix").val() == ""){
            $("#bug_fix_label").html('<label for="stage_name" id="bug_fix_label">修改的缺陷<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#bug_fix_label").html('<label for="pro_name" id="bug_fix_label">修改的缺陷</label>');
        }
    });
    $("#update_function").focus(function () {
        $("#update_function_label").html('<label for="pro_name" id="update_function_label">新增的功能</label>');
    });
    $("#update_function").blur(function(){
       if($("#update_function").val() == ""){
           $("#update_function_label").html('<label for="stage_name" id="update_function_label">新增的功能<span style="color: #F00;;">(不能为空)</span></label>');
       }else{
           $("#update_function_label").html('<label for="pro_name" id="update_function_label">新增的功能</label>');
       }
    });
    $("#exist_risk").focus(function () {
        $("#exist_risk_label").html('<label for="pro_name" id="exist_risk_label">可能存在的风险</label>');
    });
    $("#exist_risk").blur(function(){
       if($("#exist_risk").val() == ""){
           $("#exist_risk_label").html('<label for="stage_name" id="exist_risk_label">可能存在的风险<span style="color: #F00;;">(不能为空)</span></label>');
       }else{
           $("#可能存在的风险_label").html('<label for="pro_name" id="exist_risk_label">可能存在的风险</label>');
       }
    });
    $("#rollback").focus(function () {
       $("#rollback_label").html('<label for="pro_name" id="rollback_label">出现问题回滚措施</label>')
    });
    $("#rollback").blur(function () {
        if($("#rollback").val() == ""){
            $("#rollback_label").html('<label for="stage_name" id="rollback_label">出现问题回滚措施<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#rollback_label").html('<label for="pro_name" id="rollback_label">出现问题回滚措施</label>');
        }
    });
    $("#is_monitored").focus(function () {
       $("#is_monitored_label").html('<label for="pro_name" id="is_monitored_label">新上线功能是否可监控</label>')
    });
    $("#is_monitored").blur(function () {
        if($("#is_monitored").val() == ""){
            $("#is_monitored_label").html('<label for="stage_name" id="is_monitored_label">新上线功能是否可监控<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#is_monitored_label").html('<label for="pro_name" id="is_monitored_label">新上线功能是否可监控</label>');
        }
    });
    $("#instance").focus(function () {
       $("#instance_label").html('<label id="instance_label">数据库实例</label>');
    });
    $("#instance").blur(function () {
        if($("#instance").val() == ""){
            $("#instance_label").html('<label id="instance_label">数据库实例<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#instance_label").html('<label id="instance_label">数据库实例</label>')
        }
    })
     $("#develop_person").focus(function () {
       $("#develop_person_label").html('<label for="pro_name" id="develop_person_label">版本开发人员</label>')
    });
    $("#develop_person").blur(function () {
        if($("#develop_person").val() == ""){
            $("#develop_person_label").html('<label for="stage_name" id="develop_person_label">版本开发人员<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#develop_person_label").html('<label for="pro_name" id="develop_person_label">版本开发人员</label>');
        }
    });
    $("#monitored_person").focus(function () {
       $("#monitored_person_label").html('<label for="pro_name" id="monitored_person_label">升级后监控人员</label>')
    });
    $("#monitored_person").blur(function () {
        if($("#monitored_person").val() == ""){
            $("#monitored_person_label").html('<label for="stage_name" id="monitored_person_label">升级后监控人员<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#monitored_person_label").html('<label for="pro_name" id="monitored_person_label">升级后监控人员</label>');
        }
    });
    $("#verify_person").focus(function () {
       $("#verify_person_label").html('<label for="pro_name" id="verify_person_label">升级后功能验证人员</label>')
    });
    $("#verify_person").blur(function () {
        if($("#verify_person").val() == ""){
            $("#verify_person_label").html('<label for="stage_name" id="verify_person_label">升级后功能验证人员<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#verify_person_label").html('<label for="pro_name" id="verify_person_label">升级后功能验证人员</label>');
        }
    });
    $("#sql_exec").focus(function () {
        $("#sql_exec_label").html('<label id="sql_exec_label">需要执行的sql</label>');
    });
    $("#sql_exec").blur(function () {
        if($("#sql_exec").val() == ""){
            $("#sql_exec_label").html('<label id="sql_exec_label">需要执行的sql<span style="color: #F00">(不能为空)</span></label>');
        }else{
            $("#sql_exec_label").html('<label id="sql_exec_label">需要执行的sql</label>');
        }
    });
    $("#is_tested").focus(function () {
        $("#is_tested_label").html('<label id="is_tested_label">是否需要测试验证</label>');
    });
    $("#is_tested").blur(function () {
        if($("#is_tested").val() == ""){
            $("#is_tested_label").html('<label id="is_tested_label">是否需要测试验证<span style="color: #F00">(不能为空)</span></label>');
        }else{
            $("#is_tested_label").html('<label id="is_tested_label">是否需要测试验证</label>');
        }
    });
    $("#dbschema").focus(function () {
        $("#dbschema_label").html('<label id="dbschema_label">数据库schema</label>');
    });
    $("#dbschema").blur(function () {
        if($("#dbschema").val() == ""){
            $("#dbschema_label").html('<label id="dbschema_label">数据库schema<span style="color: #F00">(不能为空)</span></label>');
        }else{
            $("#dbschema_label").html('<label id="dbschema_label">数据库schema</label>');
        }
    });
    $("#solve_problem").focus(function () {
        $("#solve_problem_label").html('<label id="solve_problem_label">已解决的问题</label>');
    });
    $("#solve_problem").blur(function () {
        if($("#solve_problem").val() == ""){
            $("#solve_problem_label").html('<label id="solve_problem_label">已解决的问题<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#solve_problem_label").html('<label id="solve_problem_label">已解决的问题</label>');
        }
    });
    $("#need_test").focus(function () {
        $("#need_test_label").html('<label id="need_test_label">是否需要测试验证</label>');
    });
    $("#need_test").blur(function () {
        if($("#need_test").val() == "") {
            $("#need_test_label").html('<label id="need_test_label">是否需要测试验证<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#need_test_label").html('<label id="need_test_label">是否需要测试验证</label>');
        }
    });
    $("#handle_person").focus(function () {
        $("#handle_person_label").html('<label id="handle_person_label">升级操作人</label>');
    });
    $("#handle_person").blur(function () {
        if($("#handle_person").val() == ""){
            $("#handle_person_label").html('<label id="handle_person_label">升级操作人<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#handle_person_label").html('<label id="handle_person_label">升级操作人</label>');
        }
    });
    $("#deploy_type").focus(function () {
        $("#deploy_type_label").html('<label id="deploy_type_label">升级类型</label>');
    });
    $("#deploy_type").blur(function () {
        if($("#deploy_type").val() == ""){
            $("#deploy_type_label").html('<label id="deploy_type_label">升级类型<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#deploy_type_label").html('<label id="deploy_type_label">升级类型</label>');
        }
    });
    $("#email_person").focus(function () {
        $("#email_person_label").html('<label id="email_person_label">接受邮件的人</span></label>');
    });
    $("#email_person").blur(function () {
        if($("#email_person").val() == ""){
            $("#email_person_label").html('<label id="email_person_label">接受邮件的人<span style="color: #F00;;">(不能为空)</span></label>');
        }else{
            $("#email_person_label").html('<label id="email_person_label">接受邮件的人</span></label>');
        }
    });
    $("#upload_desc").focus(function () {
        $("#upload_desc_label").html('<label id="upload_desc_label">项目上线详细信息</label>');
    });
    $("#upload_desc").blur(function () {
       if($("#upload_desc").val() == ""){
           $("#upload_desc_label").html('<label id="upload_desc_label">项目上线详细信息<span style="color: #F00;">(不能为空)</span></label>');
       }else{
           $("#upload_desc_label").html('<label id="upload_desc_label">项目上线详细信息</label>');
       }
    });
});