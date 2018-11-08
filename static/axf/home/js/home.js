$(function () {
    //轮播图
    init_top_swiper()
    init_menu_swiper()
})

//顶部轮播
function init_top_swiper() {
    var mySwiper = new Swiper('#topSwiper', {
        loop: true,
        autoplay:1500,
            // 如果需要分页器
        pagination: '.swiper-pagination',
            // 如果需要前进后退按钮
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev',

        })
}

//下一个轮播
function init_menu_swiper() {
    var mySwiper = new Swiper('#swiperMenu', {
        slidesPerView: 3,

        })
}


