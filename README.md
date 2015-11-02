#Adimport.ru to Django
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



###Russian description###
Adimport - пример загрузки из adimport.ru в Django проект.

В файле `adimport/adimport.py` показан пример быстрой загрузки большого файла CSV с товарами из партнёрской сети [admitad.com](https://www.admitad.com/ru/promo/?ref=3b2149a63a). Тесты провотились на файле с 1 000 000 товарных позиций и весе файла около 1 гигабайта.
1. Для начала, нужно создать временную таблицу из файла `create_tmp.sql`, в корне примера. Туда будут предварительно загружаться товары из CSV файла.
2. Далее, необходимо иметь такую же или схожую структуру моделей каталога, как в примере `catalog/models.py`
Основное внимание в том, что категории каталога, должны иметь поле с ссылкой на выгрузку и должно быть поле последнего обновления товаров. Модель товаров же, желательна, но не обязательна должны быть по прототипу из файла `catalog/models.py`. Дополнительная особенность именно моей структуры в том, что я для брендов, офферов и характеристик завёл отдельные модели, которые подвязываются к карточке товара. При первичной загруки товаров в рабочую базу товаро, эти связи остаются пустыми. В последующем, через файл `adimport/change_new_item.py` я проставляю связи и попутно создаю новых оферов, бренды и характеристики, если их ранее небыло в БД.
3. Основной пример загрузки из файла во временную таблицу, а из временной в рабочую, описан в файле `adimport/adimport.py`.
 * Дастаём из базы категорий, список всех категорий с ссылками на выгрузки CSV файлов и начинаем в фикле перебирать, выполняя к каждой ссылке следующие действия:
  * заливаем файл во временную таблицу
  * из временной таблицы переносим в рабочую, только те товары, которые пришли новыми или на обновление. по завершению удаляем их из временной таблицы
  * скрываем товары в рабочей таблице, которые пришли на удаление. у меня не удаляются товары, а только скрываются. если вам это критично, можете скрытие заменить на удаление. так же очищаем временную таблицу от товаров пришедших на удаление.
 * переходим к следующему объекту цикла и повторяем операцию.