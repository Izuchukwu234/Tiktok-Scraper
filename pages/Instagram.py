import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from io import BytesIO
import logging
from time import sleep
from ensembledata.api import EDClient

# --- PAGE CONFIG ---
st.set_page_config(page_title="KOMI Instagram Scraper | KOMI Group", page_icon="komi_logo", layout="centered")

# --- Inject Custom CSS ---
st.markdown("""
    <style>
        .main {
            background-color: #ffffff;
            border-radius: 16px;
            padding: 2.5rem;
            box-shadow: 0 8px 24px rgba(0, 123, 255, 0.1);
            margin: 2rem auto;
            max-width: 900px;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }
        .header-container {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 1rem;
        }
        .header-container h1 {
            font-size: 2rem;
            background: linear-gradient(to right, #007bff, #00d4ff);
            -webkit-background-clip: text;
            color: transparent;
            font-weight: 700;
            margin: 0;
        }
        .header-divider {
            border-top: 2px solid #e2e8f0;
            margin: 1.5rem 0 2rem;
        }
        .stForm {
            background: #f8fafc;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 123, 255, 0.05);
        }
        .stTextInput > div > input,
        .stTextArea > div > textarea {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 10px 12px;
            font-size: 1rem;
            background-color: #ffffff;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }
        .stTextInput > div > input:focus,
        .stTextArea > div > textarea:focus {
            border-color: #007bff;
            box-shadow: 0 0 6px rgba(0, 123, 255, 0.2);
            outline: none;
        }
        .stSelectbox > div > select {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 10px 12px;
            font-size: 1rem;
            background-color: #ffffff;
            transition: border-color 0.3s ease;
        }
        .stButton > button {
            background: linear-gradient(to right, #007bff, #00d4ff);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            transition: transform 0.2s ease, box-shadow 0.3s ease;
        }
        .stButton > button:hover {
            box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
            transform: translateY(-2px);
        }
        .stDownloadButton > button {
            background: linear-gradient(to right, #28a745, #38d57a);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            margin-top: 1rem;
            transition: transform 0.2s ease, box-shadow 0.3s ease;
        }
        .stDownloadButton > button:hover {
            box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
            transform: translateY(-2px);
        }
        .stAlert {
            border-radius: 8px;
            padding: 1rem;
            font-size: 0.95rem;
        }
        .stDataFrame {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
        }
        .footer {
            font-size: 0.85rem;
            color: #4a5568;
            text-align: center;
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid #e2e8f0;
        }
        footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION ---
if not st.session_state.get("authentication_status", False):
    st.warning("Please log in first.")
    st.stop()

# --- Sidebar ---
st.sidebar.image("logo_2.png")
if st.sidebar.button("Logout"):
    st.session_state.authentication_status = False
    st.rerun()

# --- API SETUP ---
API_TOKEN = "lSNX5D8FW02vlTX4"
client = EDClient(API_TOKEN)
root = "https://ensembledata.com/apis"

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Retry Function for API Calls ---
def make_request(url, params, max_retries=3, initial_retry_wait=2, timeout=20, is_reels=False):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"} if is_reels else {}
    max_retries = 5 if is_reels else max_retries
    timeout = 30 if is_reels else timeout
    for attempt in range(max_retries):
        try:
            res = requests.get(url, params=params, headers=headers, timeout=timeout)
            if res.status_code == 429:
                wait_time = (2 ** attempt) * initial_retry_wait + (attempt % 2)
                logger.warning(f"Rate limit hit (429) on attempt {attempt + 1} for {url}. Waiting {wait_time}s")
                sleep(wait_time)
                continue
            res.raise_for_status()
            logger.info(f"API call succeeded for {url}: Status {res.status_code}")
            return res
        except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed after {max_retries} attempts for {url}: {e}, Response: {getattr(res, 'text', 'No response')}")
                return None
            wait_time = (2 ** attempt) * initial_retry_wait + (attempt % 2)
            logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}. Retrying in {wait_time}s")
            sleep(wait_time)
    return None

# --- INIT SESSION STATE ---
if 'scraped_df' not in st.session_state:
    st.session_state['scraped_df'] = None

# --- HEADER ---
st.image("komi_logo.png", width=100)
st.markdown("""
    <div class="header-container">
        <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" width="36">
        <h1>Instagram Scraper</h1>
    </div>
""", unsafe_allow_html=True)
st.caption("Powered by KOMI Insights · Built for the Ark Media Team.")
st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)

# --- DOWNLOAD FORMAT SELECTION ---
download_format = st.selectbox("Select download format", ["CSV", "XLSX", "TXT", "HTML", "JSON"])

# --- MAIN CONTENT ---
with st.container():
    method = st.selectbox("Select scraping method", [
        "Hashtag/Keyword", "Hashtag/Keyword (Reels)", "Username", "Username (Reels)"
    ])

with st.form("scraper_form"):
    if method in ["Hashtag/Keyword", "Hashtag/Keyword (Reels)"]:
        keyword_input = st.text_area("Enter keyword(s)/hashtag(s), separated by commas (without #)")
        if method == "Hashtag/Keyword":
            max_pages = st.slider("Depth", min_value=1, max_value=5, value=3)
        else:  # Hashtag/Keyword (Reels)
            depth = st.slider("Depth", min_value=1, max_value=5, value=2)
            max_pages = depth
            reels_depth = depth
    else:
        if method == "Username":
            username_input = st.text_area("Enter Instagram username(s), separated by commas (with or without @)", value="itsgoneviralofficial")
            depth = st.slider("Depth", min_value=1, max_value=5, value=2)
            max_pages = depth
            posts_depth = depth
            chunk_size = 20  # Hardcoded, not visible in UI
        else:  # Username (Reels)
            username_input = st.text_area("Enter Instagram username(s), separated by commas (with or without @)", value="ladbible")
            depth = st.slider("Depth", min_value=1, max_value=5, value=1)
            max_pages = depth
            posts_depth = depth
            chunk_size = 10  # Hardcoded, not visible in UI
            include_feed_video = st.checkbox("Include feed videos", value=True)

    # Show filters only for Reels methods
    if method in ["Hashtag/Keyword (Reels)", "Username (Reels)"]:
        view_filter = st.selectbox("Filter by views (Reels only)", [
            "All", "0–50K", "50K–100K", "100K–500K", "500K–1M", "1M+"
        ])
        like_filter = st.selectbox("Filter by likes", [
            "All likes", "0–50K", "50K–100K", "100K–500K", "500K–1M", "1M+"
        ])
        st.markdown(
            "<small> Using views and likes filters may reduce results. Adjust or disable for broader data.</small>",
            unsafe_allow_html=True
        )

    submit = st.form_submit_button(" Scrape Data")

    if submit:
        with st.spinner(" Scraping data... Please wait."):
            try:
                all_dfs = []
                if method == "Hashtag/Keyword":
                    endpoint = "/instagram/hashtag/posts"
                    keywords = [kw.strip().lstrip("#") for kw in keyword_input.split(",") if kw.strip()]
                    for keyword in keywords:
                        params = {"name": keyword, "cursor": "", "get_author_info": False, "token": API_TOKEN}
                        res = make_request(root + endpoint, params)
                        if not res:
                            logger.error(f"No response for keyword: {keyword}")
                            continue
                        response = res.json().get("data", {})
                        top_posts = [post["node"] for post in response.get("top_posts", [])]
                        recent_posts = [post["node"] for post in response.get("recent_posts", [])]
                        next_cursor = response.get("nextCursor")
                        page_count = 1
                        while next_cursor and page_count < max_pages:
                            params["cursor"] = next_cursor
                            paginated_res = make_request(root + endpoint, params)
                            if not paginated_res:
                                break
                            paginated_response = paginated_res.json().get("data", {})
                            recent_posts.extend([post["node"] for post in paginated_response.get("recent_posts", [])])
                            next_cursor = paginated_response.get("nextCursor")
                            page_count += 1
                            sleep(0.5)

                        all_nodes = top_posts + recent_posts
                        if not all_nodes:
                            logger.warning(f"No posts found for keyword: {keyword}")
                            continue

                        df_raw = pd.json_normalize(all_nodes)
                        df_raw['url'] = df_raw['shortcode'].apply(lambda x: f"https://www.instagram.com/p/{x}" if pd.notna(x) else None)
                        df_clean = df_raw[['id', 'shortcode', 'taken_at_timestamp', 'edge_media_to_caption.edges',
                                           'edge_media_to_comment.count', 'edge_liked_by.count', 'url', '__typename']].copy()
                        df_clean = df_clean.rename(columns={
                            'id': 'post_id', 'taken_at_timestamp': 'timestamp', 'edge_media_to_caption.edges': 'caption_data',
                            'edge_media_to_comment.count': 'comments', 'edge_liked_by.count': 'likes', 'url': 'post_url', '__typename': 'type'
                        })
                        df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'], unit='s', errors='coerce')
                        df_clean['caption'] = df_clean['caption_data'].apply(lambda edges: edges[0]['node']['text'] if edges else "")
                        df_clean.drop(columns=['caption_data'], inplace=True)
                        df_clean['total_interaction'] = df_clean['likes'] + df_clean['comments']
                        df_clean['keyword'] = keyword
                        df_clean['followers_count'] = None
                        df_clean['video_duration'] = None
                        df_clean['commentability'] = None
                        df_clean['likability'] = None

                        for idx, row in df_clean.iterrows():
                            shortcode = row['shortcode']
                            try:
                                post_detail = client.instagram.post_info_and_comments(code=shortcode).data
                                if post_detail.get("is_video"):
                                    df_clean.at[idx, 'video_duration'] = post_detail.get('video_duration', 0)
                                followers = post_detail.get("owner", {}).get("edge_followed_by", {}).get("count", None)
                                df_clean.at[idx, 'followers_count'] = followers
                                if followers and followers > 0:
                                    df_clean.at[idx, 'commentability'] = row['comments'] / followers
                                    df_clean.at[idx, 'likability'] = row['likes'] / followers
                                sleep(0.2)
                            except Exception as e:
                                logger.error(f"Error fetching post details for shortcode {shortcode}: {e}")
                                continue

                        df_clean.drop(columns=['shortcode'], inplace=True)
                        all_dfs.append(df_clean)

                elif method == "Hashtag/Keyword (Reels)":
                    hashtag_endpoint = "/instagram/hashtag/posts"
                    reels_endpoint = "/instagram/user/reels"
                    keywords = [kw.strip().lstrip("#") for kw in keyword_input.split(",") if kw.strip()]

                    for keyword in keywords:
                        logger.info(f"Processing keyword: {keyword}")
                        user_ids = set()
                        params = {"name": keyword, "cursor": "", "get_author_info": True, "token": API_TOKEN}
                        try:
                            res = requests.get(root + hashtag_endpoint, params=params)
                            res.raise_for_status()
                            response = res.json().get("data", {})
                        except Exception as e:
                            logger.error(f"No response for keyword '{keyword}': {e}")
                            continue

                        for post in response.get("top_posts", []):
                            if owner_id := post.get("node", {}).get("owner", {}).get("id"):
                                user_ids.add(owner_id)
                        for post in response.get("recent_posts", []):
                            if owner_id := post.get("node", {}).get("owner", {}).get("id"):
                                user_ids.add(owner_id)

                        next_cursor = response.get("nextCursor")
                        page_count = 1
                        while next_cursor and page_count < max_pages:
                            try:
                                params["cursor"] = next_cursor
                                paginated_res = requests.get(root + hashtag_endpoint, params=params)
                                paginated_res.raise_for_status()
                                paginated_response = paginated_res.json().get("data", {})
                                for post in paginated_response.get("recent_posts", []):
                                    if owner_id := post.get("node", {}).get("owner", {}).get("id"):
                                        user_ids.add(owner_id)
                                next_cursor = paginated_response.get("nextCursor")
                                page_count += 1
                                sleep(0.5)
                            except Exception as e:
                                logger.error(f"Error during pagination for keyword '{keyword}': {e}")
                                break

                        if not user_ids:
                            logger.warning(f"No user IDs found for keyword: {keyword}")
                            continue

                        all_reels = []
                        for user_id in user_ids:
                            try:
                                params = {
                                    "user_id": user_id,
                                    "depth": reels_depth,
                                    "include_feed_video": False,
                                    "chunk_size": 10,
                                    "start_cursor": "",
                                    "token": API_TOKEN
                                }
                                res = requests.get(root + reels_endpoint, params=params)
                                res.raise_for_status()
                                response = res.json().get("data", {})
                                if not response:
                                    logger.error(f"Empty data response for user_id: {user_id}")
                                    continue

                                reels = response.get("reels", [])
                                reel_nodes = []
                                for reel in reels:
                                    media = reel.get("media")
                                    if media and (
                                        media.get("media_type") == 2 or
                                        media.get("product_type") == "clips"
                                    ):
                                        reel_nodes.append(media)
                                        break  # Take only the first valid reel

                                next_cursor = response.get("nextCursor")
                                reel_page_count = 1
                                while not reel_nodes and next_cursor and reel_page_count < reels_depth:
                                    try:
                                        params["start_cursor"] = next_cursor
                                        paginated_res = requests.get(root + reels_endpoint, params=params)
                                        paginated_res.raise_for_status()
                                        paginated_response = paginated_res.json().get("data", {})
                                        if not paginated_response:
                                            break

                                        page_reels = paginated_response.get("reels", [])
                                        for reel in page_reels:
                                            media = reel.get("media")
                                            if media and (
                                                media.get("media_type") == 2 or
                                                media.get("product_type") == "clips"
                                            ):
                                                reel_nodes.append(media)
                                                break

                                        next_cursor = paginated_response.get("nextCursor")
                                        reel_page_count += 1
                                        sleep(0.5)
                                    except Exception as e:
                                        logger.error(f"Error during Reels pagination for user '{user_id}': {e}")
                                        break

                                all_reels.extend(reel_nodes)
                                sleep(0.5)
                            except Exception as e:
                                logger.error(f"Error fetching Reels for user '{user_id}': {e}")
                                continue

                        if not all_reels:
                            logger.warning(f"No Reels found for keyword: {keyword}")
                            continue

                        df_raw = pd.json_normalize(all_reels)
                        for col in ['id', 'code', 'taken_at', 'caption.text', 'comment_count', 'like_count', 'product_type', 'video_duration', 'play_count']:
                            if col not in df_raw.columns:
                                df_raw[col] = None
                        df_raw['url'] = df_raw['code'].apply(lambda x: f"https://www.instagram.com/reel/{x}" if pd.notna(x) else None)
                        df_clean = df_raw[['id', 'code', 'taken_at', 'caption.text', 'comment_count', 'like_count', 'url', 'product_type', 'video_duration', 'play_count']].copy()
                        df_clean = df_clean.rename(columns={
                            'id': 'post_id', 'taken_at': 'timestamp', 'caption.text': 'caption', 'comment_count': 'comments',
                            'like_count': 'likes', 'url': 'post_url', 'product_type': 'type'
                        })
                        df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'], unit='s', errors='coerce')
                        df_clean['total_interaction'] = df_clean['likes'] + df_clean['comments']
                        df_clean['keyword'] = keyword
                        df_clean['followers_count'] = None
                        df_clean['commentability'] = None
                        df_clean['likability'] = None
                        df_clean['virality'] = None

                        seen_shortcodes = set()
                        max_details = 100
                        for idx, row in df_clean.iterrows():
                            shortcode = row['code']
                            if pd.isna(shortcode) or shortcode in seen_shortcodes:
                                continue
                            try:
                                post_detail = client.instagram.post_info_and_comments(code=shortcode).data
                                seen_shortcodes.add(shortcode)
                                followers = post_detail.get("owner", {}).get("edge_followed_by", {}).get("count", None)
                                df_clean.at[idx, 'followers_count'] = followers
                                if followers and followers > 0:
                                    df_clean.at[idx, 'commentability'] = row['comments'] / followers
                                    df_clean.at[idx, 'likability'] = row['likes'] / followers
                                    df_clean.at[idx, 'virality'] = row['play_count'] / followers if row['play_count'] else None
                                sleep(0.2)
                                if len(seen_shortcodes) >= max_details:
                                    break
                            except Exception as e:
                                logger.error(f"Error fetching post details for shortcode {shortcode}: {e}")
                                continue

                        df_clean.drop(columns=['code'], inplace=True)
                        all_dfs.append(df_clean)
                        logger.info(f"Appended DataFrame for keyword '{keyword}' with {len(df_clean)} rows")

                elif method == "Username":
                    detailed_info_endpoint = "/instagram/user/detailed-info"
                    posts_endpoint = "/instagram/user/posts"
                    usernames = [un.strip().lstrip("@") for un in username_input.split(",") if un.strip()]

                    for username in usernames:
                        logger.info(f"Processing username: {username}")
                        params = {"username": username, "token": API_TOKEN}
                        res = make_request(root + detailed_info_endpoint, params)
                        if not res:
                            logger.warning(f"Failed to fetch user details for {username}")
                            continue
                        response = res.json().get("data", {})
                        user_id = response.get("id")
                        if not user_id:
                            logger.warning(f"No user ID found for username: {username}")
                            continue
                        logger.info(f"Fetched user ID {user_id} for username: {username}")

                        all_posts = []
                        params = {
                            "user_id": user_id,
                            "depth": posts_depth,
                            "chunk_size": chunk_size,
                            "start_cursor": "",
                            "alternative_method": False,
                            "token": API_TOKEN
                        }
                        page_count = 1
                        next_cursor = ""
                        while page_count <= max_pages and next_cursor is not None:
                            params["start_cursor"] = next_cursor
                            res = make_request(root + posts_endpoint, params)
                            if not res:
                                logger.error(f"Failed to fetch posts page {page_count} for user '{user_id}'")
                                break
                            response = res.json().get("data", {})
                            posts = [post.get("node") for post in response.get("posts", [])]
                            all_posts.extend(posts[:chunk_size * posts_depth])
                            next_cursor = response.get("last_cursor")
                            logger.info(f"Fetched {len(posts)} posts for user '{user_id}' on page {page_count}")
                            page_count += 1
                            sleep(0.5)

                        if not all_posts:
                            logger.warning(f"No posts found for username: {username}")
                            continue

                        df_raw = pd.json_normalize(all_posts)
                        expected_columns = [
                            'id', 'shortcode', 'taken_at_timestamp', 'edge_media_to_caption.edges',
                            'edge_media_to_comment.count', 'edge_media_preview_like.count', '__typename'
                        ]
                        for col in expected_columns:
                            if col not in df_raw.columns:
                                df_raw[col] = None

                        df_raw['caption'] = df_raw['edge_media_to_caption.edges'].apply(
                            lambda x: x[0]['node']['text'] if x and isinstance(x, list) and len(x) > 0 else None
                        )
                        df_raw['url'] = df_raw['shortcode'].apply(
                            lambda x: f"https://www.instagram.com/p/{x}" if pd.notna(x) else None
                        )

                        df_clean = df_raw[[
                            'id', 'shortcode', 'taken_at_timestamp', 'caption',
                            'edge_media_to_comment.count', 'edge_media_preview_like.count',
                            'url', '__typename'
                        ]].copy()

                        df_clean = df_clean.rename(columns={
                            'id': 'post_id',
                            'taken_at_timestamp': 'timestamp',
                            'edge_media_to_comment.count': 'comments',
                            'edge_media_preview_like.count': 'likes',
                            'url': 'post_url',
                            '__typename': 'type'
                        })

                        df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'], unit='s', errors='coerce')
                        df_clean['total_interaction'] = df_clean['likes'] + df_clean['comments']
                        df_clean['username'] = username
                        df_clean['followers_count'] = None
                        df_clean['commentability'] = None
                        df_clean['likability'] = None
                        df_clean['video_duration'] = None

                        seen_shortcodes = set()
                        max_details = 100
                        for idx, row in df_clean.iterrows():
                            shortcode = row['shortcode']
                            if pd.isna(shortcode) or shortcode in seen_shortcodes:
                                continue
                            try:
                                post_detail = client.instagram.post_info_and_comments(code=shortcode).data
                                seen_shortcodes.add(shortcode)
                                followers = post_detail.get("owner", {}).get("edge_followed_by", {}).get("count", None)
                                df_clean.at[idx, 'followers_count'] = followers
                                if post_detail.get("is_video"):
                                    df_clean.at[idx, 'video_duration'] = post_detail.get('video_duration', 0)
                                if followers and followers > 0:
                                    df_clean.at[idx, 'commentability'] = row['comments'] / followers
                                    df_clean.at[idx, 'likability'] = row['likes'] / followers
                                sleep(0.2)
                                if len(seen_shortcodes) >= max_details:
                                    break
                            except Exception as e:
                                logger.error(f"Error fetching post details for shortcode {shortcode}: {e}")
                                continue

                        df_clean.drop(columns=['shortcode'], inplace=True)
                        all_dfs.append(df_clean)
                        logger.info(f"Appended DataFrame for username '{username}' with {len(df_clean)} rows")

                elif method == "Username (Reels)":
                    detailed_info_endpoint = "/instagram/user/detailed-info"
                    reels_endpoint = "/instagram/user/reels"
                    usernames = [un.strip().lstrip("@") for un in username_input.split(",") if un.strip()]

                    for username in usernames:
                        logger.info(f"Processing username: {username}")
                        params = {"username": username, "token": API_TOKEN}
                        res = make_request(root + detailed_info_endpoint, params)
                        if not res:
                            logger.warning(f"Failed to fetch user details for {username}")
                            continue
                        response = res.json().get("data", {})
                        user_id = response.get("id")
                        if not user_id:
                            logger.warning(f"No user ID found for username: {username}")
                            continue
                        logger.info(f"Fetched user ID {user_id} for username: {username}")

                        all_reels = []
                        params = {
                            "user_id": user_id,
                            "depth": min(posts_depth, 3),
                            "chunk_size": chunk_size,
                            "start_cursor": "",
                            "include_feed_video": include_feed_video,
                            "token": API_TOKEN
                        }
                        page_count = 1
                        next_cursor = ""
                        while page_count <= max_pages and next_cursor is not None:
                            params["start_cursor"] = next_cursor
                            res = make_request(root + reels_endpoint, params, is_reels=True)
                            if not res:
                                logger.error(f"Failed to fetch Reels page {page_count} for user '{user_id}'")
                                break
                            response = res.json().get("data", {})
                            reels = [reel.get("media") for reel in response.get("reels", [])]
                            if not reels:
                                logger.info(f"No more Reels found for user '{user_id}' on page {page_count}")
                                break
                            all_reels.extend(reels[:chunk_size * posts_depth])
                            next_cursor = response.get("nextCursor")
                            logger.info(f"Fetched {len(reels)} Reels for user '{user_id}' on page {page_count}")
                            page_count += 1
                            sleep(1)

                        if not all_reels:
                            logger.warning(f"No Reels found for username: {username}")
                            continue

                        df_raw = pd.json_normalize(all_reels)
                        expected_columns = [
                            'pk', 'taken_at', 'caption.text', 'comment_count', 'like_count',
                            'product_type', 'video_duration', 'play_count', 'code'
                        ]
                        for col in expected_columns:
                            if col not in df_raw.columns:
                                df_raw[col] = None

                        df_raw['url'] = df_raw['code'].apply(
                            lambda x: f"https://www.instagram.com/reel/{x}" if pd.notna(x) else None
                        )

                        df_clean = df_raw[[
                            'pk', 'taken_at', 'caption.text', 'comment_count', 'like_count',
                            'url', 'product_type', 'video_duration', 'play_count', 'code'
                        ]].copy()

                        df_clean = df_clean.rename(columns={
                            'pk': 'post_id',
                            'taken_at': 'timestamp',
                            'caption.text': 'caption',
                            'comment_count': 'comments',
                            'like_count': 'likes',
                            'url': 'post_url',
                            'product_type': 'type'
                        })

                        df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'], unit='s', errors='coerce')
                        df_clean['total_interaction'] = df_clean['likes'].fillna(0) + df_clean['comments'].fillna(0)
                        df_clean['username'] = username
                        df_clean['followers_count'] = None
                        df_clean['commentability'] = None
                        df_clean['likability'] = None
                        df_clean['virality'] = None

                        seen_codes = set()
                        max_details = 100
                        for idx, row in df_clean.iterrows():
                            code = row['code']
                            if pd.isna(code) or code in seen_codes:
                                continue
                            try:
                                post_detail = client.instagram.post_info_and_comments(code=code).data
                                seen_codes.add(code)
                                followers = post_detail.get("owner", {}).get("edge_followed_by", {}).get("count", None)
                                df_clean.at[idx, 'followers_count'] = followers
                                if followers and followers > 0:
                                    df_clean.at[idx, 'commentability'] = row['comments'] / followers
                                    df_clean.at[idx, 'likability'] = row['likes'] / followers
                                    df_clean.at[idx, 'virality'] = row['play_count'] / followers if row['play_count'] else None
                                sleep(0.5)
                                if len(seen_codes) >= max_details:
                                    break
                            except Exception as e:
                                logger.error(f"Error fetching post details for code {code}: {e}")
                                continue

                        df_clean.drop(columns=['code'], inplace=True)
                        all_dfs.append(df_clean)
                        logger.info(f"Appended DataFrame for username '{username}' with {len(df_clean)} rows")

                if all_dfs:
                    df = pd.concat(all_dfs, ignore_index=True)
                    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                    df['likes'] = pd.to_numeric(df['likes'], errors='coerce')
                    if 'play_count' in df.columns:
                        df['play_count'] = pd.to_numeric(df['play_count'], errors='coerce')

                    # --- View and Likes Filter Logic (Reels only) ---
                    if method in ["Hashtag/Keyword (Reels)", "Username (Reels)"]:
                        if view_filter != "All":
                            df = df[df['play_count'].notna()]
                            if view_filter == "0–50K":
                                df = df[df["play_count"] <= 50000]
                            elif view_filter == "50K–100K":
                                df = df[(df["play_count"] > 50000) & (df["play_count"] <= 100000)]
                            elif view_filter == "100K–500K":
                                df = df[(df["play_count"] > 100000) & (df["play_count"] <= 500000)]
                            elif view_filter == "500K–1M":
                                df = df[(df["play_count"] > 500000) & (df["play_count"] <= 1000000)]
                            elif view_filter == "1M+":
                                df = df[df["play_count"] > 1000000]

                        if like_filter != "All likes":
                            df = df[df["likes"].notna()]
                            if like_filter == "0–50K":
                                df = df[df["likes"] <= 50000]
                            elif like_filter == "50K–100K":
                                df = df[(df["likes"] > 50000) & (df["likes"] <= 100000)]
                            elif like_filter == "100K–500K":
                                df = df[(df["likes"] > 100000) & (df["likes"] <= 500000)]
                            elif like_filter == "500K–1M":
                                df = df[(df["likes"] > 500000) & (df["likes"] <= 1000000)]
                            elif like_filter == "1M+":
                                df = df[df["likes"] > 1000000]

                    st.session_state['scraped_df'] = df
                    st.success(f" Scraped {len(df)} posts successfully.")
                    st.dataframe(df.head(10))
                else:
                    st.error(" No data scraped. Check inputs or try again.")
                    logger.warning("No data frames created. Check API responses or input validity.")

            except Exception as e:
                st.error(f" Error: {str(e)}")
                logger.error(f"Global error: {e}")

# --- Download Section ---
if st.session_state.get('scraped_df') is not None:
    df = st.session_state['scraped_df']
    try:
        if download_format == "CSV":
            st.download_button(" Download CSV", data=df.to_csv(index=False), file_name="instagram_data.csv", mime="text/csv")
        elif download_format == "XLSX":
            xlsx_buffer = BytesIO()
            df.to_excel(xlsx_buffer, index=False, engine='openpyxl')
            st.download_button(" Download XLSX", data=xlsx_buffer.getvalue(), file_name="instagram_data.xlsx", 
                              mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        elif download_format == "TXT":
            txt_data = df.to_string(index=False)
            st.download_button(" Download TXT", data=txt_data, file_name="instagram_data.txt", mime="text/plain")
        elif download_format == "HTML":
            html_data = df.to_html(index=False)
            st.download_button(" Download HTML", data=html_data, file_name="instagram_data.html", mime="text/html")
        elif download_format == "JSON":
            st.download_button(" Download JSON", data=df.to_json(orient="records"), file_name="instagram_data.json", 
                              mime="application/json")
    except Exception as e:
        st.error(f"Error in download section: {str(e)}")
        logger.error(f"Error in download section: {e}")

st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)

# --- METRICS NOTE ---
st.markdown("""
    <div style="background-color: #f8fafc; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 123, 255, 0.05); margin-bottom: 1.5rem;">
        <h3 style="font-size: 1.25rem; font-weight: 600; color: #1a1a1a; margin-bottom: 1rem;">Understanding Key Metrics</h3>
        <p style="font-size: 0.95rem; color: #4a5568; line-height: 1.5; margin-bottom: 0.75rem;">
            <span style="color: #007bff; font-weight: 600;"> Virality:</span> Measures a Reel's reach relative to the creator's audience (play_count ÷ followers). Higher values signal stronger viral potential (Reels only).
        </p>
        <p style="font-size: 0.95rem; color: #4a5568; line-height: 1.5; margin-bottom: 0.75rem;">
            <span style="color: #28a745; font-weight: 600;"> Commentability:</span> Gauges interaction level (comments ÷ followers). Higher values indicate engaging content.
        </p>
        <p style="font-size: 0.95rem; color: #4a5568; line-height: 1.5;">
            <span style="color: #d97706; font-weight: 600;"> Likability:</span> Reflects appeal (likes ÷ followers). 
            Higher values suggest well-received content.
        </p>
    </div>
""", unsafe_allow_html=True)

# --- FOOTER ---
current_year = datetime.now().strftime("%Y")
st.markdown(f"""
    <div class="footer">
        <p>© {current_year} KOMI Group. All rights reserved.</p>
        <p>This tool is the property of KOMI Group and intended solely for internal use only. 
           Unauthorized distribution or use outside the organization is strictly prohibited.</p>
    </div>
""", unsafe_allow_html=True)
