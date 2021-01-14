from django.contrib import admin

from heating.models import Manufacturer, Appliance, Parttypes, Part, BlogCategory, BlogPost
from import_export.admin import ImportExportModelAdmin, ImportMixin, ExportMixin, ImportExportMixin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget


admin.site.register(BlogPost)
admin.site.register(BlogCategory)

@admin.register(Customer)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "publishdate", "visible", "slug")

class AdminPost(admin.ModelAdmin):
    class Media:
                js = ('/static/js/tiny_mce/tiny_mce.js',)

class ApplianceResource(resources.ModelResource):

    class Meta:
        model = Appliance


class ApplianceAdmin(ImportExportModelAdmin):
    list_display = ('manufacturer', 'name', 'model', 'fuel', 'nameandmodel')
    ordering = ('name', 'model')
    search_fields = ('name', 'model')

    resource_class = ApplianceResource


admin.site.register(Appliance, ApplianceAdmin)


class ManufacturerResource(resources.ModelResource):

    class Meta:
        model = Manufacturer


class ManufacturerAdmin(ImportExportModelAdmin):
    resource_class = ManufacturerResource


admin.site.register(Manufacturer, ManufacturerAdmin)


class ParttypesResource(resources.ModelResource):

    class Meta:
        model = Parttypes


class ParttypesAdmin(ImportExportModelAdmin):
    resource_class = ParttypesResource


admin.site.register(Parttypes, ParttypesAdmin)


class PartResource(resources.ModelResource):
    man = fields.Field(
        column_name='man',
        attribute='man',
        widget=ForeignKeyWidget(Manufacturer, 'name'))
    parttype = fields.Field(
        column_name='parttype',
        attribute='parttype',
        widget=ForeignKeyWidget(Parttypes, 'name'))

    class Meta:
        model = Part


class PartAdmin(ImportExportModelAdmin):
    resource_class = PartResource


admin.site.register(Part, PartAdmin)
