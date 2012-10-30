class Template:
    
    @classmethod
    def item(cls, url, title, permalink, num_comments, score, post_power, hours_ago, subreddit, self, type):
        
        if self == True:
            self = "<img src=img/reddit.gif>"
        else:
            self = "<img src=img/web2.png>"

        if type == "image":
            type = "<img src=img/jpg.gif>"
        elif type == "video":
            type = "<img src=img/youtube16.gif>"
        else:
            type = ""

        item = "<tr><td style=\"width:60%\"><a href={0}>{1} {2} {3}</a></td><td><a href={4}>{5}</a></td><td>{6}</td><td>{7}</td><td>{8}</td><td>{9}</td></tr>\n".format(
            url, self, title, type, permalink, num_comments, score, post_power, hours_ago, subreddit)

        return item

    @classmethod
    def tablestart(cls, name, num):

        num2=num

        if num==0:
            tablestart = "<div id=tab%s class=tab_content  style=\"display: block;\">" % num
        else:
            tablestart = "<div id=tab%s class=tab_content >" % num


        tablestart += "<script>$(document).ready(function() { $(\"#tb%s\").tablesorter(); } );</script>\n\
        <table id=tb%s class=tablesorter><thead><tr>\n\
<th scope=col>%s</th>\n\
<th scope=col>Comments</th>\n\
<th scope=col>Score</th>\n\
<th scope=col>Post Power</th>\n\
<th scope=col>Posted</th>\n\
<th scope=col>Subreddit</th>\n\
        </tr></thead><tbody>" % (num, num2, name)
        return tablestart

    @classmethod
    def tableend(cls):
        tableend = "</tbody></table></div>"
        return tableend

    @classmethod
    def head(cls, num, subname):

        import datetime

        head = "<head><style type=\"text/css\">\n\
#tb0, #tb1, #tb2, #tb3, #tb4, #tb5, #tb6, #tb7, #tb8, #tb9 { font-family: \"Lucida Sans Unicode\", \"Lucida Grande\", Sans-Serif; font-size: 12px; background: #fff; margin: 5px; width: 95%; border-collapse: collapse; text-align: left; }\n\
#tb0 th, #tb1 th,  #tb2 th, #tb3 th,  #tb4 th, #tb5 th,  #tb6 th, #tb7 th,  #tb8 th, #tb9 th  { font-size: 14px; font-weight: normal; color: #039; padding: 10px 8px; border-bottom: 2px solid #6678b1; }\n\
#tb0 td, #tb1 td, #tb2 td, #tb3 td, #tb4 td, #tb5 td, #tb6 td, #tb7 td, #tb8 td, #tb9 td  { color: #669; padding: 3px 8px 3px 8px; width:8%; vertical-align:middle}\n\
#tb0 tbody tr:hover td, #tb1 tbody tr:hover td, #tb2 tbody tr:hover td, #tb3 tbody tr:hover td, #tb4 tbody tr:hover td, #tb5 tbody tr:hover td, #tb6 tbody tr:hover td, #tb7 tbody tr:hover td, #tb8 tbody tr:hover td, #tb9 tbody tr:hover td  { background-color: #d6d9fb; }\n\
a {text-decoration:none}\n\
table.tablesorter thead tr .header {background-image: url(img/bg.gif);background-repeat: no-repeat;background-position: center right;cursor: pointer;}\n\
table.tablesorter thead tr .headerSortUp {background-image: url(img/asc.gif);}\n\
table.tablesorter thead tr .headerSortDown {background-image: url(img/desc.gif);}\n\
#tabs_wrapper {\n\
    width: 422px;\n\
}\n\
#tabs_container {\n\
    border-bottom: 1px solid #ccc;\n\
}\n\
#tabs {\n\
    list-style: none;\n\
    padding: 5px 0 4px 0;\n\
    margin: 0 0 0 10px;\n\
    font: 0.75em arial;\n\
}\n\
#tabs li {\n\
    display: inline;\n\
}\n\
#tabs li a {\n\
    border: 1px solid #ccc;\n\
    padding: 4px 6px;\n\
    text-decoration: none;\n\
    background-color: #eeeeee;\n\
    border-bottom: none;\n\
    outline: none;\n\
    border-radius: 5px 5px 0 0;\n\
    -moz-border-radius: 5px 5px 0 0;\n\
    -webkit-border-top-left-radius: 5px;\n\
    -webkit-border-top-right-radius: 5px;\n\
}\n\
#tabs li a:hover {\n\
    background-color: #dddddd;\n\
    padding: 4px 6px;\n\
}\n\
#tabs li.active a {\n\
    border-bottom: 1px solid #fff;\n\
    background-color: #fff;\n\
    padding: 4px 6px 5px 6px;\n\
    border-bottom: none;\n\
}\n\
#tabs li.active a:hover {\n\
    background-color: #eeeeee;\n\
    padding: 4px 6px 5px 6px;\n\
    border-bottom: none;\n\
}\n\
#tabs li a.icon_accept {\n\
    background-image: url(accept.png);\n\
    background-position: 5px;\n\
    background-repeat: no-repeat;\n\
    padding-left: 24px;\n\
}\n\
#tabs li a.icon_accept:hover {\n\
    padding-left: 24px;\n\
}\n\
#tabs_content_container {\n\
    border: 1px solid #ccc;\n\
    border-top: none;\n\
    padding: 10px;\n\
    width: 400px;\n\
}\n\
.tab_content {\n\
    display: none;\n\
}\n\
</style>\n\
<script type=\"text/javascript\" src=\"js/jquery-latest.js\"></script> \n\
<script type=\"text/javascript\" src=\"js/jquery.tablesorter.js\"></script>\n\
<script>\n\
$(document).ready(function(){\n\
    $(\"#tabs li\").click(function() {\n\
        $(\"#tabs li\").removeClass('active');\n\
        $(this).addClass(\"active\");\n\
        $(\".tab_content\").hide();\n\
        var selected_tab = $(this).find(\"a\").attr(\"href\");\n\
        $(selected_tab).fadeIn();\n\
        return false;\n\
    });\n\
});\n\
</script>\n\
</head>\n"

        head += "<p>{}</p>".format(datetime.datetime.now().strftime("%A, %d/%m/%y"))

        head += "<div id=tabs_container>\n\
    <ul id=tabs>\n\
        <li class=active><a href=#tab0>Tab</a></li>\n\
        <li><a href=#tab1>Tab</a></li>\n\
        <li><a href=#tab2>Tab</a></li>\n\
    </ul></div>"

        return head
