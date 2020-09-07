from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, loader
from django.shortcuts import render
import cv2
import threading
import webcam.improcess as improcess
import json
import base64
import os

BASE_DIR  = os.path.join ( (os.path.abspath(os.path.dirname(os.path.dirname(__file__)))),'webcam')

#use gpio simulator

#use below when run in rasberrypi


#BASE_DIR='D:\\Deeplearning\\django\\marker_detection\\webcam'
event= threading.Event()
event_defect= threading.Event()
image_stream=None
image_stream_display=None
global template_image
image_template =None
global image_template_cropped
image_template_cropped=None

global template_size
global template_width
global horizontal_diff
global vertical_diff
global is_record
global max_record
global record_path
global is_run
is_run=threading.Event()
is_run.set()
#default parameter here
demo=True
record_path ='webcam/record'
is_record =False
max_record=5
horizontal_diff=30
vertical_diff=10
#load parameter here



def SaveParameters():
    global horizontal_diff
    global vertical_diff
    global is_record
    global max_record
    global record_path
    data = {'vertical_diff' : vertical_diff, 'horizontal_diff' : horizontal_diff,'is_record':is_record,'max_record':max_record,'record_path':record_path}
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)
def LoadParameters():
    global horizontal_diff
    global vertical_diff
    global is_record
    global max_record
    global record_path
    if (os.path.exists('data.txt')):
        with open('data.txt') as json_file:
            data = json.load(json_file)
            vertical_diff =int( data['vertical_diff'])
            horizontal_diff =int( data['horizontal_diff'])
            is_record =bool( data['is_record'])
            max_record =int( data['max_record'])
            record_path =str( data['record_path'])
    
    
def GetPath(path,directory=None):
    if (directory is None):
        return os.path.join(BASE_DIR,path)
    else:
        return  os.path.join(os.path.join(BASE_DIR,directory),path)    
def GetDataPath(path):
    return GetPath(path,'data')

if os.path.exists(GetDataPath('template_image.bmp')):
    image_template = cv2.imread(GetDataPath('template_image.bmp'),0)
print(GetDataPath('template_image_cropped.bmp'))
if os.path.exists(GetDataPath('template_image_cropped.bmp')):   
    image_template_cropped = cv2.imread(GetDataPath('template_image_cropped.bmp'),0)

    template_temp,template_size,template_width=improcess.detect_and_get_area_template(image_template_cropped)

def get_image_template_cropped(request):
    if os.path.exists(GetDataPath('template_image_cropped.bmp')):
        image_template_cropped_reload = cv2.imread(GetDataPath('template_image_cropped.bmp'),0)
        ret, image_template_cropped_reload_jpg = cv2.imencode('.jpg', image_template_cropped_reload)
        return HttpResponse(image_template_cropped_reload_jpg.tobytes(),content_type='image/jpeg')
    else:
        return HttpResponse('null')

def setting(request):
    return HttpResponse(loader.get_template('setting.html').render({}, request))
def last_image(request):
    ret, jpeg = cv2.imencode('.jpg', image_stream)
    return HttpResponse(jpeg.tobytes(),content_type='image/jpeg')
def get_image_template(request):
    if os.path.exists(GetDataPath('template_image.bmp')):
        image_template_reload = cv2.imread(GetDataPath('template_image.bmp'))
        ret, jpeg_template_reload = cv2.imencode('.jpg', image_template_reload)
        return HttpResponse(jpeg_template_reload.tobytes(),content_type='image/jpeg')
    else:
        HttpResponse('aaa')
@csrf_exempt
def update_template(request):
    rec=request.POST
    x1=int( float(rec['x1']))
    x2=int(float(rec['x2']))
    y1=int(float(rec['y1']))
    y2=int(float(rec['y2']))
    global image_template
    if (image_template is not None):
        global image_template_cropped
        
        image_template_cropped =image_template[y1:y2,x1:x2]
        cv2.imwrite(GetDataPath('template_image_cropped.bmp'),  image_template_cropped)
        global template_size
        global template_width
        template_temp,template_size,template_width=improcess.detect_and_get_area_template(image_template_cropped)
    return HttpResponse('ok')
@csrf_exempt
def set_current_image_as_template(request):
    if (image_stream is not None):
        cv2.imwrite(GetDataPath('template_image.bmp'),cv2.cvtColor(image_stream,cv2.COLOR_BGR2GRAY))
        global image_template
        image_template= cv2.cvtColor(image_stream,cv2.COLOR_BGR2GRAY)
    return HttpResponse('set current image as template ok')
def online(request):
    return 'aa'
def offline(request):
    return 'aa'


def index(request):
    global vertical_diff
    global horizontal_diff

    return render(request, "index.html", {'vertical_diff_param':vertical_diff , 'horizontal_diff_param':horizontal_diff})
    #return HttpResponse(template.render({}, request))


def history(request):
    images=[]
    if (os.path.exists(record_path)):
        for r, d, f in os.walk(record_path):
            for file in f:
                if '.jpg' in file:
                    image_read= cv2.imread(os.path.join(r, file))
                    if (image_read is not None):
                        ret,image_read_jpg= cv2.imencode('.jpg',image_read)
                        if (ret):                           
                            images.append('data:image/jpeg;base64, ' + base64.b64encode(image_read_jpg).decode('utf-8'))
    
    return render(request, "history.html", {'images': list(images)})
@csrf_exempt
def get_total(request):
    global total
    return HttpResponse(str(total))
@csrf_exempt
def clear_all_image(request):
    if (os.path.exists(record_path)):
        for r, d, f in os.walk(record_path):
            for file in f:
                if '.jpg' in file:
                    os.remove(os.path.join(r, file))
    template = loader.get_template('history.html')
    return HttpResponse(template.render({}, request))

@csrf_exempt   
def set_parameter(request):
    global vertical_diff
    global horizontal_diff
    vertical_diff =int( request.POST['vertical_field'])
    horizontal_diff = int(request.POST['horizontal_field'])
    SaveParameters()
    return HttpResponse('ok')
@csrf_exempt
def set_record_parameter(request):
    global is_record
    global max_record
    global record_path
    is_record =(request.POST['is_record'] is '1')
    max_record = int(request.POST['max_record'])
    record_path =str(request.POST['record_path'])
    if (not os.path.exists(record_path)):
        os.mkdir(record_path)
    SaveParameters()
    return HttpResponse('ok')
@csrf_exempt
def get_parameter(request):
    global vertical_diff
    global horizontal_diff
    data = {'vertical_diff' : vertical_diff, 'horizontal_diff' : horizontal_diff}
    return HttpResponse( json.dumps( data ) )
@csrf_exempt
def get_record_parameter(request):
    global is_record
    global max_record
    global record_path
    data = {'is_record' : is_record, 'max_record' : max_record, 'record_path' : record_path}
    return HttpResponse( json.dumps( data ))
# def stream():
#     cap = cv2.VideoCapture(0) 

#     while True:
#         ret, frame = cap.read()
#         ret, jpeg = cv2.imencode('.jpg', frame)
#         if not ret:
#             print("Error: failed to capture image")
#             break
        
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' +jpeg.tobytes() + b'\r\n')
@csrf_exempt
def reset_counter(request):
    improcess.total=0
    improcess.pass_count=0
    improcess.fail=0
    return HttpResponse('ok')
@csrf_exempt
def set_online(request):
    global is_run
    is_run.set()
    return HttpResponse('ok')
@csrf_exempt
def set_offline(request):
    is_run.clear()
    return HttpResponse('ok')
def video_feed(request):
    return StreamingHttpResponse(gen(), content_type='multipart/x-mixed-replace; boundary=frame')
def video_feed_defect(request):
    return StreamingHttpResponse(gen_last_defect(), content_type='multipart/x-mixed-replace; boundary=frame')
def gen():
    while True:
        global event
        global image_stream_display
        event.wait()   
        event.clear()   
        ret, jpeg = cv2.imencode('.jpg', image_stream_display)
        if ret:
            yield (b'--frame\r\n'
            b'Content-Type:image/jpeg \r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
            b'Content-Type:image/jpeg \r\n\r\n' +  b'\r\n\r\n')

def gen_last_defect():
    while True:
        global event_defect
        global image_last_defect_display
        event_defect.wait() 
        event_defect.clear()     
        ret, jpeg = cv2.imencode('.jpg', image_last_defect_display)
        if ret:
            yield (b'--frame\r\n'
            b'Content-Type:image/jpeg \r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
            b'Content-Type:image/jpeg \r\n\r\n' +  b'\r\n\r\n')



         
path = os.path.join(BASE_DIR,'sample')
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.jpg' in file:
            files.append(os.path.join(r, file))
print('Demo path: '+ path)


def mainloop():
    LoadParameters()
    global is_run
    global event
    global event_defect
    global image_stream
    global total
    global image_stream_display
    global image_last_defect_display
    global horizontal_diff
    global vertical_diff
    global is_record
    global max_record
    global record_path
    current_record_index=0
    if demo:
        import time
        while is_run.wait():
            for f in files:
                image_entry = cv2.imread(f)
                image_stream=image_entry
                image_stream_display,result=improcess.inspection(image_entry,image_template_cropped,template_width,vertical_diff,horizontal_diff)  
                if not result:
                   
                    image_last_defect_display = image_stream_display.copy()
                    event_defect.set()
                    if (is_record):
                        if (current_record_index>max_record):
                            current_record_index=0
                        cv2.imwrite(os.path.join(record_path,str(current_record_index) +'.jpg'), image_stream)
                        current_record_index=current_record_index+1
                event.set()
               
                cv2.waitKey(1)
                time.sleep(1)
                

    vid = cv2.VideoCapture(0)

    
    while is_run.wait():
        retval, image_entry = vid.read()
        if retval:
            image_stream=image_entry
            image_stream_display,result=improcess.inspection(image_entry,image_template_cropped,template_width,vertical_diff,horizontal_diff)   
            if not result:
                image_last_defect_display = image_stream_display.copy()
                event_defect.set() 
                if (is_record):
                    if (current_record_index>max_record):
                        current_record_index=0
                    cv2.imwrite(os.path.join(record_path,str(current_record_index) +'.jpg'), image_stream)
                    current_record_index=current_record_index+1
            event.set()
            cv2.waitKey(1)
# Create your views here.
