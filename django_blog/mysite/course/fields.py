# coding=utf-8
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):  # 自定义字段属性，继承模型的正整数类型
    def __init__(self, for_fileds=None, *args, **kwargs):
        self.for_fields = for_fileds
        super(OrderField, self).__init__(*args, **kwargs)

    # django 的字段属性类，都继承了Field类，pre_save()就是Field类中的一个方法。
    # pre_save的作用是：在保存之前对数值进行预处理。
    def pre_save(self, model_instance, add):  # 参数和祖先类保持一致，友好型更强。model_instance引用的实例，add为该实例是否是第一次保存
        if getattr(model_instance, self.attname) is None:  # 判断当前对象（实例）是否有某个属性
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    query = {field: getattr(model_instance, field) for field in self.for_fields}  # 得到属性名称
                    qs = qs.filter(**query)
                last_item = qs.latest(self.attname)  # 删选后的最后一条
                value = last_item.order + 1  # 进行序号的编排
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
        else:
            return super(OrderField, self).pre_save(model_instance, add)