$(function () {
    $(".confirm").click(function () {
        $current_btn = $(this);
        //知道点击的是谁
        var c_id = $(this).parents("li").attr("c_id");
    //发送请求
        $.ajax({
            url:"/myaxf/cart_status",
            data:{
                c_id:c_id,
            },
            //局部修改请求
            method:"patch",
            success:function (res) {
                if (res.code==1){
                    //修改当前按钮状态
                    if(res.data.status){
                        $current_btn.find("span").find("span").html("√");
                    }else{
                        $current_btn.find("span").find("span").html("");
                    }

                    //修改钱数
                    $("#money_id").html(res.data.sum_money);
                    //修改全选按钮
                    if (res.data.is_all_selected){
                        $(".all_select>span>span").html("√");
                    }else{
                        $(".all_select>span>span").html("");
                    }

                }
            }
        })
    });


    $(".all_select").click(function () {
        $.ajax({
            url:"/myaxf/cart_all_status",
            data:{},
            method:"put",
            success:function (res) {
                if (res.code==1){
                    $("#money_id").html(res.data.sum_money);
                    if (res.data.all_select){
                        $(".all_select>span>span").html("√");
                        $(".confirm").each(function () {
                            $(this).find("span").find("span").html("√");
                        })
                    }else{
                        $(".all_select>span>span").html("");
                        $(".confirm").each(function () {
                            $(this).find("span").find("span").html("");
                        })
                    }
                }

            }

        })
    });

//    购物车加操作
    $(".addBtn").click(function () {
        //确定数据id
        var $current_btn = $(this);
        var c_id = $(this).parents("li").attr("c_id");

    //    发送请求
        $.ajax({
            url:"/myaxf/cart_item",
            data:{
                c_id:c_id
            },
            method:"post",
            success:function (res) {
                // console.log(res)
                if (res.code==1){
                    $current_btn.prev().html(res.data.num);
                    $("#money_id").html(res.data.sum_money);
                }else{
                    alert(res.msg)
                }
            }
        })
    });


    $(".subBtn").click(function () {
        var $current_btn = $(this);
        var c_id = $current_btn.parents("li").attr("c_id");
        $.ajax({
            url:"/myaxf/cart_item",
            data:{
                c_id:c_id
            },
            method:"delete",
            success:function (res) {
                if (res.code==1){
                    if (res.data.num ==0){
                        $current_btn.parents("li").remove();
                    }else{
                        $current_btn.next().html(res.data.num);
                    }
                    $("#money_id").html(res.data.sum_money);

                }
            }
        })
    });

    //下单
    $("#order").click(function () {
        var money = $("#money_id").html();
        if (money == 0){
            alert("暂无商品下单");
        }else{
            window.open("/myaxf/order",target="_self");
        }
    })

})