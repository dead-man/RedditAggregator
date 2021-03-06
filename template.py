class Template:
    
    @classmethod
    def item(cls, url, title, permalink, num_comments, score, post_power, hours_ago, subreddit, self, type):
        
        if self == True:
            self = "<img src=img/reddit.gif>"
        else:
            self = "<img src=img/web2.png>"

        if type == "image":
            self = "&nbsp;<img src=img/jpg.gif>"
        elif type == "video":
            self = "&nbsp;<img src=img/youtube16.gif>"
        else:
            type = ""

        keywords = [["google.gif", "google", "gmail", "nexus", "android", "chrome"],
["microsoft.png", "microsoft", "windows", "surface", "hotmail"],
["apple.png", "apple", "iphone", "mac", "ipad", "ipod", "steve jobs"],
["facebook.png", "facebook", "zuckerberg"],
["samsung.png", "samsung"],
["twitter.jpg", "twitter", "tweet"],
["tpb.png", "tpb", "pirate", "torrent", "sopa", "piracy", "megaupload", "kim dotcom", "drm", "privacy"],
["amazon.png", "amazon", "aws", "kindle", "turk"],
["usa.png", "usa", "united states", "romney", "bush", "clinton", "obama", "iran", "israel", "republican", "democrat", "nixon", "roosevelt", "eisenhower", "reagan"],
["china.gif", "china", "chinese", "foxconn"],
["marijuana.gif", "marijuana", "drug", "marihuana", "weed", "trees"],
["religion.gif", "religion", "vatican", "church", "atheism", "antitheism", "god", "jesus", "allah", "islam", "yahwe", "muhammad", "hell", "heaven", "bigot", "catholic", "christian", "sagan", "hitchen", "dawkins", "child abuse", "preacher"],
["money.png", "crysis", "fed", "recession", "austerity", "bail", "unemploy", "economy", "loan", "debt"],
["politics.png", "climate", "environment", "rights", "warming", "marriage", "abortion", "contraception", "prolife", "prochoice", "pro-life", "pro-choice", "healthcare"],
["rainbow.png", "gay", "homo", "rape", "equality", "lgbt", "trans"],
["cat.png", "cat", "pussy", "kitten"],
["dog.gif", "dog", "pup"]]


        for (i, group) in enumerate(keywords):
                for word in group:
                    if title.lower().find(word) != -1:
                        type += "<img src=img/{}>&nbsp;".format(keywords[i][0])
                        break




        item = "<tr><td style=\"width:60%\"><a href={0} target=\"_blank\">{1} {2} {3}</a></td><td><a href={4} target=\"_blank\">{5}</a></td><td>{6}</td><td>{7}</td><td>{8}</td><td>{9}</td></tr>\n".format(
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
<th scope=col>Hours Ago</th>\n\
<th scope=col>Subreddit</th>\n\
        </tr></thead><tbody>" % (num, num2, name)
        return tablestart

    @classmethod
    def tableend(cls):
        tableend = "</tbody></table></div>"
        return tableend

    @classmethod
    def head(cls, tabs, subnames):

        import datetime
        from time import gmtime, strftime

        head = "<head><title>Reddit Aggregator</title><style type=\"text/css\">\n\
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
<link rel=\"shortcut icon\" href=\"img/favicon.ico\" />\n\
<link href='http://fonts.googleapis.com/css?family=Ubuntu' rel='stylesheet' type='text/css'>\n"

        ####################fucked up beyond recognition CSS multiple table sorting fix####################

        c1="#tb0"
        c2="#tb0 th"
        c3="#tb0 td"
        c4="#tb0 tbody tr:hover td"

        if tabs>1:
            for i in range(1,tabs):
                c1+=", #tb{}".format(i)
                c2+=", #tb{} th".format(i)
                c3+=", #tb{} td".format(i)
                c4+=", #tb{} tbody tr:hover td".format(i)

        css = "{0} {{ font-family: \"Lucida Sans Unicode\", \"Lucida Grande\", Sans-Serif; font-size: 12px; background: #fff; margin: 5px; width: 95%; border-collapse: collapse; text-align: left; }}\n\
{1} {{ font-size: 14px; font-weight: normal; color: #039; padding: 10px 8px; border-bottom: 2px solid #6678b1; }}\n\
{2} {{ color: #669; padding: 3px 8px 3px 8px; width:8%; vertical-align:middle}}\n\
{3} {{ background-color: #d6d9fb; }}\n".format(c1, c2, c3, c4)

        head += "<style type=\"text/css\">\n"

        head += css

        head += "</style>"

        ###################################################################################################

        head += "</head>\n"




        s1=subnames[0].split(';')[0].capitalize()

        head += "<div id=tabs_container>\n\
    <ul id=tabs>\n\
        <li class=active><a href=#tab0>{}</a></li>".format(s1)

        if tabs>1:
            j=1
            for i in range(1,tabs):
                j = subnames[i].split(';')[0].capitalize()
                head += "<li><a href=#tab{0}>{1}</a></li>\n".format(i, j)

        head += "</ul></div>"
        head += "<p align=right style=\"font-family: 'Ubuntu', sans-serif; position:absolute; top:-10px; right:20px;\">{}</p>".format(datetime.datetime.now().strftime("%A, <date>%d/%m/%Y</date>, {}:%M").format(int(datetime.datetime.now().strftime("%H"))-3))

        return head
