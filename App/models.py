from django.db import models
from django.db.models import CASCADE,SET_NULL
import datetime
# Create your models here.

BoolCharacter=(('Y','是'),('N','否'))
# kindType=((',corpInfo,','公司简介'),
#           (',topContact,','联系我们'),
#           (',topApp,','应用'),
#           (',topCase,','案例'),
#           (',topContact,','行业'))
# user type : su pow norm
class BaseModel(models.Model):
    recname = models.CharField('创建人员', max_length=32,blank=True,null=True)
    rectime = models.CharField('创建时间', max_length=19,blank=True,null=True)
    updtime = models.CharField('更新时间', max_length=19,blank=True,null=True)
    remark = models.CharField('备注',blank=True,max_length=50,null=True)

    def __getitem__(self, k):     #  支持对象直接get属性['title']
      if isinstance(k,int):        #  serialize成json报错...why?
        raise Exception("数据库对象参数错误")
      else:
        return self.__getattribute__(k)
    def __setitem__(self, key, value):
        if value == None:
            self.__setattr__(key,None)
        elif issubclass(type(self._meta.get_field_by_name(key)[0]),models.fields.DateTimeField):
            if isinstance(value,str):
                if str == '':
                    self.__setattr__(key,None)
                else:
                    self.__setattr__(key,datetime.datetime.strptime(value,'%Y-%m-%d %H:%M:%S'))
            else:
                raise Exception("日期时间型参数错误")
        elif issubclass(type(self._meta.get_field_by_name(key)[0]),models.fields.DateField):
            if isinstance(value,str):
                if str == '':
                    self.__setattr__(key,None)
                else:
                    self.__setattr__(key,datetime.datetime.strptime(value,'%Y-%m-%d').date())
            else:
                raise Exception("日期型参数错误")
        else:
            self.__setattr__(key, value)
    class Meta:
        abstract = True
class User(BaseModel):
    username = models.CharField('用户',max_length=10,primary_key=True)
    pw = models.CharField('密码',max_length=40)
    usertype = models.CharField('类型',max_length=4)
    def __str__(self):
        return self.username
    class Meta:
        db_table = 'USER'
class ArticleType(BaseModel):
    id = models.CharField('pk',primary_key=True,max_length=32)
    parent = models.ForeignKey('ArticleType',verbose_name='父类型', \
                               related_name='subarticletype',db_column='parent_id',on_delete=CASCADE,
                               blank=True,null=True)
    kind = models.CharField('内部类型名称',max_length=100,blank=True,null=True)
    title = models.CharField('标题',max_length=100,blank=True,null=True)
    link = models.CharField('链接',max_length=200,blank=True,null=True)
    exorder = models.IntegerField('排序',blank=True,null=True)
    exlink = models.CharField('扩展链接',max_length=200,blank=True,null=True)
    extitle = models.TextField('扩展内容')
    exkind = models.CharField('类型标识2',max_length=100,blank=True,null=True)
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'ARTICLETYPE'

class Article(BaseModel):
    id = models.CharField('pk',primary_key=True,max_length=32,db_index=True)
    parent = models.ForeignKey('ArticleType', \
        verbose_name='文章类型',related_name='fk_article',db_column='parent_id', \
        on_delete=SET_NULL,blank=True,null=True,db_index=True)
    kind = models.CharField('内部类型名称',max_length=100,blank=True,null=True)
    title = models.CharField('标题',max_length=100)
    content = models.TextField('内容')
    imglink = models.CharField('标题图片链接',max_length=100,blank=True,null=True)
    videolink = models.CharField('视频链接',max_length=100,blank=True,null=True)
    exorder = models.IntegerField('排序',blank=True,null=True)
    link = models.CharField('链接',max_length=200,blank=True,null=True)
    exlink = models.CharField('扩展链接',max_length=200,blank=True,null=True)
    exkind = models.CharField('类型标识2',max_length=100,blank=True,null=True)
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'ARTICLE'

