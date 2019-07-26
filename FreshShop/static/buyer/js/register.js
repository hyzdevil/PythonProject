$(function() {

	var error_name = false;
	var error_password = false;
	var error_check_password = false;
	var error_email = false;
	var error_check = false;

	$('#user_name').blur(function () {
		check_user_name();
		check_all();
	});

	$('#pwd').blur(function () {
		check_pwd();
		check_all();
	});

	$('#cpwd').blur(function () {
		check_cpwd();
		check_all();
	});

	$('#email').blur(function () {
		check_email();
		check_all();
	});

	$('#allow').click(function () {
		if ($(this).is(':checked')) {
			error_check = false;
			$(this).siblings('span').hide();
		} else {
			error_check = true;
			$(this).siblings('span').html('请勾选同意');
			$(this).siblings('span').show();
			$('#submit').attr("disabled", true);
			$('#submit').css({"background-color": "gray"});
		}
		check_all();
	});

	function check_user_name() {
		var len = $('#user_name').val().length;
		if (len < 5 || len > 20) {
			$('#user_name').next().html('请输入5-20个字符的用户名');
			$('#user_name').next().show();
			error_name = true;
			$('#submit').attr("disabled", true);
			$('#submit').css({"background-color": "gray"});
		} else {
			$.ajax({
				url: "/buyer/ajaxValid/name/?username=" + $("#user_name").val(),
				type: "get",
				data: "",
				success: function (data) {
					if (data.message) {
						error_name = true;
						$('#user_name').next().html(data.message);
						$('#user_name').next().show();
						$('#submit').attr("disabled", true);
						$('#submit').css({"background-color": "gray"});
					} else {
						$('#user_name').next().hide();
						error_name = false;
					}
				},
				error: function (error) {
					console.log(error)
				}
			});
		}
	}

	function check_pwd() {
		var len = $('#pwd').val().length;
		if (len < 8 || len > 20) {
			$('#pwd').next().html('密码最少8位，最长20位');
			$('#pwd').next().show();
			error_password = true;
			$('#submit').attr("disabled", true);
			$('#submit').css({"background-color": "gray"});
		} else {
			$('#pwd').next().hide();
			error_password = false;
		}
	}

	function check_cpwd() {
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if (pass != cpass) {
			$('#cpwd').next().html('两次输入的密码不一致');
			$('#cpwd').next().show();
			error_check_password = true;
			$('#submit').attr("disabled", true);
			$('#submit').css({"background-color": "gray"});
		} else {
			$('#cpwd').next().hide();
			error_check_password = false;
		}

	}

	function check_email() {
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

		if (re.test($('#email').val())) {
			$.ajax({
				url: "/buyer/ajaxValid/email/?email=" + $("#email").val(),
				type: "get",
				data: "",
				success: function (data) {
					if (data.message) {
						error_name = true;
						$('#email').next().html(data.message);
						$('#email').next().show();
						$('#submit').attr("disabled", true);
						$('#submit').css({"background-color": "gray"});
					} else {
						$('#email').next().hide();
						error_name = false;
					}
				},
				error: function (error) {
					console.log(error)
				}
			});
		} else {
			$('#email').next().html('你输入的邮箱格式不正确');
			$('#email').next().show();
			error_check_password = true;
			$('#submit').attr("disabled", true);
			$('#submit').css({"background-color": "gray"});
		}

	}

	function check_all() {
		if (error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false) {
			$('#submit').attr("disabled", false);
			$('#submit').css({"background-color": "#47aa34"});
		}
	}
});
