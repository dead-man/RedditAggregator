class Template:
    
    @classmethod
    def item(cls, url, title, permalink, num_comments, score, post_power, hours_ago, subreddit):
        item = "<tr><td width=60%><a href={0}>{1}</a></td><td><a href={2}>{3}</a></td><td>{4}</td><td>{5}</td><td>{6}</td><td>{7}</td></tr>\n".format(
            url, title, permalink, num_comments, score, post_power, hours_ago, subreddit)
        return item

    @classmethod
    def tablestart(cls, name):
    	tablestart = "<table id=tb><thead><tr>\n\
<th scope=col>%s</th>\n\
<th scope=col>Comments</th>\n\
<th scope=col>Score</th>\n\
<th scope=col>Post Power</th>\n\
<th scope=col>Posted</th>\n\
<th scope=col>Subreddit</th>\n\
    	</tr></thead><tbody>" % name
    	return tablestart

    @classmethod
    def tableend(cls):
    	tableend = "</tbody></table>"
    	return tableend

    @classmethod
    def head(cls):
    	head = "<head><style type=\"text/css\">\n\
#tb { font-family: \"Lucida Sans Unicode\", \"Lucida Grande\", Sans-Serif; font-size: 12px; background: #fff; margin: 5px; width: 95%; border-collapse: collapse; text-align: left; }\n\
#tb th { font-size: 14px; font-weight: normal; color: #039; padding: 10px 8px; border-bottom: 2px solid #6678b1; }\n\
#tb td { color: #669; padding: 9px 8px 0px 8px; }\n\
#tb tbody tr:hover td { background-color: #d6d9fb; }\n\
a {text-decoration:none}\n\
</style></head>\n\n"
    	return head
