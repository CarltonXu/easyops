(function ($) {
  $(document).ready(function () {
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
      var format_time = "<span class='narbar-current-time-content'>" + hour + ":" + minute + ":" + seconds + "</span>";
      var str = "现在时间: " + year + "年" + month + "月" + day + "日&nbsp" + format_time;
      $(".navbar-current-time").html(str);
    }, 1000);
  });
})(jQuery);
