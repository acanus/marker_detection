var canvas = document.getElementById("paint");
var ctx = canvas.getContext("2d");
var container=document.getElementById("canvas_container")
var width = canvas.width, height = canvas.height;
var curX, curY, prevX, prevY;
var hold = false;
var fill_value = true, stroke_value = false;
var canvas_data = { "pencil": [], "line": [], "rectangle": [], "circle": [], "eraser": [] };
ctx.lineWidth = 2;
var image = new Image()
image.src= "get_image_template"
var scalex=1
var scaley=1
image.onload=function() {
    canvas.width= image.width;  
    canvas.height=image.height;
    width= canvas.width;
    height=canvas.height;
    scalex=scaley=image.height/canvas.offsetHeight
    ctx.drawImage(image, 0, 0); 
}
 
function onloadparameter()
{
    var is_record = document.getElementById("is_record");
    var max_record = document.getElementById("max_record");
    var record_path = document.getElementById("record_path");

    let request = new XMLHttpRequest();
    request.open("GET", 'get_record_parameter', false);
    request.send(null);
    data = JSON.parse(request.response);
    is_record.checked = Boolean(data['is_record']);
    max_record.value = data['max_record'];
    record_path.value = data['record_path'];
}
function onsetparameter()
{
    var is_record = document.getElementById("is_record");
    var max_record = document.getElementById("max_record");
    var record_path = document.getElementById("record_path");
    let request = new XMLHttpRequest();
    data = new FormData();
    if (is_record.checked)
    {
        data.set('is_record','1');
    }
    else
    {
        data.set('is_record','0');
    }
    
    data.set('max_record',max_record.value);
    data.set('record_path',record_path.value);
    request.open("POST", 'set_record_parameter', true);
    request.send(data);
}
function ChangeTemplate()
{
    let request = new XMLHttpRequest();
    data = new FormData();
    data.set('x1',prevX);
    data.set('y1',prevY);
    data.set('x2',curX+prevX);
    data.set('y2',curY+prevY);
    request.open("POST", 'update_template', true);
    request.send(data);
    location.reload();
}
function setcurrentastemplate()
{
    let request = new XMLHttpRequest();
    request.open("POST", 'set_current_as_template', true);
    request.send("ok");
    location.reload();
}
function getCursorPosition(canvas, event) {
    var x, y;
    
    canoffset = $(canvas).offset();
    x = event.clientX + document.body.scrollLeft + document.documentElement.scrollLeft - Math.floor(canoffset.left);
    y = event.clientY + document.body.scrollTop + document.documentElement.scrollTop - Math.floor(canoffset.top) + 1;
    
    return [x,y];
    }

function rectangle (){
    
    onloadparameter();
    canvas.onmousedown = function (e){
        ctx.drawImage(image, 0, 0);     
        img = ctx.getImageData(0, 0, width, height);
        var pos = getCursorPosition(ctx.canvas,e)
        prevX=pos[0]*scalex;
        prevY=pos[1]*scaley;
       
        hold = true;
    };
            
    canvas.onmousemove = function (e){
        if (hold){
            ctx.putImageData(img, 0, 0);
            var pos = getCursorPosition(ctx.canvas,e);
            curX = pos[0]*scalex- prevX;
            curY = pos[1]*scaley - prevY;
            ctx.strokeRect(prevX, prevY, curX, curY);
            if (fill_value){
                ctx.strokeRect(prevX, prevY, curX, curY);
            }
            // canvas_data.rectangle.push({ "starx": prevX, "stary": prevY, "width": curX, "height": curY, 
            //     "thick": ctx.lineWidth, "stroke": stroke_value, "stroke_color": ctx.strokeStyle, "fill": fill_value,
            //     "fill_color": ctx.fillStyle });
            
        }
    };
            
    canvas.onmouseup = function (e){
        hold = false;
    };
            
    canvas.onmouseout = function (e){
        hold = false;
    };
}