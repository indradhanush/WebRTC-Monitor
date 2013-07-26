var user1 = "end1130723173627";
var pass1 = "testplivowebrtc";
var dest = "end2130723173650@phone.plivo.com";

function webrtcNotSupportedAlert() {
    $('#txtStatus').text("");
    alert("Your browser doesn't support WebRTC. You need Chrome 25 to use this demo");
}

function isNotEmpty(n) {
    return n.length > 0;
}

function formatUSNumber(n) {
    var dest = n.replace(/-/g, '');
    dest = dest.replace(/ /g, '');
    dest = dest.replace(/\+/g, '');
    dest = dest.replace(/\(/g, '');
    dest = dest.replace(/\)/g, '');
    if (!isNaN(dest)) {
        n = dest
        if (n.length == 10 && n.substr(0, 1) != "1") {
            n = "1" + n;
        }
    }
    return n;
}

function replaceAll(txt, replace, with_this) {
    return txt.replace(new RegExp(replace, 'g'),with_this);
}

function initUI() {
    //callbox
    $('#callcontainer').hide();
    $('#btn-container').hide();
    $('#status_txt').text('Waiting login');
    $('#login_box').show();
    $('#logout_box').hide();
}

function callUI() {
    //show outbound call UI
    dialpadHide();
    $('#incoming_callbox').hide('slow');
    $('#callcontainer').show();
    $('#status_txt').text('Ready');
    $('#make_call').text('Call');
}

function IncomingCallUI() {
    //show incoming call UI
    $('#status_txt').text('Incoming Call');
    $('#callcontainer').hide('slow');
    $('#incoming_callbox').show('slow');
}

function callAnsweredUI() {
    $('#incoming_callbox').hide('slow');
    $('#callcontainer').hide('slow');
    dialpadShow();
}


function onReady() {
    console.log("onReady...");
    $('#status_txt').text('Login');
    $('#login_box').show();
}

function login(username, password) {
    Plivo.conn.login(username, password);
}

function logout() {
    Plivo.conn.logout();
}

function onLogin() {
    $('#status_txt').text('Logged in');
    $('#login_box').hide();
    $('#logout_box').show();
    $('#callcontainer').show();
    Plivo.conn.call(dest);
}

function onLoginFailed() {
    $('#status_txt').text("Login Failed");
}

function onLogout() {
    initUI();
}

function onCalling() {
    console.log("onCalling");
    $('#status_txt').text('Call Connecting');
}

function onCallRemoteRinging() {
    $('#status_txt').text('Call In Progress');
}

function onCallAnswered() {
    console.log('onCallAnswered');
    callAnsweredUI();
    $('#status_txt').text('Call In Progress');
}

function onCallTerminated() {
    console.log("onCallTerminated");
    callUI();
}

function onCallFailed(cause) {
    console.log("onCallFailed:"+cause);
    callUI();
    $('#status_txt').text("Call Failed:"+cause);
}

function call() {
    if ($('#make_call').text() == "Call") {
        var dest = $("#to").val();
        if (isNotEmpty(dest)) {
            $('#status_txt').text('Calling..');
            var extraHeaders = {'X-PH-Test1': 'test1', 'X-PH-Test2': 'test2'};
            Plivo.conn.call(dest, extraHeaders);
            $('#make_call').text('End');
        }
        else{
            $('#status_txt').text('Invalid Destination');
        }

    }
    else if($('#make_call').text() == "End") {
        $('#status_txt').text('Ending..');
        Plivo.conn.hangup();
        $('#make_call').text('Call');
        $('#status_txt').text('Ready');
    }
}

function hangup() {
    $('#status_txt').text('Hanging up..');
    Plivo.conn.hangup();
    callUI()
}

function dtmf(digit) {
    console.log("send dtmf="+digit);
    Plivo.conn.send_dtmf(digit);
}
function dialpadShow() {
    $('#btn-container').show();
}

function dialpadHide() {
    $('#btn-container').hide();
}

function mute() {
    Plivo.conn.mute();
    $('#linkUnmute').show('slow');
    $('#linkMute').hide('slow');
}

function unmute() {
    Plivo.conn.unmute();
    $('#linkUnmute').hide('slow');
    $('#linkMute').show('slow');
}

function onIncomingCall(account_name, extraHeaders) {
    console.log("onIncomingCall:"+account_name);
    console.log("extraHeaders=");
    for (var key in extraHeaders) {
        console.log("key="+key+".val="+extraHeaders[key]);
    }
    IncomingCallUI();
}

function onIncomingCallCanceled() {
    callUI();
}

function  onMediaPermission (result) {
    if (result) {
        console.log("get media permission");
    } else {
        alert("you don't allow media permission, you will can't make a call until you allow it");
    }
}

function answer() {
    console.log("answering")
    $('#status_txt').text('Answering....');
    Plivo.conn.answer();
    callAnsweredUI()
}

function reject() {
    callUI()
    Plivo.conn.reject();
}

$(document).ready(function() {
    Plivo.onWebrtcNotSupported = webrtcNotSupportedAlert;
    Plivo.onReady = onReady;
    Plivo.onLogin = onLogin;
    Plivo.onLoginFailed = onLoginFailed;
    Plivo.onLogout = onLogout;
    Plivo.onCalling = onCalling;
    Plivo.onCallRemoteRinging = onCallRemoteRinging;
    Plivo.onCallAnswered = onCallAnswered;
    Plivo.onCallTerminated = onCallTerminated;
    Plivo.onCallFailed = onCallFailed;
    Plivo.onMediaPermission = onMediaPermission;
    Plivo.onIncomingCall = onIncomingCall;
    Plivo.onIncomingCallCanceled = onIncomingCallCanceled;
    Plivo.init({"listen_mode":"False"});
    login(user1, pass1);
});
