$("#submit_btn").attr("disabled", "disabled");


function changeColor(element, color){
    element.css({"color": color, "font-weight": "bold"});
}

function checkpasswords(){
    let mainPassText = $("#main_pass").val();
    let confPassText = $("#conf_pass").val();
    console.log(mainPassText === confPassText)

    if(mainPassText.length >= 8 && confPassText === ''){
        $("#password_message").text("Please, confirm password");
        changeColor($("#password_message"), 'red');
        return;
    }

    if(mainPassText === confPassText){
        if(mainPassText.length >= 8){
            $("#password_message").text("Password is compatible")
            changeColor($("#password_message"), 'green');
            $("#submit_btn").removeAttr("disabled");
        } else{
            $("#password_message").text("Password must contain at least 8 symbols")
            changeColor($("#password_message"), 'red');
        }

    } else{
        $("#password_message").text("Passwords are not equal.")
        changeColor($("#password_message"), 'red');
    }
}

function cleanmessage(){
    $('#username_message').text('');
}