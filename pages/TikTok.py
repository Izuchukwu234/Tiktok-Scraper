import streamlit as st
import pandas as pd
from datetime import datetime
from ensembledata.api import EDClient
from io import BytesIO

# --- SETTINGS ---
API_TOKEN = "lSNX5D8FW02vlTX4"
client = EDClient(API_TOKEN)

# --- PAGE CONFIG ---
st.set_page_config(page_title="KOMI Scraper | KOMI Group", page_icon="komi_logo", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        body {
            background-color: #f5f7fa;
            font-family: 'Segoe UI', sans-serif;
        }
        .main {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
            margin-top: 2rem;
        }
        .header-divider {
            border-top: 2px solid #e0e0e0;
            margin-top: 1rem;
            margin-bottom: 2rem;
        }
        .stButton>button {
            background-color: #007bff;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-size: 1rem;
        }
        .stDownloadButton>button {
            background-color: #28a745;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            margin-top: 1rem;
        }
        footer {
            visibility: hidden;
        }
        .footer {
            font-size: 0.85rem;
            color: #888;
            text-align: center;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid #ddd;
        }
    </style>
""", unsafe_allow_html=True)

# --- INIT SESSION STATE ---
if 'scraped_df' not in st.session_state:
    st.session_state.scraped_df = None

# --- HEADER ---
st.image("komi_logo.png", width=100)

col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image("tiktok_logo.png", width=36)
with col2:
    st.markdown("<h1 style='margin-bottom: 0;'>TikTok Scraper</h1>", unsafe_allow_html=True)

st.caption("Powered by KOMI Group · Built for the Ark Media Team.")
st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)
st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)

# --- DOWNLOAD FORMAT SELECTION ---
download_format = st.selectbox("Select download format", ["CSV", "XLSX", "TXT", "HTML", "JSON"])

# --- MAIN CONTENT ---
with st.container():

    method = st.selectbox("Select scraping method", ["Hashtag", "Keyword", "Username"])

    with st.form("scraper_form"):
        if method == "Hashtag":
            hashtag = st.text_input("Enter hashtag (without #)")
            days = st.slider("Days to look back", 1, 180, 30)
        elif method == "Keyword":
            keyword = st.text_input("Enter keyword")
            period = st.selectbox("Select period (days to look back)", ['0', '1', '7', '30', '90', '180'])
        else:
            username = st.text_input("Enter a valid TikTok username")
            depth = st.slider("Scrape depth (higher = more posts)", 1, 100, 20)

        view_filter = st.selectbox("Filter by views", [
            "All views", "0–50K", "50K–100K", "100K–500K", "500K–1M", "1M+"
        ])

        submit = st.form_submit_button("📥 Scrape Data")

    if submit:
        with st.spinner("⏳ Scraping data... Please wait."):
            try:
                if method == "Hashtag":
                    posts = client.tiktok.full_hashtag_search(hashtag=hashtag, days=days).data.get("posts", [])
                    df = pd.json_normalize(posts)[[
                        'itemInfos.id', 'itemInfos.createTime', 'itemInfos.text', 'itemInfos.playCount',
                        'itemInfos.diggCount', 'itemInfos.commentCount', 'itemInfos.shareCount',
                        'itemInfos.video.videoMeta.duration', 'authorInfos.uniqueId']]

                    df['share_link'] = df.apply(
                        lambda row: f"https://www.tiktok.com/@{row['authorInfos.uniqueId']}/video/{row['itemInfos.id']}", axis=1)

                    df = df[[
                        'itemInfos.id', 'itemInfos.createTime', 'itemInfos.text', 'itemInfos.playCount',
                        'itemInfos.diggCount', 'itemInfos.commentCount', 'itemInfos.shareCount',
                        'itemInfos.video.videoMeta.duration', 'share_link']]

                    df.rename(columns={
                        'itemInfos.id': 'post_id', 'itemInfos.createTime': 'timestamp', 'itemInfos.text': 'description',
                        'itemInfos.playCount': 'views', 'itemInfos.diggCount': 'likes',
                        'itemInfos.commentCount': 'comments', 'itemInfos.shareCount': 'shares',
                        'itemInfos.video.videoMeta.duration': 'duration_secs', 'share_link': 'video_url'}, inplace=True)

                elif method == "Keyword":
                    posts = client.tiktok.full_keyword_search(keyword=keyword, period=period).data
                    df = pd.json_normalize(posts)[[
                        'aweme_info.aweme_id', 'aweme_info.create_time', 'aweme_info.desc',
                        'aweme_info.statistics.play_count', 'aweme_info.statistics.digg_count',
                        'aweme_info.statistics.comment_count', 'aweme_info.statistics.share_count',
                        'aweme_info.statistics.collect_count', 'aweme_info.video.duration', 'aweme_info.share_url']]

                    df.rename(columns={
                        'aweme_info.aweme_id': 'post_id', 'aweme_info.create_time': 'timestamp', 'aweme_info.desc': 'description',
                        'aweme_info.statistics.play_count': 'views', 'aweme_info.statistics.digg_count': 'likes',
                        'aweme_info.statistics.comment_count': 'comments', 'aweme_info.statistics.share_count': 'shares',
                        'aweme_info.statistics.collect_count': 'favorites', 'aweme_info.video.duration': 'duration_secs',
                        'aweme_info.share_url': 'video_url'}, inplace=True)

                else:
                    clean_username = username.strip().lstrip("@")
                    result = client.tiktok.user_posts_from_username(username=clean_username, depth=depth)
                    df_raw = pd.DataFrame(result.data)
                    df_list = [post.data for post in df_raw.itertuples(index=False) if isinstance(post.data, dict)]
                    df_expanded = pd.json_normalize(df_list)
                    df = df_expanded[[
                        'aweme_id', 'create_time', 'desc', 'statistics.play_count', 'statistics.digg_count',
                        'statistics.comment_count', 'statistics.share_count', 'statistics.collect_count',
                        'video.duration', 'share_url']]
                    df.rename(columns={
                        'aweme_id': 'post_id', 'create_time': 'timestamp', 'desc': 'description',
                        'statistics.play_count': 'views', 'statistics.digg_count': 'likes',
                        'statistics.comment_count': 'comments', 'statistics.share_count': 'shares',
                        'statistics.collect_count': 'favorites', 'video.duration': 'duration_secs',
                        'share_url': 'video_url'}, inplace=True)

                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
                df['views'] = pd.to_numeric(df['views'], errors='coerce')

                if view_filter == "0–50K":
                    df = df[df["views"] <= 50000]
                elif view_filter == "50K–100K":
                    df = df[(df["views"] > 50000) & (df["views"] <= 100000)]
                elif view_filter == "100K–500K":
                    df = df[(df["views"] > 100000) & (df["views"] <= 500000)]
                elif view_filter == "500K–1M":
                    df = df[(df["views"] > 500000) & (df["views"] <= 1000000)]
                elif view_filter == "1M+":
                    df = df[df["views"] > 1000000]

                st.session_state.scraped_df = df
                st.success(f"✅ Scraped {len(df)} posts successfully.")
                st.dataframe(df.head(10))

            except Exception as e:
                st.error(f"⚠️ Error: ENTER A VALID TIKTOK USERNAME. {e}")

    if st.session_state.scraped_df is not None:
        df = st.session_state.scraped_df
        if download_format == "CSV":
            st.download_button("📎 Download CSV", data=df.to_csv(index=False), file_name="tiktok_data.csv", mime="text/csv")
        elif download_format == "XLSX":
            xlsx_buffer = BytesIO()
            df.to_excel(xlsx_buffer, index=False, engine='openpyxl')
            st.download_button("📎 Download XLSX", data=xlsx_buffer.getvalue(), file_name="tiktok_data.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        elif download_format == "TXT":
            txt_data = df.to_string(index=False)
            st.download_button("📎 Download TXT", data=txt_data, file_name="tiktok_data.txt", mime="text/plain")
        elif download_format == "HTML":
            html_data = df.to_html(index=False)
            st.download_button("📎 Download HTML", data=html_data, file_name="tiktok_data.html", mime="text/html")
        elif download_format == "JSON":
            st.download_button("📎 Download JSON", data=df.to_json(orient="records"), file_name="tiktok_data.json", mime="application/json")

st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)

# --- FOOTER ---
current_year = datetime.now().year
st.markdown(f"""
    <div class="footer">
        <p>© {current_year} KOMI Group. All rights reserved.</p>
        <p>This tool is the property of KOMI Group and intended solely for internal use. Unauthorised distribution or use outside the organisation is strictly prohibited.</p>
    </div>
""", unsafe_allow_html=True)
