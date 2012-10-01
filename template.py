class Template:
    
    @classmethod
    def item(cls, url, title, permalink, num_comments, score, post_power, hours_ago, subreddit, self, type):
        
        if self == True:
            self = "<img src=http://www.remedicajournals.com/ijcr/App_Themes/journal/images/icons/reddit.gif>"
        else:
            self = "<img src=http://www.100noga.com.pl/files/ikonki/web2.png>"

        if type == "image":
            type = "<img src=http://www.co-operative.coop/Corporate/PDFs/jpg.gif>"
        elif type == "video":
            type = "<img src=http://new.gbgm-umc.org/umw/media/images/icons/youtube16.gif>"
        else:
            type = ""

        item = "<tr style=\"font-family: \"Lucida Sans Unicode\", \"Lucida Grande\", Sans-Serif; font-size: 12px; color: #669; vertical-align:middle;\"><td width=60%%><a style=\"text-decoration:none; font-family: \"Lucida Sans Unicode\", \"Lucida Grande\", Sans-Serif; font-size: 12px; \" href={0}>{1} {2} {3}</a></td><td><a href={4}>{5}</a></td><td>{6}</td><td>{7}</td><td>{8}</td><td>{9}</td></tr>\n".format(
            url, self, title, type, permalink, num_comments, score, post_power, hours_ago, subreddit)

        return item

    @classmethod
    def tablestart(cls, name):
    	tablestart = "<table width=95%% style=\"font-family: \"Lucida Sans Unicode\", \"Lucida Grande\", Sans-Serif; font-size: 12px; background: #fff; margin: 5px; border-collapse: collapse; text-align: left;\"><thead><tr>\n\
<th style=\"font-size: 14px; font-weight: normal; color: #039; padding: 10px 8px; border-bottom: 2px solid #6678b1;\" align=left>%s</th>\n\
<th style=\"font-size: 14px; font-weight: normal; color: #039; padding: 10px 8px; border-bottom: 2px solid #6678b1;\">Comments</th>\n\
<th style=\"font-size: 14px; font-weight: normal; color: #039; padding: 10px 8px; border-bottom: 2px solid #6678b1;\">Score</th>\n\
<th style=\"font-size: 14px; font-weight: normal; color: #039; padding: 10px 8px; border-bottom: 2px solid #6678b1;\">Post Power</th>\n\
<th style=\"font-size: 14px; font-weight: normal; color: #039; padding: 10px 8px; border-bottom: 2px solid #6678b1;\">Posted</th>\n\
<th style=\"font-size: 14px; font-weight: normal; color: #039; padding: 10px 8px; border-bottom: 2px solid #6678b1;\">Subreddit</th>\n\
    	</tr></thead><tbody>" % name
    	return tablestart

    @classmethod
    def tableend(cls):
    	tableend = "</tbody></table>"
    	return tableend

    @classmethod
    def head(cls):
    	head = "<html><body>"
    	return head

    @classmethod
    def tail(cls):
        tail = "</body></html>"
        return tail
