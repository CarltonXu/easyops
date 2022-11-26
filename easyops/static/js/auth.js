(function ($) {
  $(document).ready(function () {
    function sleep(time) {
      return new Promise((resolve) => setTimeout(resolve, time));
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
      try {
        $("#login_region").val(returnCitySN.cname);
        $("#login_ipaddress").val(returnCitySN.cip);
      } catch (e) {
        console.error("获取IP地址属性地失败");
      }
      if ($("#username").val() == "" || $("#password").val() == "") {
        $("#tips").html("Empty user name and password");
        $(".tips-container").fadeIn("slow");
        setTimeout(function () {
          $(".tips-container").fadeOut("slow");
        }, 3000);
        return false;
      }
    });
  });
})(jQuery);
