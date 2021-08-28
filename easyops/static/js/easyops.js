function checkpassword() {
	ps1 = document.getElementById("password")
	ps2 = document.getElementById("repassword")
	if (ps1.value == ps2.value) {
		document.getElementById("tips").innerHTML="";
		document.getElementById("repassword").style.borderColor="#ccc"
		document.getElementById("bt_input").style.backgroundColor="#4CAF50";
		document.getElementById("bt_input").disabled = false;
	}
	else {
		document.getElementById("tips").innerHTML="Password Inconsistency";
		document.getElementById("repassword").style.borderColor="#FF0"
		document.getElementById("bt_input").style.backgroundColor="gray";
		document.getElementById("bt_input").disabled = true;
	}
}

(function ($){
	$(document).ready(function(){
		$("#resources_menu").click(function(ev){
			$(".fa-angle-down").toggleClass("hidden");
			$(".fa-angle-up").toggleClass("hidden");
			$("#remote_execute").slideToggle("fast");
			$("#data_sync").slideToggle("fast");
		});
		$("#login_btn").click(function() {
			if ($("#username").val == "" || $("#password").val() == ""){
				$("#tips").html("Empty user name and password");
				return false;
			};
		});
	});
})(jQuery);
