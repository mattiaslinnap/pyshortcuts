from django.contrib.gis import admin
from django.contrib.gis.geos import Point

def permission_denied(self, request, obj=None):
    return False

def readonly_admin(model, model_admin_base=admin.ModelAdmin):
    return type('ReadOnly%sAdmin' % model.__name__,
                (model_admin_base,),
                {'readonly_fields': [f.name for f in model._meta.fields],
                 'has_delete_permission': permission_denied})


class CambridgeOsmGeoAdmin(admin.OSMGeoAdmin):
    # OSMGeoAdmin uses "Google" projection.
    default_lon, default_lat = Point(0.1145, 52.2032, srid=4326).transform(900913, clone=True).coords
    default_zoom = 13
