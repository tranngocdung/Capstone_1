from .serializers import *
from .models import *
from django.http import HttpRequest
from django.db.models import Q
from .serializers import *
from operator import itemgetter

from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime

def convert_time(time):
    time = str(time)[:5]
    h,s = time.split(":")
    return (int(h)*100+int(s))/100

def check_time(a, b, time, clock):
    for i in range(0, len(time)):
        if a < clock[0] or b > clock[len(clock)-1]: 
            return False
        if a < clock[i] <= b:
            if time[i] == 1:
                return False
    return True

def get_base_url(request):
    absolute_url = HttpRequest.build_absolute_uri(request)
    base_url = absolute_url.split(request.get_full_path())[0]
    return base_url

# API for User
class RestaurantHotAPI(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Restaurant.objects.filter(is_hot=True)
    serializer_class = RestaurantSerializers
    permission_classes = [permissions.AllowAny]
    lookup_field = 'rid'

    def get(self, request, *args, **kwargs):
        rid = kwargs.get('rid')
        if rid is None:
            queryset = self.get_queryset()
            serialize = self.serializer_class(queryset, many=True, context={'request': request})

            return Response({'success': True,
                             'message': 'Get list restaurant hot successfully.',
                             'data': serialize.data
                             }, status=status.HTTP_200_OK)
        else:
            instance = self.get_object()
            serialize = RestaurantSerializers(instance, context={'request': request})
            return Response({'success': True,
                             'message': 'Get detail restaurant hot successfully.',
                             'data': serialize.data
                             }, status=status.HTTP_200_OK)


class RestaurantAPI(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializers
    permission_classes = [permissions.AllowAny]
    lookup_field = 'rid'

    def get(self, request, *args, **kwargs):
        rid = kwargs.get('rid')
        if rid is None:
            queryset = self.get_queryset()
            serialize = self.serializer_class(queryset, many=True, context={'request': request})
            return Response({'success': True,
                             'message': 'Get list restaurants successfully.',
                             'data': serialize.data
                             }, status=status.HTTP_200_OK)
        else:
            instance = self.get_object()
            serialize = RestaurantSerializers(instance, context={'request': request})
            return Response({'success': True,
                             'message': 'Get detail restaurant successfully.',
                             'data': serialize.data
                             }, status=status.HTTP_200_OK)


class DishesHotAPI(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Dish.objects.filter(featured=True)
    serializer_class = DishesSerializers
    permission_classes = [permissions.AllowAny]
    lookup_field = 'did'

    def get(self, request, *args, **kwargs):
        did = kwargs.get('did')
        if did is None:
            query_set = self.get_queryset()
            serialize = self.serializer_class(query_set, context={'request': request}, many=True)
            return Response({'success': True,
                             'message': 'Get list dish featured successfully.',
                             'data': serialize.data
                             }, status=status.HTTP_200_OK)
        else:
            instance = self.get_object()
            serialize = DishesSerializers(instance, context={'request': request})
            return Response({'success': True,
                             'message': 'Get detail dish featured successfully.',
                             'data': serialize.data
                             }, status=status.HTTP_200_OK)


class DishesAPI(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishesSerializers
    permission_classes = [permissions.AllowAny]
    lookup_field = 'did'

    def get(self, request, *args, **kwargs):
        did = kwargs.get('did')
        if did is None:
            query_set = self.get_queryset()
            serialize = self.serializer_class(query_set, context={'request': request}, many=True)
            return Response({'success': True,
                             'message': 'Get list dish successfully.',
                             'data': serialize.data
                             }, status=status.HTTP_200_OK)
        else:
            instance = self.get_object()
            serialize = DishesSerializers(instance, context={'request': request})
            return Response({'success': True,
                             'message': 'Get detail dish successfully.',
                             'data': serialize.data
                             }, status=status.HTTP_200_OK)


class CategoryAPI(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        serialize = self.serializer_class(query_set, many=True, context={'request': request})
        return Response({'success': True,
                         'message': 'Get category successfully.',
                         'data': serialize.data
                         }, status=status.HTTP_200_OK)


@api_view(['GET'])
def dish_by_category(request, *args, **kwargs):
    category = Category.objects.get(cid=kwargs.get('cid'))
    restaurant = Restaurant.objects.get(rid=kwargs.get('rid'))
    data = Dish.objects.filter(category=category, restaurant=restaurant)
    serialize = DishesSerializers(data, many=True, context={'request': request})
    return Response({'success': True,
                     'message': 'Get dishes successfully.',
                     'data': serialize.data
                     }, status=status.HTTP_200_OK)


@api_view(['GET'])
def dishes_of_restaurant(request, *args, **kwargs):
    rid = kwargs.get('rid')
    restaurant = Restaurant.objects.get(rid=rid)
    dishes = Dish.objects.filter(restaurant=restaurant)
    serialize = DishesSerializers(dishes, many=True, context={'request': request})

    return Response({'success': True,
                     'message': 'Get dishes successfully.',
                     'data': serialize.data
                     }, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_like(request, *args, **kwargs):
    uid = kwargs.get('uid')
    user = User.objects.get(id=uid)
    data = Wishlist.objects.filter(user=user)
    serialize = WishlistSerializers(data, many=True, context={'request': request})
    return Response({'success': True,
                     'message': 'Get restaurant successfully.',
                     'data': serialize.data
                     }, status=status.HTTP_200_OK)


@api_view(['POST'])
def check_order(request, **kwargs):
    rid = kwargs.get('rid')
    tid = request.data.get('tid')
    table = Table.objects.get(tid=tid)
    restaurant = Restaurant.objects.get(rid=rid)
    time_from = int(str(restaurant.time_open)[:2])
    time_to = int(str(restaurant.time_close)[:2])
    in_time = []
    out_time = []
    clock = []
    time = []

    # Khoi tao cay thoi gian cho nha hang
    for i in range(time_from, time_to):
        clock.append(i)
        clock.append(i + 0.15)
        clock.append(i + 0.30)
        clock.append(i + 0.45)
    clock.append(time_to)

    # Lay thoi gian toi -> ve cua Order co san 
    time_now = request.data.get('order_date')
    orders = Order.objects.filter(table=table, order_date=time_now)
    for order in orders:
        in_time.append(convert_time(order.time_from))
        out_time.append(convert_time(order.time_to))

    # Khoi tao lich đã có Order(1) va chua có Order(0)
    for i in clock: 
        time.append(0)
    for i in range(0, len(in_time)):
        for j in range(0, len(clock)):
            if (clock[j] > in_time[i]) and (clock[j] <= out_time[i]):
                time[j] = 1

    # Check Order moi them vao co hop le ko
    new_from = convert_time(request.data.get('time_from'))
    new_to = convert_time(request.data.get('time_to'))
    print(time_from, time_to)
    print(clock)
    print(time)
    print(in_time)
    print(out_time)
    print(new_from, new_to)
    if check_time(new_from, new_to, time, clock) == True:
        return Response({'success': True,
                            'message': 'Order valid.'
                            }, status=status.HTTP_200_OK)
    return Response({'success': False,
                            'message': 'Please choice other Table or Time from or Time to!'
                            }, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_order(request, *args, **kwargs):
    uid = kwargs.get('uid')
    rid = kwargs.get('rid')
    user = User.objects.get(id=uid)
    tid = request.data.get('tid')
    table = Table.objects.get(tid=tid)
    restaurant = Restaurant.objects.get(rid=rid)
    items = request.data.get("items")
    serialize = OrderSerializers(data=request.data, context={'request': request})

    if serialize.is_valid(raise_exception=True):
        order = serialize.save(user=user, table=table, restaurant=restaurant)
        for item in items:
            dish = Dish.objects.get(did=item['did'])
            OrderItem.objects.create(
                order=order,
                invoice_no="invoice_no_%s" %(order.id),
                quantity=item['quantity'],
                total=item['total'],
                dish=dish
            )
        return Response({'success': True,
                        'message': 'Order restaurant successfully.',
                        'data': serialize.data
                        }, status=status.HTTP_200_OK)
        
    else: return Response({'success': False,
                         'message': 'Error!'
                         }, status=status.HTTP_200_OK)


@api_view(['POST'])
def search_restaurant(request, *args, **kwargs):
    q = request.POST.get('q')
    restaurants = Restaurant.objects.filter(title__contains=q)
    serialize = RestaurantSerializers(restaurants, many=True, context={'request': request})
    return Response({'success': True,
                     'message': 'Search restaurant successfully.',
                     'data': serialize.data
                     }, status=status.HTTP_200_OK)


@api_view(['GET'])
def add_like(request, *args, **kwargs):
    uid = kwargs.get('uid')
    rid = kwargs.get('rid')
    user = User.objects.get(id=uid)
    restaurant = Restaurant.objects.get(rid=rid)
    wishlist = Wishlist.objects.filter(user=user, restaurant=restaurant)
    
    if not wishlist.exists():
        restaurant.like = int(restaurant.like) +1
        restaurant.save()
        Wishlist.objects.create(user=user, restaurant=restaurant)
        wishlist = Wishlist.objects.filter(user=user)
        serialize = WishlistSerializers(wishlist, many=True, context={'request': request})
        return Response({'success': True,
                         'message': 'Add like successfully.',
                         'data': serialize.data
                         }, status=status.HTTP_200_OK)
    return Response({'success': False,
                     'message': 'Added previously!'
                     }, status=status.HTTP_200_OK)


@api_view(['GET'])
def delete_like(request, *args, **kwargs):
    uid = kwargs.get('uid')
    rid = kwargs.get('rid')
    user = User.objects.get(id=uid)
    restaurant = Restaurant.objects.get(rid=rid)
    wishlist = Wishlist.objects.filter(user=user, restaurant=restaurant)
    if wishlist.exists():
        restaurant.like = int(restaurant.like) - 1
        restaurant.save();
        wishlist.delete()
        wishlist = Wishlist.objects.filter(user=user)
        serialize = WishlistSerializers(wishlist, many=True, context={'request': request})
        return Response({'success': True,
                         'message': 'Delete like successfully.',
                         'data': serialize.data
                         }, status=status.HTTP_200_OK)
    return Response({'success': False,
                     'message': 'Like not exists!'
                     }, status=status.HTTP_200_OK)


@api_view(['POST'])
def edit_profile(request, *args, **kwargs):
    uid = kwargs.get('uid')
    user = User.objects.get(id=uid)
    if 'address' in request.POST and request.POST['address']:
        try:
            address = Address.objects.get(user=user)
            address.address = request.POST.get('address')
            address.save()
        except Address.DoesNotExist:
            address = Address.objects.create(user=user, address=request.POST.get('address'))
    
    if 'image' in request.FILES and request.FILES['image']:
        user.image = request.FILES['image']
    elif not user.image:
        user.image = user.image
    
    if 'phone' in request.POST and request.POST['phone']:
        user.phone = request.POST.get('phone')
    
    if 'full_name' in request.POST and request.POST['full_name']:
        user.full_name = request.POST.get('full_name')
    user.verified = True
    user.save()
    
    response_data = {
        'success': True,
        'message': 'Edit profile successfully.',
        'data': {
            'id': user.id,
            'username': user.username,
            'full_name': user.full_name,
            'email': user.email,
            'phone': user.phone,
            'is_active': user.is_active,
            'date_joined': user.date_joined,
            'address': address.address,
            'verified': user.verified,
            'avatar': get_base_url(request) + (user.image.url if user.image else ''),
        }
    }
    
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_profile(request, *args, **kwargs):
    uid = kwargs.get('uid')
    try:
        user = User.objects.get(id=uid)
        try:
            address = Address.objects.get(user=user)
            return Response({'success': True,
                        'message': 'Get profile successfully.',
                        'data': {
                            'id': user.id,
                            'username': user.username,
                            'full_name': user.full_name,
                            'email': user.email,
                            'phone': user.phone,
                            'is_active': user.is_active,
                            'date_joined': user.date_joined,
                            'address': address.address,
                            'verified': user.verified,
                            'avatar': get_base_url(request) + user.image.url,
                        }
                        }, status=status.HTTP_200_OK)
        except Address.DoesNotExist:
            return Response({'success': True,
                        'message': 'Get profile successfully.',
                        'data': {
                            'id': user.id,
                            'username': user.username,
                            'full_name': user.full_name,
                            'email': user.email,
                            'phone': user.phone,
                            'is_active': user.is_active,
                            'date_joined': user.date_joined,
                            'address': "Not have",
                            'verified': user.verified,
                            'avatar': get_base_url(request) + user.image.url,
                        }
                        }, status=status.HTTP_200_OK)
    except: return Response({'success': False,
                        'message': 'User is not exist!'
                        }, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def order_detail(request, *args, **kwargs):
    oid = kwargs.get('oid')
    order = Order.objects.get(oid=oid)
    order_item = OrderItem.objects.filter(order=order)
    serialize = OrderItemSerializers(order_item, many=True, context={'request': request})
    return Response({'success': True,
                     'message': 'Get detail order successfully.',
                     'data': serialize.data
                     }, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_order(request, *args, **kwargs):
    uid = kwargs.get('uid')
    user = User.objects.get(id=uid)
    orders = Order.objects.filter(user=user)
    serialize = OrderSerializers(orders, many=True, context={'request': request})
    return Response({'success': True,
                     'message': 'Get list order successfully.',
                     'data': serialize.data
                     }, status=status.HTTP_200_OK)


@api_view(['POST'])
def manage_order_by_date(request, *args, **kwargs):
    rid = kwargs.get('rid')
    date = request.data.get("date")
    restaurant = Restaurant.objects.get(rid=rid)
    orders = Order.objects.filter(restaurant=restaurant, order_date=date)
    serialize = OrderSerializers(orders, many=True, context={'request': request})
    return Response({'success': True,
                     'message': 'Get list order successfully.',
                     'data': serialize.data
                     }, status=status.HTTP_200_OK)


@api_view(['GET'])
def bill_order(request, *args, **kwargs):
    oid = kwargs.get('oid')
    order = Order.objects.get(oid=oid)
    orders = OrderItem.objects.filter(order=order)
    serialize = OrderSerializers(order)
    serialize2 = OrderItemSerializers(orders, many=True, context={'request': request})
    return Response({'success': True,
                     'message': 'Get list order successfully.',
                     'data': {
                         'order': serialize.data,
                         'orderItems': serialize2.data
                     }
                    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def cancel_order(request, **kwargs):
    oid = kwargs.get('oid')
    try:
        order = Order.objects.get(oid=oid)
        order.product_status = "cancel"
        order.save()
        return Response({'success': True,
                         'message': 'Cancel order successfully.'
                         }, status=status.HTTP_200_OK)
    except:
        return Response({'success': False,
                         'message': 'Order not exists!'
                         }, status=status.HTTP_200_OK)


@api_view(['POST'])
def search_dishes(request):
    q = request.POST.get('q')
    dishes = Dish.objects.filter(title__contains=q)
    serialize = DishesSerializers(dishes, many=True, context={'request': request})
    return Response({'success': True,
                     'message': 'Search dishes successfully.',
                     'data': serialize.data
                     }, status=status.HTTP_200_OK)


@api_view(['GET'])
def friend_chat(request, *args, **kwargs):
    uid = kwargs.get('uid')
    result=[]
    user = User.objects.get(id=uid)
    friends = User.objects.filter(is_staff=False).exclude(id=uid)
    for friend in friends:
        friend_instance = User.objects.get(id=friend.id)
        print(friend.id)
        data_ok = ChatMessage.objects.filter(
            (Q(msg_sender=user) & Q(msg_receiver=friend_instance)) |
            (Q(msg_sender=friend_instance) & Q(msg_receiver=user))
        ).order_by('-date')
        if data_ok.exists():
            final_data = MessageSerializer(data_ok[0], context={'request': request}).data
            result.append(final_data)
    result_sorted = sorted(result, key=itemgetter('date'), reverse=True)

    return Response({'success': True,
        'message': 'Search successfully.',
        'data': result_sorted
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_review(request, *args, **kwargs):
    uid = kwargs.get("uid")
    rid = kwargs.get("rid")
    review = request.data.get('review')
    rating = request.data.get('rating')
    print(uid, rid, review, rating)
    user = User.objects.get(id=uid)
    restaurant = Restaurant.objects.get(rid=rid)
    print(user, restaurant)
    restaurantReview = RestaurantReview.objects.filter(
        user=user, 
        restaurant=restaurant
    )

    if restaurantReview is None:
        RestaurantReview.objects.create(
            user=user, 
            restaurant=restaurant, 
            review=review, 
            rating=rating
        )
        return Response({'success': True,
        'message': 'Review successfully.'
        }, status=status.HTTP_200_OK)

    return Response({'success': False,
        'message': 'Already evaluated!'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def contact_us(request, *args, **kwargs):
    serialize = ContactUsSerializers(data=request.data)
    if serialize.is_valid():
        serialize.save()
        return Response({'success': True,
                         'message': 'Send response successfully.',
                         'data': serialize.data
                         }, status=status.HTTP_200_OK)
    return Response({'success': False,
                     'message': 'Send response fail.'
                     }, status=status.HTTP_200_OK)

@api_view(['GET'])
def detail_table(request, *args, **kwargs):
    tid = kwargs.get('tid');
    table = Table.objects.get(tid=tid)
    serialize = TableSerializers(table)
    return Response({'success': True,
                     'message': 'Get success.',
                     'data': serialize.data
                     }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_order_cart_res(request, *args, **kwargs):
    rid = kwargs.get('rid')
    uid = kwargs.get('uid')
    try:
        restaurant = Restaurant.objects.get(rid=rid)
        user = User.objects.get(id=uid)
        order_cart = OrderCart.objects.get(restaurant=restaurant, user=user)
        serialize = OrderCartSerializers(order_cart)
        order_cart_item = OrderCartItem.objects.filter(ordercart=order_cart)
        serialize2 = OrderCartItemsSerializers(order_cart_item, many=True, context={'request': request})
        return Response({'success': True,
                        'message': 'Get success.',
                        'data': {
                            "order": serialize.data,
                            "orderDetail": serialize2.data
                        }
                        }, status=status.HTTP_200_OK)
    except: return Response({'success': False,
                        'message': 'Get fail.',
                        }, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def add_order_cart(request, *args, **kwargs):
    rid = kwargs.get('rid')
    uid = kwargs.get('uid')
    items = request.data.get("items")
    tid = request.data.get('tid')
    table = Table.objects.get(tid=tid)
    user = User.objects.get(id=uid)
    restaurant = Restaurant.objects.get(rid=rid)
    serialize = OrderCartSerializers(data=request.data, context={'request': request})
    if serialize.is_valid():
        order_cart = serialize.save(user=user, table=table, restaurant=restaurant)
        for item in items:
            dish = Dish.objects.get(did=item['did'])
            OrderCartItem.objects.create(
                ordercart=order_cart,
                dish=dish,
                quantity=item['quantity']
            )
        order_cart_item = OrderCartItem.objects.filter(ordercart=order_cart);
        serialize2 = OrderCartItemsSerializers(order_cart_item, many=True, context={'request': request});

        return Response({'success': True,
                         'message': 'Order restaurant successfully.',
                        #  'data': serialize.data
                        'data': {
                            "order": serialize.data,
                            "orderDetail": serialize2.data
                        }
                         }, status=status.HTTP_200_OK)
    else:
        return Response({'success': False,
                         'message': 'Error!'
                         }, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_order_cart(request, *args, **kwargs):
    rid = kwargs.get('rid')
    uid = kwargs.get('uid')
    tid = request.data.get('tid')
    table = Table.objects.get(tid=tid)
    user = User.objects.get(id=uid)
    restaurant = Restaurant.objects.get(rid=rid)
    order_cart = OrderCart.objects.get(user=user, restaurant=restaurant)
    order_cart.table = table
    order_cart.full_name = request.data.get('full_name')
    order_cart.phone = request.data.get('phone')
    order_cart.time_from = request.data.get('time_from')
    order_cart.time_to = request.data.get('time_to')
    order_cart.number_people = request.data.get('number_people')
    items = request.data.get('items')
    order_cart.save();
    serialize = OrderCartSerializers(order_cart)

    ordercart_items = OrderCartItem.objects.filter(ordercart=order_cart)
    ordercart_items.delete()
    for item in items:
        dish = Dish.objects.get(did=item['did'])
        OrderCartItem.objects.create(
            ordercart=order_cart,
            dish=dish,
            quantity=item['quantity']
        )
    order_cart_item = OrderCartItem.objects.filter(ordercart=order_cart);
    serialize2 = OrderCartItemsSerializers(order_cart_item, many=True, context={'request': request});

    return Response({'success': True,
                     'message': 'Update successfully.',
                     'data': {
                        "order": serialize.data,
                        "orderDetail": serialize2.data
                    }
                    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def delete_order_cart(request, *args, **kwargs):
    rid = kwargs.get('rid')
    uid = kwargs.get('uid')
    user = User.objects.get(id=uid)
    restaurant = Restaurant.objects.get(rid=rid);
    order_cart = OrderCart.objects.filter(user=user, restaurant=restaurant);
    order_cart.delete()
    return Response({'success': True,
                         'message': 'Delete successfully.'
                         }, status=status.HTTP_200_OK)


# API for Restaurant
@api_view(['POST'])
def add_restaurant(request, *args, **kwargs):
    uid = kwargs.get('uid')
    user = User.objects.get(id=uid)
    serialize = RestaurantSerializers(data=request.data, context={'request': request})
    if serialize.is_valid():
        serialize.save(user=user)
        return Response({'success': True,
                         'message': 'Add restaurant successfully.',
                         'data': serialize.data
                         }, status=status.HTTP_200_OK)

    return Response({'success': False,
                     'message': 'Add restaurant fail.',
                     }, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_category(request, *args, **kwargs):
    serialize = CategorySerializers(data=request.data)
    if serialize.is_valid():
        serialize.save()
        return Response({'success': True,
                         'message': 'Add category successfully.',
                         }, status=status.HTTP_200_OK)
    return Response({'success': False,
                     'message': 'Add category fail.',
                     }, status=status.HTTP_200_OK)


@api_view(['GET'])
def delete_category(request, *args, **kwargs):
    cid = kwargs.get('cid')
    try:
        category = Category.objects.get(cid=cid)
        category.delete()
        return Response({'success': True,
                         'message': 'Delete category successfully.'
                         }, status=status.HTTP_200_OK)
    except:
        return Response({'success': False,
                         'message': 'Category not exists!',
                         }, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_category(request, *args, **kwargs):
    cid = kwargs.get('cid')
    category = Category.objects.get(cid=cid)
    category.title = request.data.get('title')
    category.image = request.FILES.get('image')
    category.save()
    return Response({'success': True,
                     'message': 'Update category successfully.',
                     }, status=status.HTTP_200_OK)


@api_view(['GET'])
def wishlist_restaurant(request, *args, **kwargs):
    rid = kwargs.get('rid')
    restaurant = Restaurant.objects.get(rid=rid)
    wishlist = Wishlist.objects.filter(restaurant=restaurant)
    serialize = WishlistRestaurantSerializers(wishlist, many=True, context={'request': request})
    return Response({'success': True,
                     'message': 'Get wishlist successfully.',
                     'data': serialize.data
                     }, status=status.HTTP_200_OK)


@api_view(['GET'])
def review_restaurant(request, *args, **kwargs):
    rid = kwargs.get("rid")
    restaurant = Restaurant.objects.get(rid=rid)
    reviews = RestaurantReview.objects.filter(restaurant=restaurant)
    serialize = RestaurantReviewSerializers(reviews, many=True, context={'request': request})
    return Response({'success': True,
                     'message': 'Get reviews successfully.',
                     'data': serialize.data
                     }, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_dish(request, *args, **kwargs):
    rid = kwargs.get('rid')
    cid = request.data.get('cid')
    restaurant = Restaurant.objects.get(rid=rid)
    category = Category.objects.get(cid=cid)
    serialize = DishesSerializers(data=request.data, context={'request': request})
    if serialize.is_valid(raise_exception=True):
        serialize.save(restaurant=restaurant, category=category)
        return Response({'success': True,
                         'message': 'Add dish successfully.',
                         'data': serialize.data
                         }, status=status.HTTP_200_OK)
    return Response({'success': False,
                     'message': 'Add dish fail.'
                     }, status=status.HTTP_200_OK)


@api_view(['GET'])
def delete_dish(request, *args, **kwargs):
    did = kwargs.get('did')
    rid = kwargs.get('rid')
    try:
        dish = Dish.objects.get(did=did)
        dish.delete()
        restaurant = Restaurant.objects.get(rid=rid)
        dishes = Dish.objects.filter(restaurant=restaurant)
        serialize = DishesSerializers(dishes, many=True, context={'request': request})
        return Response({'success': True,
                         'message': 'Delete dish successfully.',
                        'data': serialize.data
                         }, status=status.HTTP_200_OK)
    except:
        return Response({'success': False,
                         'message': 'Delete dish fail.'
                         }, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_dish(request, *args, **kwargs):
    did = kwargs.get('did')
    # try:
    dish = Dish.objects.get(did=did)
    dish.title = request.data.get('title')
    if 'image' in request.data:
        dish.image = request.FILES.get('image')
    dish.description = request.data.get('description')
    dish.price = request.data.get('price')
    dish.old_price = request.data.get('old_price')
    dish.specifications = request.data.get('specifications')
    dish.product_status = request.data.get('product_status')
    dish.featured = request.data.get('featured').title()
    dish.digital = request.data.get('digital').title()
    cid = request.data.get('cid')
    category = Category.objects.get(cid=cid)
    dish.category = category
    dish.save()
    return Response({'success': True,
                         'message': 'Update dish successfully.'
                         }, status=status.HTTP_200_OK)


@api_view(['GET'])
def order_restaurant(request, *args, **kwargs):
    rid = kwargs.get('rid')
    restaurant = Restaurant.objects.get(rid=rid)
    order = Order.objects.filter(restaurant=restaurant)
    serialize = OrderSerializers(order, many=True, context={'request': request})
    return Response({'success': True,
                     'message': 'Get order successfully.',
                     'data': serialize.data
                     }, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_table(request, *args, **kwargs):
    rid = kwargs.get('rid')
    restaurant = Restaurant.objects.get(rid=rid)
    serialize = TableSerializers(data=request.data, context={'request': request})
    if serialize.is_valid(raise_exception=True):
        serialize.save(restaurant=restaurant)
        return Response({'success': True,
                         'message': 'Add table successfully.',
                         'data': serialize.data
                         }, status=status.HTTP_200_OK)
    return Response({'success': False,
                     'message': 'Add table fail.'
                     }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_table(request, *args, **kwargs):
    rid = kwargs.get('rid')
    restaurant = Restaurant.objects.get(rid=rid)
    tables = Table.objects.filter(restaurant=restaurant)
    serialize = TableSerializers(tables, many=True, context={'request': request})
    return Response({'success': True,
                     'message': 'Get table successfully.',
                     'data': serialize.data
                     }, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_table(request, *args, **kwargs):
    tid = kwargs.get('tid')
    try:
        table = Table.objects.get(tid=tid)
        table.title = request.data.get('title')
        table.number_seat = request.data.get('number_seat')
        table.save()
        return Response({'success': True,
                         'message': 'Update table successfully.'
                         }, status=status.HTTP_200_OK)
    except:
        return Response({'success': False,
                         'message': 'Update table fail.'
                         }, status=status.HTTP_200_OK)


@api_view(['GET'])
def delete_table(request, *args, **kwargs):
    tid = kwargs.get('tid')
    rid = kwargs.get('rid')
    try:
        table = Table.objects.get(tid=tid)
        table.delete()
        rid = kwargs.get('rid')
        restaurant = Restaurant.objects.get(rid=rid)
        data = Table.objects.filter(restaurant=restaurant)
        serialize = TableSerializers(data, many=True)
        return Response({'success': True,
                         'message': 'Delete table successfully.',
                         'data': serialize.data
                         }, status=status.HTTP_200_OK)
    except:
        return Response({'success': False,
                         'message': 'Delete table fail.'
                         }, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def update_order_item(request, *args, **kwargs):
    oid = kwargs.get('oid')
    did = kwargs.get('did')
    order = Order.objects.get(oid=oid)
    dish = Dish.objects.get(did=did)
    quantity = int(request.data.get('quantity'))
    total = quantity*dish.price
    try:
        orderitem = OrderItem.objects.get(order=order, dish=dish)
        orderitem.quantity += quantity
        orderitem.total += dish.price*quantity
        orderitem.save()
    except:
        OrderItem.objects.create(
            order=order, 
            dish=dish, 
            invoice_no="invoice_no_%s" %(oid),
            quantity=quantity, 
            total=total
        )
    order.price += dish.price*quantity
    order.save()
    orders = OrderItem.objects.filter(order=order)
    serialize = OrderSerializers(order)
    serialize2 = OrderItemSerializers(orders, many=True, context={'request': request})
    return Response({'success': True,
                     'message': 'Get list order successfully.',
                     'data': {
                         'order': serialize.data,
                         'orderItems': serialize2.data
                     }
                    }, status=status.HTTP_200_OK)
        

@api_view(['GET'])
def delete_order_item(request, *args, **kwargs):
    oid = kwargs.get('oid')
    did = kwargs.get('did')
    order = Order.objects.get(oid=oid)
    dish = Dish.objects.get(did=did)
    try:
        orderitem = OrderItem.objects.get(order=order, dish=dish)
        order.price -= orderitem.total
        order.save()
        orderitem.delete()
        orders = OrderItem.objects.filter(order=order)
        serialize = OrderSerializers(order)
        serialize2 = OrderItemSerializers(orders, many=True, context={'request': request})
        return Response({'success': True,
                        'message': 'Get list order successfully.',
                        'data': {
                            'order': serialize.data,
                            'orderItems': serialize2.data
                        }
                        }, status=status.HTTP_200_OK)
    except: return Response({'success': False,
                         'message': 'Delete dish fail!'
                         }, status=status.HTTP_200_OK)
    

@api_view(['POST'])
def update_status_order(request, *args, **kwargs):
    oid = kwargs.get('oid')
    order = Order.objects.get(oid=oid)
    order.product_status = request.data.get("product_status")
    order.save();
    return Response({'success': True,
             'message': 'Update status Order success.'        
    }, status=status.HTTP_200_OK)