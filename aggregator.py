
import json
import urllib
import time

class RedditPost:

    ref_score = 0

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
    def calculate_ref_score(cls, reddit_posts):
        ref_score = 0
        for item in reddit_posts[:3]:
            ref_score += item.score + item.num_comments
        ref_score /= 7.0
        cls.ref_score = ref_score
        return cls.ref_score

    def post_power(self):
        ago = (time.time() - self.created_utc) / 3600
        postscore = self.score + self.num_comments
        pp = (25 / ago) * postscore / self.ref_score
        return pp

class RedditLoader:
    last_req_time = 0
    opener = urllib.FancyURLopener()

    @classmethod
    def load_json_from_url(cls, url):
        urllib.FancyURLopener.version = "u/afterbirth personal bot for news aggregation2"
        time_elapsed_since_last_req = time.time() - cls.last_req_time
        time_required = 30
        if (time_elapsed_since_last_req < time_required):
            print 'sleeping for ' , time_required - time_elapsed_since_last_req
            time.sleep(time_required - time_elapsed_since_last_req)
        cls.last_req_time = time.time()
        print 'requesting url ' , url
        return json.load(cls.opener.open(url))['data']['children']

    @classmethod
    def load_subreddit(cls, subreddit, suffix = '', t = '', post_no = 25):
        url = 'http://www.reddit.com/r/' + subreddit + '/' + suffix + '.json' + t
        posts = cls.load_json_from_url(url)
        if len(posts) == 0 : return
        while len(posts) < post_no:
             last_post_id = posts[-1]['data']['name']
             posts += cls.load_json_from_url(url + '&after=' + last_post_id)
        return posts[:post_no]

def main():

    value = ""
    subreddits = ['philosophy', 'cogsci', 'minimalism', 'webdev', 'windows', 'linux', 'videos', 'funny', 'wtf', 'aww', 'atheism']

    for subreddit in subreddits:

        
        top_posts_json = RedditLoader.load_subreddit(subreddit, 'top/', '?t=month')
        top_posts = RedditPost.load_posts(top_posts_json)
        
        RedditPost.calculate_ref_score(top_posts)


        posts_json = RedditLoader.load_subreddit(subreddit)
        posts = RedditPost.load_posts(posts_json)
       

        print ('-----------------------------------')
        for item in posts:
            if (time.time()-item.created_utc)<90000:
                print(item)

            value += u'{} - {}'.format(item.title, item.url).encode('utf-8')
            value += "\n"

        print RedditPost.ref_score

if __name__ == "__main__":
    main()
