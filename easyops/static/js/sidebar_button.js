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
      $(".resources-panel").slideToggle("fast");
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
