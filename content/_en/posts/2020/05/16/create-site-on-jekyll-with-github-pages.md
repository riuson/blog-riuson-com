---
title:  "Creating Jekyll site with GitHub Pages"
date:   2020-05-16 13:22:00 +0500
categories: jekyll
---
How to setup Jekyll for GitHub Pages on local machine.
<!-- more -->
{% highlight bash %}
gem install bundler:2.1.4
bundle init
bundle add jekyll -v 3.8.5
 gem "github-pages", "~> 204", group: :jekyll_plugins
bundle update
bundle exec jekyll –version
bundle add jekyll new . --force
{% endhighlight %}

Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].

[jekyll-docs]: https://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
