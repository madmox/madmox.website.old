$(function() {
    $.fn.selectText = function() {
        if (document.body.createTextRange) { //ms
            var range = document.body.createTextRange();
            range.moveToElementText(this[0]);
            range.select();
        } else if (window.getSelection) { //all others
            var selection = window.getSelection();        
            var range = document.createRange();
            range.selectNodeContents(this[0]);
            selection.removeAllRanges();
            selection.addRange(range);
        }
    }
    $(".selectable").click(function(){
        $(this).selectText();
    }).selectText();
});
