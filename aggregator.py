
import json
import urllib2
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
import datetime
import sys # just for testing

class RedditOpener:
    def __init__(self):
        self.user_agent = 'PrivateRedditAggregatorBot/1.0'
        self.opener = urllib2.build_opener()
        self.opener.add_handler(urllib2.HTTPCookieProcessor())
        self.opener.addheaders = [('User-agent', self.user_agent)]

    def open(self, url):
        try:
            return self.opener.open(url)
        except urllib2.HTTPError as error:
            return error

class RedditPost:

    ref_score = {}

    def __init__(self, **data ):

        self.subreddit = data['subreddit']
        self.id = data['id']
        self.title = data['title']
        self.num_comments = data['num_comments']
        self.score = data['score']
        self.permalink = 'http://reddit.com' + data['permalink']
        self.name = data['name']
        self.url = data['url']
        self.created_utc  = data['created_utc']

    def __str__(self):
        return u'title: {} - score: {} - posted: {} hours ago - post_power: {}'.format(self.title, 
            self.score + self.num_comments, (time.time() - self.created_utc) / 3600, self.post_power()).encode("utf-8")

    @classmethod
    def load_posts(cls, posts_json):
        return [RedditPost(**post['data']) for post in posts_json ]

    @classmethod
    def calculate_ref_score(cls, reddit_posts, subreddit = ''):
        ref_score = 0
        if subreddit == '' and len(reddit_posts) > 0:
            subreddit = reddit_posts[0].subreddit
        for item in reddit_posts[:3]:
            ref_score += item.score + item.num_comments
        ref_score /= 7.0
        cls.ref_score[subreddit] = ref_score
        return ref_score

    def post_power(self):
        ago = (time.time() - self.created_utc) / 3600
        postscore = self.score + self.num_comments
        pp = (25 / ago) * postscore / self.ref_score[self.subreddit]
        return pp

class RedditLoader:
    last_req_time = 0
    retries = 0
    opener = RedditOpener()
    reddit_cache = {}

    @classmethod
    def load_json_from_url(cls, url, delay = 2, cache_refresh_interval = 300):

        if url in cls.reddit_cache and time.time() - cls.reddit_cache[url]['last_refresh'] < cache_refresh_interval:
            print 'url ' + url + ' arleady in cache, NOT REQUESTING'
            return cls.reddit_cache[url]['posts']

        time_elapsed_since_last_req = time.time() - cls.last_req_time
        time_required = delay
        if (time_elapsed_since_last_req < time_required):
            #print 'sleeping for ' , time_required - time_elapsed_since_last_req
            time.sleep(time_required - time_elapsed_since_last_req)
        print 'requesting url ' , url
        cls.last_req_time = time.time()
        response = cls.opener.open(url)
        print 'site responded with HTTP code: ', response.getcode()

        json_message = response.read()
        #print '...and message: ', json_message
        json_dct = json.loads(json_message)

        if 'data' in json_dct and 'children' in json_dct['data']:
            cls.retries = 0
            if url not in cls.reddit_cache: 
                cls.reddit_cache[url] = {}
            cls.reddit_cache[url]['last_refresh'] = time.time()
            cls.reddit_cache[url]['posts'] = json_dct['data']['children']
            return json_dct['data']['children']
        elif cls.retries >= 20:
            print ' retries no exceeded... exiting'
            sys.exit(1)
        else:
            print ' site returned no posts: ', json_dct
            
            
            cls.retries += 1
            print 'retrying....', cls.retries

            ''' ZROBIONE REKURENCYJNIE TYLKO DO TESTOW!!!!!!!!!!!!!!!#$@%^%'''
            return cls.load_json_from_url(url, delay = delay*1.5)
            #sys.exit(1)

    @classmethod
    def load_subreddit(cls, subreddit, suffix = '', t = '', post_no = 25):
        url = 'http://www.reddit.com/r/' + subreddit + '/' + suffix + '.json' + t
        posts = cls.load_json_from_url(url)
        loaded = len(posts)
        if loaded < 25 : 
            return RedditPost.load_posts(posts)
        else:
            while len(posts) >= 25 and len(posts) < post_no and loaded > 0:
                 last_post_id = posts[-1]['data']['name']
                 next_site = cls.load_json_from_url(url + '&after=' + last_post_id)
                 loaded = len(next_site)
                 posts += next_site
            return RedditPost.load_posts(posts[:post_no])

    @classmethod
    def aggregate_subreddits(cls, reddit_list, ref_cat = 'top/', ref_t = '?t=month', posts_per_sub = 25 , 
        time_frame = 90000, pp_treshold = 0.5):

        output_list = []

        for subreddit in reddit_list:
        
            post_list = []

            top_posts = RedditLoader.load_subreddit(subreddit, ref_cat, ref_t)
            RedditPost.calculate_ref_score(top_posts)

            posts = RedditLoader.load_subreddit(subreddit, post_no = posts_per_sub)
            
            for item in posts:
                #TODO sprawdzic zwracane czasy (time() nie zwraca czasu utc)
                if (time.time()-item.created_utc) < time_frame and item.post_power() >= pp_treshold: 

                    post_list.append([item.title, item.url])

            output_list.append({subreddit : post_list})
                  
  

        return output_list

class UserCfg:
    def __init__(self, **usercfg):
        self.username = usercfg['username']
        self.usr_mail = usercfg['usr_mail']
        self.gmail_login_user = usercfg['gmail_login_user']
        self.gmail_login_pwd = usercfg['gmail_login_pwd']
        self.subject_tmpl = usercfg['subject_tmpl']
        self.ref_cat = usercfg['ref_cat']
        self.ref_t = usercfg['ref_t']
        self.posts_per_sub = usercfg['posts_per_sub']
        self.time_frame = usercfg['time_frame']
        self.pp_treshold = usercfg['pp_treshold']
        self.subreddits = usercfg['subreddits']
        


def mail(to, subject, text, gmail_user, gmail_pwd):
   msg = MIMEMultipart()
   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject
   msg.attach(MIMEText(text))
   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   mailServer.close()

def load_configs():
    ''' TODO  docelowo funkcja powinna ladowac configi z plik[u|ow] '''

    user1_cfg = {
        'username' : 'user1',
        'usr_mail' : 'xelnyq@gmail.com',
        'gmail_login_user' : 'raggregator@gmail.com',
        'gmail_login_pwd' : 'secret',
        'subject_tmpl' : 'Reddit Aggregator\'s news for {date}',
        'ref_cat' : 'top/', 'ref_t' : '?t=month', 'posts_per_sub' : 25 , 'time_frame' : 90000, 'pp_treshold' : 0.5,
        'subreddits' : ['philosophy', 'cogsci', 'minimalism', 'webdev']
        # 'subreddits' : ['philosophy', 'cogsci', 'minimalism', 'webdev', 'windows', 'linux', 'videos', 'funny', 'wtf', 
        # 'aww', 'atheism', 'science', 'technology', 'neuro', 'psychology', 'CultCinema']
    }

    user2_cfg = {
        'username' : 'user2',
        'usr_mail' : 'xelnyq@gmail.com',
        'gmail_login_user' : 'raggregator@gmail.com',
        'gmail_login_pwd' : 'secret',
        'subject_tmpl' : 'Reddit Aggregator\'s news for {date}',
        'ref_cat' : 'top/', 'ref_t' : '?t=month', 'posts_per_sub' : 25 , 'time_frame' : 90000, 'pp_treshold' : 0.5,
        'subreddits' : ['philosophy', 'minimalism',  'windows', 'webdev', 'linux', 'videos']
        # 'subreddits' : ['philosophy', 'cogsci', 'minimalism', 'webdev', 'windows', 'linux', 'videos', 'funny', 'wtf', 
        # 'aww', 'atheism', 'science', 'technology', 'neuro', 'psychology', 'CultCinema']
    }

    return [UserCfg(**user1_cfg)] + [UserCfg(**user2_cfg)]


def main():


    userlist = load_configs()


    
    for user in userlist:

        value = RedditLoader.aggregate_subreddits(user.subreddits, ref_cat = user.ref_cat, ref_t = user.ref_t, 
            posts_per_sub = user.posts_per_sub , time_frame = user.time_frame, pp_treshold = user.pp_treshold)

        print '########################################################################################################'
        print 'POSTS FOR USER: ' + user.username
        print json.dumps(value, indent = 4)

        # TEMPORARILY commented out
        # text = json.dumps(value, indent = 4)
        # mail(user.usr_mail, user.subject_tmpl.format(date = datetime.datetime.now().strftime("%d-%m-%Y")), text, 
        #     user.gmail_login_user, user.gmail_login_pwd)
       

if __name__ == "__main__":
    main()
