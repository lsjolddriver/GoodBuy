
function lookUser(name) {
    var myName = name
    post_data = {
        'myName': myName
    }
    $.ajax({
        url: "/admin_user_manage/lookUser/",
        headers:{"X-CSRFToken":$.cookie('csrftoken')},
        type: "POST",
        data: post_data,
        success: function (data) {

            if (data.code == 200) {
                alert(data.password)
            } else {
                alert(data.code);
            }
        }
    });
}

function deleteUser(name) {
    var myName = name
    post_data = {
        'myName': myName
    }
    if(confirm("确定删除该管理员?")) {
        //点击确定后操作


        $.ajax({
            url: "/admin_user_manage/deleteUser/",
            headers:{"X-CSRFToken":$.cookie('csrftoken')},
            type: "POST",
            data: post_data,
            success: function (data) {

                if (data.code == 200) {
                    alert(data.msg)
                    location.reload()
                } else {
                    alert(data.code);
                }
            }
        });
    }
}