
 function load()
{
    var ho_input = document.getElementById('horizontal_name')
    var ve_input =document.getElementById('vertical_name')
    let request = new XMLHttpRequest();
    request.open("GET", 'get_parameter', false);
    request.send(null);
    data = JSON.parse(request.response);
    ho_input.value = data['horizontal_diff'];
    ve_input.value = data['vertical_diff'];
}
function Online()
{
    let request = new XMLHttpRequest();
    request.open("POST", 'set_online', true);
    request.send(null);
}
function Offline()
{
    let request = new XMLHttpRequest();
    request.open("POST", 'set_offline', true);
    request.send(null);
}
function ResetCounter()
{
    let request = new XMLHttpRequest();
    request.open("POST", 'reset_counter', true);
    request.send(null);
}
function change_parameter()
{
    var ho_input = document.getElementById('horizontal_name')
    var ve_input =document.getElementById('vertical_name')
    let request = new XMLHttpRequest();
    data = new FormData();
    data.set('horizontal_field',ho_input.value);
    data.set('vertical_field',ve_input.value);
    request.open("POST", 'set_parameter', true);
    request.send(data);
    
}