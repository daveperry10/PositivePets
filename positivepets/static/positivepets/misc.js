/* client-side functions to populate html select elements for animal shelter page */

function openNewEmailWindow(action, email_id){
    //alert("open");
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