(function($) {
    $(document).ready(function() {
        var objectifyForm = function(formArray) {
            var returnArray = {};
            for (var i = 0; i < formArray.length; i++){
               returnArray[formArray[i]["name"]] = formArray[i]["value"];
            };
            return returnArray;
        };

        $("#command_form :input").on("blur", (function() {
            if ($("#exec_cmd").val() == "" || $("#exec_host").val() == "") {
                $("#tips").html("Empty content!")
                $("#exec_btn").attr("disabled", true)
            } else {
                $("#tips").html("")
                $("#exec_btn").attr("disabled", false)
            }
        })).keyup(function(){
            $(this).triggerHandler("blur");
        }).focus(function(){
            $(this).triggerHandler("blur"); 
        });

        $("#exec_btn").on("click", (function() {
            $("#op_box").val("");
            var form = $("#command_form");
            var select_host = $("#remote_hosts").val()
            var formdata = form.serializeArray()
            var formdata = objectifyForm(formdata);
            formdata["host"] = select_host;
            formdata["module"] = "shell";
            var execute_cmd = formdata["cmd"]
            $("#show_cmd").val("CMD: " + execute_cmd)
            $.ajax({
                type: "POST",
                url: "/api/v1.0/execute",
                data: formdata,
                success: function(data) {
                    toastr.success("Send execution command succeeded!");
                    $(".modal-content").html(data);
                    $("#show_cmd").val("CMD: " + execute_cmd)
                },
                error: function() {
                    toastr.error("Send execution command failed!");
                }
            });
        }));
    });
})(jQuery);
