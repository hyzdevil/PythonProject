import json
import hashlib

from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render,HttpResponseRedirect
from rest_framework import viewsets

from Store.models import *
from Store.serializers import *

class GoodsViewSet(viewsets.ModelViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

class GoodsTypeViewSet(viewsets.ModelViewSet):
    queryset = GoodsType.objects.all()
    serializer_class = GoodsTypeSerializer

# Create your views here.
""" 地址选择 """
# 获取省份信息
def getProvince(request):
    provinces = Area.objects.filter(aparent__isnull=True)
    res = []
    for i in provinces:
        res.append([i.id, i.atitle])
    return JsonResponse({"provinces":res})
# 获取市信息
def getCity(request):
    city_id = request.GET.get('city_id')
    cities = Area.objects.filter(aparent_id=city_id)
    res = []
    for i in cities:
        res.append([i.id, i.atitle])
    return JsonResponse({"cities":res})
# 获取县信息
def getDistrict(request):
    district_id = request.GET.get('district_id')
    cities = Area.objects.filter(aparent_id=district_id)
    res = []
    for i in cities:
        res.append([i.id, i.atitle])
    return JsonResponse({'district': res})
# 密码加密功能
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()
# 注册
def register(request):
    result = {"message":""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        apassword = request.POST.get("apassword")
        if username and password and apassword:
            user = Seller.objects.filter(username=username).first()
            if user:
                result["message"] = "用户名已被注册"
                return render(request, 'store/register.html', locals())
            if password == apassword:
                Seller.objects.create(
                    username=username,
                    password=setPassword(password),
                    nickname=username
                )
                return HttpResponseRedirect("/store/login/")
            else:
                result["message"] = "两次输入密码不一致"
        else:
            result["message"] = "注册信息不能为空"
    return render(request, 'store/register.html', locals())
# 登录
def login(request):
    result = {"message": ""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = Seller.objects.filter(username=username).first()
            if user:
                if user.password == setPassword(password):
                    response = HttpResponseRedirect('/store/index/')
                    response.set_cookie("username", json.dumps(username))
                    request.session["username"] = username
                    request.session["user_id"] = user.id
                    return response
                else:
                    result["message"] = "用户名或密码错误"
            else:
                result["message"] = "用户名不存在"
        else:
            result["message"] = "登录信息不能为空"
    return render(request, 'store/login.html', locals())
# 登录验证
def loginValid(fun):
    def inner(request, *args, **kwargs):
        c_name = request.COOKIES.get("username")
        s_name = request.session.get("username")
        if c_name and s_name:
            c_name = json.loads(c_name)
            user = Seller.objects.filter(username=c_name).first()
            if user and user.username == c_name:
                return fun(request, *args, **kwargs)
        return HttpResponseRedirect("/store/login/")
    return inner
# 首页
@loginValid
def index(request):
    return render(request, 'store/index.html', locals())
# 退出
def login_out(request):
    response = HttpResponseRedirect("/store/login/")
    response.delete_cookie("username")
    request.session.flush()
    return response
# 注册店铺
@loginValid
def register_store(request):
    storeType = StoreType.objects.all()
    if request.method == "POST":
        user_id = int(request.session.get("user_id"))
        store_name = request.POST.get("store_name")
        store_description = request.POST.get("store_description")
        store_phone = request.POST.get("store_phone")
        store_money = request.POST.get("store_money")
        store_logo = request.FILES.get("store_logo")
        store_type = request.POST.get("store_type")
        province_id = request.POST.get('province')
        city_id = request.POST.get('city')
        district_id = request.POST.get('district')
        province = Area.objects.get(id=province_id)
        city = Area.objects.get(id=city_id)
        district = Area.objects.get(id=district_id)
        detail = request.POST.get('detail')
        store_address = str(province) + str(city) + str(district) + str(detail)
        store = Store()
        store.store_name = store_name
        store.store_description = store_description
        store.store_phone = store_phone
        store.store_money = store_money
        store.store_logo = store_logo
        store.store_address = store_address
        store.user = Seller.objects.filter(id=user_id).first()
        store.save()
        for i in store_type:
            store.type.add(StoreType.objects.get(id=i))
        store.save()
        return HttpResponseRedirect("/store/index/")
    return render(request, "store/register_store.html", {"storeType":storeType})
# 添加商品
@loginValid
def add_goods(request):
    user_id = request.session.get("user_id")
    store = Store.objects.filter(user_id=user_id)
    goods_type_list = GoodsType.objects.all()
    if request.method == "POST":
        goods_name = request.POST.get("goods_name")
        goods_description = request.POST.get("goods_description")
        goods_price = request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_images = request.FILES.get("goods_images")
        goods_date = request.POST.get("goods_date")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_type = request.POST.get("goods_type")
        store_type = request.POST.get("store_type")
        goods = Goods()
        goods.goods_name = goods_name
        goods.goods_description = goods_description
        goods.goods_price = float(goods_price)
        goods.goods_number = goods_number
        goods.goods_images = goods_images
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_type_id = goods_type
        goods.store_id = store_type
        goods.save()
        return HttpResponseRedirect("/store/list_goods/up/")
    return render(request, 'store/add_goods.html', {"store":store,"type_list":goods_type_list})
# 商品列表
@loginValid
def list_goods(request, state):
    if state == "up":
        status = 1
    else:
        status = 0
    keywords = request.GET.get("keywords","")
    page_num = request.GET.get("page_num", 1)
    store = Store.objects.filter(id=request.session.get("user_id"))
    goods_list = []
    if keywords:
        for i in store:
            goods = i.goods_set.filter(goods_name__contains=keywords, goods_status=status)
            goods_list += goods
    else:
        for i in store:
            goods = i.goods_set.filter(goods_status=status)
            goods_list += goods
    goods_list = list(set(goods_list))
    paginator = Paginator(goods_list, 10)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request, 'store/goods_list.html', locals())
# 商品详情
@loginValid
def goods_detail(request, goods_id):
    # user_id = request.session.get("user_id")
    # store = Store.objects.filter(user_id=user_id)
    goods_type_list = GoodsType.objects.all()
    goods = Goods.objects.filter(id = goods_id).first()
    return render(request, 'store/goods_detail.html', locals())
# 修改商品
@loginValid
def update_goods(request, goods_id):
    user_id = request.session.get("user_id")
    store = Store.objects.filter(user_id=user_id)
    goods = Goods.objects.filter(id = goods_id).first()
    if request.method == "POST":
        goods_name = request.POST.get("goods_name")
        goods_description = request.POST.get("goods_description")
        goods_price = request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_images = request.FILES.get("goods_images")
        goods_date = request.POST.get("goods_date")
        goods_safeDate = request.POST.get("goods_safeDate")
        store_type = request.POST.getlist("store_type")
        goods = Goods.objects.get(id=int(goods_id))
        goods.goods_name = goods_name
        goods.goods_description = goods_description
        goods.goods_price = float(goods_price)
        goods.goods_number = goods_number
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        if goods_images:
            goods.goods_images = goods_images
        goods.save()
        if store_type:
            goods.store_id.clear()
            for i in store_type:
                goods.store_id.add(Store.objects.get(id=i))
        goods.save()
        return HttpResponseRedirect("/store/detail_goods/%s/"%goods_id)
    return render(request, "store/update_goods.html", locals())
# 找回密码
def reset_password(request):
    return render(request, 'store/forgot_password.html')
# 设置商品状态
def set_goods(request, state):
    if state == "up":
        status = 1
    else:
        status = 0
    goods_id = request.GET.get("goods_id")
    referer = request.META.get("HTTP_REFERER")
    if goods_id:
        goods = Goods.objects.get(id = int(goods_id))
        if state == "delete":
            goods.delete()
        else:
            goods.goods_status = status
            goods.save()
    return HttpResponseRedirect(referer)
# 商品类别列表
def goods_type_list(request):
    page_num = request.GET.get("page_num", 1)
    type_list = GoodsType.objects.all()
    paginator = Paginator(type_list, 10)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request, 'store/goods_type_list.html', locals())
# 添加商品类别
def add_goods_type(request):
    if request.method == "POST":
        type_name = request.POST.get("type_name")
        type_description = request.POST.get("type_description")
        type_image = request.FILES.get("type_image")
        GoodsType.objects.create(
            type_name=type_name,
            type_description=type_description,
            type_picture=type_image
        )
    return HttpResponseRedirect("/store/goods_type_list/")
# 删除商品类别
def del_goodsType(request):
    referer = request.META.get("HTTP_REFERER")
    goods_type_id = request.GET.get("goods_type_id")
    GoodsType.objects.filter(id=goods_type_id).delete()
    return HttpResponseRedirect(referer)

def ajax_get_list(request):
    return render(request, 'store/ajax_get_list.html')

# def add(request):
#     goods_list = [
#         ["山楂","核果类水果，核质硬，果肉薄，味微酸涩。果可生吃或作果脯果糕，干制后可入药，是中国特有的药果兼用树种，具有降血脂、血压、强心、抗心律不齐等作用，同时也是健脾开胃、消食化滞、活血化痰的良药，对胸膈脾满、疝气、血淤、闭经等症有很好的疗效。山楂内的黄酮类化合物牡荆素，是一种抗癌作用较强的药物，其提取物对抑制体内癌细胞生长、增殖和浸润转移均有一定的作用。",13.5,600,
#          "store/images/fruit/page_1_2.jpg",
#          "2018-05-24",1,1,1],
#         ["苹果","水果中的一种，是蔷薇科苹果亚科苹果属植物，其树为落叶乔木。苹果营养价值很高，富含矿物质和维生素，含钙量丰富，有助于代谢掉体内多余盐分，苹果酸可代谢热量，防止下半身肥胖。苹果是人们经常食用的水果之一。苹果是一种低热量食物，每100克产生60千卡热量。苹果中营养成分可溶性大，易被人体吸收，故有“活水”之称。它有利于溶解硫元素，使皮肤润滑柔嫩",9.5,600,
#          "store/images/fruit/page_1_3.jpg",
#          "2019-05-24",1,1,1],
#         ["草莓","多年生草本植物。高10-40厘米，茎低于叶或近相等，密被开展黄色柔毛。叶三出，小叶具短柄，质地较厚，倒卵形或菱形，上面深绿色，几无毛，下面淡白绿色，疏生毛，沿脉较密；叶柄密被开展黄色柔毛。聚伞花序，花序下面具一短柄的小叶；花两性；萼片卵形，比副萼片稍长；花瓣白色，近圆形或倒卵椭圆形。聚合果大，宿存萼片直立，紧贴于果实；瘦果尖卵形，光滑。花期4-5月，果期6-7月。",30,600,
#          "store/images/fruit/page_2_7.jpg",
#          "2019-06-24",1,1,1],
#         ["西瓜","一年生蔓生藤本；茎、枝粗壮，具明显的棱。卷须较粗壮，具短柔毛，叶柄粗，密被柔毛；叶片纸质，轮廓三角状卵形，带白绿色，两面具短硬毛，叶片基部心形。雌雄同株。雌、雄花均单生于叶腋。雄花花梗长3-4厘米，密被黄褐色长柔毛；花萼筒宽钟形；花冠淡黄色；雄蕊近离生，花丝短，药室折曲。雌花：花萼和花冠与雄花同；子房卵形，柱头肾形。果实大型，近于球形或椭圆形，肉质，多汁，果皮光滑，色泽及纹饰各式。种子多数，卵形，黑色、红色，两面平滑，基部钝圆，通常边缘稍拱起，花果期夏季。",2.3,600,
#          "store/images/fruit/page_2_19.jpg",
#          "2019-07-24",1,1,1],
#         ["山竹","莽吉柿，俗称山竹。其果肉含丰富的膳食纤维、糖类、维生素及镁、钙、磷、钾等矿物元素。对机体有很好的补养作用，对体弱、病后、营养不良都有很好的调养作用。莽吉柿含有一种特殊物质，具有降燥、清凉解热的作用，这使山竹能克榴莲之燥热。山竹含有丰富的蛋白质和脂类，对机体有很好的补养作用，对体弱、营养不良、病后都有很好的调养作用。",30,600,
#          "store/images/fruit/page_2_21.jpg",
#          "2019-06-24",2,1,1],
#         ["青枣","鲜食肉质脆嫩多汁，甜度高，口感佳，风味独特，单果重100～400克，因而有“热带小苹果”“维生素丸”之美称。鲜枣中的维生素最高243mg/100g,远比猕猴桃的62mg/100g高。维生素C是一种抗氧化剂，有预防缺铁性贫血、促进伤口愈合、预防过敏、降低胆固醇等作用。",5.8,600,
#          "store/images/fruit/page_2_16.jpg",
#          "2019-06-13",1,1,1],
#         ["石榴","石榴是一种浆果，其营养丰富，维生素C比苹果、梨高1~2倍。原产中国西域，汉代传出中原。石榴成熟后，全身都可用，果皮可入药，果实可食用或压汁。性味甘、酸涩、温，具有杀虫、收敛、涩肠、止痢等功效。石榴果实营养丰富，维生素C含量比苹果、梨要高出一二倍。研究发现，石榴含大量的有机酸、糖类、蛋白质、脂肪、维生素以及钙、磷、钾等矿物质。中医认为，石榴具清热、解毒、平肝、补血、活血和止泻功效，适合黄疸性肝炎、哮喘和久泻的患者及经期过长的女性。",15.3,600,
#          "store/images/fruit/page_2_18.jpg",
#          "2019-07-26",1,1,1],
#         ["青提葡萄","提子含丰富的维他命C及E，为皮肤提供抗氧化保护，有效对抗游离基，减轻皮肤受外来环境的侵袭。提子是营养价值很高的果品，特别是含糖量很高。能补诸虚不足，延长寿命。有滋养、健胃、益气功能，适合于虚弱体质者食用，能开胃增进食欲，并有补虚、止呕、镇痛的功效。提子中含有一种抗癌微量元素，可以防止健康细胞癌变，阻止癌细胞扩散。葡萄汁可以帮助器官移植手术患者减少排异反应，促进健康恢复速度。",8.5,600,
#          "store/images/fruit/page_2_26.jpg",
#          "2019-05-24",1,1,1],
#         ["奇异果","猕猴桃，也称奇异果。猕猴桃的质地柔软，口感酸甜。味道被描述为草莓、香蕉、菠萝三者的混合。猕猴桃除含有猕猴桃碱、蛋白水解酶、单宁果胶和糖类等有机物，以及钙、钾、硒、锌、锗等微量元素和人体所需17种氨基酸外，还含有丰富的维生素C、葡萄酸、果糖、柠檬酸、苹果酸、脂肪。",25,600,
#          "store/images/fruit/page_3_8.jpg",
#          "2019-02-24",1,1,1],
#         ["红提葡萄","红提葡萄又名红地球，欧亚种。自我国1987年引入该品种以来，华北及西北大部分地区栽培表现极好，果实品质优，晚熟，耐贮运，丰产，是发展葡萄的首选优质高效品种。食用，有果实品质优，晚熟，耐贮运，丰产特点。",13.5,600,
#          "store/images/fruit/page_3_11.jpg",
#          "2019-07-16",1,1,1],
#         ["丑橘","丑橘：即丑桔、丑柑，学名不知火，又称凸顶柑、丑八怪、丑橙等，是由日本农水省园艺试验场于1972年以清见柑橘与中野3号椪柑杂交育成。营养价值比同类水果高出很多。可以生津止渴，化痰理气，具有着高营养值，高药用价值，是一种不错的具有着平民价位的水果。丑橘的皮晒干后可以入药，放在冰箱里可以除臭。",10,600,
#          "store/images/fruit/page_3_19.jpg",
#          "2019-03-24",1,1,1],
#         ["芒果","芒果为著名热带水果之一，芒果果实含有糖、蛋白质、粗纤维，芒果所含有的维生素A的前体胡萝卜素成分特别高，是所有水果中少见的。其次维生素C含量也不低。矿物质、蛋白质、脂肪、糖类等，也是其主要营养成分。可制果汁、果酱、罐头、腌渍、酸辣泡菜及芒果奶粉、蜜饯等。",13.5,600,
#          "store/images/fruit/page_3_23.jpg",
#          "2019-05-24",1,1,1],
#         ["火龙果","火龙果为热带、亚热带水果，多年生攀援性的多肉植物。火龙果不仅味道香甜，还具有很高的营养价值，它集于水果、花蕾、蔬菜、医药优点于一身。不但营养丰富、功能独特，很少有病虫害，几乎不使用任何农药都可以正常生长。因此，火龙果是一种绿色、环保果品和具有必定疗效的保健养分食品。值得注意的是火龙果的果肉几乎不含果糖和蔗糖，糖分以葡萄糖为主，这种天然葡萄糖，容易吸收，适合运动后食用。在吃火龙果时，可以用小刀刮下内层的紫色果皮——他们可以生吃，也可以凉拌或者像霸王花一样放入汤里。",13.5,600,
#          "store/images/fruit/page_3_27.jpg",
#          "2019-07-14",1,1,1],
#         ["黄梨","晚秋黄梨果糖含量高达16.8，比一般梨要高出很多；它还富含钙、铁、锌、钾等多种微量元素及维生素B和C、胡萝卜素以及苹果酸、柠檬酸等有机酸和果酸。这些成分对于人类非常有益，特别是其所含的天门冬素，对人体健康尤其是肾脏具有特殊的医疗保健功效。黄梨不仅营养丰富，中医学认为梨性为甘寒，有润肺,清心,止咳,消痰,解肺热、火盛、酒毒、胸闷及气短等；",12.5,600,
#          "store/images/fruit/page_4_10.jpg",
#          "2019-06-24",1,1,1],
#         ["香蕉","香蕉属高热量水果，据分析每100克果肉的发热量达91大卡。在一些热带地区香蕉还作为主要粮食。香蕉果肉营养价值颇高，每100克果肉含碳水化合物20克、蛋白质1.2克、脂肪0.6克；此外，还含多种微量元素和维生素。其中维生素A能促进生长，增强对疾病的抵抗力，是维持正常的生殖力和视力所必需；硫胺素能抗脚气病，促进食欲、助消化，保护神经系统；核黄素能促进人体正常生长和发育。香蕉除了能平稳血清素和褪黑素外，它还含有可具有让肌肉松弛效果的镁元素，经常工作压力比较大的朋友可以多食用。",13.5,600,
#          "store/images/fruit/page_4_13.jpg",
#          "2019-06-12",1,1,1],
#         ["血桃","血桃的养分价值血桃有补益气血，养阴生津的作用，可用于大病之后，气血亏虚，面黄肌瘦，心悸气短者；血桃的含铁量较高，是缺铁性贫血病人的理想帮助食物；血桃含钾多，含钠少，合适水肿病人食用；血桃仁有活血化淤，润肠通便作用，可用于闭经跌打损伤等帮助治疗；血桃仁提取物有抗凝血作用，并能克制咳嗽中枢而止咳，同时能使血压降落，可用于高血压病人的帮助治疗。",18,600,
#          "store/images/fruit/page_4_8.jpg",
#          "2019-03-24",1,1,1],
#         ["蓝莓","蓝莓果实中含有丰富的营养成分，尤其富含花青素，它不仅具有良好的营养保健作用，还具有防止脑神经老化、强心、抗癌、软化血管、增强人体免疫等功能。蓝莓栽培最早的国家是美国，但至今也不到百年的栽培史。因为其具有较高的保健价值所以风靡世界，是世界粮食及农业组织推荐的五大健康水果之一。",13.5,600,
#          "store/images/fruit/page_4_7.jpg",
#          "2019-07-09",1,1,1],
#         ["龙眼","龙眼原产于中国南部地区，分布于福建、台湾、海南、广东、广西、云南、贵州、四川等省（区），主产于福建、台湾、广西。生长在南亚热带地区，喜温暖湿润气候，能忍受短期霜冻，在0-4℃的低温条件，短期内不会冻死。经济用途以作果品为主，因其假种皮富含维生素和磷质，有益脾、健脑的作用，故亦入药；种子含淀粉，经适当处理后，可酿酒；木材坚实，甚重，暗红褐色，耐水湿，是造船、家具、细工等的优良材。",26,600,
#          "store/images/fruit/page_5_4.jpg",
#          "2019-07-04",1,1,1],
#         ["荔枝","荔枝分布于中国的西南部、南部和东南部，广东和福建南部栽培最盛。亚洲东南部也有栽培，非洲、美洲和大洋洲有引种的记录。 荔枝与香蕉、菠萝、龙眼一同号称“南国四大果品”。荔枝味甘、酸、性温，入心、脾、肝经；可止呃逆，止腹泻，是顽固性呃逆及五更泻者的食疗佳品，同时有补脑健身，开胃益脾，有促进食欲之功效。因性热，多食易上火。荔枝木材坚实，纹理雅致，耐腐，历来为上等名材。",20,600,
#          "store/images/fruit/page_5_12.jpg",
#          "2019-06-14",1,1,1],
#         ["小黄瓜","小黄瓜含有胡萝卜素、抗坏血酸、硫胺素、核黄素及其他对人体有益的矿物质营养成分。黄瓜有生食、熟食、泡菜等吃法，各种食法都别有风味。 小黄瓜的丙醇和乙醇含量居瓜菜类的首位，主要作用是抑制糖类转变为脂肪，所以有减肥的作用。因含有可抑制糖类转化成脂肪的物质，所以适合有肥胖倾向并爱吃糖类食品的人吃，可抑制糖类的转化和脂肪的积累，达到减肥的目的。黄瓜还是十分有效的天然美容品。鲜黄瓜中所含的黄瓜酶是一种有很强生物活性的生物酶，能有效地促进机体的新陈代谢，扩张皮肤毛细血管，促进血液循环，增强皮肤的氧化还原作用，有令人惊异的润肤美容效果，因此它是很多护肤品的主要原料，市场前景大。",10,600,
#          "store/images/fruit/page_5_15.jpg",
#          "2019-02-14",1,1,1],
#         ["椰子","椰汁及椰肉含大量蛋白质、果糖、葡萄糖、蔗糖、脂肪、维生素B1、维生素E、维生素C、钾、钙、镁等。椰肉色白如玉，芳香滑脆；椰汁清凉甘甜。椰肉、椰汁是老少皆宜的美味佳果。在每100克椰子中，能量达到了900多千焦，蛋白质4克，脂肪12克，膳食纤维4克，另外还有多种微量元素，碳水化合物的含量也很丰富。椰子性味甘、平，入胃、脾、大肠经；果肉具有补虚强壮，益气祛风，消疳杀虫的功效，久食能令人面部润泽，益人气力及耐受饥饿，治小儿涤虫、姜片虫病；椰水具有滋补、清暑解渴的功效，主治暑热类渴，津液不足之口渴；椰子壳油治癣，疗杨梅疮。",13.5,600,
#          "store/images/fruit/page_5_24.jpg",
#          "2019-05-24",1,1,1],
#         ["榴莲","榴莲是热带著名水果之一，原产马来西亚。东南亚一些国家种植较多， 其中以泰国最多。中国广东﹑海南也有种植。榴莲在泰国最负有盛名，被誉为“水果之王”。它的气味浓烈、爱之者赞其香，厌之者怨其臭。榴莲性热，可以活血散寒，缓解痛经，特别适合受痛经困扰的女性食用；它还能改善腹部寒凉的症状，可以促使体温上升，是寒性体质者的理想补品。榴莲营养价值极高，经常食用可以强身健体，健脾补气，补肾壮阳，暖和身体。",20,600,
#          "store/images/fruit/page_7_13.jpg",
#          "2019-05-24",1,1,1],
#     ]
#     for i in goods_list:
#         goods = Goods()
#         goods.goods_name = i[0]
#         goods.goods_description = i[1]
#         goods.goods_price = i[2]
#         goods.goods_number = i[3]
#         goods.goods_images = i[4]
#         goods.goods_date = i[5]
#         goods.goods_safeDate = i[6]
#         goods.goods_type_id = i[7]
#         goods.store_id_id = i[8]
#         goods.save()
#     return HttpResponse("添加成功")