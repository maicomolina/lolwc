$(document).ready(function() {
    $(".tabs-div").hide();
    $("#tabs-4").show();
})

function tab(tab){
    numTab=tab.value;
    $(".tabs-div").hide();
    $(".tab").removeClass("pestana_opciones_active")
    $(tab).addClass("pestana_opciones_active");
    $("#tabs-"+numTab).show();
}
