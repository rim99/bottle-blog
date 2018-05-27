<template>
    <div id="front-page">
        <div>
        </div>
        <div id="header-container">
            <ul id="header">
                <li id="logo">
                     見微知著
                </li>
                <li id="left-option">
                    <a src="">About me</a>
                </li>
            </ul>
        </div>
        <div id="body-container">
            <div id="list-container" v-if="!showBlog">
                <ul id="post-list">
                    <li v-for="item in postList" id="post-item">
                        <div id="item-content" v-on:click="getBlog(item.blog_id)">
                            <div id="item-title">
                                {{ item.title }}
                            </div>
                            <div id="item-post-date">
                                {{ item.postDate }}
                            </div>
                            <ul id="item-tags">
                                <li v-for="tag in item.tags" id="tag-container">
                                    <div id="tag">
                                        {{ tag }}
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </li>
                </ul>
            </div>
            <div id="blog-post" v-if="showBlog">
               <div id="blog-container">
                    <div id="blog-close-btn" v-on:click="closeBlog">
                                <a href="" id="close-btn">&times;</a>
                    </div>
                    <div id="blog-date">
                        Posted on {{postDate}}
                    </div>
                    <div id="blog-content" v-html="blogContent"></div>
                    <div id="blog-end">- End -</div>
               </div>
            </div>
        </div>
        <div id="bottom">
            <div id="show-off">
                <span>💪 </span> <span id="after-symol">by Nginx</span>
            </div>
            <div id="license-container">
                <span>
                    <a id="license-block" rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
                        本博客内容采用<u>知识共享署名-相同方式共享 4.0 国际许可协议 (CC BY-SA 4.0) </u>进行许可。
                    </a>
                </span>
                <span> CopyRight Always @ Zhang, Xin </span>
                <div id="license-block">Icon made from <a id="license-block" href="http://www.onlinewebfonts.com/icon">Icon Fonts</a> is licensed by CC BY 3.0</div>
            </div> 
        </div>
    </div>    
</template>

<script>
export default {
  name: 'Blog',
  methods:{
      getBlog: function (id) {
            this.scrollY = window.scrollY
            this.postDate = "2018-01-01 00:00:000"
            this.blogContent = '<div id=\"blogpost\">\n<h1 id=\"toc_0\"><a name=\"toc_0\" class=\"vnote-anchor\" href=\"#\"></a>如何自定义数据类型</h1>\n<blockquote>\n<p>本文主要摘译自<a href=\"http://www.ccs.neu.edu/home/matthias/HtDP2e/part_one.html\">HtDP第五章</a>，并结合Python语言的实际情况略作修改。原有语言DrRacket改写为Python。</p>\n</blockquote>\n<p>通常的，编程语言都会提供基本的预定义数据类型，比如整型、浮点型、字符串类型等等。但是，当用编程来解决实际问题时，我们往往会发现这些很难满足需求。比如，我们需要建立一个公司的员工数据模型，其中包含姓名，年龄，性别，职务，联系手机等信息。这个模型包含了五条信息，根本没法用语言预先定义的数据类型来表达。</p>\n<p>幸运的是，编程语言还提供了自定义数据类型的方法：面向过程的语言，如C，可以自定义一个结构体(Struct)；面向对象的语言，如Python可以自定义一个类(Class)。</p>\n<pre><code class=\"lang-python hljs\"><table class=\"hljs-ln\"><tbody><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"1\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-meta\">&gt;&gt;&gt; </span><span class=\"hljs-class\"><span class=\"hljs-keyword\">class</span> <span class=\"hljs-title\">Personel_Info</span><span class=\"hljs-params\">(object)</span>:</span></div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"2\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-meta\">... </span>    <span class=\"hljs-function\"><span class=\"hljs-keyword\">def</span> <span class=\"hljs-title\">__init__</span><span class=\"hljs-params\">(self, name, age, gender, post, cellphone_no)</span>:</span></div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"3\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-meta\">... </span>            self.name = name</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"4\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-meta\">... </span>            self.age = age</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"5\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-meta\">... </span>            self.gender = gender</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"6\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-meta\">... </span>            self.post = post</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"7\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-meta\">... </span>            self.cellphone_no = cellphone_no</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"8\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-meta\">... </span></div></td></tr></tbody></table></code></pre>\n<p>实际上，定义一个数据类型的同时，也还定义了三类函数：</p>\n<ul>\n<li>\n<p>构造函数(constructor)，使用这一函数能够继续构造同样类型的数据实例(instance)。例如，李明，29岁，男，经理，手机号码：29900123456。</p>\n<pre><code class=\"lang-python hljs\"><table class=\"hljs-ln\"><tbody><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"1\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-meta\">&gt;&gt;&gt; </span>li_ming = Personel_Info(<span class=\"hljs-string\">\"Li Ming\"</span>, <span class=\"hljs-number\">29</span>, <span class=\"hljs-string\">\"Male\"</span>, <span class=\"hljs-string\">\"Manager\"</span>, <span class=\"hljs-number\">29900123456</span>)</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"2\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-meta\">&gt;&gt;&gt; </span>li_ming</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"3\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\">&lt;__main__.Personel_Info object at <span class=\"hljs-number\">0x10e13b990</span>&gt;</div></td></tr></tbody></table></code></pre>\n</li>\n<li>\n<p>指针函数(selector)，使用这一函数能够对数据实例的具体某一项执行取赋值操作。下例展示了对<code>li_ming</code>的<code>name</code>项的取赋值操作。</p>\n<pre><code class=\"lang-python hljs\"><table class=\"hljs-ln\"><tbody><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"1\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-meta\">&gt;&gt;&gt; </span>li_ming.name</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"2\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-string\">\"Li Ming\"</span></div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"3\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-meta\">&gt;&gt;&gt; </span>li_ming.name=<span class=\"hljs-string\">\"Wang Lili\"</span></div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"4\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-meta\">&gt;&gt;&gt; </span>li_ming.name</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"5\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-string\">\"Wang Lili\"</span></div></td></tr></tbody></table></code></pre>\n</li>\n<li>\n<p>判断函数(structure predicate)，使用这一函数能够判断某一数据是否为所定义的类型。Python使用<code>instance()</code>函数判断，数据实例和数据类型为该函数的参数。</p>\n<pre><code class=\"lang-python hljs\"><table class=\"hljs-ln\"><tbody><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"1\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-meta\">&gt;&gt;&gt; </span>isinstance(li_ming, Personel_Info)</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"2\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-keyword\">True</span></div></td></tr></tbody></table></code></pre>\n</li>\n</ul>\n<h2 id=\"toc_1\"><a name=\"toc_1\" class=\"vnote-anchor\" href=\"#\"></a>编写数据类型的说明</h2>\n<p>之前的例子有个小瑕疵：<strong>缺乏说明</strong>。</p>\n<p>试想一下，如果数据录入人员不清楚<code>age</code>的类型，有可能会录入字符串<code>\"29\"</code>，如果再换一个人，又可能录入了数字类型<code>29</code>。这些差异会对后期数据处理造成麻烦：得先判断是什么类型，然后执行下一步指令。从而，严重拖累程序效率。</p>\n<p>这是本书推荐的数据类型说明样例：</p>\n<pre><code class=\"lang-python hljs\"><table class=\"hljs-ln\"><tbody><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"1\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\"><span class=\"hljs-class\"><span class=\"hljs-keyword\">class</span> <span class=\"hljs-title\">Personel_Info</span><span class=\"hljs-params\">(object)</span>:</span></div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"2\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\">\t<span class=\"hljs-string\">\"\"\"</span></div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"3\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\">\tA Personel_Info is a class: Personel_Info( str, int, str, str, int)  # 写出构造函数，参数中注明数据类型，可以是语言预定义的类型，也可以是之前定义好的自定义类型</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"4\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\">\t</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"5\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\">\tInterpretation : Represent a person of the company.  # 注明该数据类型所表达的实际意义</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"6\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\">\t\"\"\"</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"7\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\">\t</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"8\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\">    <span class=\"hljs-function\"><span class=\"hljs-keyword\">def</span> <span class=\"hljs-title\">__init__</span><span class=\"hljs-params\">(self, name, age, gender, post, cellphone_no)</span>:</span></div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"9\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\">            self.name = name</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"10\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\">            self.age = age</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"11\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\">            self.gender = gender</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"12\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\">            self.post = post</div></td></tr><tr><td class=\"hljs-ln-numbers\"><div class=\"hljs-ln-line hljs-ln-n\" data-line-number=\"13\"></div></td><td class=\"hljs-ln-code\"><div class=\"hljs-ln-line\">            self.cellphone_no = cellphone_no </div></td></tr></tbody></table></code></pre>\n<p>如有必要，还应该在说明中举例：</p>\n<ol>\n<li>如果是语言的预定义类型，数字、字符串、布尔值等，可以直接给出自己喜欢的例子；（有些指南会建议取一个描述性的名字，然而还是比不上好的数据类型说明）</li>\n<li>对于枚举类型，可以从中选择若干；</li>\n<li>对于区间类型，应该给出边际值，如果包含的话，同时再给出一个区间中间值；</li>\n<li>如果是选择结构类型（类似于数学中的分类函数），应该各自举例；</li>\n<li>对于自定义类型，就给出一个数据实例。</li>\n</ol>\n\n</div><table><thead><tr><th style=\"text-align:center\">表头1</th><th style=\"text-align:left\">表头2</th></tr></thead><tbody><tr><td style=\"text-align:center\">表哥1</td><td style=\"text-align:left\">表格2</td></tr><tr><td style=\"text-align:center\">表格3</td><td style=\"text-align:left\">表格4</td></tr></tbody></table>'
            this.showBlog = true
            window.scrollTo(0,0);
        },
      closeBlog: function() {
          this.showBlog = false;
          var yPlot = this.scrollY;
          console.log(yPlot)
          setTimeout(function () {
                console.log(yPlot)
                window.scrollTo(0, yPlot);
            }, 50); 
        }
  },
  data () {
    return {
      scrollY: 0,
      blogContent: "",
      showBlog: false,
      postList: [
        { title: '学习 JavaScript',
          blog_id:"learn_js",
          tags: ["tag1", "tag2"],
          postDate: "2016-08-10 09:18:42.222" },
        { title: '两个PostgreSQL和Spring Data JPA之间的坑',
          blog_id:"pitfall_about_pqsql_jpa",
          tags: ["tag1", "tag2"],
          postDate: "2016-08-10 09:18:42.222" },
        { title: '整个牛项目',
          tags: ["tag1", "tag2"],
          postDate: "2016-08-10 09:18:42.222" },
          { title: '学习 JavaScript',
          tags: ["tag1", "tag2"],
          postDate: "2016-08-10 09:18:42.222" },
        { title: '学习 Vue',
          tags: ["tag1", "tag2"],
          postDate: "2016-08-10 09:18:42.222" },
        { title: '整个牛项目',
          tags: ["tag1", "tag2"],
          postDate: "2016-08-10 09:18:42.222" },
          { title: '学习 JavaScript',
          tags: ["tag1", "tag2"],
          postDate: "2016-08-10 09:18:42.222" },
        { title: '学习 Vue',
          tags: ["tag1", "tag2"],
          postDate: "2016-08-10 09:18:42.222" },
        { title: '整个牛项目',
          tags: ["tag1", "tag2"],
          postDate: "2016-08-10 09:18:42.222" },
          { title: '学习 JavaScript',
          tags: ["tag1", "tag2"],
          postDate: "2016-08-10 09:18:42.222" },
        { title: '学习 Vue',
          tags: ["tag1", "tag2"],
          postDate: "2016-08-10 09:18:42.222" },
        { title: '整个牛项目',
          tags: ["tag1", "tag2"],
          postDate: "2016-08-10 09:18:42.222" },
          { title: '学习 JavaScript',
          tags: ["tag1", "tag2"],
          postDate: "2016-08-10 09:18:42.222" },
        { title: '学习 Vue',
          tags: ["tag1", "tag2"],
          postDate: "2016-08-10 09:18:42.222" },
        { title: '整个牛项目',
          tags: ["tag1", "tag2"],
          postDate: "2016-08-10 09:18:42.222" }
      ]
    }
  }
//   template: '<PostList/>'
//   el: '#post-list',
//   data: {
//     posts: []
//   },
//   created: function () {
//     // Alias the component instance as `vm`, so that we  
//     // can access it inside the promise function
//     var vm = this
//     // Fetch our array of posts from an API
//     fetch('https://jsonplaceholder.typicode.com/posts')
//       .then(function (response) {
//         return response.json()
//       })
//       .then(function (data) {
//         vm.posts = data
//       })
//   }
//   template:"<h1> list </h1>"
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style src="../assets/blog-content.css"></style>

<style scoped>
/* Header Style*/
div#header-container {
    top: 0;
    left: 0;
    right: 0;
    margin: 0;
    padding: 0;
    position: fixed;
    width: 100%;
    height: 6em;
    background-color: #fff;
    box-sizing: border-box;
    display: block!important;
    box-shadow: 0 0 8px rgba(0,0,0,.2);
    opacity: 0.999995;
    border-bottom-style: solid;
    border-bottom-color: rgb(221, 218, 218);
    border-bottom-width: 0.2px;
    z-index: 10000;
}

ul#header {
    text-align: center;
    display: table;
    padding-left: 4%;
    padding-right: 4%;
    width: 92%;
    height: 85%;
}

li#logo {
    display: table-cell;
    width: 2em;
    text-align: left;
    padding-left: 0;
    width: 50%;
    vertical-align: middle;
    font-family: Arial, Helvetica, "STHeiti Light", "Hiragino Sans GB", "STXihei", "Microsoft YaHei", sans-serif;
    font-size: 3em;
}

li#left-option {
    display: table-cell;
    width: 2em;
    padding: 0;
    width: 50%;
    text-align: right;
    vertical-align: middle;
}

li#left-option a {
  color: #42b983;
  margin-top: 0;
}

/* Post List Style */
ul#post-list, div#blog-post {
    display:table;
    margin: auto;
    margin-top: 6em;
    width: 70em;
    -webkit-padding-start: 0;
}

div#blog-post {
    opacity: 0.98;
    padding-top: 8%;
    padding-bottom: 5%; 
}

div#blog-close-btn {
    text-align: right;
    padding-right: 1.5%;
    font-size: 3em;
}
a#close-btn {
    text-decoration: none;
}

div#blog-date, div#blog-content{
    margin: auto;
    width: 50em;
}

div#blog-date {
    display: table;
    text-align: left;
    font-style: italic;
    font-family: 'Courier New', Courier, monospace;
}

div#blog-end {
    margin-top: 6%;
    width: auto;
    text-align: center;
}

div#blog-container {
    background-color: beige;
    margin-top: 3%;
    padding-bottom: 3%;
    box-shadow: 4px 4px 18px rgba(0,0,0,.2);  
    width: 100%;
    border-radius: 1.7em;
}

li#post-item {
    display: table-row;
    width: 100%;
    position: relative;
}

div#item-content, div#item-background {
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    margin: auto;
    width: 55em;
    height: 100%;
    padding-bottom: 1em; 
    margin-top: 2.5em; 
    border-radius: 0.7em;
} 

div#item-content {
    background-color: whitesmoke;
    border: lightgray;
    box-shadow: 1px 3px 2px gray;
    opacity: 0.99;
    z-index: 100;
}

div#item-content:hover {
    filter: brightness(1.2);
    box-shadow: 2px 6px 4px rgb(95, 94, 94);
}

div#item-title {
    width: 100%;
    height: 2.0em;
    font-size: 2em;
    padding-top: 0.8em;
    text-align: left;
    text-indent: 0.9em;
}

ul#tags {
    display: table;
}

li#tag-container {
    display: table-cell;
}

div#tag {
    background-color: red;
    margin-right: 1em;
    padding-left: 0.7em;
    padding-right: 0.7em;

}

div#item-post-date {
    text-align: right;
    margin-right: 2em;
}

div#bottom {
    z-index: 10000;
    margin-top: 2em;
    margin-bottom: 0;
    text-align: center;
    display: table;
    padding-left: 8%;
    padding-right: 8%;
    width: 84%;
    height: 4.2em;
    background-color: #134b4b;
    opacity: 0.9;
    color:gold; 
}

div#show-off {
    margin-top:1em;
}

span#after-symol {
    margin-left: 0.3em;
}

div#license-container {
    margin-top: 0.3em;
    margin-bottom: 0.3em;
    font-size: 0.2em;
    font-style:italic;
}

a#license-block {
    text-decoration: none;
    color: white;
    vertical-align: middle;
    text-align: center;
    width: 100%;
    height: 100%;
}

div#license-block {
    text-decoration: none;
    color: white;
    vertical-align: middle;
    text-align: center;
    width: 100%;
    height: 100%;
}
</style>
