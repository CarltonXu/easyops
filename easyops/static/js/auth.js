(function ($) {
  $(document).ready(function () {
    function sleep(time) {
      return new Promise((resolve) => setTimeout(resolve, time));
    }

    if ($.cookie("username") != null) {
      //往input#username填入存到cookie中username的值
      $("#username").val($.cookie("username"));
      //往input#password填入存到cookie中username的值
      $("#password").val($.cookie("password"));
      //让“记住我”的复选框保持被选中状态
      $("input:checkbox").attr("checked", true);
    }

    $("#password").keyup(function () {
      ps1 = $("#password").val();
      ps2 = $("#repassword").val();
      if (ps1 == ps2) {
        $("#tips").html("");
        $("#repassword").css("border-color", "#ccc");
        $("bt_input").css("background-color", "#fcaf50");
        $("bt_input").attr("disabled", false);
      } else {
        $("#tips").html("Password Inconsistency");
        $("#repassword").css("border-color", "#ff0");
        $("bt_input").css("background-color", "gray");
        $("bt_input").attr("disabled", true);
      }
    });

    $("#wy-lg-eye-btn").click(function () {
      const changeInputBtnType = $("#wy-lg-eye-btn").siblings("input");
      if (changeInputBtnType.attr("type") == "password") {
        $("#wy-lg-eye-btn").removeClass("glyphicon-eye-open").addClass("glyphicon-eye-close");
        changeInputBtnType.attr("type", "text");
      } else {
        $("#wy-lg-eye-btn").removeClass("glyphicon-eye-close").addClass("glyphicon-eye-open");
        changeInputBtnType.attr("type", "password");
      }
    });

    $("#repassword").keyup(function () {
      ps1 = $("#password").val();
      ps2 = $("#repassword").val();
      if (ps1 == ps2) {
        $("#tips").html("");
        $("#repassword").css("border-color", "#ccc");
        $("bt_input").css("background-color", "#fcaf50");
        $("bt_input").attr("disabled", false);
      } else {
        $("#tips").html("Password Inconsistency");
        $("#repassword").css("border-color", "#ff0");
        $("bt_input").css("background-color", "gray");
        $("bt_input").attr("disabled", true);
      }
    });

    $("#login_btn").click(function () {
      if ($("#username").val() == "" || $("#password").val() == "") {
        $("#tips").html("Empty user name and password");
        $(".tips-container").fadeIn("slow");
        setTimeout(function () {
          $(".tips-container").fadeOut("slow");
        }, 3000);
        return false;
      }
    });

    // 设置登录的来源IP地址信息
    $.ajax({
      type: "GET",
      url: "https://ip.help.bj.cn",
      data: "",
      success: function (data) {
        $("#login_ipaddress").val(data.data[0].ip);
        $("#login_region").val(data.data[0].city);
      },
      error: function (data) {
        console.log("Error: " + data);
      },
    });
  });
})(jQuery);
