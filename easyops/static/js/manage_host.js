(function($) {
    $(document).ready(function() {
        var sleep = function(time) {
            return new Promise(resolve => {
                setTimeout(() => {
                    resolve();
                }, time);
            });
        };

        var objectifyForm = function(formArray) {
            var returnArray = {};
            for (var i = 0; i < formArray.length; i++){
               returnArray[formArray[i]["name"]] = formArray[i]["value"];
            };
            return returnArray;
        };

        $("#file_upload").fileinput({
            language: 'zh',
            showPreview: false,
            showUpload: false,
            /*
            uploadUrl: "/execute/manage_host/batch_ad"d",
            previewSettings: {//预览图片大小设置
                image: { width: "500px", height: "500px" }
            },
            */
            showCancel: true,
            autoReplace: true,
            initialPreviewFileType: "excel",
            elErrorContainer: "#kartik_file_errors",
            allowedFileExtensions: ["xlsx", "xls"],
            browseClass: "btn btn-primary",
            maxFileCount: 1,
            validateInitialCount:true,
            msgFilesTooMany: "选择上传的文件数量({n}) 超过允许的最大数值{m}！",
            previewFileIcon: "<i class='glyphicon glyphicon-king'></i>",
        });

        $(".add_hosts_btn").on("click", (function(event) {
            $("#select_all").attr("checked", false);
            $("tbody td:first-child input").prop("checked", false);
            $("#delete_host").attr("disabled", true);
            $(".add_hosts_menu").slideToggle();
        }));

        $(".add_hosts_btn").on("blur", (function(event) {
            $(".add_hosts_menu").slideUp();
        }));

        $(".add_one_host, .add_batch_host").on("click", (function() {
            $(".add_hosts_menu").css("display","none");
        }));

        $("#add_host_form :input").on("blur", (function() {
            if ($("#manage_hostname").val() == "" || $("#manage_ipaddr").val() == "" ||
            $("#manage_port").val() == "" || $("#manage_user").val() == "" || $("#manage_password").val() == "") {
                $("#manage_btn").attr("disabled", true)
            } else {
                $("#manage_btn").attr("disabled", false)
            }
        })).keyup(function(){
            $(this).triggerHandler("blur");
        }).focus(function(){
            $(this).triggerHandler("blur"); 
        });

        $("#update_host_form :input").on("blur", (function() {
            if ($("#update_hostname").val() == "" || $("#update_ipaddr").val() == "" ||
            $("#update_port").val() == "" || $("#update_user").val() == "") {
                $("#update_btn").attr("disabled", true)
            } else {
                $("#update_btn").attr("disabled", false)
            }
        })).keyup(function(){
            $(this).triggerHandler("blur");
        }).focus(function(){
            $(this).triggerHandler("blur"); 
        });



        $("#select_all").on("click", function() {
            var check_num = $("tbody td:first-child input").filter(":checked").length;
            if ($(this).attr("checked") == "checked") {
                $(this).attr("checked", false)
                $("tbody td:first-child input").prop("checked", false);
                ChangeButtonStatus()
            } else {
                $(this).attr("checked", true)
                $("tbody td:first-child input").prop("checked", true);
                $("#delete_host").attr("disabled", false)
                ChangeButtonStatus()
            };
        });

        var ChangeButtonStatus = function() {
            var check_num = $("tbody td:first-child input").filter(":checked").length;
            if (check_num > 1) {
                $("#delete_host").attr("disabled", false);
                $("#update_host").attr("disabled", true);
            } else if (check_num <= 0) {
                $("#update_host").attr("disabled", true);
                $("#delete_host").attr("disabled", true);
                $("#select_all").attr("checked", false);
            } else if (check_num == 1){
                $("#update_host").attr("disabled", false); 
                $("#delete_host").attr("disabled", false); 
            };
        };

        $("tbody td:first-child input").on("click", function() {
            if ($(this)[0].checked) {
                ChangeButtonStatus()
            } else {
                ChangeButtonStatus()
            };
        });

        $("#manage_btn").on("click", (function() {
            var form = $("#add_host_form");
            var formdata = form.serializeArray()
            var formdata = objectifyForm(formdata);
            $.ajax({
                type: "POST",
                url: "/api/v1.0/host/add",
                data: formdata,
                success: function(data) {
                    toastr.success("Add remote host successful.");
                    $("#manage_close_btn").click()
                    sleep(300).then(() => {
                        $("#context").html(data);
                    });
                },
                error: function(data) {
                    toastr.error(data.responseText);
                }
            });
        }));

        $("#add_batch_btn").on("click", (function() {
            var fileobj = $("#file_upload")[0].files[0];
            if (typeof(fileobj) == "undefined" || fileobj.size <= 0) {
                toastr.error("Upload file not exsits.")
                return
            }
            var formFile = new FormData();
            formFile.append("filesize", fileobj.size); 
            formFile.append("file", fileobj); 
            var data = formFile
            $.ajax({
                type: "POST",
                url: "/api/v1.0/host/batch_add",
                data: data,
                processData: false,
                contentType: false,
                success: function(data) {
                    toastr.success("Add batch servers successful.")
                    $("#add_batch_close_btn").click()
                    sleep(300).then(() => {
                        $("#context").html(data)
                    });
                },
                error: function(data) {
                    toastr.error(data.responseText)
                }
            });
        }));

        $("#delete_host").on("click", (function() {
            var obj_parents = $("tbody td:first-child input").filter(":checked").parent()
            var selectdata = {}
            for (var n = 0; n < obj_parents.length; n++) {
                selectdata[n] = obj_parents[n].siblings()[1].innerHTML
            };
            if (confirm("是否确定删除主机?")) {
                $.ajax({
                    type: "POST",
                    url: "/api/v1.0/host/delete",
                    data: selectdata,
                    success: function(data) {
                       $("#context").html(data);
                       toastr.success("Delete host successful."); 
                    },
                    error: function() {
                        toastr.error("Delete hosts failed.");
                    }
                });
            };
        }));

        $("#update_host").on("click", (function() {
           var update_host_obj = $("tbody td:first-child input").filter(":checked").parent() 
           var update_host_siblings = update_host_obj[0].siblings()
           for (var x = 0; x < update_host_siblings.length; x++) {
               if (x == 0) {
                   $("#update_hostname").val(update_host_siblings[x].innerHTML);
               } else if (x == 4) {
                   $("#update_group").val(update_host_siblings[x].innerHTML);
               } else if (x == 1) {
                   $("#update_ipaddr").val(update_host_siblings[x].innerHTML);
               } else if (x == 2) {
                   $("#update_port").val(update_host_siblings[x].innerHTML);
               } else if (x == 3) {
                   $("#update_user").val(update_host_siblings[x].innerHTML);
               } else {
                   $("#update_password").val("");
               }
           };
        }));

        $("#update_btn").on("click", (function() {
            var form = $("#update_host_form");
            var formdata = form.serializeArray()
            var formdata = objectifyForm(formdata);
            $.ajax({
                type: "POST",
                url: "/api/v1.0/host/update",
                data: formdata,
                success: function(data) {
                    toastr.success("Add remote host successful.");
                    $("#update_close_btn").click()
                    sleep(300).then(() => {
                        $("#context").html(data);
                    })
                },
                error: function(data) {
                    toastr.error(data.responseText);
                }
            }); 
        }));

        $(".overall-mask").on("click", (function() {
            $(this).hide();
            $(".host_details").hide();
        }));

        $("tbody tr td:not(:first-child)").on("click", (function() {
            var select_details_host_name = $(this).parent().children()[1].innerHTML;
            var select_details_host_ip = $(this).parent().children()[2].innerHTML;
            var select_details_host_ctime = $(this).parent().children()[6].innerHTML;
            var data = {
                "host": select_details_host_ip,
                "module": "setup",
                "cmd": ""
            }
            if (confirm("是否加载主机详细信息?")) {
                $(".overall-mask").show();
                $(".host_details").show();
                $(".host_details").html("<h1>信息加载中...</h1>");
                $.ajax({
                    type: "POST",
                    url: "/api/v1.0/execute/host_details",
                    data: data,
                    success: function(data) {
                        toastr.success("Load host details success");
                        $(".host_details").html(data)
                        $("#display_name").html(select_details_host_name);
                        $("#create_time").html(select_details_host_ctime);
                        var mem_container_pro_width = $(".mem_usage_container").css("width").split("px")[0];
                        var mem_usage_obj = $(".mem_usage")
                        var mem_pro_value = mem_usage_obj.html().split("%")[0];
                        var mem_pro_width = ((mem_container_pro_width -4) * (mem_pro_value / 100));
                        if (mem_pro_value >= 0 && mem_pro_value <= 30) {
                            $(".mem_usage").after(mem_usage_obj.html());
                            $(".mem_usage").html("");
                        };
                        mem_usage_obj.css("width", mem_pro_width);

                        var mount_container_pro_width = $(".mount_usage_container").css("width").split("px")[0];
                        var mount_usage_obj = $(".mount_usage");
                        for (var x = 0; x < mount_usage_obj.length; x++) {
                            var mount_pro_value = mount_usage_obj[x].innerText.split("%")[0];
                            var mount_pro_width = ((mount_container_pro_width - 4) * (mount_pro_value / 100));
                            if (mount_pro_value >= 0 && mount_pro_value <= 30) {
                                mount_usage_obj[x].after(mount_usage_obj[x].innerText);
                                mount_usage_obj[x].innerText = "";
                            };
                            mount_usage_obj[x].style.width = mount_pro_width + "px";
                        }
                    }, 
                    error: function() {
                        toastr.error("Load host details failed");
                        $(".host_details").hide();
                        $(".overall-mask").hide();
                    }
                });
            };
        }));
    });
})(jQuery);
