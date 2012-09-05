
import json
import urllib
import time

import sys # just for testing

class RedditOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

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

    @classmethod
    def load_json_from_url(cls, url, delay = 2):
        time_elapsed_since_last_req = time.time() - cls.last_req_time
        time_required = delay
        if (time_elapsed_since_last_req < time_required):
            print 'sleeping for ' , time_required - time_elapsed_since_last_req
            time.sleep(time_required - time_elapsed_since_last_req)
        #cls.last_req_time = time.time()
        print 'requesting url ' , url
        response = cls.opener.open(url)
        cls.last_req_time = time.time()
        print 'site responded with HTTP code: ', response.getcode()

        json_message = response.read()
        print '...and message: ', json_message
        json_dct = json.loads(json_message)

        if 'data' in json_dct and 'children' in json_dct['data']:
            cls.retries = 0
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
    def aggregate_subreddits(cls, reddit_list, ref_cat = 'top/', ref_t = '?t=month', posts_per_sub = 25 , time_frame = 90000, pp_treshold = 0.5):

        output_list = []

        for subreddit in reddit_list:
        
            post_list = []

            top_posts = RedditLoader.load_subreddit(subreddit, ref_cat, ref_t)
            RedditPost.calculate_ref_score(top_posts)

            posts = RedditLoader.load_subreddit(subreddit)
            
            for item in posts:
                #TODO sprawdzic zwracane czasy (time() nie zwraca czasu utc)
                if (time.time()-item.created_utc) < time_frame and item.post_power() >= pp_treshold: 

                    post_list.append([item.title, item.url])

            output_list.append({subreddit : post_list})
                  
  

        return output_list



def main():

    
    subreddits = ['philosophy', 'cogsci', 'minimalism', 'webdev', 'windows', 'linux', 'videos', 'funny', 'wtf', 'aww', 'atheism',
        'science', 'technology', 'neuro', 'psychology', 'minimalism', 'CultCinema']

    subreddits = ['philosophy', 'cogsci', 'minimalism', 'webdev', 'windows', 'linux', 'videos']

    value = RedditLoader.aggregate_subreddits(subreddits)

    print json.dumps(value, indent = 4)

   

if __name__ == "__main__":
    main()
