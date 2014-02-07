$(function() {
    var all_ul = $("#accordion").children('ul');
    var active_ul = $("#accordion > ul.active");
    var index = all_ul.index(active_ul);
    $( "#accordion" ).accordion({
        heightStyle: "content",
        active: index
    });
});
