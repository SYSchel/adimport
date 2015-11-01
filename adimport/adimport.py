# -*- coding: utf-8 -*-
import os
import urllib
from django.utils import timezone
from datetime import datetime
from django.db import connection
from catalog.models import Category
cursor = connection.cursor()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def start():
    """

    Run through the categories of getting a link to upload.
    Download file into a temporary database.
    Move data from temporary table to main.
    Turning off the items which came to destruction.

    """

    # Temporary file where we will save what you downloaded from adimport.ru for each category
    file_url = "%s/files/adimport_items.csv" % BASE_DIR
    # Iterate list of category ID and links to download.
    for cat in Category.objects.filter(show=True).only('pk', 'csv_adimport'):
        # Added option to adimport.ru that would have been transferred to the row of field names.
        csv_file = '%s&fields_name=true' % cat.csv_adimport
        # If the "last_import" is not empty, then have been downloaded and need to specify the date of the last injection.
        if cat.last_import:
            csv_file = csv_file.replace('&last_import=', '&last_import=%s' % datetime.strftime(cat.last_import, '%Y.%m.%d.%H.%m'))
        # Download CSV file and add it to a temporary file
        urllib.urlretrieve(csv_file, file_url)
        # Be moved from the temporary file into the temporary database
        _file_to_mysql(file_url)
        # Written to the category the date of the last update.
        cat.last_import = timezone.now()
        cat.save()
        # Move items from a temporary table in working.
        _temp_to_project(category=cat.pk)
        # Turning off the items came in unloading "to delete"
        _delete_old_items()

    return True


def _file_to_mysql(file):
    """
    The name of the fields and the order in the table must match the names and order of fields in the file.
    The @ symbol means to ignore the field.
    """

    sql = u"LOAD DATA LOCAL INFILE '%s' INTO TABLE adimport_tmp CHARACTER SET utf8 FIELDS TERMINATED BY '|'" \
          u" ENCLOSED BY \"'\" LINES TERMINATED BY '\n' IGNORE 1 LINES " \
          u"(id_adimport,@ISBN,@adult,@age,article," \
          u"@attrs,@author,available,@barcode,@binding,@brand,@categoryId,@country_of_origin,currencyId,delivery," \
          u"description,@downloadable,@format,@gender,id,@local_delivery_cost,@manufacturer_warranty,@market_category," \
          u"@model,@modified_time,name,oldprice,@orderingTime,@page_extent,param,@performed_by,@pickup,picture,price," \
          u"@publisher,@sales_notes,@series,@store,@syns,@topseller,@type,@typePrefix,url,vendor,@vendorCode,@weight," \
          u"@year,advcampaign_id,advcampaign_name,@deeplink);" % file
    cursor.execute(sql)
    return True


def _temp_to_project(category=None):
    today = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    # Move items from a temporary table in working.
    sql = u"INSERT INTO `catalog_item` (`id`, `create`, `update`, `show`, `url`, `subtext`, `name`, `price`," \
          u" `oldprice`, `description`, `id_adimport`, `picture`, `available`, `currency`, `delivery`, `admitad_id`," \
          u" `model`, `ref_url`, `article`, `vendor_name`, `advcampaign_id`, `advcampaign_name`, `param`," \
          u" `category_id`, `offer_id`, `vendor_id`, `new_item`) " \
          u"SELECT NULL, '%s', '%s', '0', NULL, NULL, `name`, `price`," \
          u" `oldprice`, NULL, `id_adimport`, `picture`, `available`, `currencyId`, `delivery`, `id`," \
          u" NULL, `url`, `article`, `vendor`, `advcampaign_id`, `advcampaign_name`, `param`," \
          u" '%s', NULL, NULL, '1' " \
          u"FROM `adimport_tmp` " \
          u"WHERE `adimport_tmp`.`url` IS NOT NULL" \
          u" ON DUPLICATE KEY UPDATE `catalog_item`.`price` = `adimport_tmp`.`price`," \
          u" `catalog_item`.`oldprice` = `adimport_tmp`.`oldprice`" \
          u";" % (today, today, category)
    cursor.execute(sql)
    # Delete from the temporary database new or updated items
    delete_sql = u"DELETE FROM `adimport_tmp` WHERE `url` IS NOT NULL;"
    cursor.execute(delete_sql)

    return True


def _delete_old_items():
    # Hide items in the worksheet, come to the removal of the discharge.
    today = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    show_sql = u"UPDATE `catalog_item` SET `show`='0', `delete`='%s' WHERE `id_adimport`IN (SELECT `id_adimport`" \
               u" FROM `adimport_tmp` WHERE `url` IS NULL);" % today
    cursor.execute(show_sql)
    # Remove items "to delete" from the temporary database
    delete_show_sql = u"DELETE FROM `adimport_tmp` WHERE `url` IS NULL;"
    cursor.execute(delete_show_sql)
    # My hook
    convert_null_param_sql = u"UPDATE `catalog_item` SET `param` = NULL WHERE `param` = '' OR `param` = '0';"
    cursor.execute(convert_null_param_sql)
    return True
