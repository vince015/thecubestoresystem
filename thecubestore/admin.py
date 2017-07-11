from django.contrib import admin
from thecubestore.models import Profile, Cube, Item
from thecubestore.models import Store, Payment, Sales

admin.site.register(Profile)
admin.site.register(Cube)
admin.site.register(Item)
admin.site.register(Store)
admin.site.register(Payment)
admin.site.register(Sales)
