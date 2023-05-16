import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

uploaded_file = st.file_uploader("By Dayのデータはこちらにアップロード")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    day_df = pd.read_csv(uploaded_file, index_col="日付", parse_dates=True)
    day_df = day_df[['Tweets published', 'インプレッション']]
    day_df.rename(columns={'Tweets published': 'tweets', 'インプレッション': 'view'}, inplace=True)
    view_sum = sum(day_df['view']) / len(day_df['view'])
    day_df['view_t'] = day_df['view'] / day_df['tweets']
    day_df.loc[day_df['view_t'] == float('inf'), 'view_t'] = 0
    x = day_df.index

    y0 = day_df['tweets']
    y1 = day_df['view']
    y3 = day_df['view_t']
    fig, ax = plt.subplots(figsize=(15, 5), tight_layout=True, linewidth=22)
    ax.bar(x, y0, color='#1DA1F2', label='Posted Tweets')
    ax2 = ax.twinx()
    ax2.plot(x, y1, color='#14171A', label="Impression")
    ax2.bar(x, y3, color='green', label="Impression per Tweet", width=-0.3)
    ax2.axhline(y=view_sum, color='#AAB8C2', label="impressionAverage")
    ax2.legend(title='Right Ax', loc=(-0.2, 0.6))
    ax.legend(title='Left Ax', loc=(-0.2, 0.85))
    st.pyplot(fig)

uploaded_file = st.file_uploader("By Tweetのデータはこちらにアップロード")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    tweet_df = pd.read_csv(uploaded_file)
    tweet_df = tweet_df[['ツイートの固定リンク', 'ツイート本文', '時間', 'インプレッション', 'エンゲージメント',
                         'エンゲージメント率', 'リツイート', '返信', 'いいね', 'ユーザープロフィールクリック', 'URLクリック数',
                         '詳細クリック', 'メディアの再生数', 'メディアのエンゲージメント数']]
    tweet_df['時間'] = pd.to_datetime(tweet_df['時間']) + datetime.timedelta(hours=9)
    tweet_df['時間'] = tweet_df['時間'].dt.strftime('%m月%d日（%a）%H:%M')
    tweet_df[['インプレッション', 'エンゲージメント', 'リツイート', '返信', 'いいね', 'ユーザープロフィールクリック', 'URLクリック数', '詳細クリック',
              'メディアのエンゲージメント数']] = tweet_df[
        ['インプレッション', 'エンゲージメント', 'リツイート', '返信', 'いいね', 'ユーザープロフィールクリック', 'URLクリック数',
         '詳細クリック', 'メディアのエンゲージメント数']].astype(int)
    best3_df = tweet_df.sort_values(['エンゲージメント', 'エンゲージメント率'], ascending=False).head(3).drop(
        columns=['ツイートの固定リンク']).reset_index(drop=True)
    worst2_df = tweet_df.sort_values(['エンゲージメント', 'エンゲージメント率'], ascending=False).tail(2).drop(
        columns=['ツイートの固定リンク']).reset_index(drop=True)

    st.title("Best3 Tweets")
    st.dataframe(best3_df.style.highlight_null().highlight_max(color='teal', subset=['エンゲージメント', 'エンゲージメント率']).format({"エンゲージメント率": "{:.1%}"}))
    #graph
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Best Tweet")
        labels = ['like', 'retweet', 'reply', 'click Profile', 'click tweet', 'click URL']
        colors = ['#1DA1F2', '#14171A', '#657786', '#AAB8C2', '#E1E8ED', '#F5F8FA']

        fig, ax = plt.subplots(figsize=(5, 5), facecolor='white')
        ax = plt.pie(best3_df[['いいね', 'リツイート', '返信', 'ユーザープロフィールクリック', '詳細クリック', 'URLクリック数']].iloc[0].values,
                 counterclock=False,
                 startangle=90,
                 autopct="%1.1f%%",
                 pctdistance=0.8,
                 labels=labels,
                 colors=colors,
                 textprops={"color": "black"})
        st.pyplot(fig)
    with col2:
        st.header("Second Best")
        labels = ['like', 'retweet', 'reply', 'click Profile', 'click tweet', 'click URL']
        colors = ['#1DA1F2', '#14171A', '#657786', '#AAB8C2', '#E1E8ED', '#F5F8FA']

        fig, ax = plt.subplots(figsize=(5, 5), facecolor='white')
        ax = plt.pie(best3_df[['いいね', 'リツイート', '返信', 'ユーザープロフィールクリック', '詳細クリック', 'URLクリック数']].iloc[1].values,
                 counterclock=False,
                 startangle=90,
                 autopct="%1.1f%%",
                 pctdistance=0.8,
                 labels=labels,
                 colors=colors,
                 textprops={"color": "black"})
        st.pyplot(fig)
    with col3:
        st.header("Third")
        labels = ['like', 'retweet', 'reply', 'click Profile', 'click tweet', 'click URL']
        colors = ['#1DA1F2', '#14171A', '#657786', '#AAB8C2', '#E1E8ED', '#F5F8FA']

        fig, ax = plt.subplots(figsize=(5, 5),facecolor='white')
        ax = plt.pie(best3_df[['いいね', 'リツイート', '返信', 'ユーザープロフィールクリック', '詳細クリック', 'URLクリック数']].iloc[2].values,
                 counterclock=False,
                 startangle=90,
                 autopct="%1.1f%%",
                 pctdistance=0.8,
                 labels=labels,
                 colors=colors,
                 textprops={"color": "black"})
        st.pyplot(fig)




    st.title("Worst2 Tweets")
    st.dataframe(worst2_df.style.format({"エンゲージメント率": "{:.1%}"}))
