# import streamlit as st
# import pandas as pd
# import numpy as np
# from datetime import datetime
# from ensembledata.api import EDClient
# from io import BytesIO
# from auth import get_authenticator
# from style import inject_custom_css

# # --- PAGE CONFIG ---
# st.set_page_config(page_title="Reddit Scraper | KOMI Group", page_icon="📸")

# inject_custom_css()

# # --- AUTHENTICATION ---
# authenticator = get_authenticator()

# # Check login status
# if not st.session_state.get("authentication_status"):
#     st.warning("🔒 Please log in first.")
#     st.stop()

# # --- Show logout in sidebar ---
# authenticator.logout("Logout", location="sidebar")
# # st.sidebar.markdown("<br>", unsafe_allow_html=True)
# st.sidebar.image("logo_2.png")

# st.image("komi_logo.png", width=100)
# st.markdown("""
# <div style="display: flex; align-items: center; gap: 10px;">
#     <img src="https://cdn-icons-png.flaticon.com/512/1409/1409938.png" width="36">
#     <h1 style="margin: 0;">Reddit Scraper</h1>
# </div>
# """, unsafe_allow_html=True)

# # --- API Client ---
# API_TOKEN = "lSNX5D8FW02vlTX4"
# client = EDClient(API_TOKEN)

# # --- SESSION STATE INIT ---
# if 'posts_df' not in st.session_state:
#     st.session_state.posts_df = None
# if 'comments_df' not in st.session_state:
#     st.session_state.comments_df = None
# if 'selected_post' not in st.session_state:
#     st.session_state.selected_post = None

# # --- HEADER ---
# # st.title("Reddit Scraper")
# st.caption("Powered by KOMI Insights · Built for the Ark Media Team.")
# st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)
# st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)

# # --- DOWNLOAD FORMAT ---
# download_format = st.selectbox("Select download format", ["CSV", "XLSX", "TXT", "HTML", "JSON"])

# # --- SCRAPE SUBREDDIT POSTS FORM ---
# with st.form("scrape_posts_form"):
#     subreddit = st.text_input("Enter subreddit name", placeholder="e.g  'SkincareAddiction'")
#     sort = st.selectbox("Sort by", ["hot", "new", "top", "rising"], index=2)

#     if sort == "top":
#         period = st.selectbox("Select period", ["hour", "day", "week", "month", "year", "all"], index=0)
#     else:
#         period = "day"

#     min_comments = st.slider("Minimum number of comments", 0, 500, 0)
#     max_posts = st.slider("Maximum number of posts to scrape", 10, 500, 100, step=10)

#     submit_posts = st.form_submit_button("📅 Scrape Posts")

# if submit_posts:
#     with st.spinner("Scraping posts..."):
#         try:
#             next_cursor = None
#             all_posts = []

#             while len(all_posts) < max_posts:
#                 result = client.reddit.subreddit_posts(
#                     name=subreddit,
#                     sort=sort,
#                     period=period,
#                     cursor=next_cursor
#                 )

#                 posts = result.data.get('posts', [])
#                 if not posts:
#                     break

#                 all_posts.extend([post['data'] for post in posts])
#                 next_cursor = result.data.get("nextCursor")
#                 if not next_cursor:
#                     break

#             all_posts = all_posts[:max_posts]  # Trim to exact number requested
#             df_raw = pd.DataFrame(all_posts)

#             # Ensure 'score' exists for renaming
#             if 'score' not in df_raw.columns:
#                 df_raw['score'] = np.nan

#             # --- Clean and Transform Data ---
#             df_clean = df_raw[[
#                 'id', 'created_utc', 'title', 'author', 'selftext', 'url',
#                 'link_flair_text', 'ups', 'num_comments', 'upvote_ratio', 'score', 'permalink'
#             ]].copy()

#             df_clean.rename(columns={
#                 'id': 'post_id',
#                 'created_utc': 'timestamp',
#                 'title': 'description',
#                 'link_flair_text': 'flair',
#                 'ups': 'upvotes_downvotes',
#                 'score': 'total_score'
#             }, inplace=True)

#             # Compute virality
#             df_clean['upvotes_downvotes'] = df_clean['upvotes_downvotes'].replace(0, np.nan)
#             df_clean['virality'] = (df_clean['num_comments'] / df_clean['upvotes_downvotes']).fillna(0).round(2)
#             cols = list(df_clean.columns)
#             cols.insert(3, cols.pop(cols.index('virality')))
#             df_clean = df_clean[cols]

#             # Format timestamp
#             df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'], unit='s')

#             # Filter based on min_comments
#             df_clean = df_clean[df_clean['num_comments'] >= min_comments].reset_index(drop=True)

#             # Save and display
#             st.session_state.posts_df = df_clean
#             st.session_state.comments_df = None
#             st.session_state.selected_post = None

#             st.success(f"✅ Scraped {len(df_clean)} posts from r/{subreddit}")
#             st.dataframe(df_clean)

#         except Exception as e:
#             st.error("⚠️ INVALID SUBREDDIT NAME.. PLEASE CROSS-CHECK")

# # --- SELECT POST TO SCRAPE COMMENTS ---
# if st.session_state.posts_df is not None:
#     posts_df = st.session_state.posts_df
#     post_titles = posts_df['description'] + " (" + posts_df['num_comments'].astype(str) + " comments)"
#     selected_idx = st.selectbox("Select a post to scrape comments", options=post_titles)

#     if st.button("📅 Scrape Comments"):
#         with st.spinner("Scraping comments..."):
#             try:
#                 selected_post = posts_df.iloc[post_titles.tolist().index(selected_idx)]
#                 permalink = selected_post['permalink']
#                 response = client.reddit.post_comments(permalink=permalink)
#                 comments_data = response.data.get("comments", [])

#                 if not comments_data:
#                     st.warning("No comments found for this post.")
#                     st.session_state.comments_df = None
#                 else:
#                     flat_comments = [c['data'] for c in comments_data if 'data' in c]
#                     df_comments = pd.DataFrame(flat_comments)

#                     expected_cols = ['id', 'created_utc', 'author', 'body', 'score', 'parent_id', 'link_id', 'depth']
#                     available_cols = [col for col in expected_cols if col in df_comments.columns]
#                     df_comments = df_comments[available_cols]

#                     rename_map = {
#                         'id': 'comment_id',
#                         'created_utc': 'timestamp',
#                         'body': 'comment_text',
#                         'score': 'upvotes'
#                     }
#                     rename_map = {k: v for k, v in rename_map.items() if k in df_comments.columns}
#                     df_comments.rename(columns=rename_map, inplace=True)

#                     if 'timestamp' in df_comments.columns:
#                         df_comments['timestamp'] = pd.to_datetime(df_comments['timestamp'], unit='s')
#                     if 'comment_text' in df_comments.columns:
#                         df_comments['comment_text'] = df_comments['comment_text'].fillna("").str.strip()
#                     if 'upvotes' in df_comments.columns:
#                         df_comments['upvotes'] = pd.to_numeric(df_comments['upvotes'], errors='coerce')

#                     st.session_state.comments_df = df_comments
#                     st.session_state.selected_post = selected_post

#                     st.success(f"✅ Scraped {len(df_comments)} comments for the post.")
#                     st.dataframe(df_comments.head(10))

#             except Exception as e:
#                 st.error("⚠️ Error scraping comments")

# # --- DOWNLOAD BUTTONS ---
# if st.session_state.posts_df is not None:
#     df = st.session_state.posts_df
#     st.markdown("#### Download Posts Data")
#     if download_format == "CSV":
#         st.download_button("📌 Download Posts CSV", data=df.to_csv(index=False), file_name="reddit_posts.csv", mime="text/csv")
#     elif download_format == "XLSX":
#         buf = BytesIO()
#         df.to_excel(buf, index=False, engine='openpyxl')
#         st.download_button("📌 Download Posts XLSX", data=buf.getvalue(), file_name="reddit_posts.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
#     elif download_format == "TXT":
#         txt = df.to_string(index=False)
#         st.download_button("📌 Download Posts TXT", data=txt, file_name="reddit_posts.txt", mime="text/plain")
#     elif download_format == "HTML":
#         html = df.to_html(index=False)
#         st.download_button("📌 Download Posts HTML", data=html, file_name="reddit_posts.html", mime="text/html")
#     elif download_format == "JSON":
#         st.download_button("📌 Download Posts JSON", data=df.to_json(orient="records"), file_name="reddit_posts.json", mime="application/json")

# if st.session_state.comments_df is not None:
#     df = st.session_state.comments_df
#     st.markdown(f"#### Download Comments Data (Post: {st.session_state.selected_post['description'][:50]}...)")
#     if download_format == "CSV":
#         st.download_button("📌 Download Comments CSV", data=df.to_csv(index=False), file_name="reddit_comments.csv", mime="text/csv")
#     elif download_format == "XLSX":
#         buf = BytesIO()
#         df.to_excel(buf, index=False, engine='openpyxl')
#         st.download_button("📌 Download Comments XLSX", data=buf.getvalue(), file_name="reddit_comments.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
#     elif download_format == "TXT":
#         txt = df.to_string(index=False)
#         st.download_button("📌 Download Comments TXT", data=txt, file_name="reddit_comments.txt", mime="text/plain")
#     elif download_format == "HTML":
#         html = df.to_html(index=False)
#         st.download_button("📌 Download Comments HTML", data=html, file_name="reddit_comments.html", mime="text/html")
#     elif download_format == "JSON":
#         st.download_button("📌 Download Comments JSON", data=df.to_json(orient="records"), file_name="reddit_comments.json", mime="application/json")

# st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)

# # --- FOOTER ---
# current_year = datetime.now().year
# st.markdown(f"""
#     <div class="footer">
#         <p>© {current_year} KOMI Group. All rights reserved.</p>
#         <p>This tool is the property of KOMI Group and intended solely for internal use only. Unauthorised distribution or use outside the organisation is strictly prohibited.</p>
#     </div>
# """, unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from ensembledata.api import EDClient
from io import BytesIO
import praw
from auth import get_authenticator
from style import inject_custom_css

# --- PAGE CONFIG ---
st.set_page_config(page_title="Reddit Scraper | KOMI Group", page_icon="📸")

inject_custom_css()

# --- AUTHENTICATION ---
authenticator = get_authenticator()

# Check login status
if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please log in first.")
    st.stop()

# --- Show logout in sidebar ---
authenticator.logout("Logout", location="sidebar")
st.sidebar.image("logo_2.png")

st.image("komi_logo.png", width=100)
st.markdown("""
<div style="display: flex; align-items: center; gap: 10px;">
    <img src="https://cdn-icons-png.flaticon.com/512/1409/1409938.png" width="36">
    <h1 style="margin: 0;">Reddit Scraper</h1>
</div>
""", unsafe_allow_html=True)

# --- API Clients ---
# Ensemble Data API
API_TOKEN = "lSNX5D8FW02vlTX4"
client = EDClient(API_TOKEN)

# Reddit API (PRAW)
reddit = praw.Reddit(
    client_id="NW1nDIFhrT185Fqyf-bC_w",
    client_secret="9azLHn6wBNqOv94U5Gi9mV18VowLYg",
    user_agent="my_reddit_scraper by /u/Southern_Plate_7428"
)

# --- SESSION STATE INIT ---
if 'posts_df' not in st.session_state:
    st.session_state.posts_df = None
if 'keyword_posts_df' not in st.session_state:
    st.session_state.keyword_posts_df = None

# --- HEADER ---
st.caption("Powered by KOMI Insights · Built for the Ark Media Team.")
st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)
st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)

# --- DOWNLOAD FORMAT ---
download_format = st.selectbox("Select download format", ["CSV", "XLSX", "TXT", "HTML", "JSON"])

# --- SCRAPING METHOD SELECTION ---
scrape_method = st.radio("Select scraping method", ["Subreddit", "Keyword Search"], index=0)

# --- SCRAPE SUBREDDIT POSTS FORM ---
if scrape_method == "Subreddit":
    with st.form("scrape_posts_form"):
        subreddit = st.text_input("Enter subreddit name", placeholder="e.g  'SkincareAddiction'")
        sort = st.selectbox("Sort by", ["hot", "new", "top", "rising"], index=2)

        if sort == "top":
            period = st.selectbox("Select period", ["hour", "day", "week", "month", "year", "all"], index=0)
        else:
            period = "day"

        min_comments = st.slider("Minimum number of comments", 0, 500, 0)
        max_posts = st.slider("Maximum number of posts to scrape", 10, 500, 100, step=10)

        submit_posts = st.form_submit_button("📅 Scrape Posts")

    if submit_posts:
        with st.spinner("Scraping posts..."):
            try:
                next_cursor = None
                all_posts = []

                while len(all_posts) < max_posts:
                    result = client.reddit.subreddit_posts(
                        name=subreddit,
                        sort=sort,
                        period=period,
                        cursor=next_cursor
                    )

                    posts = result.data.get('posts', [])
                    if not posts:
                        break

                    all_posts.extend([post['data'] for post in posts])
                    next_cursor = result.data.get("nextCursor")
                    if not next_cursor:
                        break

                all_posts = all_posts[:max_posts]  # Trim to exact number requested
                df_raw = pd.DataFrame(all_posts)

                # Ensure 'score' exists for renaming
                if 'score' not in df_raw.columns:
                    df_raw['score'] = np.nan

                # --- Clean and Transform Data ---
                df_clean = df_raw[[
                    'id', 'created_utc', 'title', 'author', 'selftext', 'url',
                    'link_flair_text', 'ups', 'num_comments', 'upvote_ratio', 'score', 'permalink'
                ]].copy()

                df_clean.rename(columns={
                    'id': 'post_id',
                    'created_utc': 'timestamp',
                    'title': 'description',
                    'link_flair_text': 'flair',
                    'ups': 'upvotes_downvotes',
                    'score': 'total_score'
                }, inplace=True)

                # Compute virality
                df_clean['upvotes_downvotes'] = df_clean['upvotes_downvotes'].replace(0, np.nan)
                df_clean['virality'] = (df_clean['num_comments'] / df_clean['upvotes_downvotes']).fillna(0).round(2)
                cols = list(df_clean.columns)
                cols.insert(3, cols.pop(cols.index('virality')))
                df_clean = df_clean[cols]

                # Format timestamp
                df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'], unit='s')

                # Filter based on min_comments
                df_clean = df_clean[df_clean['num_comments'] >= min_comments].reset_index(drop=True)

                # Save and display
                st.session_state.posts_df = df_clean
                st.session_state.keyword_posts_df = None

                st.success(f"✅ Scraped {len(df_clean)} posts from r/{subreddit}")
                st.dataframe(df_clean)

            except Exception as e:
                st.error("⚠️ INVALID SUBREDDIT NAME.. PLEASE CROSS-CHECK")

# --- SCRAPE KEYWORD SEARCH POSTS FORM ---
elif scrape_method == "Keyword Search":
    with st.form("scrape_keyword_posts_form"):
        keywords_input = st.text_input("Enter keywords (comma-separated)", placeholder="e.g  'epl, man utd, arsenal'")
        sort = st.selectbox("Sort by", ["new", "hot", "top", "relevance"], index=0)
        min_comments = st.slider("Minimum number of comments", 0, 500, 0)
        batch_size = st.slider("Maximum number of posts to scrape", 10, 500, 100, step=10)

        submit_keyword_posts = st.form_submit_button("📅 Scrape Posts by Keywords")

    if submit_keyword_posts:
        with st.spinner("Scraping posts by keywords..."):
            try:
                keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]
                if not keywords:
                    st.error("⚠️ Please enter at least one keyword.")
                else:
                    all_posts = []
                    for keyword in keywords:
                        posts = reddit.subreddit("all").search(
                            query=keyword,
                            sort=sort,
                            limit=batch_size
                        )

                        for post in posts:
                            all_posts.append({
                                'keyword': keyword,
                                'id': post.id,
                                'created_utc': post.created_utc,
                                'title': post.title,
                                'author': str(post.author),
                                'selftext': post.selftext,
                                'url': post.url,
                                'link_flair_text': post.link_flair_text,
                                'ups': post.ups,
                                'num_comments': post.num_comments,
                                'upvote_ratio': post.upvote_ratio,
                                'score': post.score,
                                'permalink': post.permalink
                            })

                    df_raw = pd.DataFrame(all_posts)

                    if not df_raw.empty:
                        df_clean = df_raw[[
                            'keyword', 'id', 'created_utc', 'title', 'author', 'selftext', 'url',
                            'link_flair_text', 'ups', 'num_comments', 'upvote_ratio', 'score', 'permalink'
                        ]].copy()

                        df_clean.rename(columns={
                            'id': 'post_id',
                            'created_utc': 'timestamp',
                            'title': 'description',
                            'link_flair_text': 'flair',
                            'ups': 'upvotes_downvotes',
                            'score': 'total_score'
                        }, inplace=True)

                        df_clean['upvotes_downvotes'] = df_clean['upvotes_downvotes'].replace(0, np.nan)
                        df_clean['virality'] = (df_clean['num_comments'] / df_clean['upvotes_downvotes']).fillna(0).round(2)

                        cols = list(df_clean.columns)
                        cols.insert(4, cols.pop(cols.index('virality')))
                        df_clean = df_clean[cols]

                        df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'], unit='s')
                        df_clean = df_clean[df_clean['num_comments'] >= min_comments].reset_index(drop=True)

                        st.session_state.keyword_posts_df = df_clean
                        st.session_state.posts_df = None

                        st.success(f"✅ Scraped {len(df_clean)} posts for keywords: {', '.join(keywords)}")
                        st.dataframe(df_clean)

                    else:
                        st.warning("⚠️ No posts were retrieved for the given keywords.")

            except Exception as e:
                st.error(f"⚠️ Error during keyword search: {e}")

# --- DOWNLOAD BUTTONS ---
if st.session_state.posts_df is not None:
    df = st.session_state.posts_df
    st.markdown("#### Download Posts Data")
    if download_format == "CSV":
        st.download_button("📌 Download Posts CSV", data=df.to_csv(index=False), file_name="reddit_posts.csv", mime="text/csv")
    elif download_format == "XLSX":
        buf = BytesIO()
        df.to_excel(buf, index=False, engine='openpyxl')
        st.download_button("📌 Download Posts XLSX", data=buf.getvalue(), file_name="reddit_posts.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    elif download_format == "TXT":
        txt = df.to_string(index=False)
        st.download_button("📌 Download Posts TXT", data=txt, file_name="reddit_posts.txt", mime="text/plain")
    elif download_format == "HTML":
        html = df.to_html(index=False)
        st.download_button("📌 Download Posts HTML", data=html, file_name="reddit_posts.html", mime="text/html")
    elif download_format == "JSON":
        st.download_button("📌 Download Posts JSON", data=df.to_json(orient="records"), file_name="reddit_posts.json", mime="application/json")

if st.session_state.keyword_posts_df is not None:
    df = st.session_state.keyword_posts_df
    st.markdown("#### Download Keyword Posts Data")
    if download_format == "CSV":
        st.download_button("📌 Download Keyword Posts CSV", data=df.to_csv(index=False), file_name="reddit_keyword_posts.csv", mime="text/csv")
    elif download_format == "XLSX":
        buf = BytesIO()
        df.to_excel(buf, index=False, engine='openpyxl')
        st.download_button("📌 Download Keyword Posts XLSX", data=buf.getvalue(), file_name="reddit_keyword_posts.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    elif download_format == "TXT":
        txt = df.to_string(index=False)
        st.download_button("📌 Download Keyword Posts TXT", data=txt, file_name="reddit_keyword_posts.txt", mime="text/plain")
    elif download_format == "HTML":
        html = df.to_html(index=False)
        st.download_button("📌 Download Keyword Posts HTML", data=html, file_name="reddit_keyword_posts.html", mime="text/html")
    elif download_format == "JSON":
        st.download_button("📌 Download Keyword Posts JSON", data=df.to_json(orient="records"), file_name="reddit_keyword_posts.json", mime="application/json")

st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)

# --- FOOTER ---
current_year = datetime.now().year
st.markdown(f"""
    <div class="footer">
        <p>© {current_year} KOMI Group. All rights reserved.</p>
        <p>This tool is the property of KOMI Group and intended solely for internal use only. Unauthorised distribution or use outside the organisation is strictly prohibited.</p>
    </div>
""", unsafe_allow_html=True)
