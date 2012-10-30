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
        tablestart = "<script>$(document).ready(function() { $(\"#tb%s\").tablesorter(); } );</script>\n\
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
        tableend = "</tbody></table>"
        return tableend

    

    @classmethod
    def head(cls):
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
</style>\n\
<script type=\"text/javascript\" src=\"js/jquery-latest.js\"></script> \n\
<script type=\"text/javascript\" src=\"js/jquery.tablesorter.js\"></script>\n\
</head>\n"

        head += "<p>{}</p>".format(datetime.datetime.now().strftime("%A, %d/%m/%y"))

        return head
