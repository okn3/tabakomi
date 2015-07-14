# Required

```zsh
pip3 install flask
pip3 install PyMySQL3
pip3 install tweepy
pip3 install JpTokenPreprocessing
pip3 install mecab-python
```


# API Docs

## /get_user
ユーザー情報の取得

| key | explanation |
|:-----------:|:------------:|
| user_id       |  取得したい対象ユーザのID |


返り値例

- 対象ユーザがいた場合
	- Twitterデータなし

```js
{
	"result":{
		"id": 53,
		"name": "hogee",
		"screen_name": "",
		"comment": "hello world!",
		"twitetr": ""
	}
}
```

- 対象ユーザがいた場合
	- Twitterデータあり

```js
{
	"result":{
		"comment": "hello world!",
		"id": 53,
		"name": "hogee",
		"screen_name": "taka_say",
		"twitetr":[
			"Memo",
			"Flask",
			"Python",
			"ルイズ",
			"文字",
			"Android",
			"アニメ",
			"エディタ",
			"Vivaldi",
			"英語"
		]
	}
}
```

- 対象ユーザがいなかった場合

```js
{
	"result": ""
}
```

## /register_user
ユーザー登録

| key | explanation |
|:-----------:|:------------:|
| name       |  登録ユーザー名 |
| password     | パスワード |

返り値例

```js
{
	"user_id": 51
}
```


## /register_profile
プロフィール登録（TwitterID, Comment）

|   key   | explanation  |
| :-----: | :----------: |
| user_id |   自分のID   |
| twitter |  twitterのID（ない場合は空） |
| comment | 一言コメント（ない場合は空） |


返り値例

```js
{
	"status": "success"
}
```


## /post_location
位置情報送信（バックグラウンドで行うやつ）  
**およびYahhoの確認**

| key | explanation |
|:-----------:|:------------:|
| user_id     | 自分のID |
| lat       |  緯度 |
| lng     | 経度 |

返り値例

- 自分あてのYahhoがない場合

```js
{
	"result": ""
}
```

- 自分あてのYahhoがある場合

```js
{
	"result":{
		"id": 4,
		"lat": 140,
		"lng": 39,
		"modified": "Thu, 09 Jul 2015 15:30:05 GMT",
		"name": "hoge",
		"position": null,
		"pushed_user_id": 53,
		"pushing_user_id": 52
	}
}
```

## /get\_near\_location_users
周辺ユーザ取得

| key | explanation |
|:-----------:|:------------:|
| user_id     | 自分のID |
| lat       |  緯度 |
| lng     | 経度 |

返り値例

- 近くに人がいる場合

```js
{
	"locations":[
		{"lat": 39, "lng": 140, "name": "fuga", "user_id": 1},
		{"lat": 39, "lng": 140, "name": "piyo", "user_id": 100}
	]
}
```

- 近くに人がいない場合

```js
{
	"locations":[]
}
```

## /push_yahho
Yahho送信

| key | explanation |
|:-----------:|:------------:|
| lat       |  緯度 |
| lng     | 経度 |
| pushing\_user\_id  |  YahhoをしたユーザのID（端末側） |
| pushed\_user\_id     | Yahho対象のユーザID（ピン側） |

返り値

```js
{
	"status": "success"
}
```


## /get_tags
設定可能なTagの一覧と、登録したユーザーのタグ取得


| key | explanation |
|:-----------:|:------------:|
| user_id       |  自分のID |

返り値

```js
{
	"tags":[
		"スポーツ",
		"ゲーム",
		"ラーメン",
		"車",
		"バイク",
		"タバコ",
		"IT",
		"アニメ",
		"ルイズ",
		"ゼロの使い魔"
	],
	"user_tags":[
		"スポーツ",
		"ゼロの使い魔"
	]
}
```


## /set_tag
タグの登録

| key | explanation |
|:-----------:|:------------:|
| user_id       |  自分のID |
| name     | タグの名前 |

返り値

```js
{
	"status": "success"
}
```

## /remove_tag
登録したTagの削除  

| key | explanation |
|:-----------:|:------------:|
| user_id       |  自分のID |
| name     | タグの名前 |

返り値

```js
{
	"status": "success"
}
```


## /enter_ibeacon
iBeacon範囲内に入った時

| key | explanation |
|:-----------:|:------------:|
| user_id       |  自分のID |

返り値

```js
{
	"status": "success"
}
```


## /exit_ibeacon
iBeacon範囲内から出た時

| key | explanation |
|:-----------:|:------------:|
| user_id       |  自分のID |

返り値

```js
{
	"status": "success"
}
```

# Caution
Twitter related file isn't pushed.