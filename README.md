# Documentation

Data such as iPhone model, storage, price and color are collected from website [MP3.sk](https://www.mp3.sk/bazar-mobily-apple-bazar-c-207355_207356.html)

## Running the program

Project is compatible with Python 3.X version. Typing this command to terminal will execute current program.

```Python
python3 main.py
```

## Data

Every time program is executed it generates object as collection of data and stores it into folder named **datums**, with name represented as current date e.g. 2019-12-24-13-28-30 (year-day-month-hour-minute-second).


```HTML
8003 4b0e 2e80 0363 5f5f 6d61 696e 5f5f
0a49 7465 6d0a 7100 2981 7101 7d71 0228
5805 0000 006d 6f64 656c 7103 5809 0000
.
.
.
```

After reading data from file it may look like this

```HTML
iPhone 6S       32GB   299.99€      Space Gray https://www.mp3.sk/apple-iphone-6s-32gb-space-gray-novy-tovar-neotvorene-balenie-p-360109.html
iPhone 7        32GB   379.99€           Black https://www.mp3.sk/apple-iphone-7-32gb-black-novy-tovar-neotvorene-balenie-p-358071.html
iPhone 7        32GB   379.99€          Silver https://www.mp3.sk/apple-iphone-7-32gb-silver-novy-tovar-neotvorene-balenie-p-358068.html
iPhone 6S Plus  64GB   449.99€       Rose Gold https://www.mp3.sk/apple-iphone-6s-plus-64gb-rose-gold-novy-tovar-neotvorene-balenie-p-354619.html
iPhone Xr       64GB   719.99€            Blue https://www.mp3.sk/apple-iphone-xr-64gb-blue-novy-tovar-neotvorene-balenie-p-400224.html
iPhone Xs       64GB   759.99€      Space Gray https://www.mp3.sk/apple-iphone-xs-64gb-space-gray-novy-tovar-neotvorene-balenie-p-390661.html
iPhone Xs       256GB  889.99€      Space Gray https://www.mp3.sk/apple-iphone-xs-256gb-space-gray-novy-tovar-neotvorene-balenie-p-390837.html
iPhone Xs Max   256GB  999.99€          Silver https://www.mp3.sk/apple-iphone-xs-max-256gb-silver-novy-tovar-neotvorene-balenie-p-401562.html
iPhone 11 Pro   64GB  1129.99€            Gold https://www.mp3.sk/apple-iphone-11-pro-64gb-gold-novy-tovar-neotvorene-balenie-p-402213.html
iPhone 11 Pro   64GB  1129.99€  Midnight Green https://www.mp3.sk/apple-iphone-11-pro-64gb-midnight-green-novy-tovar-neotvorene-balenie-p-404830.html
```

If there was a new item it would be highlighted entire row in green color.