(function($) {
    $(document).ready(function() {
        const progress = $("#progress")
        const prev = $("#storage_prev_btn")
        const next = $("#storage_next_btn")
        const circles = $(".setup")

        let currentActive = 1

        var sleep = function(time) {
            return new Promise(resolve => {
                setTimeout(() => {
                    resolve();
                }, time);
            });
        }

        $("#select_all_storages").on("click", function() {
            var check_num = $("tbody td:first-child input").filter(":checked").length;
            if ($(this).attr("checked") == "checked") {
                $(this).attr("checked", false)
                $("tbody td:first-child input").prop("checked", false);
                ChangeButtonStatus()
            } else {
                $(this).attr("checked", true)
                $("tbody td:first-child input").prop("checked", true);
                $("#delete_storage").attr("disabled", false)
                ChangeButtonStatus()
            };
        });

        $("tbody td:first-child input").on("click", function() {
            if ($(this)[0].checked) {
                ChangeButtonStatus()
            } else {
                ChangeButtonStatus()
            };
        });

        var ChangeButtonStatus = function() {
            var check_num = $("tbody td:first-child input").filter(":checked").length;
            if (check_num > 1) {
                $("#delete_storage").attr("disabled", false);
            } else if (check_num <= 0) {
                $("#delete_storage").attr("disabled", true);
                $("#select_all_storages").attr("checked", false);
            } else if (check_num == 1){
                $("#delete_storage").attr("disabled", false); 
            };
        };

        var change_storage_provider_content = function() {
            var storage_type = $(".storage_type select").val();
            if (storage_type == "s3") {
                $(".storage_provider").css("display", "flex");
            } else {
                $(".storage_provider").css("display", "none");
            };
        };

        var update_step_progress = function() {
            circles.each(function(idx, circle) {
                if(idx < currentActive) {
                    circle.addClassName('active');
                } else {
                    circle.removeClassName('active');
                };
            });
        
            const actives = circles.filter(".active");
        
            progress.css("width", (actives.length - 1) / (circles.length - 1) * 100 + '%')
        
            if(currentActive === 1) {
                $(".step01_content").css("display", "block");
                $(".step02_content").css("display", "none");
                $(".step03_content").css("display", "none");
                $("#storage_close_btn").css("display", "inline-block");
                $("#storage_submit_btn").css("display", "none");
                prev.attr("disabled", false);
                prev.css("display", "none");
            } else if(currentActive === circles.length) {
                $(".step01_content").css("display", "none")
                $(".step02_content").css("display", "none")
                $(".step03_content").css("display", "block")
                $("#storage_submit_btn").css("display", "inline-block");
                prev.css("display", "inline-block");
                prev.attr("disable", false);
                next.css("display", "none");
            } else {
                $(".step01_content").css("display", "none");
                $(".step02_content").css("display", "block");
                $(".step03_content").css("display", "none");
                $("#storage_close_btn").css("display", "none");
                $("#storage_submit_btn").css("display", "none");
                prev.css("display", "inline-block");
                prev.attr("disabled", false);
                next.css("display", "inline-block");
                next.attr("disabled", false);
            };
        };

        change_storage_provider_content();

        $(".storage_type select").on("change", function() {
            change_storage_provider_content();
        });

        $(".step01_content :input").on("blur", function() {
            if ($(this).val() == "") {
                $("#storage_next_btn").attr("disabled", true);
            } else {
                $("#storage_next_btn").attr("disabled", false);
            };
        }).keyup(function(){
            $(this).triggerHandler("blur");
        }).focus(function(){
            $(this).triggerHandler("blur");
        });


        next.on("click", function() {
            currentActive++
            
            // 如果是active=2则表示进入了第2个步骤，点击了第一个下一步按钮, 后台获取第二步骤页面内容
            if (currentActive == 2) {
                var formData = new FormData()
                var storage_type = $(".storage_type select").val()
                if (storage_type == "s3") {
                    var storage_provider = $(".storage_provider select").val()
                    formData.append("storage_provider", storage_provider);
                };
                formData.append("storage_type", storage_type);
                var data = formData
                $.ajax({
                    type: "POST",
                    url: "/api/v1.0/storage/type",
                    data: data,
                    processData: false,
                    contentType: false,
                    success: function(data) {
                        $(".step_content").html(data);
                        update_step_progress();
                    },
                    error: function(data) {
                        toastr.error(data.responseText)
                        currentActive--
                    }
                });
            // 如果是active=cirles.length 也就是3，则表示进入了第3个步骤，点击了第二个下一步按钮，后台获取第三步骤页面内容
            } else if (currentActive == circles.length) {

                update_step_progress();
            // 如果是active > cirles.length 也就是 > 3，则表示点击了第二个下一步按钮，这里js做了处理，不会显示下一步按钮，故下面逻辑暂不会触发
            } else if (currentActive > circles.length) {
                currentActive = circles.length;
                update_step_progress();
            };
        });

        prev.on("click", function() {
            currentActive--
            if(currentActive < 1) {
                currentActive = 1
            };
            update_step_progress()
        });

        $("#storage_submit_btn").on("click", function() {
            var storages_data = new FormData()
            $(".setup_content :input").each(function() {
                var storage_key_name = $(this).parent().attr("class");
                var storage_value = $(this).val();
                if ($(this).attr("type") == "checkbox") {
                    var storage_value = $(this).prop("checked")
                };
                storages_data.append(storage_key_name, storage_value);
            });
            $.ajax({
                type: "POST",
                url: "/api/v1.0/storage/add",
                data: storages_data,
                processData: false,
                contentType: false,
                success: function(data) {
                    $("#storage_close_btn").click()
                    toastr.success("Add storage successfully");
                    sleep(300).then(() => {
                        $("#context").html(data);
                    });
                },
                error: function(data) {
                    toastr.error(data.responseText)
                }
            });
        });

        $("#delete_storage").on("click", (function() {
            var obj_parents = $("tbody td:first-child input").filter(":checked").parent()
            var selectdata = {}
            for (var n = 0; n < obj_parents.length; n++) {
                selectdata[n] = obj_parents[n].siblings()[0].innerHTML
            };
            if (confirm("是否确定删除存储?")) {
                $.ajax({
                    type: "POST",
                    url: "/api/v1.0/storage/delete",
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
    });
})(jQuery);