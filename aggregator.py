
import json
import urllib2, httplib
import time
import smtplib
from datetime import date, timedelta
import shutil
import math
import sys
import glob
import this
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import config as cfg
import template
import logging

class RedditOpener:
    def __init__(self):
        self.user_agent = cfg.user_agent
        self.opener = urllib2.build_opener()
        self.opener.add_handler(urllib2.HTTPCookieProcessor())
        self.opener.addheaders = [('User-agent', self.user_agent)]

    def open(self, url):
            return self.opener.open(url)


class RedditPost:
    ref_score = {}

    def __init__(self, ref_subreddit = None, pp_alg = cfg.default_user_cfg['pp_alg'], **data ):

        self.subreddit = data['subreddit']
        self.id = data['id']
        self.title = data['title']
        self.num_comments = data['num_comments']
        self.score = data['score']
        self.permalink = 'http://reddit.com' + data['permalink']
        self.name = data['name']
        self.url = data['url']
        self.created_utc  = data['created_utc']
        self.domain = data['domain']
        self.is_self = data['is_self']
        self.pp_alg = pp_alg
        self.time_of_download = time.time()

        self._pp = None
        self._ha = None
        self._tp = None
        self.hours_ago_int = int(math.ceil((self.time_of_download - self.created_utc) / 3600))

        if ref_subreddit == None:
            self.ref_subreddit = self.subreddit
        else:
            self.ref_subreddit = ref_subreddit


    def __str__(self):
        return u'title: {} - score: {} - posted: {} hours ago - post_power: {}'.format(self.title, 
            self.score + self.num_comments, (time.time() - self.created_utc) / 3600, self.post_power()).encode("utf-8")

    @classmethod
    def load_posts(cls, posts_json, ref_subreddit = None, pp_alg = cfg.default_user_cfg['pp_alg']):
        return [RedditPost(pp_alg = pp_alg, ref_subreddit = ref_subreddit, **post['data']) for post in posts_json ]

    @classmethod
    def calculate_ref_score(cls, reddit_posts, subreddit = '', pp_alg = cfg.default_user_cfg['pp_alg']):
        if len(reddit_posts) > 0:
            if subreddit == '':
                subreddit = reddit_posts[0].subreddit
            pp_alg = reddit_posts[0].pp_alg

        cls.ref_score[subreddit] = {}

        if pp_alg == 'default':
            cls.ref_score[subreddit][pp_alg] = cls._calculate_ref_score_default(reddit_posts, subreddit = subreddit)
        else:
            raise NotImplementedError('Unknown post_power alghorithm.')
        logging.debug('ref_score for subreddit '+ subreddit + ': ' + str(cls.ref_score[subreddit][pp_alg]) + ' pp_alg: ' + pp_alg)
        return cls.ref_score[subreddit][pp_alg]

    @classmethod
    def _calculate_ref_score_default(cls, reddit_posts, subreddit = ''):
        ref_score = 0
        
        for item in reddit_posts[:3]:
            ref_score += item.score + item.num_comments
        ref_score /= 7.0
        return ref_score

    def post_power(self):
        if self.ref_subreddit not in self.ref_score:
            raise RuntimeError('Invalid state: call calculate_ref_score() BEFORE post_power()')
        if self._pp != None: return self._pp

       
        if self.pp_alg == 'default':
             self._pp = self._post_power_default()
        else:
            raise NotImplementedError('Unknown post_power alghorithm.')

        return self._pp
        
    def _post_power_default(self):
        ago = (time.time() - self.created_utc) / 3600
        postscore = self.score + self.num_comments
        pp = (25 / ago * postscore / self.ref_score[self.ref_subreddit][self.pp_alg])


        return pp

    def hours_ago(self):
        if self._ha != None: return self._ha

        ago = self.hours_ago_int# int(math.ceil((self.time_of_download - self.created_utc) / 3600))


        string = "%r" % (ago)
        self._ha = string
        return string

    

    def type(self):
        if self._tp != None: return self._tp
        type=''

        for item in cfg.image_types:
            if self.url.find(item) != -1:
                type = 'image'

        for item in cfg.video_types:
            if self.url.find(item) != -1:
                type = 'video'
        self._tp = type        
        return type


class RedditLoader:
    last_req_time = 0
    retries = 0
    opener = RedditOpener()
    reddit_cache = {}

    @classmethod
    def get_url(cls, url, delay = 0):
        time_elapsed_since_last_req = time.time() - cls.last_req_time
        time_required = delay
        if (time_elapsed_since_last_req < time_required):
            logging.debug('Sleeping for {}'.format(time_required - time_elapsed_since_last_req))
            time.sleep(time_required - time_elapsed_since_last_req)
        logging.info('Requesting url {}'.format(url))
        cls.last_req_time = time.time()


        try:
            response = cls.opener.open(url)
            logging.info('Site responded with HTTP code: {}'.format(response.code))
            json_message = response.read()
        except urllib2.HTTPError as error:
            logging.error('Site responded with unhandled HTTP error code: {}'.format(error.code))
            json_dct = {}
        except urllib2.URLError as error: 
            logging.error('Request failed to reach a server. Reason: {}'.format(error.reason))
            json_dct = {}
        except httplib.IncompleteRead as error: 
            logging.error('Request failed, httplib.IncompleteRead encounterd. Reason: {}'.format(error.reason))
            json_dct = {}
        except:
            logging.error('Unexpected error from urllib2:', sys.exc_info()[0])
            raise
        else:
            logging.debug('Message recieved: {}'.format(json_message))
            json_dct = json.loads(json_message)

        return json_dct

    @classmethod
    def load_json_from_url(cls, url, delay = cfg.default_request_delay, cache_refresh_interval = cfg.default_cache_refresh_interval):

        if cls.is_cached(url, cache_refresh_interval):
            logging.info('Url ' + url + ' arleady in cache, NOT REQUESTING')
            return cls.get_cache(url)

        json_dct = cls.get_url(url, delay)

        if 'data' in json_dct and 'children' in json_dct['data']:
            cls.retries = 0
            cls.set_cache(url, json_dct['data']['children'])
            return json_dct['data']['children']

        elif cls.retries >= cfg.max_retries:
            logging.error('max_retries exceeded... exiting')
            sys.exit(1)

        else:
            logging.info('Response cointained no posts: {}'.format(json_dct))
            cls.retries += 1
            logging.warning('Retrying last request.... retry count: {}'.format(cls.retries))
            return cls.load_json_from_url(url, delay = delay * cfg.retry_delay_multiplier, cache_refresh_interval = cache_refresh_interval)

    @classmethod
    def is_cached(cls, url, refresh_time = cfg.default_cache_refresh_interval):
        return url in cls.reddit_cache and time.time() - cls.reddit_cache[url]['last_refresh'] < refresh_time

    @classmethod
    def get_cache(cls, url):
        return cls.reddit_cache[url]['posts']

    @classmethod
    def set_cache(cls, url, data, entry_limit = cfg.cache_entry_limit):
        if len(cls.reddit_cache) + 1 >= entry_limit:
            logging.info("Cache entry limit reached, making free space...")
            cls._del_cache_entries(no_oldest = len(cls.reddit_cache) + 1 - entry_limit + cfg.cache_entries_to_clear)
        if url not in cls.reddit_cache: 
                cls.reddit_cache[url] = {}
                cls.reddit_cache[url]['last_refresh'] = time.time()
                cls.reddit_cache[url]['posts'] = data

    @classmethod
    def _del_cache_entries(cls, no_oldest = cfg.cache_entries_to_clear):
        logging.info("Deleting {} oldest entr(y/ies) from cache".format(no_oldest))

        for url in sorted(cls.reddit_cache.keys(), key = lambda k: cls.reddit_cache[k]['last_refresh']):
            if no_oldest <= 0: break
            logging.debug('Deleting cache entry for url: {}'.format(url))
            del cls.reddit_cache[url]
            no_oldest -= 1



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
            return RedditPost.load_posts(posts, pp_alg = pp_alg, ref_subreddit = subreddit)
        else:
            while len(posts) >= cfg.posts_in_json_page and len(posts) < post_no and loaded > 0:
                 last_post_id = posts[-1]['data']['name']
                 next_site = cls.load_json_from_url(cls.build_url(subreddit, site = suffix, t = t, after = last_post_id))
                 loaded = len(next_site)
                 posts += next_site
            return RedditPost.load_posts(posts[:post_no], pp_alg = pp_alg, ref_subreddit = subreddit)

    @classmethod
    def aggregate_subreddits(cls, reddit_list = [], user = None, ref_cat = cfg.default_user_cfg['ref_cat'], 
        ref_t = cfg.default_user_cfg['ref_t'], 
        posts_per_sub = cfg.default_user_cfg['posts_per_sub'] , 
        time_frame = cfg.default_user_cfg['time_frame'], 
        pp_treshold = cfg.default_user_cfg['pp_treshold'], 
        sort_key = None, reverse_sort_order = True, 
        pp_alg = cfg.default_user_cfg['pp_alg'] , 
        domain_filter = cfg.default_user_cfg['domain_filter'] , 
        reverse_domain_filter = cfg.default_user_cfg['reverse_domain_filter']):

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
            reverse_domain_filter = user.reverse_domain_filter


        output_list = []

        for entry in reddit_list:
        
            post_list = []

            if not isinstance(entry, list):  
                grouplist = [entry]
            else:
                grouplist = entry

            for subreddit in grouplist:
                top_posts = RedditLoader.load_subreddit(subreddit, ref_cat, ref_t)
                RedditPost.calculate_ref_score(top_posts, subreddit = subreddit)
                posts = RedditLoader.load_subreddit(subreddit, post_no = posts_per_sub)

                for item in posts:

                    
                    filtered = False
                    if domain_filter != '':
                        for expr in domain_filter.split(cfg.domain_filter_spliter):  
                            if item.domain.find(expr) != -1: 
                                filtered = True
                                break

                    if not filtered and reverse_domain_filter != '':
                        for expr in reverse_domain_filter.split(cfg.domain_filter_spliter):  
                            if item.domain.find(expr) != -1 : break
                        else:
                            filtered = True


                    if not filtered and (time.time()-item.created_utc) < time_frame and item.post_power() >= pp_treshold: 
                        post_list.append(item)

            if post_list:
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
        self.reverse_domain_filter = usercfg['reverse_domain_filter']
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
            self.sort_key = lambda post: post.hours_ago_int
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
                post_list.append([item.title, item.url, item.subreddit, item.num_comments, item.score, item.permalink, 
                    item.post_power(), item.hours_ago()])
        output_list.append({subreddit : post_list})

    return json.dumps(output_list, indent = 4)

def mail(to, subject, text, gmail_user, gmail_pwd):
   msg = MIMEMultipart()
   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject
   msg.attach(MIMEText(text, 'html'))
   mailServer = smtplib.SMTP(cfg.gmail_smtp_server, cfg.gmail_smtp_port)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   mailServer.quit()

   logging.info('Email sent to: {}'.format(to))

def load_configs():
    logging.info('Started loading user configs')
    configs =[]

    for cfg_file in glob.iglob(cfg.userconfig_file_pattern):
        with open(cfg_file) as usrcfg:
            try:
                configs.append(UserCfg(**json.load(usrcfg)))
                logging.info('Config from file: {} successfully loaded'.format(cfg_file))
            except ValueError:
                logging.error('Error parsing config file: ' + cfg_file + ', file ommited.')

    logging.info('Finished loading user configs')   
    return configs

def build_html(value, html, user):
    output=''
    
    tabs=0
    for subreddit in value:
        tabs+=1

    subnames=[]
    for subreddit in value:
        for name, posts in subreddit.iteritems():
            subnames.append(name)


    output+= html.head(tabs, subnames)

    num=0
    for subreddit in value:
        for name, posts in subreddit.iteritems():
            tit=' | '.join(name.title().split(';'))
            if tit.__len__() > 150:
                tit2=tit
                tit3=tit
                tit=tit[0:150]
                tit+="&nbsp;<img src=img/questionmark.gif alt='{}' title='{}'>".format(tit2, tit3)
            output+= html.tablestart(tit, num)
            for item in posts:
                output+= html.item(item.url.encode('ascii', 'replace'), item.title.encode('ascii', 'replace'), 
                    item.permalink.encode('ascii', 'replace'), item.num_comments, item.score, 
                    '{0:.2f}'.format(item.post_power()), item.hours_ago(), item.subreddit, item.is_self, item.type())

            output+= html.tableend()
            num+=1
    return output


def main():

    userlist = load_configs()
    html = template.Template

    for user in userlist:
        logging.info('###################### Started processing user: {}'.format(user.username))
        
        value = RedditLoader.aggregate_subreddits(user = user)
        output = build_html(value, html, user)

        if not os.path.exists('public/archive/'):
            os.makedirs('public/archive/')

        if os.path.exists('public/' + user.username + '.html')==True:
            filedate = time.strftime("%m-%d-%Y",time.localtime(os.path.getmtime('public/' + user.username +'.html')))
            shutil.move('public/' + user.username +'.html', 'public/archive/' + user.username + '-' + filedate + '.html')

############### CIEPIEL'S temporary testing code        ########################################################
        if os.path.exists('public/hn.html')==True:
            filedate = time.strftime("%m-%d-%Y",time.localtime(os.path.getmtime('public/hn.html')))
            shutil.move('public/hn.html', 'public/archive/HackerNews-' + filedate + '.html')
################################################################################################################

        f = open('public/' + user.username + '.html', 'w+')
        f.write(output)
        f.close()

        #mail(user.usr_mail, user.subject_tmpl.format(date = datetime.datetime.now().strftime("%d-%m-%Y")), output, user.gmail_login_user, user.gmail_login_pwd)

if __name__ == "__main__":
    cfg.logging_config['level'] = getattr(logging, cfg.logging_config['level'].upper())
    logging.basicConfig(**cfg.logging_config)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(cfg.logging_config['format'])
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logging.info('########################## Application started')
    main()
    logging.info('########################## Application finished')
