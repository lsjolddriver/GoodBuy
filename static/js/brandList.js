function changeCat(word) {
    var content = window.prompt('请填入修改后的品牌名,按确认提交', word);
        //点击确定后操作
    post_data = {
        'myName': word,
        'content': content,
    }
    if(content != null){
        $.ajax({
            url: "/goods_manage/brandChange/",
            type: "POST",
            headers:{"X-CSRFToken":$.cookie('csrftoken')},
            data: post_data,
            success: function (data) {
                if (data.code == 200) {
                    alert(data.msg)
                    window.location.href='/goods_manage/brandList/';
                } else {
                    alert(data.code);
                }
            }
        });
    }else {
        alert('名称不能为空!')
    }
}


function removeCat(word) {

    var myName = word
    post_data = {
        'myName': myName,
    }
    if(confirm("确定删除该品牌?")) {
        //点击确定后操作
        $.ajax({
            url: "/goods_manage/brandRemove/",
            type: "POST",
            headers:{"X-CSRFToken":$.cookie('csrftoken')},
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


