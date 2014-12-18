import requests
import time
import logging
import urlparse

from django.conf import settings

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')

f = open(settings.RESTMOTE_SNAP_FILE, 'r+')
root = urlparse.urljoin(settings.RESTMOTE_HOST+":"+settings.RESTMOTE_PORT, settings.RESTMOTE_API_ROOT)
get_params = "?" + settings.RESTMOTE_FILTER_FIELD + "=" + f.read().strip()

f.close()

def get_data(url):
    r = requests.get(url, timeout=15)
    if r.ok:
        logging.info(url)
        logging.info(r.json())
        return r.json()
    else:
        return []

def build_objects(obj_class, obj_string, data, field_bindings, nested=[], key=None):
    for e in data:

        try:
            if key:
                o = obj_class.objects.get(**{'id'+obj_string : e[key]["id"]})
            else:
                o = obj_class.objects.get(**{'id'+obj_string : e["id"]})
        except obj_class.DoesNotExist:
            o = obj_class()

        for f in [x for x in e if x in field_bindings]:
            setattr(o, field_bindings[f], e[f])

        for n in nested:
            for f in [x for x in e[n] if x in field_bindings]:
                setattr(o, field_bindings[f], e[n][f])


        if key:
            setattr(o, "id"+obj_string, e[key]["id"])
        else:
            setattr(o, "id"+obj_string, e["id"])
        o.save()


def sync_objects(url, obj_class, obj_string, field_bindings, nested=[], key=None):
    data = get_data(root + url + get_params)
    build_objects(obj_class, obj_string, data, field_bindings, nested, key)


# Order IS important!! Care with relationships

f = open(settings.RESTMOTE_SNAP_FILE, 'w')
f.write(time.strftime("%Y-%m-%d %H:%M", (time.localtime(time.time()))))
f.close()
