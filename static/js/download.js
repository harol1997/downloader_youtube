let socketio = io();

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
        window.close()
    }
});

//events socket
