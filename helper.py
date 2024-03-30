import streamlit
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users']== selected_user]
    num_messages = df.shape[0]
    words = []
    num_media_messages = df[df['message'].str.contains('<Media omitted>')].shape[0]  # Count media messages
    for message in df['message']:
        words.extend(message.split())
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['users'].value_counts()  # Use 'users' column instead of 'user'
    df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'users': 'Names','count':'Chat %'})
    # df.remove('group_notifications')
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    wc = WordCloud(width=500,height=500,min_font_size= 10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc
def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    temp = df[df['users'] != 'group_notifications']
    temp = temp[temp['message'] != '<Media omitted>']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        words.extend(message.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return  most_common_df
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    timeline = df.groupby(['year', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline
def daywise_analysis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return df['day_name'].value_counts()
def monthly_analysis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return df['month'].value_counts()










