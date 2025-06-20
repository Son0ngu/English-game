// ---------Responsive-navbar-active-animation-----------
function test() {
    var tabsNewAnim = $('#navbarSupportedContent');
    var selectorNewAnim = $('#navbarSupportedContent').find('li').length;
    var activeItemNewAnim = tabsNewAnim.find('.active');
    var activeWidthNewAnimHeight = activeItemNewAnim.innerHeight();
    var activeWidthNewAnimWidth = activeItemNewAnim.innerWidth();
    var itemPosNewAnimTop = activeItemNewAnim.position();
    var itemPosNewAnimLeft = activeItemNewAnim.position();
    $(".hori-selector").css({
        "top": itemPosNewAnimTop.top + "px",
        "left": itemPosNewAnimLeft.left + "px",
        "height": activeWidthNewAnimHeight + "px",
        "width": activeWidthNewAnimWidth + "px"
    });
    $("#navbarSupportedContent").on("click", "li", function (e) {
        $('#navbarSupportedContent ul li').removeClass("active");
        $(this).addClass('active');
        var activeWidthNewAnimHeight = $(this).innerHeight();
        var activeWidthNewAnimWidth = $(this).innerWidth();
        var itemPosNewAnimTop = $(this).position();
        var itemPosNewAnimLeft = $(this).position();
        $(".hori-selector").css({
            "top": itemPosNewAnimTop.top + "px",
            "left": itemPosNewAnimLeft.left + "px",
            "height": activeWidthNewAnimHeight + "px",
            "width": activeWidthNewAnimWidth + "px"
        });
    });
}
$(document).ready(function () {
    setTimeout(function () { test(); });
});
$(window).on('resize', function () {
    setTimeout(function () { test(); }, 500);
});
$(".navbar-toggler").click(function () {
    $(".navbar-collapse").slideToggle(300);
    setTimeout(function () { test(); });
});

$(document).ready(function () {
    // Show Register Form
    $("#showRegister").click(function() {
        $(".login-form").hide();
        $(".register-form").show();
    });

    // Show Login Form
    $("#showLogin").click(function() {
        $(".register-form").hide();
        $(".login-form").show();
    });
});

// --------------add active class-on another-page move----------
// jQuery(document).ready(function ($) {
//     // Get current path and find target link
//     var path = window.location.pathname.split("/").pop();

//     // Account for home page with empty path
//     if (path == '') {
//         path = 'index.html';
//     }

//     var target = $('#navbarSupportedContent ul li a[href="' + path + '"]');
//     // Add active class to target link
//     target.parent().addClass('active');
// });

$(document).ready(function () {
    // Change active class on tab switch
    $('#navbarSupportedContent a').on('click', function () {
        $('#navbarSupportedContent .nav-item').removeClass('active');
        $(this).parent().addClass('active');
    });

    $('#navbarSupportedContent a').on('click', function (e) {
        e.preventDefault();
        var targetTab = $(this).attr('href');
        $('.tab-pane').removeClass('show active');
        $(targetTab).tab('show');
    });

    // Initialize the active item when the page loads
    var path = window.location.pathname.split("/").pop();
    if (path == '') {
        path = 'index.html';
    }

    var target = $('#navbarSupportedContent ul li a[href="' + path + '"]');
    target.parent().addClass('active');
});


// Add active class on another page linked
// ==========================================
// $(window).on('load',function () {
//     var current = location.pathname;
//     console.log(current);
//     $('#navbarSupportedContent ul li a').each(function(){
//         var $this = $(this);
//         // if the current path is like this link, make it active
//         if($this.attr('href').indexOf(current) !== -1){
//             $this.parent().addClass('active');
//             $this.parents('.menu-submenu').addClass('show-dropdown');
//             $this.parents('.menu-submenu').parent().addClass('active');
//         }else{
//             $this.parent().removeClass('active');
//         }
//     })
// });
