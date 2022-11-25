(function ($) {
  $(document).ready(function () {
    $("#overview").click(function () {
      $("#context").hide();
      $.ajax({
        type: "GET",
        url: "/api/v1.0/overview",
        data: "",
        success: function (data) {
          $("#context").fadeIn();
          $("#context").html(data);
        },
        error: function (data) {
          toastr.error("Failed to obtain the page resource!");
        },
      });
    });
    $("#host").click(function () {
      $("#context").hide();
      $.ajax({
        type: "GET",
        url: "/api/v1.0/manage_host",
        data: "",
        success: function (data) {
          $("#context").fadeIn();
          $("#context").html(data);
        },
        error: function (data) {
          toastr.error("Failed to obtain the page resource!");
        },
      });
    });
    $("#storage").click(function () {
      $("#context").hide();
      $.ajax({
        type: "GET",
        url: "/api/v1.0/storage",
        data: "",
        success: function (data) {
          $("#context").fadeIn();
          $("#context").html(data);
        },
        error: function (data) {
          toastr.error("Failed to obtain the page resource!");
        },
      });
    });

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

    $("#remote_execute").click(function () {
      $("#context").hide();
      $.ajax({
        type: "GET",
        url: "/api/v1.0/execute",
        data: "",
        success: function (data) {
          $("#context").fadeIn();
          $("#context").html(data);
        },
        error: function (data) {
          toastr.error("Failed to obtain the page resource!");
        },
      });
    });
    $("#data_sync").click(function () {
      $("#context").hide();
      $.ajax({
        type: "GET",
        url: "/api/v1.0/datasync",
        data: "",
        success: function (data) {
          $("#context").fadeIn();
          $("#context").html(data);
        },
        error: function (data) {
          toastr.error("Failed to obtain the page resource!");
        },
      });
    });

    $("#user").click(function () {
      $("#context").hide();
      $.ajax({
        type: "GET",
        url: "/api/v1.0/user",
        data: "",
        success: function (data) {
          $("#context").fadeIn();
          $("#context").html(data);
        },
        error: function (data) {
          toastr.error("Failed to obtain the page resource!");
        },
      });
    });
  });
})(jQuery);
