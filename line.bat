curl -v -X POST https://api.line.me/v2/bot/richmenu -H 'Authorization: Bearer 9MIxXkeIKFOk6+zOI4oFcXP6eS9ty9/GCtgdOGvbeJMFyUgn15UvdGogm6gUtR0J4f0qIF6lLQnpaK9amEFHNee/NYv0Sx6V1xNQiAAk3zSccPD56pR29O5AbHhAKGxGBa5IKwAPY+KxxoVKU+EmcAdB04t89/1O/w1cDnyilFU=' -H 'Content-Type: application/json' -d '{     "size": {         "width": 2500,         "height": 843     },     "selected": true,     "name": "richmenu-a",     "chatBarText": "Menu",     "areas": [         {             "bounds": {                 "x": 0,                 "y": 0,                 "width": 1250,                 "height": 843             },             "action": {                 "type": "richmenuswitch",                 "richMenuAliasId": "richmenu-alias-b",                 "data": "richmenu-changed-to-b"             }         },         {             "bounds": {                 "x": 1251,                 "y": 0,                 "width": 1250,                 "height": 843             },             "action": {                 "type": "uri",                 "uri": "https://cool-heliotrope-f8f19e.netlify.app/"             }         }     ] }'



curl -v -X POST https://api-data.line.me/v2/bot/richmenu/richmenu-bfccbf2687982f4fcd4139fad825e40f/content -H "Authorization: Bearer 9MIxXkeIKFOk6+zOI4oFcXP6eS9ty9/GCtgdOGvbeJMFyUgn15UvdGogm6gUtR0J4f0qIF6lLQnpaK9amEFHNee/NYv0Sx6V1xNQiAAk3zSccPD56pR29O5AbHhAKGxGBa5IKwAPY+KxxoVKU+EmcAdB04t89/1O/w1cDnyilFU=" -H "Content-Type: image/png" -T mainmenu.png




curl -v -X POST https://api.line.me/v2/bot/user/all/richmenu/richmenu-81a3ad492933e9d7ba956a0e0ba4933f -H "Authorization: Bearer 9MIxXkeIKFOk6+zOI4oFcXP6eS9ty9/GCtgdOGvbeJMFyUgn15UvdGogm6gUtR0J4f0qIF6lLQnpaK9amEFHNee/NYv0Sx6V1xNQiAAk3zSccPD56pR29O5AbHhAKGxGBa5IKwAPY+KxxoVKU+EmcAdB04t89/1O/w1cDnyilFU="



curl -v -X POST https://api.line.me/v2/bot/richmenu -H 'Authorization: Bearer 9MIxXkeIKFOk6+zOI4oFcXP6eS9ty9/GCtgdOGvbeJMFyUgn15UvdGogm6gUtR0J4f0qIF6lLQnpaK9amEFHNee/NYv0Sx6V1xNQiAAk3zSccPD56pR29O5AbHhAKGxGBa5IKwAPY+KxxoVKU+EmcAdB04t89/1O/w1cDnyilFU=' -H 'Content-Type: application/json' -d 
'{
    "size": {
        "width": 2500,
        "height": 1686
    },
    "selected": false,
    "name": "richmenu-b",
    "chatBarText": "Menu",
    "areas": [
        {
            "bounds": {
                "x": 0,
                "y": 0,
                "width": 1250,
                "height": 843
            },
            "action": {
                "type": "message",
                "text": "sample1"
            }
        },
        {
            "bounds": {
                "x": 1251,
                "y": 0,
                "width": 1250,
                "height": 843
            },
            "action": {
                "type": "message",
                "text": "sample2"
            }
        },
                {
            "bounds": {
                "x": 0,
                "y": 844,
                "width": 1250,
                "height": 843
            },
            "action": {
                "type": "message",
                "text": "sample3"
            }
        },
        {
            "bounds": {
                "x": 1251,
                "y": 844,
                "width": 1250,
                "height": 843
            },
            "action": {
                "type": "richmenuswitch",
                "richMenuAliasId": "richmenu-alias-a",
                "data": "richmenu-changed-to-a"
            }
        }
    ]
}'



curl -v -X POST https://api-data.line.me/v2/bot/richmenu/richmenu-f576ece775e12b2df9513af79e60c640/content -H 'Authorization: Bearer 9MIxXkeIKFOk6+zOI4oFcXP6eS9ty9/GCtgdOGvbeJMFyUgn15UvdGogm6gUtR0J4f0qIF6lLQnpaK9amEFHNee/NYv0Sx6V1xNQiAAk3zSccPD56pR29O5AbHhAKGxGBa5IKwAPY+KxxoVKU+EmcAdB04t89/1O/w1cDnyilFU=' -H "Content-Type: image/png" -T dwn_menu.png

curl -v -X POST https://api.line.me/v2/bot/richmenu/alias -H 'Authorization: Bearer 9MIxXkeIKFOk6+zOI4oFcXP6eS9ty9/GCtgdOGvbeJMFyUgn15UvdGogm6gUtR0J4f0qIF6lLQnpaK9amEFHNee/NYv0Sx6V1xNQiAAk3zSccPD56pR29O5AbHhAKGxGBa5IKwAPY+KxxoVKU+EmcAdB04t89/1O/w1cDnyilFU=' -H 'Content-Type: application/json' -d '{"richMenuAliasId": "richmenu-alias-b", "richMenuId": "richmenu-f576ece775e12b2df9513af79e60c640"}'

richmenu-bfccbf2687982f4fcd4139fad825e40f
richmenu-81a3ad492933e9d7ba956a0e0ba4933f