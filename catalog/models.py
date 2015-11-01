# -*- coding: utf-8 -*-
from django.db import models

"""
    This is a minimal example models.py product catalog

    The purpose of the models below:
    Category() - Categories of goods on which required fields links to download from adimport.ru and date of last upload
    Item() - Model of products, with a required parameter (unique) - id_adimport
    ItemOffer() - Another model to offer sorting and individual pages of the list of offers
    ItemVendor() - Model brands similar to offer
    ItemParamsName() - A list of attributes for the filters placed in a separate model.
            Taken from "param" of the goods.
            Example name: "Color", "Size", "Season"
    ItemParams() - The values of attributes with communication on the model of names of attributes(ItemParamsName)
            and the items to which this attributes value.
            Example value: "Red", "42", "Summer 2016"
"""


class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    show = models.BooleanField(default=True)
    csv_adimport = models.CharField(verbose_name=u'Url on CSV in aDimport categories', max_length=255, null=True, blank=False)
    last_import = models.DateTimeField(verbose_name=u"last import", blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.name


class Item(models.Model):
    show            = models.BooleanField(default=False, db_index=True)

    category        = models.ForeignKey(Category, related_name='item_category')

    name            = models.CharField(max_length=255, null=True, blank=False)
    price           = models.IntegerField(default=0, blank=True)
    oldprice        = models.IntegerField(verbose_name=u"Old price", default=0, blank=True)
    description     = models.TextField(null=True, blank=True)

    picture         = models.TextField(null=True, blank=True)
    available       = models.CharField(max_length=255, null=True, blank=True)
    currency        = models.CharField(max_length=255, null=True, blank=True)
    delivery        = models.CharField(max_length=255, null=True, blank=True, help_text=u"true, false")
    model           = models.CharField(max_length=255, null=True, blank=True)
    article         = models.CharField(max_length=255, null=True, blank=True)

    vendor_name     = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    advcampaign_id  = models.CharField(verbose_name=u'ID offer in admitad.com', max_length=255,
                                       null=True, blank=True, db_index=True)
    advcampaign_name = models.CharField(verbose_name=u'Name offer in admitad.com', max_length=255,
                                        null=True, blank=True, db_index=True)
    param           = models.TextField(null=True, blank=True)
    admitad_id      = models.CharField(verbose_name=u'ID in adimport.ru', max_length=255, null=True, blank=True)

    offer           = models.ForeignKey('ItemOffer', null=True, blank=True, related_name='offer_item')
    vendor          = models.ForeignKey('ItemVendor', null=True, blank=True, related_name='vendor_item')

    new_item        = models.BooleanField(default=True, editable=False)
    delete          = models.DateTimeField(blank=True, null=True, editable=False)

    id_adimport     = models.CharField(max_length=255, null=True, blank=True, unique=True)

    def __unicode__(self):
        return u"%s" % self.name


class ItemOffer(models.Model):
    name            = models.CharField(max_length=255, null=True, blank=True, unique=True)
    code            = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.name


class ItemVendor(models.Model):
    name            = models.CharField(verbose_name=u'Бренд', max_length=255, null=True, blank=True, unique=True)
    code            = models.CharField(verbose_name=u'Код бренда', max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.name


class ItemParams(models.Model):
    item           = models.ForeignKey('Item', related_name='param_item')
    attr           = models.ForeignKey('ItemParamsName', related_name='param_name')
    value          = models.CharField(max_length=20000, null=True, blank=True)
    sub_value      = models.CharField(max_length=500, verbose_name=u'Unit value', help_text=u"Kd, sm, mb, usd, ...",
                                      null=True, blank=True)

    def __unicode__(self):
        return u'%s - %s' % (self.attr, self.value)


class ItemParamsName(models.Model):
    name = models.CharField(max_length=255, help_text=u"Color, size, season, ...", unique=True)

    def __unicode__(self):
        return u'%s' % self.name