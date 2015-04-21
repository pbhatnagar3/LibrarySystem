Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
});


var main = function(){

	$( "form input:radio" ).click(function(){
		// alert("yolos war");
	 $('form input:radio:checked').each(function(){
      this.checked = false;  
  });
	 this.checked = true;
		var selected = $("form input[type='radio']:checked");
	if (selected.length > 0) {
    	selectedVal = selected.val();
    	// alert("here is selectedVal" +  selectedVal);
    	$('#selected-book-isbn').val(selectedVal);
	}
	
		
	})

	 $('#hold-request-date').val(
	 	new Date()
	 		.toDateInputValue()
	 		);
	 var estimateReturnDate = new Date();

	 estimateReturnDate.setDate(
	 	estimateReturnDate.getDate() + 17
	 	);
	 $('#estimated-return-date').val(
	 	estimateReturnDate.toDateInputValue()
	 	);
}

$( document ).ready(main);