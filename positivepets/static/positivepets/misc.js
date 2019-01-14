/* client-side functions to populate html select elements for animal shelter page */

function openNewEmailWindow(action, email_id){
    if (action == 'reply'){
        window.open("/positivepets/email/compose/reply/" + email_id + "/","New Mail", "width:20, height:20");
    }
    else if (action == 'reply_all'){
        window.open("/positivepets/email/compose/reply-all/" + email_id + "/","Reply All", "width:20, height:20");
    }
    else{
        window.open("/positivepets/email/compose/none/" + email_id + "/","Reply", "width:20, height:20");
    }
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}


//values of redirect can be (chat|email|profile|pet_detail))
function myChangeFunction(pet_id,redirect){
    var http = new XMLHttpRequest();
    var group_id = document.getElementById("new_active_group").value
    var csrftoken = getCookie('csrftoken');
    if(redirect == 'pet_detail'){
        var url = '/positivepets/profile/change_active_group/' + redirect + '/' + pet_id + '/';
    }
    else{
        var url = '/positivepets/profile/change_active_group/' + redirect + '/1/';
    }


    var data = 'active_friend_group=' + group_id;

    http.open('POST', url, true);
    http.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
    http.setRequestHeader("X-CSRFToken", csrftoken);

    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {
            location.reload();
        }
    }

    http.send(data);

}