---
title:  "Zyxel Keenetic + NameCheap DDNS"
date:   2017-06-10 12:55:00 +0500
excerpt: Настройка DDNS от Namecheap на роутере Zyxel Keenetic.
---
Выбор провайдеров DDNS в роутере оказался на удивление малым:

![List of providers]({{ '/assets/images/posts/2017/06/10/zyxel-keenetic-namecheap-ddns-1.png' | relative_url }}){:class="img-fluid"}

DDNS на Namecheap настраивается по их инструкции: [How do I set up a Host for Dynamic DNS?](https://www.namecheap.com/support/knowledgebase/article.aspx/43/11/how-do-i-set-up-a-host-for-dynamic-dns)

Namecheap предоставляет следующие параметры, по [инструкции для DD-WRT](https://www.namecheap.com/support/knowledgebase/article.aspx/9356/11/how-to-configure-a-ddwrt-router):
* **DYNDNS Server**: dynamicdns.park-your-domain.com - the name of the server should not be changed
* **Username**: yourdomain.com - replace it with your domain name
* **Password**: Dynamic DNS password for your domain (Domain List >> click on the Manage button next to the domain >> the Advanced DNS tab >> Dynamic DNS)
* **Hostname**: Your subdomain (@ for yourdomain.com, www for www.yourdomain.com, etc.)
* **URL**: /update?domain=yourdomain.com&password=DynamicDNSPassword&host=

Параметр URL, как оказалось, в Zyxel указывать негде.

Однако, есть ещё инструкция для обновления через браузер: [How do I use a browser to dynamically update the host's IP?](https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-do-i-use-a-browser-to-dynamically-update-the-hosts-ip)

Обновить адрес можно, выполнив обычный запрос вида https://dynamicdns.park-your-domain.com/update?host=[host]&domain=[domain_name]&password=[ddns_password]&ip=[your_ip]<br>
Где
* Host = @
* Domain Name = yourdomain.tld
* Dynamic DNS Password = Domain List >> click Manage next to the domain >>Advanced DNS tab >> Dynamic DNS. If it is not enabled, enable it to check the password.
* IP Address = optional value. If you don't specify any IP, the IP from which you are accessing this URL will be set for the domain.

При необходимости обновления субдомена, вместо @ надо указать его имя. Для test.yourdomain.tld это будет просто test.

Далее надо подставить свои параметры в указанный выше URL и прописать его в настройках DDNS у Zyxel. Параметр your_ip не указывается. В этом случае, в качестве ip адреса будет взят тот внешний IP адрес, с которого поступит запрос. Т.е. внешний адрес роутера.

![Settings]({{ '/assets/images/posts/2017/06/10/zyxel-keenetic-namecheap-ddns-2.png' | relative_url }}){:class="img-fluid"}
