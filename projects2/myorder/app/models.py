from django.db import models
from django.utils import timezone #시간정보에 관한 모듈
# Create your models here.
class Order(models.Model):
    # 번호는 pk설정 안하면 장고가 자동으로  id 부여해줌

    ##필드와 필드사이에 컴마 금지###
    
    order_date = models.DateTimeField(default = timezone.now)
    order_text = models.TextField(null = False, blank = False)
    price = models.IntegerField(default=0)
    address = models.CharField(max_length = 30)  
      