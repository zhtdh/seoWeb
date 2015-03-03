# seoWeb

rendSec.html -- cont - list 模版。
cont -- 只需要一个模版就够了。
list 可以多个。都从rendSec继承下来就可以。
---------------------------单记录的模版----------------------------------
    <ol class="breadcrumb block-shadow">
      {% for iPos in renderVal.position %}
        <li><a href="{{ iPos.1 }}">{{ iPos.0 }}</a></li>
      {% endfor %}
    </ol>

    <div class="block-border-all block-shadow" style="min-height:600px; width:100%;padding:20px;">
        <p>{{ renderVal.contSingle.content | safe }}</p>
    </div>
---------------------------单记录的模版----------------------------------
---------------------------多记录的模版----------------------------------
    <div class="block-border-all block-shadow" style="min-height:400px; width:100%;padding:20px;">

      {% for iListItem in renderVal.contList %}
        {% cycle '<div class="row">' '' '' %}
          <div class="col-xs-4  block-center" style="padding:5px;">
            <a href="#" class="thumbnail">
              <img src="{{ iListItem.imglink }}" alt="Generic placeholder thumbnail">
            </a>
            {{ iListItem.content }}
            <br>
            <a href="{{ iListItem.link }}" type="button" class="btn btn-primary btn-xs">
              <i class="glyphicon glyphicon-forward"></i> 详细信息
            </a>
          </div>
        {% cycle  '' ''  '</div>' %}
      {% endfor %}
    </div>

---------------------------多记录的模版----------------------------------

多记录模版的类型：
rendSec-list.html : 一行3个。循环无限？。
