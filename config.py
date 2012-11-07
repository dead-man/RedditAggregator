


user_agent = 'PrivateRedditAggregatorBot/1.0'

default_request_delay = 2 
default_cache_refresh_interval = 300
cache_entry_limit = default_cache_refresh_interval / default_request_delay  # Simple way to avoid memory exhaustion i.e. MemoryError
cache_entries_to_clear = 20 # When cache_entry_limit is reached this many entries will be deleted

max_retries = 20
retry_delay_multiplier = 1.5

userconfig_file_pattern = '*.usercfg'

domain_filter_spliter = ';'

default_user_cfg = {
        'username' : 'defaultuser',
        'usr_mail' : '',
        'gmail_login_user' : 'raggregator@gmail.com',
        'gmail_login_pwd' : 'test',
        'subject_tmpl' : 'Reddit Aggregator\'s news for {date}',
        'posts_sort_by' : 'None', 'posts_sort_order' : 'dsc',
        'ref_cat' : 'top', 'ref_t' : 'month', 'posts_per_sub' : 25 , 'time_frame' : 90000, 'pp_treshold' : 0.5,
        'pp_alg' : 'default',
        'domain_filter' : '',
        'reverse_domain_filter' : '',
        'subreddits' : []
    }

image_types = ['.jpg', '.png', '.gif', 'imgur.com/', 'media.tumblr.com/']
video_types = ['www.youtube.com', 'vimeo.com', 'youtu.be', 'liveleak.com/', 'photobucket.com/']


logging_config = {
    'filename' : 'aggregator.log', 
    'level'  : 'INFO',
    'format' : '%(asctime)s  %(levelname)-8s %(message)s'
}


############# CRITICAL VARIABLES, DO NOT MODIFY:#################

posts_in_json_page = 25

gmail_smtp_server = 'smtp.gmail.com'
gmail_smtp_port = 587

