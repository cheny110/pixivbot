from fake_useragent import UserAgent

header={
"authority": "stats.g.doubleclick.net",
"scheme": "https",
"accept": "*/*",
"accept-encoding": "gzip, deflate, br",
"accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
"content-type": "text/plain",
"cookie": "id=OPT_OUT; DSID=ADtk6HMrHURwU7d-qPnp9lwyF7oCNnRyMrX9OMgHUvvu9U7uj7iLg6MA_uNW6VWYOqqVF3CJqF2_KQhBYtd7RcjVE9_a99_g8grm2c9Az66qEYJy14YxpFM6dKOmG4mcO7-Co2Z-vvQTOj1Z5A-4mbdhiHD5YdYZsWu8eUnk7L4fBBi9CE-NHc7xqFwzWIrJ3Ej6p46rNNZOR-FwBRg9hSC7Zo0pLnZFn8Q5VVLZfb0-k8ommHfdxBgrZ9yCqTGOULQbiEYSENmXnteWJ6cqN3PMdTbEJ4dO74V7EdIGIIwB0rHQpkJ4o8Y",
"dnt": '1',
"origin": "https://www.pixiv.net",
"referer": "https://www.pixiv.net/",
"sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "Linux",
"sec-fetch-dest": "empty",
"sec-fetch-mode": "cors",
"sec-fetch-site": "cross-site",
"user-agent":str(UserAgent(path="ua.json").random)
}