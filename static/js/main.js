/**
 * Created by Administrator on 2018/1/2.
 */

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // 这些HTTP方法不要求CSRF包含
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
//新增游戏
function submit_game(){
    var keys = ["game_id","game_name","url_update","game_server","game_desc"];
    var data = {}
   for (var i = 0; i < keys.length; i++) {
       var key = keys[i];
       data[key] = document.getElementById(key).value;
    };

    $.post("/add/",data,function (response) {
        if(response['code'] == 0){
            $('#myModal').modal('hide');
            alert(response['msg']);
        }else{
            alert(response['msg']);
        }

    });
}


function addDevice() {

     var data = {}
     data["name"] = document.getElementById("id_input_1").value;
     data["uuid"] = document.getElementById("id_input_2").value;
     data["platform"] = $('#id_radio_platform input:radio:checked').val();

     $.post("/white/",data,function (response) {
        if(response['code'] == 0){
            $('#id_modal_device').modal('hide');
            location.reload();
            alert(response['msg']);
        }else{
            alert(response['msg']);
        }

    });
}


function addGame() {

     var data = {}
     var keys = ["game_id","game_name","update_url","game_server","game_desc"]
    for(var i=0;i<keys.length;++i){
        data[keys[i]] = document.getElementById("id_input_" + (i+1)).value;
    }
     $.post("/game/",data,function (response) {
        if(response['code'] == 0){
            $('#id_modal_device').modal('hide');
            location.reload();
            alert(response['msg']);
        }else{
            alert(response['msg']);
        }

    });
}