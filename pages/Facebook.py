import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from io import BytesIO
import numpy as np
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib.parse
import time
from auth import get_authenticator
from style import inject_custom_css

# --- PAGE CONFIG ---
st.set_page_config(page_title="KOMI Facebook Scraper | KOMI Group", page_icon="komi_logo", layout="centered")
inject_custom_css()

# --- AUTHENTICATION ---
authenticator = get_authenticator()
if not st.session_state.get("authentication_status"):
    st.warning("Please log in first.")
    st.stop()

# --- Show logout in sidebar ---
authenticator.logout("Logout", location="sidebar")
st.sidebar.image("logo_2.png")

# --- SETTINGS ---
API_KEY = "eb8778fb7948455fbb55579f18131e97"

# --- CUSTOM CSS (Reused from TikTok Scraper) ---
st.markdown("""
    <style>
        /* General page styling */
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
            -webkit-text-fill-color: transparent;
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
        .stSelectbox > div > select:focus {
            border-color: #007bff;
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
        .stAlert[role="alert"] {
            background-color: #fff1f0;
            color: #c53030;
        }
        .stAlert[role="success"] {
            background-color: #e6ffed;
            color: #2e7d32;
        }
        .stAlert[role="warning"] {
            background-color: #fff8e1;
            color: #d97706;
        }
        .stDataFrame {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            overflow: hidden;
        }
        .stDataFrame table {
            width: 100%;
            border-collapse: collapse;
        }
        .stDataFrame th {
            background-color: #f1f5f9;
            font-weight: 600;
            padding: 0.75rem;
        }
        .stDataFrame td {
            padding: 0.75rem;
            border-top: 1px solid #e2e8f0;
        }
        .stDataFrame tr:nth-child(even) {
            background-color: #f8fafc;
        }
        .footer {
            font-size: 0.85rem;
            color: #4a5568;
            text-align: center;
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid #e2e8f0;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }
        footer {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# --- INIT SESSION STATE ---
if 'scraped_df' not in st.session_state:
    st.session_state.scraped_df = None

# --- HEADER ---
st.image("komi_logo.png", width=100)
st.markdown("""
    <div class="header-container">
        <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" width="36">
        <h1>Facebook Scraper</h1>
    </div>
""", unsafe_allow_html=True)
st.caption("Powered by KOMI Insights · Built for the Ark Media Team.")
st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)
st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)

# --- DOWNLOAD FORMAT SELECTION ---
download_format = st.selectbox("Select download format", ["CSV", "XLSX", "TXT", "HTML", "JSON"])

# --- HELPER FUNCTIONS (FROM PROTOTYPES) ---
def flatten_node(current_path, json_node, result_map):
    if isinstance(json_node, dict):
        path_prefix = f"{current_path}." if current_path else ""
        for key, value in json_node.items():
            flatten_node(f"{path_prefix}{key}", value, result_map)
    elif isinstance(json_node, list):
        for i, item in enumerate(json_node):
            flatten_node(f"{current_path}[{i}]", item, result_map)
    else:
        if json_node is None:
            result_map[current_path] = ""
        else:
            result_map[current_path] = str(json_node)

def find_first_value(data: dict, keys: list):
    for key in keys:
        if key in data:
            return data[key]
    return None

def to_int(num_str):
    if num_str is None:
        return None
    try:
        return int(num_str)
    except ValueError:
        return 0

def parse_follower_text(text: str) -> int:
    if not text:
        return 0
    text = text.strip().lower()
    match = re.search(r"([\d,.]+)\s*([kmb]?)", text)
    if not match:
        return 0
    number_str, suffix = match.groups()
    number_str = number_str.replace(",", "")
    try:
        number = float(number_str)
    except ValueError:
        return 0
    multiplier = {'k': 1_000, 'm': 1_000_000, 'b': 1_000_000_000}.get(suffix, 1)
    return int(number * multiplier)

def get_follower_count(url: str) -> int:
    info_url = "http://api.axesso.de/fba/v2/facebook-page-info"
    headers = {"axesso-api-key": API_KEY}
    params = {"url": url}
    try:
        response = requests.get(info_url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return parse_follower_text(data.get("countFollowerText", ""))
    except requests.RequestException as e:
        st.error(f"Error fetching follower count for {url}: {e}")
        return 0

def parse_view_count(text: str) -> int:
    if not text:
        return 0
    match = re.search(r"(\d+\.?\d*[KMB]?) views", text, re.IGNORECASE)
    if not match:
        return 0
    view_str = match.group(1).lower()
    number = float(view_str[:-1]) if view_str[-1] in 'kmb' else float(view_str)
    multiplier = {'k': 1_000, 'm': 1_000_000, 'b': 1_000_000_000}.get(view_str[-1], 1)
    return int(number * multiplier)

def parse_timestamp(text: str) -> str:
    if not text:
        return ""
    parts = text.split("·")
    return parts[0].strip() if parts else ""

def is_valid_facebook_url(url: str) -> bool:
    return url and url.startswith("https://www.facebook.com")

# --- MAIN CONTENT ---
with st.container():
    method = st.selectbox("Select scraping method", ["By Keywords", "By Username", "By Username Reels"])

with st.form("scraper_form"):
    if method == "By Keywords":
        keyword_input = st.text_area("Enter keyword(s), separated by commas")
        keywords = [kw.strip() for kw in keyword_input.split(",") if kw.strip()]
        sort = "RECENT"
        fetch_limit = st.slider("Number of posts to scrape (max 500)", 1, 500, 50)
    elif method == "By Username":
        username_input = st.text_area("Enter Facebook username(s), separated by commas (with or without @)")
        usernames = [un.strip().lstrip("@") for un in username_input.split(",") if un.strip()]
        fetch_limit = st.slider("Number of posts to scrape (max 500)", 1, 500, 50)
        post_filter = st.selectbox("Filter by post type", ["All Posts", "Picture Only (Views = 0)"])
    else:  # By Username Reels
        username_input = st.text_area("Enter Facebook username(s), separated by commas (with or without @)")
        usernames = [un.strip().lstrip("@") for un in username_input.split(",") if un.strip()]
        fetch_limit = st.slider("Number of posts to scrape (max 500)", 1, 500, 50)

    # Views and Likes Filters (for By Keywords and By Username Reels)
    if method in ["By Keywords", "By Username Reels"]:
        view_filter = st.selectbox("Filter by views", [
            "All views", "0–50K", "50K–100K", "100K–500K", "500K–1M", "1M+"
        ])
        like_filter = st.selectbox("Filter by likes", [
            "All likes", "0–50K", "50K–100K", "100K–500K", "500K–1M", "1M+"
        ])

    # Data reduction notice
    st.markdown(
        "<small> Using views and likes filters may significantly reduce the number of posts returned. "
        "Try adjusting or disabling filters for broader results.</small>",
        unsafe_allow_html=True
    )

    submit = st.form_submit_button("Scrape Data")

# --- SCRAPING LOGIC ---
if submit:
    with st.spinner("Scraping data... Please wait."):
        try:
            all_extracted_data = []

            if method == "By Keywords":
                # Setup session with retry logic
                session = requests.Session()
                retries_config = Retry(total=5, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
                session.mount("http://", HTTPAdapter(max_retries=retries_config))
                headers = {"axesso-api-key": API_KEY}

                def get_post_details(post_url: str) -> dict:
                    default_response = {"timestamp": "", "likes": None, "comments": None, "shares": None, "views": None}
                    if not is_valid_facebook_url(post_url):
                        return default_response
                    details_url = "http://api.axesso.de/fba/facebook-post-details"
                    params = {"url": post_url}
                    try:
                        response = session.get(details_url, headers=headers, params=params, timeout=30)
                        response.raise_for_status()
                        data = response.json()
                        post_details = data.get("postDetails")
                        if not post_details:
                            return default_response
                        included_posts = post_details.get("includedPosts", [{}])[0].get("result", {}).get("data", {}).get("feedback", {})
                        return {
                            "timestamp": post_details.get("date", ""),
                            "likes": included_posts.get("reaction_count", {}).get("count", None),
                            "comments": included_posts.get("total_comment_count", None),
                            "shares": included_posts.get("share_count", {}).get("count", None),
                            "views": included_posts.get("video_view_count_renderer", {}).get("count", None)
                        }
                    except requests.RequestException:
                        return default_response

                def process_video(video):
                    rendering = video.get("rendering_strategy", {}).get("view_model", {})
                    video_metadata = rendering.get("video_metadata_model", {})
                    owner_profile = video_metadata.get("video_owner_profile", {})
                    owner_url = owner_profile.get("url", "")
                    video_id = video_metadata.get("video", {}).get("id", "")
                    description = video_metadata.get("title", "")
                    relative_time_string = video_metadata.get("relative_time_string", "")
                    fallback_timestamp = parse_timestamp(relative_time_string)
                    views = parse_view_count(relative_time_string)
                    video_url = rendering.get("video_click_model", {}).get("click_metadata_model", {}).get("payload", {}).get("open_video_uri", "")
                    full_video_url = f"https://www.facebook.com{video_url}" if video_url else ""
                    followers_count = get_follower_count(owner_url) if owner_url else 0
                    post_details = get_post_details(full_video_url) if full_video_url else {
                        "timestamp": fallback_timestamp, "likes": None, "comments": None, "shares": None, "views": None
                    }
                    final_views = post_details["views"] if post_details["views"] is not None else views
                    final_timestamp = post_details["timestamp"] if post_details["timestamp"] else fallback_timestamp
                    return {
                        "username": owner_profile.get("name", ""),
                        "followers_count": followers_count,
                        "post_id": video_id,
                        "timestamp": final_timestamp,
                        "description": description,
                        "views": final_views,
                        "likes": post_details["likes"],
                        "comments": post_details["comments"],
                        "shares": post_details["shares"],
                        "post_url": full_video_url,
                        "virality": round(final_views / followers_count, 5) if followers_count and final_views else None,
                        "sharability": round(post_details["shares"] / final_views, 5) if final_views and post_details["shares"] else None,
                        "commentability": round(post_details["comments"] / final_views, 5) if final_views and post_details["comments"] else None
                    }

                # Fetch videos
                search_url = "http://api.axesso.de/fba/facebook-search-videos"
                all_videos = []
                for keyword in keywords:
                    cursor = None
                    page = 1
                    keyword_videos = []
                    while len(keyword_videos) < fetch_limit:
                        params = {"keyword": keyword, "sort": sort}
                        if cursor:
                            params["cursor"] = urllib.parse.unquote(cursor)
                        response = session.get(search_url, headers=headers, params=params, timeout=30)
                        response.raise_for_status()
                        data = response.json()
                        videos = data.get("posts", [])
                        cursor = data.get("cursor")
                        has_next = data.get("hasNextPage", False)
                        keyword_videos.extend(videos)
                        if not has_next or not cursor:
                            break
                        page += 1
                    all_videos.extend(keyword_videos[:fetch_limit])
                all_videos = all_videos[:fetch_limit]

                # Process videos
                if all_videos:
                    max_workers = 8
                    with ThreadPoolExecutor(max_workers=max_workers) as executor:
                        future_to_video = {executor.submit(process_video, video): video for video in all_videos}
                        for future in as_completed(future_to_video):
                            try:
                                all_extracted_data.append(future.result())
                            except Exception as e:
                                st.error(f"Error processing video: {e}")

            elif method == "By Username":
                def map_response(response, input_url):
                    data = response.json()
                    results = []
                    if response.status_code == 404:
                        results.append({
                            'statusCode': response.status_code,
                            'statusMessage': "NOT_FOUND",
                            'url': input_url
                        })
                    else:
                        posts = data.get('posts', [])
                        for post in posts:
                            post_flatten = {}
                            flatten_node("", post, post_flatten)
                            results.append({
                                'statusCode': response.status_code,
                                'statusMessage': "FOUND",
                                'text': post['text'],
                                'pageId': data['pageId'],
                                'creationDate': post['date'],
                                'id': post['id'],
                                'feedbackId': post['feedbackId'],
                                'imageUrlList': post['imageUrlList'],
                                'pageUrl': find_first_value(post_flatten, [
                                    'data.result.data.user.timeline_list_feed_units.edges[0].node.comet_sections.content.story.actors[0].url',
                                    'data.result.data.node.comet_sections.context_layout.story.comet_sections.actor_photo.story.actors[0].profile_url'
                                ]),
                                'creationTime': to_int(find_first_value(post_flatten, [
                                    'data.result.data.user.timeline_list_feed_units.edges[0].node.comet_sections.context_layout.story.comet_sections.metadata[0].story.creation_time',
                                    'data.result.data.user.timeline_list_feed_units.edges[0].node.comet_sections.context_layout.story.comet_sections.metadata[1].story.creation_time',
                                    'data.result.data.node.comet_sections.content.story.comet_sections.context_layout.story.comet_sections.metadata[0].story.creation_time',
                                    'data.result.data.node.comet_sections.content.story.comet_sections.context_layout.story.comet_sections.metadata[1].story.creation_time'
                                ])),
                                'postUrl': find_first_value(post_flatten, [
                                    'data.result.data.user.timeline_list_feed_units.edges[0].node.comet_sections.context_layout.story.comet_sections.metadata[0].story.url',
                                    'data.result.data.user.timeline_list_feed_units.edges[0].node.comet_sections.context_layout.story.comet_sections.metadata[1].story.url',
                                    'data.result.data.node.comet_sections.content.story.comet_sections.context_layout.story.comet_sections.metadata[0].story.url',
                                    'data.result.data.node.comet_sections.content.story.comet_sections.metadata[1].story.url'
                                ]),
                                'postId': find_first_value(post_flatten, [
                                    'data.result.data.user.timeline_list_feed_units.edges[0].node.comet_sections.content.story.post_id',
                                    'data.result.data.node.comet_sections.feedback.story.feedback_context.interesting_top_level_comments[0].comment.parent_post_story.attachments[0].media.id',
                                    'data.result.data.node.comet_sections.feedback.story.feedback_context.feedback_target_with_context.comet_ufi_summary_and_actions_renderer.feedback.subscription_target_id'
                                ]),
                                'reactionCount': to_int(find_first_value(post_flatten, [
                                    'data.result.data.user.timeline_list_feed_units.edges[0].node.comet_sections.feedback.story.story_ufi_container.story.feedback_context.feedback_target_with_context.comet_ufi_summary_and_actions_renderer.feedback.reaction_count.count',
                                    'data.result.data.node.comet_sections.feedback.story.feedback_context.feedback_target_with_context.comet_ufi_summary_and_actions_renderer.feedback.reaction_count.count'
                                ])),
                                'shareCount': to_int(find_first_value(post_flatten, [
                                    'data.result.data.user.timeline_list_feed_units.edges[0].node.comet_sections.feedback.story.story_ufi_container.story.feedback_context.feedback_target_with_context.comet_ufi_summary_and_actions_renderer.feedback.share_count.count',
                                    'data.result.data.node.comet_sections.feedback.story.feedback_context.feedback_target_with_context.comet_ufi_summary_and_actions_renderer.feedback.share_count.count'
                                ])),
                                'commentCount': to_int(find_first_value(post_flatten, [
                                    'data.result.data.user.timeline_list_feed_units.edges[0].node.comet_sections.feedback.story.story_ufi_container.story.feedback_context.feedback_target_with_context.comet_ufi_summary_and_actions_renderer.feedback.comments_count_summary_renderer.feedback.comment_rendering_instance.comments.total_count',
                                    'data.result.data.node.comet_sections.feedback.story.feedback_context.feedback_target_with_context.comet_ufi_summary_and_actions_renderer.feedback.comments_count_summary_renderer.feedback.comment_count.total_count'
                                ])),
                                'externalUrl': find_first_value(post_flatten, [
                                    'data.result.data.user.timeline_list_feed_units.edges[0].node.comet_sections.content.story.attachments[0].comet_footer_renderer.attachment.target.external_url',
                                    'data.result.data.node.comet_sections.content.story.attachments[0].comet_footer_renderer.attachment.target.external_url'
                                ]),
                                'videoViewCount': to_int(find_first_value(post_flatten, [
                                    'data.result.data.user.timeline_list_feed_units.edges[0].node.comet_sections.feedback.story.story_ufi_container.story.feedback_context.feedback_target_with_context.comet_ufi_summary_and_actions_renderer.feedback.video_view_count',
                                    'data.result.data.node.comet_sections.feedback.story.feedback_context.feedback_target_with_context.comet_ufi_summary_and_actions_renderer.feedback.video_view_count'
                                ])),
                                'inputUrl': input_url
                            })
                    return results

                for username in usernames:
                    page_url = f"https://www.facebook.com/{username}"
                    followers_count = get_follower_count(page_url)
                    posts_url = "http://api.axesso.de/fba/facebook-lookup-posts"
                    headers = {"axesso-api-key": API_KEY}
                    all_posts = []
                    current_url = page_url
                    page = 1
                    while len(all_posts) < fetch_limit:
                        params = {"url": current_url}
                        response = requests.get(posts_url, headers=headers, params=params)
                        if response.status_code != 200:
                            st.error(f"API error for {username}: {response.status_code}")
                            break
                        mapped_posts = map_response(response, current_url)
                        posts = [post for post in mapped_posts if post['statusMessage'] == "FOUND"]
                        next_url = response.json().get("nextUrl")
                        all_posts.extend(posts)
                        if not next_url:
                            break
                        current_url = next_url
                        page += 1
                        time.sleep(0.5)

                    if all_posts:
                        for post in all_posts[:fetch_limit]:
                            views = post.get("videoViewCount", 0)
                            shares = post.get("shareCount", 0)
                            comments = post.get("commentCount", 0)
                            likes = post.get("reactionCount", 0)
                            post_url = post.get("postUrl", "")
                            all_extracted_data.append({
                                "username": username,
                                "followers_count": followers_count,
                                "post_id": post.get("id"),
                                "timestamp": post.get("creationDate"),
                                "description": post.get("text"),
                                "views": views,
                                "likes": likes,
                                "comments": comments,
                                "shares": shares,
                                "post_url": post_url,
                                "virality": round(views / followers_count, 5) if followers_count else None,
                                "sharability": round(shares / views, 5) if views else None,
                                "commentability": round(comments / views, 5) if views else None
                            })

            else:  # By Username Reels
                reels_url = "http://api.axesso.de/fba/facebook-lookup-reels"
                headers = {"axesso-api-key": API_KEY}
                for username in usernames:
                    page_url = f"https://www.facebook.com/{username}"
                    followers_count = get_follower_count(page_url)
                    all_reels = []
                    cursor = None
                    page = 1
                    while len(all_reels) < fetch_limit:
                        params = {"url": page_url}
                        if cursor:
                            params["cursor"] = urllib.parse.unquote(cursor)
                        response = requests.get(reels_url, headers=headers, params=params)
                        if response.status_code != 200:
                            st.error(f"API error for {username}: {response.status_code}")
                            break
                        data = response.json()
                        reels = data.get("details", [])
                        cursor = data.get("cursor")
                        has_next = data.get("hasNextPage", False)
                        all_reels.extend(reels)
                        if not has_next or not cursor:
                            break
                        page += 1
                        time.sleep(0.5)

                    if all_reels:
                        for reel in all_reels[:fetch_limit]:
                            views = reel.get("videoViewCount", 0)
                            shares = reel.get("shareCount", 0)
                            comments = reel.get("commentCount", 0)
                            likes = reel.get("likersCount", reel.get("reactionCount", 0))
                            all_extracted_data.append({
                                "username": username,
                                "followers_count": followers_count,
                                "post_id": reel.get("postId"),
                                "timestamp": reel.get("date"),
                                "description": reel.get("text"),
                                "views": views,
                                "likes": likes,
                                "comments": comments,
                                "shares": shares,
                                "post_url": reel.get("url"),
                                "virality": round(views / followers_count, 5) if followers_count else None,
                                "sharability": round(shares / views, 5) if views else None,
                                "commentability": round(comments / views, 5) if views else None
                            })

            # Create DataFrame
            if all_extracted_data:
                df = pd.DataFrame(all_extracted_data)
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
                df['views'] = pd.to_numeric(df['views'], errors='coerce')
                df['likes'] = pd.to_numeric(df['likes'], errors='coerce')

                # Apply Picture Only Filter for By Username
                if method == "By Username" and post_filter == "Picture Only (Views = 0)":
                    df = df[df["views"] == 0]

                # Apply Views and Likes Filters for By Keywords and By Username Reels
                if method in ["By Keywords", "By Username Reels"]:
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

                st.session_state.scraped_df = df
                st.success(f"Scraped {len(df)} posts successfully.")
                st.dataframe(df.head(10))
            else:
                st.error("No posts found for the given input.")

        except Exception as e:
            st.error(f"Error: {str(e)}")

# --- DOWNLOAD BUTTON ---
if st.session_state.scraped_df is not None:
    df = st.session_state.scraped_df
    if download_format == "CSV":
        st.download_button("Download CSV", data=df.to_csv(index=False), file_name="facebook_data.csv", mime="text/csv")
    elif download_format == "XLSX":
        xlsx_buffer = BytesIO()
        df.to_excel(xlsx_buffer, index=False, engine='openpyxl')
        st.download_button("Download XLSX", data=xlsx_buffer.getvalue(), file_name="facebook_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    elif download_format == "TXT":
        txt_data = df.to_string(index=False)
        st.download_button("Download TXT", data=txt_data, file_name="facebook_data.txt", mime="text/plain")
    elif download_format == "HTML":
        html_data = df.to_html(index=False)
        st.download_button("Download HTML", data=html_data, file_name="facebook_data.html", mime="text/html")
    elif download_format == "JSON":
        st.download_button("Download JSON", data=df.to_json(orient="records"), file_name="facebook_data.json", mime="application/json")

st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)

# --- METRICS NOTE ---
st.markdown("""
    <div style="background-color: #f8fafc; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 123, 255, 0.05); margin-bottom: 1.5rem;">
        <h3 style="font-size: 1.25rem; font-weight: 600; color: #1a1a1a; margin-bottom: 1rem;">Understanding Key Metrics</h3>
        <p style="font-size: 0.95rem; color: #4a5568; line-height: 1.5; margin-bottom: 0.75rem;">
            <span style="color: #007bff; font-weight: 600;"> Virality:</span> Measures a post's reach relative to the creator's audience (views ÷ follower count). Higher values signal stronger viral potential.
        </p>
        <p style="font-size: 0.95rem; color: #4a5568; line-height: 1.5; margin-bottom: 0.75rem;">
            <span style="color: #28a745; font-weight: 600;"> Sharability:</span> Gauges the likelihood of sharing (shares ÷ views). Elevated values indicate resonant, share-worthy content.
        </p>
        <p style="font-size: 0.95rem; color: #4a5568; line-height: 1.5;">
            <span style="color: #d97706; font-weight: 600;"> Commentability:</span> Reflects engagement via interaction (comments ÷ views). Higher values suggest discussion-driven content.
        </p>
    </div>
""", unsafe_allow_html=True)

# --- FOOTER ---
current_year = datetime.now().year
st.markdown(f"""
    <div class="footer">
        <p>© {current_year} KOMI Group. All rights reserved.</p>
        <p>This tool is the property of KOMI Group and intended solely for internal use only. Unauthorised distribution or use outside the organisation is strictly prohibited.</p>
    </div>
""", unsafe_allow_html=True)
