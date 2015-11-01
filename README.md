#Adimport.ru to Django
========
This is an example of the work with the unloading of the merchandise affiliate system admitad.com through the app adimport.ru.


Description
=====
1. Create a temporary table from file `create_tmp.sql` in the root of the example
2. An example of the structure of the product catalog in the file `catalog/models.py`
3. In the file `adimport/adimport.py` proceed:
 * The searched product categories to get the category ID and the link to the CSV file from adimport.ru
 * Be moved from the temporary file into the temporary database
 * Move items from a temporary table in working.
 * Turning off the items came in unloading "to delete"
4. Additional file `adimport/change_new_item.py` I do a little magic. Namely:
 * Get characteristics of the product in the format phpserialize (`adimport/phpserialize.py`), convert them into a list and insert it into the outer table of the characteristics of the goods. That would later use them in filters in sections (sorting or searching).
 * Tie the brand of the product, to the external table brands to use filters on sections. And as for the possibility of creating a separate page list all brands of products in the store.
 * Tie the merchandise to a foreign table offer. As for sorting in section and the create a list page of all offers.
 * Include the display of new products on display. So when loading from adimport.ru before you run this file, I display the cards.
  

File execution `adimport/adimport.py` test 1000000 of products(~1gb) and VPS(SSD/4gb_RAM), takes 2-4 minutes, excluding the download time of the file. That is, loading into a database.

###Links:###
 * [Admitad.com](http://admitad.com/) - This a platform for affiliate programs, logs targeted actions of visitors, and pays you royalties for those actions ([referals url](https://www.admitad.com/ru/promo/?ref=3b2149a63a))
 * [Adimport.ru](http://adimport.ru/) - 
Service for structured and uniform unloading of the products from the affiliate network Admitad ([referals url](http://www.cpasoft.ru/register.html?r=1169))