(function ($) {
  //检查cookie
  $(document).ready(function () {
    if ($.cookie("username") != null) {
      //往input#username填入存到cookie中username的值
      $("#username").val($.cookie("username"));
      //往input#password填入存到cookie中username的值
      $("#password").val($.cookie("password"));
      //让“记住我”的复选框保持被选中状态
      $("input:checkbox").attr("checked", true);
    }
  });
})(jQuery);
