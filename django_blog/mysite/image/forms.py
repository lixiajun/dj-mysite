from django import forms
from django.core.files.base import ContentFile
from slugify import slugify
from urllib import request

from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')

    def clean_url(self):   # clean_<fieldname> 处理某个字段值
        url = self.cleaned_data['url']   # 通过 self.cleand_data来获取数据
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("The given Url does not match valid image extension.")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageForm, self).save(commit=False)   # 建立实例，但是还没有保存数据
        image_url = self.cleaned_data['url']
        image_name = '{0}.{1}'.format(slugify(image.title), image_url.rsplit('.',1)[1].lower())

        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)  # 继承的FileField,有一个save方法，save(name,content,save=True)
        if commit:
            image.save()

        return image
