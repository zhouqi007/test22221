var cate_toggle_tag = false;
var sort_toggle_tag = false;
$(function () {
    //给所有的添加点击事件
    $("#all_cate").click(cate_toggle);
    $("#cates").click(cate_toggle);
    //给排序添加点击事件
    $('#all_sort').click(sort_toggle);
    $("#sorts").click(sort_toggle);

    //加操作
    $(".addShopping").click(function () {
        //获取当前的点击事件
        $current_bt = $(this);
        //获取点击的商品id
        var g_id = $current_bt.attr("g_id")

        $.ajax({
            url:"/myaxf/cart_api",
            data:{
                g_id:g_id,
                //说明是加操作
                type:"add"
            },
            method:"post",
            success:function (res) {
                console.log(res)
                if (res.code == 1){
                    $current_bt.prev().html(res.data)
                }
                if (res.code == 2){
                    window.open(res.data,target="_self")
                }
            }
        })
    })

    //减操作
    $(".subShopping").click(function () {
        $current_bt = $(this);
        //获取点击的商品id
        var g_id = $current_bt.attr("g_id")
        //判断当前显示是不是0，如果是0就return 不发送请求
        if($current_bt.next().html() == "0"){
            return ;
        }
        $.ajax({
            url:"/myaxf/cart_api",
            data:{
                g_id:g_id,
                //说明是加操作
                type:"sub"
            },
            method:"post",
            success:function (res) {
                if (res.code == 1){
                    $current_bt.next().html(res.data)
                }
                if (res.code == 2){
                    window.open(res.data,target="_self")
                }
            }
        })
    })
})


function cate_toggle() {
    $("#cates").toggle();
    if (cate_toggle_tag == false) {
         $(this).find("span").removeClass("glyphicon glyphicon-chevron-down").addClass("glyphicon glyphicon-chevron-up");
            cate_toggle_tag = true;
    }else{
         $(this).find("span").removeClass("glyphicon glyphicon-chevron-up").addClass("glyphicon glyphicon-chevron-down");
         cate_toggle_tag =false;
    }

}


function sort_toggle() {
    $("#sorts").toggle();    /* 实现切换元素的可见状态3*/
    if (sort_toggle_tag == false) {
        $("#all_sort").find("span").removeClass("glyphicon glyphicon-chevron-down").addClass("glyphicon glyphicon-chevron-up");
        sort_toggle_tag = true;
    }else{
        $("#all_sort").find("span").removeClass("glyphicon glyphicon-chevron-up").addClass("glyphicon glyphicon-chevron-down");
        sort_toggle_tag = false;
    }
}


