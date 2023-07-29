from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Profile, Avatar


class ProfileAdmin(admin.ModelAdmin):
    def photo(self, profile):
        return mark_safe(f'<img src="{profile.avatar.src}" width="100"/>')

    photo.allow_tags = True
    list_display = "pk", "fullName", "user", "photo"


class AvatarAdmin(admin.ModelAdmin):
    def image(self, img):
        if img.src:
            return mark_safe(f'<img src="{img.src}" width="100"/>')

    image.allow_tags = True
    list_display = "pk", "image", "alt"


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Avatar, AvatarAdmin)
