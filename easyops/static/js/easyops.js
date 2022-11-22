function checkpassword() {
  ps1 = document.getElementById("password");
  ps2 = document.getElementById("repassword");
  if (ps1.value == ps2.value) {
    document.getElementById("tips").innerHTML = "";
    document.getElementById("repassword").style.borderColor = "#ccc";
    document.getElementById("bt_input").style.backgroundColor = "#4CAF50";
    document.getElementById("bt_input").disabled = false;
  } else {
    document.getElementById("tips").innerHTML = "Password Inconsistency";
    document.getElementById("repassword").style.borderColor = "#FF0";
    document.getElementById("bt_input").style.backgroundColor = "gray";
    document.getElementById("bt_input").disabled = true;
  }
}

(function ($) {
  $(document).ready(function () {
    $("#resources_menu").click(function (ev) {
      $(".fa-angle-down").toggleClass("hidden");
      $(".fa-angle-up").toggleClass("hidden");
      $("#remote_execute").slideToggle("fast");
      $("#data_sync").slideToggle("fast");
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
    $("#login_ipaddress").val(returnCitySN.cip);
    $("#login_region").val(returnCitySN.cname);

    setInterval(function time() {
      var date = new Date();
      var year = date.getFullYear();
      var month = date.getMonth();
      var day = date.getDate();
      var hour = date.getHours();
      hour = hour < 10 ? "0" + hour : hour;
      var minute = date.getMinutes();
      minute = minute < 10 ? "0" + minute : minute;
      var seconds = date.getSeconds();
      seconds = seconds < 10 ? "0" + seconds : seconds;
      var str = "现在时间: " + year + "年" + month + "月" + day + "日&nbsp" + hour + ":" + minute + ":" + seconds;
      $(".navbar-current-time").html(str);
    }, 1000);
  });
})(jQuery);
