# app.py
import streamlit as st
from data import Work, SAMPLE_WORKS, get_work_by_id, get_works_by_category

st.set_page_config(
    page_title="百合收藏馆 | 女同作品推荐",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 样式设置 ---
st.markdown("""
<style>
    .main > div {
        padding: 1rem 2rem;
    }
    .st-emotion-cache-1y4p8pa {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        font-family: 'Noto Sans SC', sans-serif;
    }
    .work-card {
        background-color: #f8f0f6;
        border: 1px solid #e0d4e0;
        border-radius: 15px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .work-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    }
    .work-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .work-meta {
        color: #7a6b7a;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    .work-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.3rem;
        margin: 0.5rem 0;
    }
    .work-tag {
        background-color: #e8dce8;
        color: #4a3a4a;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
    }
    .work-rating {
        font-weight: bold;
        color: #d4a0a0;
    }
    .work-platforms {
        margin-top: 0.8rem;
        padding-top: 0.5rem;
        border-top: 1px dashed #e0d4e0;
    }
    .work-platform-link {
        background-color: #e8dce8;
        color: #4a3a4a;
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        text-decoration: none;
        margin-right: 0.3rem;
    }
    .work-platform-link:hover {
        background-color: #d4a0a0;
        color: white;
    }
    .stButton button {
        background-color: #d4a0a0;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1.5rem;
        transition: background-color 0.2s;
    }
    .stButton button:hover {
        background-color: #c08080;
    }
    .platform-section {
        background-color: #f0e8f0;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
    }
    .platform-section h4 {
        color: #4a3a4a;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 辅助函数 ---
def display_work_card(work):
    """显示单个作品的卡片"""
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            # 占位图，后续可以替换为实际图片URL
            st.image("https://via.placeholder.com/150x200/FAEBD7/000000?text=📖", width=150)
        with col2:
            st.markdown(f"<div class='work-title'>{work.title}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='work-meta'>🖊️ {work.author} | ⭐ <span class='work-rating'>{work.rating}</span> | 📅 {work.year if work.year else '未知'} | 🏷️ {work.category}</div>", unsafe_allow_html=True)
            tags_html = "".join([f"<span class='work-tag'>#{tag}</span>" for tag in work.tags])
            st.markdown(f"<div class='work-tags'>{tags_html}</div>", unsafe_allow_html=True)
            st.write(work.description[:120] + ("..." if len(work.description) > 120 else ""))
            
            # 显示观看渠道（如果有的话）
            if work.platforms:
                platforms_html = "<div class='work-platforms'>📺 可观看于: "
                for platform, url in list(work.platforms.items())[:2]:  # 最多显示2个
                    platforms_html += f"<a href='{url}' target='_blank' class='work-platform-link'>{platform}</a> "
                platforms_html += "</div>"
                st.markdown(platforms_html, unsafe_allow_html=True)
            
            if st.button("查看详情", key=f"detail_{work.id}"):
                st.session_state.selected_work = work
                st.rerun()

def show_work_detail(work):
    """显示作品详情页"""
    st.title(work.title)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://via.placeholder.com/300x450/FAEBD7/000000?text=📖", width=300)
    with col2:
        st.markdown(f"**作者：** {work.author}")
        st.markdown(f"**分类：** {work.category}")
        st.markdown(f"**评分：** ⭐ **{work.rating}**")
        st.markdown(f"**年份：** {work.year if work.year else '未知'}")
        tags_html = "".join([f"<span class='work-tag'>#{tag}</span>" for tag in work.tags])
        st.markdown(f"**标签：** <div class='work-tags'>{tags_html}</div>", unsafe_allow_html=True)
        
        # 显示观看渠道
        if work.platforms:
            st.markdown("---")
            st.markdown("### 📺 观看渠道")
            platforms_html = "<div class='platform-section'>"
            platforms_html += "<h4>以下平台可观看此作品：</h4>"
            for platform, url in work.platforms.items():
                platforms_html += f"<p>🔗 <a href='{url}' target='_blank'><strong>{platform}</strong></a></p>"
            platforms_html += "</div>"
            st.markdown(platforms_html, unsafe_allow_html=True)
        else:
            st.info("💡 暂时没有收录此作品的观看渠道，如果你知道，欢迎在评论区补充！")
    
    st.markdown("---")
    st.markdown("**作品简介：**")
    st.write(work.description)
    
    if st.button("← 返回列表"):
        st.session_state.pop("selected_work", None)
        st.rerun()

def render_sidebar():
    """渲染侧边栏"""
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
        search_query = st.text_input("输入作品名/关键词", placeholder="例如：夏日限定")
        if search_query:
            st.session_state.search_query = search_query
            st.session_state.page = "search"
            st.session_state.pop("selected_work", None)
            st.rerun()
        st.markdown("---")
        st.markdown("### 筛选")
        st.session_state.filter_rating = st.slider("最低评分", 0.0, 10.0, 0.0, 0.1)
        all_tags = set()
        for work in SAMPLE_WORKS:
            all_tags.update(work.tags)
        st.session_state.filter_tags = st.multiselect("选择标签", sorted(all_tags))
        if st.button("清除筛选", use_container_width=True):
            st.session_state.filter_rating = 0.0
            st.session_state.filter_tags = []
            st.rerun()
    return search_query

def render_home():
    """渲染首页"""
    st.title("🌸 百合收藏馆")
    st.markdown("> 欢迎来到百合收藏馆！这里为你精心整理了女同题材的优秀作品，涵盖文学、影视和动漫。")
    st.markdown("---")
    
    # 首页展示三个分类的推荐
    cols = st.columns(3)
    categories = ["文学", "影视", "动漫"]
    for i, col in enumerate(cols):
        with col:
            st.subheader(f"📚 {categories[i]}")
            works = get_works_by_category(categories[i])[:3]  # 各取前3部
            for work in works:
                display_work_card(work)

def render_category(category):
    """渲染分类页面"""
    st.title(f"📚 {category}作品")
    works = get_works_by_category(category)
    
    if not works:
        st.info("该分类下暂时没有作品，请管理员添加。")
        return
    
    # 应用筛选
    if st.session_state.get("filter_rating", 0.0) > 0:
        works = [w for w in works if w.rating >= st.session_state.filter_rating]
    if st.session_state.get("filter_tags", []):
        works = [w for w in works if any(tag in w.tags for tag in st.session_state.filter_tags)]
    
    if not works:
        st.info("没有找到符合条件的作品，请尝试调整筛选条件。")
        return
    
    st.write(f"共找到 {len(works)} 部作品")
    col1, col2 = st.columns(2)
    for index, work in enumerate(works):
        with col1 if index % 2 == 0 else col2:
            display_work_card(work)

def render_search():
    """渲染搜索结果页面"""
    query = st.session_state.get("search_query", "")
    st.title(f"🔍 搜索结果：\"{query}\"")
    
    if not query:
        st.info("请输入关键词进行搜索。")
        return
    
    matched_works = [w for w in SAMPLE_WORKS if w.title and query.lower() in w.title.lower()]
    
    if not matched_works:
        st.info(f"没有找到与 \"{query}\" 相关的作品。")
        st.markdown("💡 **建议：**")
        st.markdown("- 检查关键词拼写是否正确")
        st.markdown("- 尝试使用更通用的关键词")
        st.markdown("- 浏览分类页面查看所有作品")
        return
    
    st.write(f"共找到 {len(matched_works)} 部作品")
    for work in matched_works:
        display_work_card(work)

def render_detail():
    """渲染详情页"""
    if st.session_state.get("selected_work"):
        show_work_detail(st.session_state.selected_work)
    else:
        st.warning("请从列表中选择一部作品查看详情。")
        if st.button("返回首页"):
            st.session_state.page = "home"
            st.rerun()

# --- 主路由 ---
def main():
    # 初始化session_state
    if "page" not in st.session_state:
        st.session_state.page = "home"
        st.session_state.search_query = ""
        st.session_state.selected_work = None
        st.session_state.filter_rating = 0.0
        st.session_state.filter_tags = []
    
    render_sidebar()
    
    # 页面路由
    if st.session_state.selected_work:
        render_detail()
    elif st.session_state.page == "home":
        render_home()
    elif st.session_state.page == "search":
        render_search()
    else:
        render_category(st.session_state.page)

if __name__ == "__main__":
    main()