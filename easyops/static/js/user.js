(function ($) {
  var sleep = function (time) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve();
      }, time);
    });
  };
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

    function cancel_edit_btn() {
      $("#person_phone_number").removeClass("person_phone_number");
      $("#person_phone_number").removeAttr("contenteditable");
      $("#person_email").removeClass("person_email");
      $("#person_email").removeAttr("contenteditable");
      $("#person_sex").removeClass("person_sex");
      $("#person_sex").removeAttr("contenteditable");

      $("#edit_user_btn").show();
      $("#update_user_btn").hide();
      $("#cancel_edit_btn").hide();
    }

    function edit_user_btn() {
      $("#person_phone_number").addClass("person_phone_number");
      $("#person_phone_number").attr("contenteditable", true);
      $("#person_email").addClass("person_email");
      $("#person_email").attr("contenteditable", true);
      $("#person_sex").addClass("person_sex");
      $("#person_sex").attr("contenteditable", true);

      $("#edit_user_btn").hide();
      $("#update_user_btn").show();
      $("#cancel_edit_btn").show();
    }

    $("#edit_user_btn").click(function () {
      edit_user_btn();
    });

    $("#cancel_edit_btn").click(function () {
      cancel_edit_btn();
    });

    $("#update_user_btn").click(function () {
      var person_phone_number = $("#person_phone_number").text();
      var person_email = $("#person_email").text();
      var person_sex = $("#person_sex").text();
      if (person_sex == "男") {
        person_sex = 1;
      } else if (person_sex == "女") {
        person_sex = 2;
      } else {
        person_sex = 1;
      }
      if (person_phone_number != "" && person_email != "" && person_sex != "") {
        var user_data = {};
        user_data["person_sex"] = person_sex;
        user_data["person_email"] = person_email;
        user_data["person_phone_number"] = person_phone_number;
        $.ajax({
          type: "POST",
          url: "/api/v1.0/update_user",
          data: user_data,
          success: function (data) {
            sleep(300).then(() => {
              $("#context").html(data);
            });
            toastr.success("更新用户信息成功");
          },
          error: function () {
            toastr.error("更新用户信息失败");
          },
        });
      } else {
        toastr.error("信息不能为空");
      }
    });

    $("#avatar_file").change(function () {
      var avatar_obj = $("#avatar_file")[0].files[0];
      if (typeof avatar_obj == undefined) {
        return;
      } else if (avatar_obj.size <= 0) {
        toastr.error("上传文件大小不能为0");
        return;
      }
      var reads = new FileReader();
      reads.readAsDataURL(avatar_obj);
      reads.onload = function (e) {
        $("#user_avatar_img").attr("src", this.result);
      };
      var formFile = new FormData();
      formFile.append("filesize", avatar_obj.size);
      formFile.append("file", avatar_obj);
      var data = formFile;
      $.ajax({
        type: "POST",
        url: "/api/v1.0/update_avatar",
        data: data,
        processData: false,
        contentType: false,
        success: function (data) {
          sleep(300).then(() => {
            $("#context").html(data);
          });
          var new_avatar = $("#user_avatar_img").attr("src");
          $("#navbar-avatar").attr("src", new_avatar);
          toastr.success("更新头像成功");
        },
        error: function (data) {
          toastr.error(data);
          $("#user").click();
        },
      });
    });

    $("#reset_password_btn").click(function () {
      var username = $(".user_base_info_username").text();
      $("#reset_username").val(username);
    });

    $("#submit_reset_password").click(function () {
      var username = $("#reset_username").val();
      var password = $("#reset_password").val();
      var resetpassword = $("#reset_repassword").val();
      var data = {};
      data["username"] = username;
      data["password"] = password;
      data["resetpassword"] = resetpassword;
      $.ajax({
        type: "POST",
        url: "/api/v1.0/resetpassword",
        data: data,
        success: function (data) {
          toastr.success("修改密码成功");
          $("#close_reset_password").click();
          sleep(300).then(() => {
            $("#context").html(data);
          });
        },
        error: function (data) {
          toastr.error(data.responseText);
        },
      });
    });
  });
})(jQuery);
