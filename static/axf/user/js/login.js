$(function () {
    $("#submit").click(login);
})

function login() {
    //拿用户输入数据
    var name = $("#uid").val();
    var pwd = $("#u_pwd").val();
    //校验数据格式
    if (name.length <3){
        alert("用户名太短");
        return;
    }
    if (pwd.length <6) {
        alert('密码过短');
        return;
    }
    //给密码加密
    var enc_pwd = md5(pwd);
   //发送ajax请求
    $.ajax({
        url:"/myaxf/login",
        data:{
            "name":name,
            "pwd":enc_pwd
        },
        method:"post",
        success:function (res) {
            //成功跳转到mine.html界面   数据后端传来
            if (res.code==1){
                window.open(res.data,target="_self");
            }else{
                alert(res.msg);
            }
        },
        errror:function () {
            //错误提示
        },
        complete:function () {
            //  请求完成时被执行
        }
    })
}