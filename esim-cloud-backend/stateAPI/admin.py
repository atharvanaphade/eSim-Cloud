from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from stateAPI.models import State, Delta, Groups, DeltaMetadata

# Register your models here.

@admin.register(State)
class CircuitStates(admin.ModelAdmin):
    list_display=['title']


@admin.register(Delta)
class Deltas(admin.ModelAdmin):
    
    list_display=['title','init_state','new_state']

@admin.register(DeltaMetadata)
class DeltaMetadatas(admin.ModelAdmin):
    
    readonly_fields = ('__all__')
    list_display = ('__all__')

class GroupInline(admin.TabularInline):
    model = Groups
    can_delete = False
    verbose_name_plural = 'custom groups'

class GroupAdmin(BaseGroupAdmin):
    inlines = (GroupInline, )

admin.site.register(Group, GroupAdmin)