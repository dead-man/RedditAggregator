
import json
import urllib2
import time
import smtplib
import datetime
import math
import sys
import glob
import urlparse
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
import config as cfg
from template import Template

class RedditOpener:
    def __init__(self):
        self.user_agent = cfg.user_agent
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


    def __init__(self, pp_alg = cfg.default_user_cfg['pp_alg'], **data ):

        self.subreddit = data['subreddit']
        self.id = data['id']
        self.title = data['title']
        self.num_comments = data['num_comments']
        self.score = data['score']
        self.permalink = 'http://reddit.com' + data['permalink']
        self.name = data['name']
        self.url = data['url']
        self.created_utc  = data['created_utc']

        self.pp_alg = pp_alg

    def __str__(self):
        return u'title: {} - score: {} - posted: {} hours ago - post_power: {}'.format(self.title, 
            self.score + self.num_comments, (time.time() - self.created_utc) / 3600, self.post_power()).encode("utf-8")

    @classmethod
    def load_posts(cls, posts_json, pp_alg = cfg.default_user_cfg['pp_alg']):
        return [RedditPost(pp_alg = pp_alg, **post['data']) for post in posts_json ]


    @classmethod
    def calculate_ref_score(cls, reddit_posts, subreddit = ''):
        if subreddit == '' and len(reddit_posts) > 0:
            subreddit = reddit_posts[0].subreddit
            pp_alg = reddit_posts[0].pp_alg

        cls.ref_score[subreddit] = {}

        if pp_alg == 'default':
            cls.ref_score[subreddit][pp_alg] = cls._calculate_ref_score_default(reddit_posts, subreddit = subreddit)
        else:
            raise NotImplementedError('Unknown post_power alghorithm.')
        #print 'ref_score for subreddit '+ subreddit + ': ' + str(cls.ref_score[subreddit][pp_alg]) + ' pp_alg: ' + pp_alg
        return cls.ref_score[subreddit][pp_alg]


    @classmethod
    def _calculate_ref_score_default(cls, reddit_posts, subreddit = ''):
        ref_score = 0
        
        for item in reddit_posts[:3]:
            ref_score += item.score + item.num_comments
        ref_score /= 7.0
        #cls.ref_score[subreddit] = ref_score
        return ref_score

    def post_power(self):
        if self.pp_alg == 'default':
            return self._post_power_default()
        else:
            raise NotImplementedError('Unknown post_power alghorithm.')


    def _post_power_default(self):
        ago = (time.time() - self.created_utc) / 3600
        postscore = self.score + self.num_comments
        pp = (25 / ago) * postscore / self.ref_score[self.subreddit][self.pp_alg]
        return pp

    def hours_ago(self):
        ago = int(math.ceil((time.time() - self.created_utc) / 3600))

        if ago==1:
            hr="hour"
        else:
            hr="hours"

        string = "%r %s ago" % (ago, hr)
        return string

class RedditLoader:
    last_req_time = 0
    retries = 0
    opener = RedditOpener()
    reddit_cache = {}

    @classmethod
    def load_json_from_url(cls, url, delay = cfg.default_request_delay, cache_refresh_interval = cfg.default_cache_refresh_interval):

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
        elif cls.retries >= cfg.max_retries:
            print ' retries no exceeded... exiting'
            sys.exit(1)
        else:
            print ' site returned no posts: ', json_dct
            
            
            cls.retries += 1
            print 'retrying....', cls.retries
            return cls.load_json_from_url(url, delay = delay * cfg.retry_delay_multiplier, cache_refresh_interval = cache_refresh_interval)

    @classmethod
    def build_url(cls, subreddit, site = '', t = '', after = ''):
        if subreddit == '':
            return 'http://www.reddit.com/'

        if site == '':
            url = 'http://www.reddit.com/r/' + subreddit + '/.json'
        else:
            url = 'http://www.reddit.com/r/' + subreddit + '/' + site + '/.json'

        params = []

        if t != '':
            params.append('t=' + t)
        if after != '':
            params.append('after=' + after)

        if len(params) == 0:
            return url
        else:
            url += '?'
            for i, param in enumerate(params):
                url += param
                if i + 1 == len(params): break
                url += '&'

        return url


    @classmethod
    def load_subreddit(cls, subreddit, suffix = '', t = '', post_no = cfg.posts_in_json_page, pp_alg = cfg.default_user_cfg['pp_alg']):
        posts = cls.load_json_from_url(cls.build_url(subreddit, site = suffix, t = t))
        loaded = len(posts)
        if loaded < cfg.posts_in_json_page : 
            return RedditPost.load_posts(posts, pp_alg = pp_alg)
        else:
            while len(posts) >= cfg.posts_in_json_page and len(posts) < post_no and loaded > 0:
                 last_post_id = posts[-1]['data']['name']
                 next_site = cls.load_json_from_url(cls.build_url(subreddit, site = suffix, t = t, after = last_post_id))
                 loaded = len(next_site)
                 posts += next_site
            return RedditPost.load_posts(posts[:post_no], pp_alg = pp_alg)

    @classmethod
    def aggregate_subreddits(cls, reddit_list = [], user = None, ref_cat = cfg.default_user_cfg['ref_cat'], 
        ref_t = cfg.default_user_cfg['ref_t'], 
        posts_per_sub = cfg.default_user_cfg['posts_per_sub'] , 
        time_frame = cfg.default_user_cfg['time_frame'], 
        pp_treshold = cfg.default_user_cfg['pp_treshold'], 
        sort_key = None, reverse_sort_order = True, 
        pp_alg = cfg.default_user_cfg['pp_alg'] , 
        domain_filter = cfg.default_user_cfg['domain_filter']):

        if user != None:
            reddit_list = user.subreddits 
            ref_cat = user.ref_cat 
            ref_t = user.ref_t 
            posts_per_sub = user.posts_per_sub
            time_frame = user.time_frame
            pp_treshold = user.pp_treshold
            sort_key = user.sort_key
            reverse_sort_order = user.reverse_sort_order
            pp_alg = user.pp_alg
            domain_filter = user.domain_filter


        output_list = []

        for entry in reddit_list:
        
            post_list = []

            if not isinstance(entry, list):  
                grouplist = [entry]
            else:
                grouplist = entry

            for subreddit in grouplist:
                top_posts = RedditLoader.load_subreddit(subreddit, ref_cat, ref_t)

                RedditPost.calculate_ref_score(top_posts)
   
                posts = RedditLoader.load_subreddit(subreddit, post_no = posts_per_sub)

                for item in posts:


                    filtered = False
                    if domain_filter != '':
                        for expr in domain_filter.split(cfg.domain_filter_spliter):  
                            if urlparse.urlparse(item.url).netloc.find(expr) != -1: 
                                filtered = True
                                break

                    if not filtered and (time.time()-item.created_utc) < time_frame and item.post_power() >= pp_treshold: 
                        post_list.append(item)
            if sort_key != None: post_list.sort(key = sort_key, reverse = reverse_sort_order)
            output_list.append({';'.join(grouplist) : post_list})
                  
  

        return output_list

class UserCfg:

    _default_cfg = cfg.default_user_cfg

    def __init__(self, **usercfg):

        for key in self._default_cfg.iterkeys():
            if key not in usercfg:
                usercfg[key] = self._default_cfg[key]

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
        self.pp_alg = usercfg['pp_alg']
        self.domain_filter = usercfg['domain_filter']
        self.subreddits = usercfg['subreddits']

        self.posts_sort_by = usercfg['posts_sort_by']
        self.posts_sort_order = usercfg['posts_sort_order']


        if self.posts_sort_by == 'num_comments':
            self.sort_key = lambda post: post.num_comments 
        elif self.posts_sort_by == 'score':
            self.sort_key = lambda post: post.score
        elif self.posts_sort_by == 'post_power':
            self.sort_key = lambda post: post.post_power()
        elif self.posts_sort_by == 'hours_ago':
            self.sort_key = lambda post: post.hours_ago()
        else:
            self.sort_key = None

        if usercfg['posts_sort_order'] == 'asc':
            self.reverse_sort_order = False
        else:
            self.reverse_sort_order = True


        
def dump_posts_to_json(posts):
    output_list = []
    for subreddit_dct in posts:
        post_list = []
        name = ''
        for subreddit, postlist in subreddit_dct.iteritems():
            name += subreddit 
            for item in postlist:
                post_list.append([item.title, item.url, item.subreddit, item.num_comments, item.score, item.permalink, item.post_power(), item.hours_ago()])
        output_list.append({subreddit : post_list})

    return json.dumps(output_list, indent = 4)

def mail(to, subject, text, gmail_user, gmail_pwd):
   msg = MIMEMultipart()
   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject
   msg.attach(MIMEText(text))
   mailServer = smtplib.SMTP(cfg.gmail_smtp_server, cfg.gmail_smtp_port)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   mailServer.close()

def load_configs():

    configs =[]

    for cfg_file in glob.iglob(cfg.userconfig_file_pattern):
        with open(cfg_file) as usrcfg:
            try:
                configs.append(UserCfg(**json.load(usrcfg)))
            except ValueError:
                print '!!!!!!!!!error parsing config file: ' + cfg_file + ', file ommited'
   
    return configs

def main():

    userlist = load_configs()
    html = Template

    
    for user in userlist:

        value = RedditLoader.aggregate_subreddits(user = user)
        output=""
        print '########################################################################################################'
        output+= html.head()
        #text = dump_posts_to_json(value)
        #print text
        
        for subreddit in value:
            for name, posts in subreddit.iteritems():
                output+= html.tablestart(name.title())
                for item in posts:
                    output+= html.item(item.url, item.title.encode('ascii', 'replace'), item.permalink, item.num_comments, item.score, 
                        '{0:.2f}'.format(item.post_power()), item.hours_ago(), item.subreddit)
                output+= html.tableend()

        #delete those outputs later
        output+= '<hr></hr><p>' + 'Username: ' + user.username + '</p>'
        output+= '<p>' + 'Post Power threshold: ' + str(user.pp_treshold) + '</p>'
        output+= '<p>' + 'Sorted by: ' + user.posts_sort_by + '</p>'
        ##########

        f = open(user.username + '.html', 'w+')
        f.write(output)
        f.close()

        # TEMPORARILY commented out
        # mail(user.usr_mail, user.subject_tmpl.format(date = datetime.datetime.now().strftime("%d-%m-%Y")), text, 
        #     user.gmail_login_user, user.gmail_login_pwd)
       



if __name__ == "__main__":
    main()
