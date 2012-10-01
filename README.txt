Reddit Aggregator v0.9


TODO:
- exceptions logging to file
- reversed (inclusive/exclusive) domain filter
- more power post algorithms
- correct time frame calculation for post filtering
- configuration correctness chcecking
- logging errors to mail message


ISSUES:
- application hangs up when network interface is turned of during operation
- logging system crashes the application when no free space left on a disk. see (1)
- application crashes when network cable is pulled off during operation. see (2)
- links and post titles cointaining unicode crashes application (current workaround: ascii encoding: no crash, but link is unusable). see (3)
- application crashes during some of network problems. conditions for error reproduction should be further examined. see (4)
- memory exhaustion causes application to crash. see (5) 
- in some cases httplib raises IncompleteRead error and crashes application. error circumstances are unknown. see (6)




(1)

2012-09-26 12:58:13,635  INFO     Requesting url http://www.reddit.com/r/cogsci/top/.json?t=month
2012-09-26 12:58:14,161  INFO     Site responded with HTTP code: 200
Traceback (most recent call last):
  File "C:\Python27\lib\logging\__init__.py", line 866, in emit
    self.flush()
  File "C:\Python27\lib\logging\__init__.py", line 828, in flush
    self.stream.flush()
IOError: [Errno 28] No space left on device
Logged from file aggregator.py, line 156
2012-09-26 12:58:15,634  INFO     Requesting url http://www.reddit.com/r/cogsci/.json
Traceback (most recent call last):
  File "C:\Python27\lib\logging\__init__.py", line 866, in emit
    self.flush()
  File "C:\Python27\lib\logging\__init__.py", line 828, in flush
    self.stream.flush()
IOError: [Errno 28] No space left on device
Logged from file aggregator.py, line 159
2012-09-26 12:58:16,390  INFO     Site responded with HTTP code: 200
Traceback (most recent call last):
  File "C:\Python27\lib\logging\__init__.py", line 866, in emit
    self.flush()
  File "C:\Python27\lib\logging\__init__.py", line 828, in flush
    self.stream.flush()
IOError: [Errno 28] No space left on device



(2)

Traceback (most recent call last):
  File "C:\Users\marcin\Documents\GitHub\RedditAggregator\aggregator.py", line 430, in <module>
    main()
  File "C:\Users\marcin\Documents\GitHub\RedditAggregator\aggregator.py", line 403, in main
    value = RedditLoader.aggregate_subreddits(user = user)
  File "C:\Users\marcin\Documents\GitHub\RedditAggregator\aggregator.py", line 257, in aggregate_subreddits
    top_posts = RedditLoader.load_subreddit(subreddit, ref_cat, ref_t)
  File "C:\Users\marcin\Documents\GitHub\RedditAggregator\aggregator.py", line 210, in load_subreddit
    posts = cls.load_json_from_url(cls.build_url(subreddit, site = suffix, t = t))
  File "C:\Users\marcin\Documents\GitHub\RedditAggregator\aggregator.py", line 158, in load_json_from_url
    response = cls.opener.open(url)
  File "C:\Users\marcin\Documents\GitHub\RedditAggregator\aggregator.py", line 26, in open
    return self.opener.open(url)
  File "C:\Python27\lib\urllib2.py", line 394, in open
    response = self._open(req, data)
  File "C:\Python27\lib\urllib2.py", line 412, in _open
    '_open', req)
  File "C:\Python27\lib\urllib2.py", line 372, in _call_chain
    result = func(*args)
  File "C:\Python27\lib\urllib2.py", line 1199, in http_open
    return self.do_open(httplib.HTTPConnection, req)
  File "C:\Python27\lib\urllib2.py", line 1174, in do_open
    raise URLError(err)
urllib2.URLError: <urlopen error [Errno 10065] Prˇba przeprowadzenia operacji, wykonywanej przez gniazdo, na nieosi╣galnym hoťcie>
[Finished in 31.2s with exit code 1]


(3)

only urls, permalinks and titles seem to be the problem

"permalink": "/r/aww/comments/10h8by/\u3147\u3145\u3147/"
http://reddit.com/r/aww/comments/10h8by/%C5%83%C5%AF%C3%A7%C5%83%C5%AF%C5%AF%C5%83%C5%AF%C3%A7/  # <- probably the desired form
http://reddit.com/r/aww/comments/10h8by/ŃůçŃůůŃůç/

http://www.reddit.com/r/todayilearned/comments/10mm5g/til_the_language_of_piraha_has_so_few_consonants/
"url": "http://en.wikipedia.org/wiki/Pirah\u00e3_people#section_2"
http://en.wikipedia.org/wiki/Pirah%C3%A3_people#section_2

Traceback (most recent call last):
  File "C:\Users\marcin\Documents\GitHub\RedditAggregator\aggregator.py", line 430, in <module>
    main()
  File "C:\Users\marcin\Documents\GitHub\RedditAggregator\aggregator.py", line 405, in main
    output = build_html(value, html, user)
  File "C:\Users\marcin\Documents\GitHub\RedditAggregator\aggregator.py", line 382, in build_html
    item.score, '{0:.2f}'.format(item.post_power()), item.hours_ago(), item.subreddit, item.is_self, item.type())
  File "C:\Users\marcin\Documents\GitHub\RedditAggregator\template.py", line 19, in item
    url, self, title, type, permalink, num_comments, score, post_power, hours_ago, subreddit)
UnicodeEncodeError: 'ascii' codec can't encode characters in position 40-42: ordinal not in range(128)


(4)

Traceback (most recent call last):
 File "C:\Users\bakemono\Dropbox\python\helper\RedditAggregator\aggregator.py", line 403, in <module>
   main()
 File "C:\Users\bakemono\Dropbox\python\helper\RedditAggregator\aggregator.py", line 358, in main
   value = RedditLoader.aggregate_subreddits(user = user)
 File "C:\Users\bakemono\Dropbox\python\helper\RedditAggregator\aggregator.py", line 240, in aggregate_subreddits
   posts = RedditLoader.load_subreddit(subreddit, post_no = posts_per_sub)
 File "C:\Users\bakemono\Dropbox\python\helper\RedditAggregator\aggregator.py", line 191, in load_subreddit
   posts = cls.load_json_from_url(cls.build_url(subreddit, site = suffix, t = t))
 File "C:\Users\bakemono\Dropbox\python\helper\RedditAggregator\aggregator.py", line 142, in load_json_from_url
   json_message = response.read()
 File "C:\Python27\lib\socket.py", line 351, in read
   data = self._sock.recv(rbufsize)
 File "C:\Python27\lib\httplib.py", line 541, in read
   return self._read_chunked(amt)
 File "C:\Python27\lib\httplib.py", line 592, in _read_chunked
   value.append(self._safe_read(amt))
 File "C:\Python27\lib\httplib.py", line 647, in _safe_read
   chunk = self.fp.read(min(amt, MAXAMOUNT))
 File "C:\Python27\lib\socket.py", line 380, in read
   data = self._sock.recv(left)
socket.error: [Errno 10054] An existing connection was forcibly closed by the remote host
[Finished in 584.3s with exit code 1]


(5)

need to identify code fragments that commit to filling up memory, and free it up manualy in case of error


Traceback (most recent call last):
 File "aggregator.py", line 425, in <module>
   main()
 File "aggregator.py", line 399, in main
   value = RedditLoader.aggregate_subreddits(user = user)
 File "aggregator.py", line 258, in aggregate_subreddits
   top_posts = RedditLoader.load_subreddit(subreddit, ref_cat, ref_t)
 File "aggregator.py", line 211, in load_subreddit
   posts = cls.load_json_from_url(cls.build_url(subreddit, site = suffix, t = t))
 File "aggregator.py", line 162, in load_json_from_url
   json_message = response.read()
 File "/usr/lib/python2.7/socket.py", line 358, in read
   buf.write(data)
MemoryError: out of memory


(6)

2012-10-01 21:12:26,340  INFO     Site responded with HTTP code: 200
2012-10-01 21:12:26,777  INFO     Requesting url http://www.reddit.com/r/dailydo t/.json 2012-10-01 21:12:28,384  INFO     Site responded with HTTP code: 200
2012-10-01 21:12:28,778  INFO     Requesting url http://www.reddit.com/r/dailydo t/.json?after=t3_z2n44 2012-10-01 21:12:30,753  INFO     Site responded with HTTP code: 200
2012-10-01 21:12:31,775  INFO     Requesting url http://www.reddit.com/r/tldr/to p/.json?t=month 2012-10-01 21:12:32,724  INFO     Site responded with HTTP code: 200
2012-10-01 21:12:33,776  INFO     Requesting url http://www.reddit.com/r/tldr/.j
son
2012-10-01 21:12:34,834  INFO     Site responded with HTTP code: 200
2012-10-01 21:12:35,777  INFO     Requesting url http://www.reddit.com/r/tldr/.j son?after=t3_xu4el 2012-10-01 21:12:37,420  INFO     Site responded with HTTP code: 200
Traceback (most recent call last):
 File "aggregator.py", line 425, in <module>
   main()
 File "aggregator.py", line 399, in main
   value = RedditLoader.aggregate_subreddits(user = user)
 File "aggregator.py", line 260, in aggregate_subreddits
   posts = RedditLoader.load_subreddit(subreddit, post_no = posts_per_sub)
 File "aggregator.py", line 218, in load_subreddit
   next_site = cls.load_json_from_url(cls.build_url(subreddit, site = suffix, t
= t, after = last_post_id))
 File "aggregator.py", line 162, in load_json_from_url
   json_message = response.read()
 File "/usr/lib/python2.7/socket.py", line 351, in read
   data = self._sock.recv(rbufsize)
 File "/usr/lib/python2.7/httplib.py", line 541, in read
   return self._read_chunked(amt)
 File "/usr/lib/python2.7/httplib.py", line 586, in _read_chunked
   raise IncompleteRead(''.join(value))
httplib.IncompleteRead: IncompleteRead(2316 bytes read)
r@server:~/RedditAggregator$


