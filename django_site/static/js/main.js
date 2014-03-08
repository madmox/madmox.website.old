$(function() {
    var all_ul = $("#accordion").children('ul');
    var active_ul = $("#accordion > ul.active");
    var index = all_ul.index(active_ul);
    if (index == -1) { index = 0; }
    $( "#accordion" ).accordion({
        heightStyle: "content",
        active: index
    });
});
