# app.py
import streamlit as st
from data import Work, get_all_works, get_work_by_id, get_works_by_category, SAMPLE_WORKS

st.set_page_config(
    page_title="百合收藏馆 | 女同作品推荐",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 缓存数据加载 ---
@st.cache_data(ttl=3600, show_spinner=False)
def load_all_works():
    return get_all_works()

# --- 样式设置 ---
st.markdown("""
<style>
    .main > div { padding: 1rem 2rem; }
    h1, h2, h3 { font-family: 'Noto Sans SC', sans-serif; }
    .work-card {
        background-color: #f8f0f6;
        border: 1px solid #e0d4e0;
        border-radius: 15px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .work-title { font-size: 1.2rem; font-weight: 600; margin-bottom: 0.3rem; }
    .work-meta { color: #7a6b7a; font-size: 0.9rem; margin-bottom: 0.5rem; }
    .work-tags { display: flex; flex-wrap: wrap; gap: 0.3rem; margin: 0.5rem 0; }
    .work-tag {
        background-color: #e8dce8; color: #4a3a4a;
        padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.8rem;
    }
    .work-rating { font-weight: bold; color: #d4a0a0; }
    .work-platforms { margin-top: 0.8rem; padding-top: 0.5rem; border-top: 1px dashed #e0d4e0; }
    .work-platform-link {
        background-color: #e8dce8; color: #4a3a4a;
        padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem;
        text-decoration: none; margin-right: 0.3rem;
    }
    .stButton button {
        background-color: #d4a0a0; color: white;
        border-radius: 20px; border: none; padding: 0.5rem 1.5rem;
    }
    .platform-section {
        background-color: #f0e8f0; border-radius: 10px; padding: 1rem; margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def display_work_card(work, all_works):
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            if work.cover_url:
                st.image(work.cover_url, width=120)
            else:
                st.image("https://via.placeholder.com/120x180/FAEBD7/000000?text=🌸", width=120)
        with col2:
            st.markdown(f"<div class='work-title'>{work.title}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='work-meta'>🖊️ {work.author} | ⭐ <span class='work-rating'>{work.rating}</span> | 📅 {work.year or '未知'} | 🏷️ {work.category}</div>", unsafe_allow_html=True)
            tags_html = "".join([f"<span class='work-tag'>#{tag}</span>" for tag in work.tags])
            st.markdown(f"<div class='work-tags'>{tags_html}</div>", unsafe_allow_html=True)
            st.write(work.description[:120] + ("..." if len(work.description) > 120 else ""))
            if work.platforms:
                platforms_html = "<div class='work-platforms'>📺 可观看于: "
                for platform, url in list(work.platforms.items())[:2]:
                    platforms_html += f"<a href='{url}' target='_blank' class='work-platform-link'>{platform}</a> "
                platforms_html += "</div>"
                st.markdown(platforms_html, unsafe_allow_html=True)
            if st.button("查看详情", key=f"detail_{work.id}"):
                st.session_state.selected_work = work
                st.rerun()


def show_work_detail(work):
    st.title(work.title)
    col1, col2 = st.columns([1, 2])
    with col1:
        if work.cover_url:
            st.image(work.cover_url, width=250)
        else:
            st.image("https://via.placeholder.com/250x370/FAEBD7/000000?text=🌸", width=250)
    with col2:
        st.markdown(f"**作者：** {work.author}")
        st.markdown(f"**分类：** {work.category}")
        st.markdown(f"**评分：** ⭐ **{work.rating}**")
        st.markdown(f"**年份：** {work.year or '未知'}")
        tags_html = "".join([f"<span class='work-tag'>#{tag}</span>" for tag in work.tags])
        st.markdown(f"**标签：** <div class='work-tags'>{tags_html}</div>", unsafe_allow_html=True)
        if work.platforms:
            st.markdown("---")
            st.markdown("### 📺 观看渠道")
            for platform, url in work.platforms.items():
                st.markdown(f"🔗 [{platform}]({url})")
        else:
            st.caption("💡 暂无收录观看渠道")
    st.markdown("---")
    st.markdown("**作品简介：**")
    st.write(work.description)
    if st.button("← 返回列表"):
        st.session_state.pop("selected_work", None)
        st.rerun()


def render_sidebar(all_works):
    with st.sidebar:
        st.markdown("## 🌸 百合收藏馆")
        st.markdown("---")
        st.markdown("### 导航")
        if st.button("🏠 首页", use_container_width=True):
            st.session_state.page = "home"
            st.session_state.pop("selected_work", None)
            st.rerun()
        if st.button("📚 文学", use_container_width=True):
            st.session_state.page = "文学"
            st.session_state.pop("selected_work", None)
            st.rerun()
        if st.button("🎬 影视", use_container_width=True):
            st.session_state.page = "影视"
            st.session_state.pop("selected_work", None)
            st.rerun()
        if st.button("🎮 动漫", use_container_width=True):
            st.session_state.page = "动漫"
            st.session_state.pop("selected_work", None)
            st.rerun()
        st.markdown("---")
        st.markdown("### 搜索")
        search_query = st.text_input("输入作品名/关键词", placeholder="例如：终将成为你")
        if search_query:
            st.session_state.search_query = search_query
            st.session_state.page = "search"
            st.session_state.pop("selected_work", None)
            st.rerun()
        st.markdown("---")
        st.markdown("### 筛选")
        st.session_state.filter_rating = st.slider("最低评分", 0.0, 10.0, 0.0, 0.1)
        all_tags = set()
        for work in all_works:
            all_tags.update(work.tags)
        st.session_state.filter_tags = st.multiselect("选择标签", sorted(all_tags))
        if st.button("清除筛选", use_container_width=True):
            st.session_state.filter_rating = 0.0
            st.session_state.filter_tags = []
            st.rerun()
        st.markdown("---")
        st.caption(f"共收录 {len(all_works)} 部作品")
    return search_query


def render_home(all_works):
    st.title("🌸 百合收藏馆")
    st.markdown("> 欢迎来到百合收藏馆！这里为你精心整理了女同题材的优秀作品，涵盖文学、影视和动漫。")
    st.markdown("---")
    cols = st.columns(3)
    categories = ["文学", "影视", "动漫"]
    for i, col in enumerate(cols):
        with col:
            st.subheader(f"{'📚' if i==0 else '🎬' if i==1 else '🎮'} {categories[i]}")
            works = get_works_by_category(categories[i], all_works)[:3]
            for work in works:
                display_work_card(work, all_works)


def render_category(category, all_works):
    st.title(f"{'📚' if category=='文学' else '🎬' if category=='影视' else '🎮'} {category}作品")
    works = get_works_by_category(category, all_works)
    if not works:
        st.info("该分类下暂时没有作品。")
        return
    if st.session_state.get("filter_rating", 0.0) > 0:
        works = [w for w in works if w.rating >= st.session_state.filter_rating]
    if st.session_state.get("filter_tags", []):
        works = [w for w in works if any(tag in w.tags for tag in st.session_state.filter_tags)]
    if not works:
        st.info("没有找到符合条件的作品。")
        return
    st.write(f"共找到 {len(works)} 部作品")
    col1, col2 = st.columns(2)
    for index, work in enumerate(works):
        with col1 if index % 2 == 0 else col2:
            display_work_card(work, all_works)


def render_search(all_works):
    query = st.session_state.get("search_query", "")
    st.title(f"🔍 搜索结果：\"{query}\"")
    if not query:
        st.info("请输入关键词进行搜索。")
        return
    matched = [w for w in all_works if w.title and query.lower() in w.title.lower()]
    if not matched:
        st.info(f"没有找到与 \"{query}\" 相关的作品。")
        return
    st.write(f"共找到 {len(matched)} 部作品")
    for work in matched:
        display_work_card(work, all_works)


def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"
        st.session_state.search_query = ""
        st.session_state.selected_work = None
        st.session_state.filter_rating = 0.0
        st.session_state.filter_tags = []

    with st.spinner("正在加载作品数据..."):
        all_works = load_all_works()

    render_sidebar(all_works)

    if st.session_state.get("selected_work"):
        show_work_detail(st.session_state.selected_work)
    elif st.session_state.page == "home":
        render_home(all_works)
    elif st.session_state.page == "search":
        render_search(all_works)
    else:
        render_category(st.session_state.page, all_works)


if __name__ == "__main__":
    main()
