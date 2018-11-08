$(function () {
    $("#myform").submit(function () {
        //判断用户名
        var name = $("#uid").val();
        if (name.length <3){
            alert("用户名过短");
            return false;
        }

        var pwd = $("#u_pwd").val();
        var confrim_pwd = $("#u_confrim_pwd").val();

        if (pwd == confrim_pwd & pwd.length>6){
            //加密
            var enc_pwd = md5(pwd);
            var enc_confrim_pwd = md5(confrim_pwd);

            //设置回去
            $("#u_pwd").val(enc_pwd);
            $("#u_confrim_pwd").val(enc_confrim_pwd);
        }else{
            alert("密码过短或不一致");
            return false;
        }
    })

    $("#uid").change(function () {
        var uname = $("#uid").val();
        $.ajax({
            url:"/myaxf/check_uname",
            data:{
                "uname":uname
            },
            method:"get",
            success:function (res) {
                    if (res.code == 1){
                        $("#uname_msg").html(res.msg);
                    }else{
                        //错误提示
                        alert(res.msg)
                    }
            }
        })
    })
})