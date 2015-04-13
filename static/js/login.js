var main = function(){
	$('#loginBttn').click(function(){
		// console.log('login bttn pressed');
		
		var username = $('#username').val();
		var password = $('#password').val();
		console.log(username, password);
	});

};

$(document).ready(main);