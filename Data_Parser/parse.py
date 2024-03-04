import re

# convert text to number for views, retweets, replies, likes
def convert_to_int(input_string):
    input_string = input_string.replace(',', '')
    if 'K' in input_string:
        number = float(input_string.replace('K', '')) * 1000
        return int(number) 
    elif 'M' in input_string:
        number = float(input_string.replace('M', '')) * 1000000
        return int(number)
    elif input_string == '':
        return 0
    else:
        return int(input_string)
    
# parse tweets
def parse_tweets(page_source,query_wordstring, query_kol):
    tweets = page_source.find_all('article', attrs={'data-testid': 'tweet'})
    tweets_info = []
    if len(tweets) > 0:
        for tweet_element in tweets:
            tweet_text_element = tweet_element.find('div', attrs={'data-testid': 'tweetText'})
            tweet_time_element = tweet_element.find('time')
            if tweet_text_element and tweet_time_element:
                tweet_text = tweet_text_element.get_text()
                tweet_time = tweet_time_element['datetime']
            else:
                break      
            tweet_stats_element = tweet_element.find('div', attrs={'class': 'css-175oi2r r-1kbdv8c r-18u37iz r-1wtj0ep r-1ye8kvj r-1s2bzr4'})
            if tweet_stats_element is None:
                tweet_stats_element = tweet_element.find('div', attrs={'class': 'css-175oi2r r-1kbdv8c r-18u37iz r-1oszu61 r-3qxfft r-s1qlax r-1dgieki r-1efd50x r-5kkj8d r-h3s6tt r-1wtj0ep r-j5o65s r-rull8r r-qklmqi'})
            if tweet_stats_element:  
                tweet_stats_string = tweet_stats_element['aria-label']
                tweet_username_elements = tweet_element.find_all('div', attrs={'data-testid': 'User-Name'})      

                user_name_element = tweet_username_elements[0]
                user_name = user_name_element.get_text()
                language_value = tweet_text_element['lang']
                replies = 0
                reposts = 0
                likes = 0
                bookmarks = 0
                views = 0
                if tweet_stats_string != "":
                    stats_parts = tweet_stats_string.split(',')
                    for part in stats_parts:

                        part = part.lstrip()
                        stat_type = part.split(' ')[1]
                        stat_value = int(part.split(' ')[0])
                        if stat_type.lower() == 'replies' or stat_type.lower() == "reply":
                            replies = stat_value
                        elif stat_type.lower() == 'reposts' or stat_type.lower() == 'repost':
                            reposts = stat_value
                        elif stat_type.lower() == 'likes' or stat_type.lower() == 'like':
                            likes = stat_value
                        elif stat_type.lower() == 'bookmarks' or stat_type.lower() == 'bookmark':
                            bookmarks = stat_value
                        else:
                            views = stat_value
                    
                    tweets_info.append((user_name,tweet_text, tweet_time, replies, reposts, likes, bookmarks, views,query_wordstring, query_kol, language_value))
            else:
                tweet_username_elements = tweet_element.find_all('div', attrs={'data-testid': 'User-Name'})      

                user_name_element = tweet_username_elements[0]
                user_name = user_name_element.get_text()
                language_value = tweet_text_element['lang']


                tweet_reply_element = tweet_element.find('div', attrs={'data-testid': 'reply'})
                if tweet_reply_element:
                    replies = convert_to_int(tweet_reply_element.get_text())
                    if replies == "" or replies is None:
                        replies = 0
                tweet_retweet_element = tweet_element.find('div', attrs={'data-testid': 'retweet'})
                if tweet_retweet_element:
                    reposts = convert_to_int(tweet_retweet_element.get_text())
                    if reposts == "" or reposts is None:
                        reposts = 0
                tweet_like_element = tweet_element.find('div', attrs={'data-testid': 'like'})
                if tweet_like_element:
                    likes = convert_to_int(tweet_like_element.get_text()) 
                    if likes == "" or likes is None:
                        likes = 0
                tweet_aria_label_elements = tweet_element.find_all('a', attrs={'aria-label':True})      
                views = None          
                for elem in tweet_aria_label_elements:     
                    if 'views. View post analytics' in elem['aria-label']:
                        match = re.search(r'(\d+) views', elem['aria-label'])
                        if match:
                            views = match.group(1)
                            break 
                    elif 'View post analytics' == elem['aria-label']:
                        views = 0
                if views is not None:
                    tweet_view_element = tweet_element.find('span', attrs={'class':'css-1qaijid r-bcqeeo r-qvutc0 r-poiln3 r-1b43r93 r-1cwl3u0 r-b88u0q'})
                    if tweet_view_element:
                        views = convert_to_int(tweet_view_element.get_text())
                tweet_bookmark_element = tweet_element.find('div', attrs={'data-testid': 'bookmark'})
                if tweet_bookmark_element:
                    bookmarks = convert_to_int(tweet_bookmark_element.get_text())
                    if bookmarks == "" or bookmarks is None:
                        bookmarks = 0
                tweets_info.append((user_name,tweet_text, tweet_time, replies, reposts, likes, bookmarks, views,query_wordstring, query_kol, language_value))
        return tweets_info
    else:
        return None