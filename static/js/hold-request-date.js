Date.prototype.toDateInputValue = (function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0,10);
});


var main = function(){
 $('#hold-request-date').val(new Date().toDateInputValue());
 var estimateReturnDate = new Date();
 estimateReturnDate.setDate(estimateReturnDate.getDate() + 17);
 $('#estimate-return-date').val(estimateReturnDate.toDateInputValue());
}

$( document ).ready(main);