
$('#form-convert').submit(function(event){
    event.preventDefault();
    url = $("#input-url").val()
    url = url.split("=");
    window.open(`downloadh/${url[url.length-1]}`)
});

