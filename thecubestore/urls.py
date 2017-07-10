from django.conf.urls import url
from django.conf.urls import include
from thecubestore.views import home, user, profile, store, cube, lease, payment, merchant, item, sales

urlpatterns = [url(r'^login/$', home.user_login, name='login'),
               url(r'^logout/$', home.user_logout, name='logout'),
               url(r'^home/$', home.dashboard, name='home'),
               url(r'^$', home.dashboard),
               url(r'^user/add$', user.add, name='user_add'),
               # Profile
               url(r'^profile/add/(?P<user_id>[0-9]+)$', profile.add, name='profile_add'),
               url(r'^profile/view/(?P<user_id>[0-9]+)$', profile.view, name='profile_view'),
               # Store
               url(r'^store/add/(?P<user_id>[0-9]+)$', store.add, name='store_add'),
               url(r'^store/view/(?P<store_id>[0-9]+)$', store.view, name='store_view'),
               url(r'^store/edit/(?P<store_id>[0-9]+)$', store.edit, name='store_edit'),
               url(r'^store/delete/(?P<store_id>[0-9]+)$', store.delete, name='store_delete'),
               url(r'^store/list$', store.list, name='store_list'),
               # Cube
               url(r'^cube/add/(?P<user_id>[0-9]+)$', cube.add, name='cube_add'),
               url(r'^cube/view/(?P<cube_id>[0-9]+)$', cube.view, name='cube_view'),
               url(r'^cube/edit/(?P<cube_id>[0-9]+)$', cube.edit, name='cube_edit'),
               url(r'^cube/delete/(?P<cube_id>[0-9]+)$', cube.delete, name='cube_delete'),
               url(r'^cube/list$', cube.list, name='cube_list'),
               # Lease
               url(r'^lease/add/(?P<user_id>[0-9]+)$', lease.add, name='lease_add'),
               url(r'^lease/view/(?P<lease_id>[0-9]+)$', lease.view, name='lease_view'),
               url(r'^lease/edit/(?P<lease_id>[0-9]+)$', lease.edit, name='lease_edit'),
               url(r'^lease/delete/(?P<lease_id>[0-9]+)$', lease.delete, name='lease_delete'),
               url(r'^lease/list$', lease.list, name='lease_list'),
               # Payment
               url(r'^payment/add/(?P<user_id>[0-9]+)$', payment.add, name='payment_add'),
               url(r'^payment/view/(?P<payment_id>[0-9]+)$', payment.view, name='payment_view'),
               url(r'^payment/edit/(?P<payment_id>[0-9]+)$', payment.edit, name='payment_edit'),
               url(r'^payment/delete/(?P<payment_id>[0-9]+)$', payment.delete, name='payment_delete'),
               url(r'^payment/list$', payment.list, name='payment_list'),
               # Item
               url(r'^item/add/(?P<cube_id>[0-9]+)$', item.add, name='item_add'),
               url(r'^item/view/(?P<item_id>[0-9]+)$', item.view, name='item_view'),
               url(r'^item/edit/(?P<item_id>[0-9]+)$', item.edit, name='item_edit'),
               url(r'^item/delete/(?P<item_id>[0-9]+)$', item.delete, name='item_delete'),
               url(r'^item/list$', item.list, name='item_list'),
               # Sales
               url(r'^sales/add$', sales.add, name='sales_add'),
               url(r'^sales/list$', sales.list, name='sales_list'),
               # Mercahnt
               url(r'^merchant/list$', merchant.list, name='merchant_list'),]