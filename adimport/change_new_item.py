# -*- coding: utf-8 -*-
import math

from django.db import transaction
from django.db.models import Count

from tools import create_url, convert_param, clean_text
from catalog.models import Item, ItemParams, ItemParamsName, ItemOffer, ItemVendor


def start():
    print "_update_param()"
    _update_param()
    print "_update_vendor()"
    _update_vendor()
    print "_update_offer()"
    _update_offer()
    print "_update_show()"
    _update_show()
    return True


def _update_param(step=1000):
    """
    Convert the string parameters of the goods from the serialization in the list and write them to the database
    :param step: The number of products per pass 1
    """
    count = Item.objects.filter(show=False, delete__isnull=True, param__isnull=False).only('show').count()
    round_for = int(math.ceil(float(count) / step))

    for a in xrange(round_for):
        with transaction.atomic():
            for item in Item.objects.filter(show=False, delete__isnull=True, param__isnull=False).only('param', 'id_adimport')[:step]:
                db_params = convert_param(item.param)
                if db_params:
                    for k, v in db_params.items():
                        item_param = ItemParams()
                        item_param.item_id = item.pk
                        item_param.attr = ItemParamsName.objects.get_or_create(name=k)[0]
                        item_param.value = v
                        item_param.save()
                item.param = None
                item.save(update_fields=['param'])


def _update_vendor(step=10):
    """
    Create vendor
    :param step: The number of products per pass
    """
    vendor_list = {}
    for vendor in Item.objects.values_list('vendor_name', flat=True).filter(vendor_name__isnull=False).\
            annotate(count=Count('vendor_name')).order_by('-count'):
        clean_vendor = clean_text(vendor)
        if len(clean_vendor) > 2:
            vendors = ItemVendor.objects.get_or_create(name=clean_text(clean_vendor))[0]
            vendor_list[vendor] = int(vendors.pk)

    round_for = int(math.ceil(float(len(vendor_list)) / step))
    for a in xrange(round_for):
        start =a*step
        stop = (a+1)*step
        with transaction.atomic():
            for k, v in vendor_list.items()[start:stop]:
                Item.objects.filter(vendor__isnull=True, vendor_name=u"%s" % k).\
                    update(vendor_id=v, vendor_name=None)


def _update_offer(step=1):
    """
    Create offer
    :param step: The number of products per pass
    """

    offer_list = {}
    for offer in Item.objects.values('advcampaign_name', 'advcampaign_id').filter(advcampaign_name__isnull=False).\
            annotate(count=Count('advcampaign_name')).order_by('-count'):
        clean_offer = offer.get('advcampaign_name').strip()
        clean_offer_id = offer.get('advcampaign_id').strip()

        offers = ItemOffer.objects.get_or_create(name=clean_offer, code=clean_offer_id)[0]
        offer_list[clean_offer] = int(offers.pk)
    #
    round_for = int(math.ceil(float(len(offer_list)) / step))
    for a in xrange(round_for):
        start =a*step
        stop = (a+1)*step
        with transaction.atomic():
            for k, v in offer_list.items()[start:stop]:
                Item.objects.filter(offer__isnull=True, advcampaign_name=u"%s" % k).\
                    update(offer_id=v, advcampaign_name=None, advcampaign_id=None)


def _update_show():
    Item.objects.\
        filter(show=False, offer__isnull=False, vendor__isnull=False, param__isnull=True, delete__isnull=True).\
        update(show=True)
    Item.objects.\
        filter(show=True, offer__isnull=False, vendor__isnull=False, param__isnull=True, delete__isnull=True).\
        update(new_item=False)