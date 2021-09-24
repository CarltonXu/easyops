(function($) {
    $(document).ready(function() {
        var SearchRemotesType = function(remote_name) {
            var searchObj = $("#sidebar-remote ul li a");
            for (var i = 0; i < searchObj.length; i++){
                var search_obj_name = searchObj[i].innerText.split(": ")[0];
                if (search_obj_name == remote_name) {
                   var remote_type = searchObj[i].innerText.split(": ")[1].replace("(", "").replace(")", "");
                   break;
            }};
            return remote_type;
        };
        
        $(".nav-link").click(function() {
            var remote_name = $(this)[0].innerText.split(":")[0];
            var remote_type = $(this)[0].innerText.split(": ")[1].replace("(", "").replace(")","");
            $.ajax({
                type: "POST",
                url: "/api/v1.0/datasync/" + remote_name + "/",
                data: {"type": remote_type},
                success: function(data) {
                    $("#file_manager_context").html(data);
                },
                error: function(data) {
                    toastr.error("Failed to obtain the page resource!");
                }
            });
        });

        $("body").delegate("table > tbody > tr > td:nth-child(2) > a", "mouseover", function(event) {
            var remote_url = new Array();
            remote_url[0] = $(this).attr("value");
            if (remote_url[0] == "") {
                return
            } else {
                if ($(this).prev().attr("class") == "glyphicon glyphicon-file") {
                    $(this).attr("href", window.document.location.origin + remote_url[0]);
                    $(this).attr("target", "_blank");
                    $(this).attr("value", "");
                };
            };
        });

        $("body").delegate("table > tbody > tr > td:nth-child(2) > a", "click", function() {
            var remote_url = $(this).attr("value");
            var remote_name = remote_url.split("datasync/")[1].split("/")[0]
            var remote_type = SearchRemotesType(remote_name)
            if (remote_url == "") { return };
            $.ajax({
                type: "POST",
                url: remote_url,
                data: {"type": remote_type},
                success: function(data) {
                    $("#file_manager_context").html(data);
                },
                error: function(data) {
                    toastr.error("Failed to obtain the page resource!");
                }
            });
        });

        $("body").delegate("#file_manager_context > p > a", "click", function() {
            var remote_url = $(this).attr("value")
            var remote_name = remote_url.split("datasync/")[1].split("/")[0]
            var remote_type = SearchRemotesType(remote_name)
            $.ajax({
                type: "POST",
                url: remote_url,
                data: {"type": remote_type},
                success: function(data) {
                    $("#file_manager_context").html(data);
                },
                error: function(data) {
                    toastr.error("Failed to obtain the page resource!");
                }
            });
        });
    });
})(jQuery);