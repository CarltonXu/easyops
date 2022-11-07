(function ($) {
  $(document).ready(function () {
    var SearchRemotesType = function (remote_name) {
      var searchObj = $("#sidebar-remote ul li a");
      for (var i = 0; i < searchObj.length; i++) {
        var search_obj_name = searchObj[i].innerText.split(": ")[0];
        if (search_obj_name == remote_name) {
          var remote_type = searchObj[i].innerText.split(": ")[1].replace("(", "").replace(")", "");
          break;
        }
      }
      return remote_type;
    };

    $(".nav-link").click(function () {
      var remote_name = $(this)[0].innerText.split(":")[0];
      var remote_type = $(this)[0].innerText.split(": ")[1].replace("(", "").replace(")", "");
      $.ajax({
        type: "POST",
        url: "/api/v1.0/datasync/" + remote_name + "/",
        data: { type: remote_type },
        success: function (data) {
          $("#file_manager_context").html(data);
        },
        error: function (data) {
          toastr.error("Failed to obtain the page resource!");
        },
      });
    });

    $("body").delegate("#prev_path_btn", "click", function () {
      var remote_url = "/" + $("#remote-storage-path")[0].value;
      var remote_name = $("#remote-storage-name")[0].innerText.split(":")[0];
      var remote_type = SearchRemotesType(remote_name);
      var prev_remote_path = remote_url == "" ? "" : remote_url.substring(0, remote_url.lastIndexOf("/"));
      if (prev_remote_path == "") {
        var prev_remote_url = "/api/v1.0/datasync/" + remote_name + "/";
      } else {
        var prev_remote_url = "/api/v1.0/datasync/" + remote_name + prev_remote_path + "/";
      }
      $.ajax({
        type: "POST",
        url: prev_remote_url,
        data: { type: remote_type },
        success: function (data) {
          $("#file_manager_context").html(data);
        },
        error: function (data) {
          toastr.error("Failed to obtain the page resource!");
        },
      });
    });

    $("body").delegate("#refresh_path_btn", "click", function () {
      var remote_url = "/" + $("#remote-storage-path")[0].value;
      var remote_name = $("#remote-storage-name")[0].innerText.split(":")[0];
      var remote_type = SearchRemotesType(remote_name);
      if (remote_url == "/") {
        var refresh_remote_url = "/api/v1.0/datasync/" + remote_name + "/";
      } else {
        var refresh_remote_url = "/api/v1.0/datasync/" + remote_name + remote_url + "/";
      }
      $.ajax({
        type: "POST",
        url: refresh_remote_url,
        data: { type: remote_type },
        success: function (data) {
          $("#file_manager_context").html(data);
          toastr.success("Refresh current directory success.");
        },
        error: function (data) {
          toastr.error("Failed to obtain the page resource!");
        },
      });
    });

    $("body").delegate("#submit-storage-path_btn", "click", function () {
      var remote_url = $("#remote-storage-path")[0]
        .value.replace(/[\W]+[\W]+/g, "/")
        .replace(/(^\/)|(\/$)/g, "");
      var remote_name = $("#remote-storage-name")[0].innerText.split(":")[0];
      var remote_type = SearchRemotesType(remote_name);
      if (remote_url == "" || remote_url == "/") {
        var obtain_remote_url = "/api/v1.0/datasync/" + remote_name + "/";
      } else {
        var obtain_remote_url = "/api/v1.0/datasync/" + remote_name + "/" + remote_url + "/";
      }
      $.ajax({
        type: "POST",
        url: obtain_remote_url,
        data: { type: remote_type },
        success: function (data) {
          $("#file_manager_context").html(data);
          toastr.success("Obtain current directory success.");
        },
        error: function (data) {
          toastr.error("Failed to obtain the page resource!");
        },
      });
    });

    $("body").delegate("table > tbody > tr > td:nth-child(2) > a", "click", function () {
      var remote_url = $(this).attr("value");
      var remote_name = remote_url.split("datasync/")[1].split("/")[0];
      var remote_type = SearchRemotesType(remote_name);
      if (remote_url == "") {
        return;
      }
      $.ajax({
        type: "POST",
        url: remote_url,
        data: { type: remote_type },
        success: function (data) {
          $("#file_manager_context").html(data);
        },
        error: function (data) {
          toastr.error("Failed to obtain the page resource!");
        },
      });
    });

    $("body").delegate("#file_manager_context > p > a", "click", function () {
      var remote_url = $(this).attr("value");
      var remote_name = remote_url.split("datasync/")[1].split("/")[0];
      var remote_type = SearchRemotesType(remote_name);
      $.ajax({
        type: "POST",
        url: remote_url,
        data: { type: remote_type },
        success: function (data) {
          $("#file_manager_context").html(data);
        },
        error: function (data) {
          toastr.error("Failed to obtain the page resource!");
        },
      });
    });

    $("body").delegate(".delete_file_menu", "click", function () {
      var remote_url = $(this).attr("value");
      var remote_name = remote_url.split("datasync/")[1].split("/")[0];
      var remote_type = SearchRemotesType(remote_name);
      var tips_msg = "是否确定删除 " + remote_url.split("/").slice(-2)[0] + " 文件或目录?";
      if (confirm(tips_msg)) {
        $.ajax({
          type: "DELETE",
          url: remote_url,
          data: { type: remote_type },
          success: function (data) {
            $("#file_manager_context").html(data);
          },
          error: function (data) {
            toastr.error("Failed to Delete the remote resource!");
          },
        });
      }
    });
  });
})(jQuery);
