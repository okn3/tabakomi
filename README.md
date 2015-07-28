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
		"image": "http://pbs.twimg.com/profile_images/542757120005787648/t5TKVRcm_normal.jpeg",
		"sex": 0,
		"twitetr": "",
		"tags": [
			"スポーツ",
			"ゼロの使い魔"
		]
	}
}
```

- 対象ユーザがいた場合
	- Twitterデータあり

```js
{
	"result":{
		"id": 53,
		"name": "hogee",
		"screen_name": "taka_say",
		"comment": "hello world!",
		"image": "http://pbs.twimg.com/profile_images/542757120005787648/t5TKVRcm_normal.jpeg",
		"sex": 0,
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
		],
		"tags": [
			"スポーツ",
			"ゼロの使い魔"
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
| sex     | 性別（女 => 0, 男 => 1） |

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
		"id": 34,  // yahho id
		"lat": 40,
		"lng": 140,
		"name": "hogee",
		"pushed_user_id": 109,  // yahhoの対象
		"pushing_user_id": 53,  // yahhoしてきた相手のid
		"reply": 0,  // 返信かどうか 0 => 初めて, 1 => 返信
		"screen_name": "taka_say",
		"comment": "hello world!",
		"image": "http://pbs.twimg.com/profile_images/542757120005787648/t5TKVRcm_normal.jpeg",
		"sex": 0,
		// tagが登録されている場合
		"tags":[
			"ゼロの使い魔",
			"ルイズ"
		],
		// twitter_idが登録されている場合
		"twitter":[
			"Flask",
			"ルイズ",
			"Python",
			"Vivaldi",
			"文字",
			"エディタ",
			"アニメ",
			"英語",
			"Android",
			"やる気"
		]
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
		{
			"user_id": 112,
			"name": "chinko",
			"sex": 1,
			"lat": 39.90218401,
			"lng": 140.1029481,
			"image": "http://abs.twimg.com/sticky/default_profile_images/default_profile_2_200x200.png"
		},
		{
			"user_id": 113,
			"name": "chinko2",
			"sex": 0,
			"lat": 39,
			"lng": 140,
			"image": "http://pbs.twimg.com/profile_images/542757120005787648/t5TKVRcm_normal.jpeg"
		}
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

|        key        |           explanation           |
| :---------------: | :-----------------------------: |
|        lat        |               緯度              |
|        lng        |               経度              |
| pushing\_user\_id | YahhoをしたユーザのID（端末側） |
|  pushed\_user\_id |  Yahho対象のユーザID（ピン側）  |
|       reply       |       返信のYahhoかどうか（通常時は設定不要,返信の場合は1をいれる）   |

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
| uuid       |  iBeaconのuuid |
| major       |  iBeaconのmajor値 |
| minor       |  iBeaconのminor値 |

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


## /get_ibeacons
iBeacon範囲内にいるユーザの取得  

| key | explanation |
|:-----------:|:------------:|
| user_id       |  自分のID |
| uuid       |  iBeaconのuuid |
| major       |  iBeaconのmajor値 |
| minor       |  iBeaconのminor値 |

返り値

```js
{
	"result":[
		{
			"user_id": 113,
			"name": "chinko2",
			"sex": 0,
			"comment": "chiko dashichau yooooooo",
			"image": "http://pbs.twimg.com/profile_images/542757120005787648/t5TKVRcm_bigger.jpeg"
		},
		{
			"user_id": 115,
			"name": "unkokko",
			"sex": 1,
			"comment": "unko morechau kamo!",
			"image": "http://abs.twimg.com/sticky/default_profile_images/default_profile_2_bigger.png"
		}
	]
}
```

## /get_trends
現在地周辺のTwitterトレンドを取得

| key | explanation |
|:-----------:|:------------:|
| user_id       |  自分のID |
| lat       |  緯度（ない場合東京） |
| lng       |  経度（ない場合東京） |

返り値

```js
{
	"trends":[
		"あなたの行動年齢",
		"世界的アニメーション・クリエイター",
		"花火大会",
		"モンスト",
		"隅田川",
		"赤漆塗木鉢",
		"浴衣の人",
		"ラブライバーファン帝国",
		"人混み",
		"岡村ちゃん"
	]
}
```


## /post_photo
写真を投稿し、Twitterにアップロード後、つぶやく  
（Content-Type：multipart/form-dataで送信）

| key | explanation |
|:-----------:|:------------:|
| user_id1       |  自分のID |
| user_id2       |  相手のID |
| lat       |  緯度（省略可） |
| lng       |  経度（省略可） |
| photo       |  写真のデータ |

返り値

```js
{
	"url": "http://twitter.com/TwittemSSI/status/624919189338243072/photo/1"
}
```


# Caution
Twitter related file isn't pushed.

Please excecute on root directory.