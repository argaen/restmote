import requests
import logging
import urlparse

from django.conf import settings

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')

root = urlparse.urljoin(settings.RESTMOTE_HOST + ":" + settings.RESTMOTE_PORT, settings.RESTMOTE_API_ROOT)


def get_data(url):
    r = requests.get(url, timeout=15)
    if r.ok:
        logging.info(url)
        logging.info(r.json())
        return True, r.json()
    else:
        logging.info("Connection failed: %s" % r.text)
        return False, []


def build_objects(obj_class, obj_string, data, field_bindings, nested=[]):
    for e in data:

        try:
            o = obj_class.objects.get(**{'id' + obj_string: e["id"]})
        except obj_class.DoesNotExist:
            o = obj_class()

        for f in [x for x in e if x in field_bindings]:
            setattr(o, field_bindings[f], e[f])

        for n in nested:
            for f in [x for x in e[n] if x in field_bindings]:
                setattr(o, field_bindings[f], e[n][f])

        setattr(o, "id" + obj_string, e["id"])
        o.save()
        logging.info("Added %s: %s" % (obj_string, o.pk))


def sync_objects(url, qfilter, obj_class, obj_string, field_bindings, nested=[]):
    status, data = get_data(root + url + '?' + qfilter)
    if status:
        build_objects(obj_class, obj_string, data, field_bindings, nested)
        return 1
    else:
        return 0


def remove_objects(url, obj_class, obj_string):
    status, remote_ids = get_data(root + url)
    if status:
        local_ids = obj_class.objects.values_list('id' + obj_string, flat=True)
        must_remove = list(set(local_ids).difference(remote_ids))
        obj_class.objects.filter(**{'id' + obj_string + '__in': must_remove}).delete()
        if must_remove:
            logging.info("Deleted %s: %s" % (obj_string, ', '.join(must_remove)))
        return 1
    else:
        return 0
