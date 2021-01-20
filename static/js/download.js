let socketio = io(window.location.protocol+'//'+document.domain+':'+location.port);

//events socket

socketio.on('connect',function(){
    socketio.emit('url',{
        url: window.location.href
    })
});

socketio.on('progressbar',function(value){
    if(value.state == "progress"){
        percent = value.value
        //width:${percent}%;
        $('#content-bar').css("width",`${percent}%`);
        $('#measure-bar').text(`${percent}%`);
    }
    else if(value.state == "finish"){
        window.open(`/download/${value.name}`)
    }
});

//events socket
