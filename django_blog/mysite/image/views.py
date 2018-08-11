# coding=utf-8
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm
from .models import Image


@login_required(login_url='/account/login/')
@csrf_exempt
@require_POST
def upload_image(request):
    form = ImageForm(data=request.POST)
    print '获取到form'
    if form.is_valid():
        try:
            new_item_info = form.save(commit=False)
            if new_item_info['status'] == 0:
                new_item = new_item_info['image_obj']
                new_item.user = request.user
                new_item.save()
                return JsonResponse({'status': '0'})
            else:
                return JsonResponse({'status': '1001', 'error_info':new_item_info['error_info']})
        except:
            return JsonResponse({'status': '1002'})


@login_required(login_url='/account/login/')
def list_images(request):
    images = Image.objects.filter(user=request.user)
    return render(request, 'image/list_images.html', {'images': images})


@login_required(login_url='/account/login/')
@require_POST
@csrf_exempt
def del_image(request):
    image_id = request.POST['image_id']        # 类似删除的功能，可以写一个通用的类
    try:
        image = Image.objects.get(id=image_id)
        image.delete()
        return JsonResponse({'status': '1'})
    except:
        return JsonResponse({'status': '2'})
