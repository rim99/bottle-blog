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
                        <div id="item-content" v-on:click="getBlog(item.id)">
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
                        Posted on {{ postDate }}
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
  created: function() {
      this.getList();
  },
  filters: {
      time: function (value) {
            return value.split(" ")[0];
        }
  },
  methods:{
      getList: function() {
            // Alias the component instance as `vm`, so that we  
            // can access it inside the promise function
            let headers = new Headers();
            headers.append('Content-Type', 'application/json');
            headers.append('Accept', 'application/json');
            headers.append('Access-Control-Allow-Origin', 'http://localhost:1024');
            headers.append('Access-Control-Allow-Credentials', 'true');
            var vm = this
            fetch('http://localhost:1024/api/blog/list', headers=headers)
            .then(function (response) {
                console.log('get response')
                var ans = response.json();
                console.log(ans)
                return ans;
            })
            .then(function (data) {
                console.log('get data')
                console.log(data)
                vm.postList = data
            })
        },
      getBlog: function (id) {
            this.scrollY = window.scrollY
            let headers = new Headers();
            headers.append('Content-Type', 'application/json');
            headers.append('Accept', 'application/json');
            headers.append('Access-Control-Allow-Origin', 'http://localhost:1024');
            headers.append('Access-Control-Allow-Credentials', 'true');
            var vm = this
            fetch('http://localhost:1024/api/blog/blog_id/'+id, headers=headers)
            .then(function (response) {
                console.log('get response')
                var ans = response.json();
                return ans;
            })
            .then(function (data) {
                vm.postDate = data.postDate
                vm.blogContent = data.content
            })
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
  data() {
      return {
        scrollY: 0,
        blogContent: "",
        showBlog: false,
        postList: null 
      }
  }
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
    color: white;
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


@media (max-width: 1050px) {
    div#item-content, div#item-background {
        margin-left: 5%;
        width: 60%;
    } 
    div#body-container {
        width:65%;
    }
    div#blog-container {
        margin-top: 0;
        width: 59%;
        margin-left: 1%;
    }
    div#blog-date{
        padding-left: 2em;
    }
    div#blog-content {
        margin-left: 2em;
    }
}


@media (max-width: 700px) {
    div#item-content, div#item-background {
        margin-left: 5%;
        width: 50%;
    } 
    div#body-container {
        width:50%;
    }
    div#blog-container {
        margin-top: 0;
        width: 59%;
        margin-left: 1%;
    }
    div#blog-date{
        padding-left: 2em;
    }
    div#blog-content {
        margin-left: 2em;
    }
}



@media (max-width: 640px) {
    div#item-content, div#item-background {
        margin-left: 2%;
        width: 30%;
    }
    div#item-title{
        font-size: 1.2em;
    }
    div#item-post-date{
        font-size: 0.5em;
        margin-right: 1em;
    }
    ul#item-tags {
         padding-left: 1em;
    }
    div#tag {
     font-size: 0.5em;

    }
    li#logo {
        font-size: 2em;
    }	
    div#blog-container {
        margin-top: 0;
        width: 39%;
        margin-left: 1%;
    }
}

</style>
