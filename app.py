import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor
import helper

st.sidebar.title('WhatsApp Chat Analysis')
uploaded_file = st.sidebar.file_uploader("Choose a File")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Display the preprocessed data
    # st.dataframe(df)
    user_list = df['users'].unique().tolist()

    if 'group_notifications' in user_list:
        user_list.remove('group_notifications')

    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], c='navy')
        plt.xticks(rotation='vertical', fontweight='bold')
        plt.yticks(fontweight='bold')
        st.pyplot(fig)

        st.title('Day wise analysis')
        col1,col2 = st.columns(2)
        with col1:
            st.header('Most busy days')
            busy_day = helper.daywise_analysis(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color = '#003366')
            plt.xticks(rotation='vertical', fontweight='bold')
            plt.yticks(fontweight='bold')
            st.pyplot(fig)

            with col2:
                st.header('Monthly Analysis')
                busy_month = helper.monthly_analysis(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values,color = '#3cb371')
                plt.xticks(rotation='vertical', fontweight='bold')
                plt.yticks(fontweight='bold')
                st.pyplot(fig)


            # monthly timeline
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='#008080')
                ax.set_facecolor('#ffe4e1')
                plt.xticks(rotation='vertical', fontsize=14, fontweight='bold', color='navy')
                plt.yticks(fontsize=14, fontweight='bold', color='navy')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        st.title('BUZZ WORDS  or  WORD CLOUD')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        most_common_df = helper.most_common_words(selected_user, df)
        # st.dataframe(most_common_df)
        fig,ax = plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1],color = '#00a877')
        ax.set_facecolor('#ffefd5')
        plt.xticks(rotation='vertical', fontsize=11, fontweight='bold', color='navy')
        st.pyplot(fig)

