var main = function(){
	$('#test').html( 'hi there');
	console.log($('test'));
	$('#test').text( 'hi there');
};

$(document).ready(main);