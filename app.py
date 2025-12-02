import re, frontmatter, mistletoe as mst
from collections import Counter
from datetime import datetime
from fasthtml.common import *
from fastlite import *
from monsterui.all import *
from urllib.parse import quote, unquote

hdrs = (*Theme.slate.headers(highlightjs=True),
        Link(rel="icon", href="/static/favicon.ico"),
        Script(src="https://unpkg.com/hyperscript.org@0.9.12"),
        Link(rel="preconnect", href="https://fonts.googleapis.com"), Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        Link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono&display=swap"),
        Style("body { font-family: 'IBM Plex Sans', sans-serif; } code, pre { font-family: 'IBM Plex Mono', monospace; }"))

app = FastHTML(hdrs=hdrs)
app.mount("/static", StaticFiles(directory="static"), name="static")
rt = app.route

db = database("data/subscribers.db")
class Subscriber: id:int; email:str; created_at:str
subscribers = db.create(Subscriber, transform=True)

def theme_toggle():
    return Button(UkIcon("moon", cls="dark:hidden"), UkIcon("sun", cls="hidden dark:block"),
        _="""on click
                toggle .dark on <html/>
                set franken to (localStorage's __FRANKEN__ or '{}') as Object
                if the first <html/> matches .dark set franken's mode to 'dark' else set franken's mode to 'light' end
                set localStorage's __FRANKEN__ to franken as JSON""",
        cls="p-1 hover:scale-110 shadow-none", type="button")

def x_icon(): return Svg(ft_hx("path", d="M12.6.75h2.454l-5.36 6.142L16 15.25h-4.937l-3.867-5.07-4.425 5.07H.316l5.733-6.57L0 .75h5.063l3.495 4.633L12.601.75Zm-.86 13.028h1.36L4.323 2.145H2.865z"), width=20, height=20, fill="currentColor", viewBox="0 0 16 16", aria_hidden="true")

def social_link(k, v):
    ext = dict(rel="nofollow noindex") if k == "mail" else {} if k == "rss" else dict(target="_blank", rel="noopener noreferrer")
    return A(x_icon() if k == "twitter" else UkIcon(k, width=20, height=20), href=v, aria_label=k.title(), cls="hover:text-primary transition-colors", **ext)

socials = dict(github="https://github.com/jackhogan", twitter="https://x.com/j_h0gan", linkedin="https://www.linkedin.com/in/hogan-jack/", rss="/rss.xml", mail="/contact")
ftr_content = Div(*[social_link(k,v) for k,v in socials.items()], cls="flex justify-center gap-6 text-muted-foreground")

def hx_attrs(target="#main-content"): return dict(hx_target=target, hx_push_url="true", hx_swap="innerHTML show:window:top")

def hx_link(txt, href, cls="text-primary underline", target="#main-content", **kw):
    return A(txt, href=href, hx_get=href, cls=cls, **hx_attrs(target), **kw)

def navbar():
    menu_id,btn_id = f"menu-{unqid()}",f"btn-{unqid()}"
    brand = A(Img(src="/static/images/pixelated_portrait.png", alt="Jack Hogan", cls="w-6 h-6 rounded-full"), Span("Jack Hogan"), href="/", hx_get="/", cls="flex items-center gap-2 text-lg font-bold", **hx_attrs())
    def navlinks(_=None): return [hx_link(txt, f"/{txt.lower()}", cls="hover:scale-110", _=_) for txt in ["About", "Blog", "Now"]]
    hamburger = Button(UkIcon("menu", width=30, height=30), cls="p-0 border-0 shadow-none", _=f"on click toggle .hidden on #{menu_id}", type="button", id=btn_id)
    return Nav(cls="border rounded-lg shadow backdrop-blur-md bg-background/98")(
            Div(brand, Div(*navlinks(), theme_toggle(), cls="hidden md:flex items-center space-x-4 ml-auto"),
                Div(theme_toggle(), hamburger, cls="flex md:hidden items-center gap-4 ml-auto"), cls="flex items-center p-4"),
            Div(*navlinks(_=f"on click add .hidden to #{menu_id}"), cls="flex flex-col space-y-4 p-4 text-center hidden", id=menu_id, _=f"on click elsewhere if event.target.closest('#{btn_id}') is null add .hidden to me")
    )

def layout(*content, htmx, title=None):
    if htmx and htmx.request: return (Title(title), *content)
    main = Main(*content, cls='w-full max-w-2xl mx-auto px-6 py-8 space-y-8', id="main-content")
    ctr_cls = 'w-full max-w-2xl mx-auto'
    return Title(title), Div(cls="flex flex-col min-h-screen")(
        Div(navbar(), cls=f'{ctr_cls} px-4 sticky top-0 z-50 mt-4'),
        main,
        Footer(Divider(), ftr_content, cls=f'{ctr_cls} px-6 mt-auto mb-6')
    )

class Post:
    def __init__(self, path):
        self.path,self.slug                         = (p := Path(path)),p.stem
        self.content,self.meta                      = (post := frontmatter.load(path)).content,post.metadata
        self.title,self.date,self.excerpt,self.tags = self.meta['title'],self.meta['date'],self.meta.get('excerpt',''),L(self.meta.get('tags', []))
        self.datestr                                = self.date.strftime('%d %b %Y')
        self.external_url                           = self.meta.get('external_url')

def get_posts(n=None):
    if not (posts_dir := Path('posts')).exists(): return []
    posts = posts_dir.ls(file_exts='.md').map(Post).sorted(key=lambda p: p.date, reverse=True)
    return posts[:n] if n else posts

def tag_pill(tag, selected=None, avail=None, link=False):
    base = "text-xs px-2 py-1 rounded border transition-all"
    if tag is None:
        return ft_hx("button", UkIcon("x", width=12, height=12), "Clear", cls=f"{base} flex items-center gap-1 cursor-pointer hover:shadow-sm", **hx_attrs("#posts-list"), hx_get="/blog")
    if selected is None:
        if not link: return Span(tag, cls=f"{base} bg-muted")
        url = f"/blog?tags={quote(tag)}"
        hx = hx_attrs() if link == True else hx_attrs("#posts-list")
        return A(tag, href=url, cls=f"{base} bg-muted hover:bg-primary/20", hx_get=url, **hx)
    new = ','.join(quote(t) for t in selected ^ {tag})
    url = f"/blog?tags={new}" if new else "/blog"
    hx = hx_attrs("#posts-list")
    if tag in selected: return A(tag, href=url, cls=f"{base} bg-primary cursor-pointer text-primary-foreground", hx_get=url, **hx)
    if avail and tag in avail: return A(tag, href=url, cls=f"{base} cursor-pointer bg-muted hover:bg-primary/20", hx_get=url, **hx)
    return Span(tag, cls=f"{base} opacity-30 cursor-not-allowed")

def tag_filter(selected, all_posts, filtered):
    counts = Counter(all_posts.attrgot('tags').concat())
    if not counts: return Div(id="tag-filter")
    avail = set(filtered.attrgot('tags').concat())
    tags = sorted(counts, key=lambda t: (-counts[t], t))
    btns = [tag_pill(t, selected, avail) for t in tags]
    if selected: btns.append(tag_pill(None))
    return Div(Span("Filter:", cls="text-sm font-medium mr-1"), *btns, cls="border-b pb-4 flex flex-wrap items-center gap-2", id="tag-filter")

def post_card(p):
    date_and_tags = Div(Span(p.datestr, cls="text-sm text-muted-foreground"),
                        Div(*p.tags.map(partial(tag_pill, link='htmx')), cls="flex gap-2 flex-wrap"),
                        cls="flex justify-between items-center")
    content = Div(H3(hx_link(p.title, blogpost.to(slug=p.slug), cls="")), P(p.excerpt, cls="text-muted-foreground leading-relaxed"), date_and_tags,
                  cls='space-y-2 border-b -mb-4 pb-4 group-hover:border-transparent transition-all')
    return Li(content, hx_get=blogpost.to(slug=p.slug), hx_trigger="click[!event.target.closest('a') && !getSelection().toString()]",
              cls="group p-4 -mx-4 hover:rounded-lg hover:shadow-md transition-all cursor-pointer", **hx_attrs())

def subscribe_form():
    return Div(
        P("Subscribe via ", A("RSS", href="/rss.xml", cls="text-primary underline"), " or enter your email to get notified of new posts directly in your inbox", cls="text-sm text-muted-foreground mb-2"),
        Form(Input(type="email", name="email", placeholder="your@email.com", required=True, cls="flex-1 rounded-l-md"), Button("Subscribe", cls=(ButtonT.primary, "rounded-l-none rounded-r-md")), cls="flex", hx_post="/subscribe", hx_swap="outerHTML"),
        cls="mt-6")

def blog_section():
    if not (posts := get_posts(3)): return Div()
    def item(p): return Div(hx_link(p.title, blogpost.to(slug=p.slug), cls="hover:underline font-medium"), Span(p.datestr, cls="text-muted-foreground text-sm whitespace-nowrap"), cls="flex justify-between items-baseline gap-4 py-2 border-b")
    return Section(Div(H3("Latest Posts", cls="text-2xl font-semibold"), hx_link("View all →", blog), cls="flex justify-between items-baseline mb-4"), *posts.map(item), subscribe_form(), cls="border rounded-lg shadow bg-muted p-4")

def work_item(role, org, years, logo_light, logo_dark=None):
    logo_dark = logo_dark or logo_light
    img_cls = "w-6 h-6 rounded object-contain"
    imgs = (Img(src=f"/static/images/logos/{logo_light}", alt=org, cls=f"{img_cls} dark:hidden"),
            Img(src=f"/static/images/logos/{logo_dark}", alt=org, cls=f"{img_cls} hidden dark:block"))
    return Div(Div(*imgs, Span(org, cls="font-medium"), cls="flex items-center gap-2"),
               Div(Span(role, cls="text-muted-foreground text-sm"),
                   Span(cls="flex-1 border-b border-dotted"),
                   Span(years, cls="text-muted-foreground text-sm whitespace-nowrap"), cls="flex items-baseline gap-2"),
               cls="flex flex-col gap-1 py-2")

def work_section():
    roles = [("Founding AI Research Scientist", "Agemo AI", "2024–2025", "codewords_dark.png", "codewords_light.png"),
             ("Co-founder and CEO", "Shoji", "2020–2022", "shoji_dark.png", "shoji_light.png"),
             ("PhD Statistical Machine Learning", "Imperial College London", "2017–2023", "imperial.png")]
    return Section(
        H3("Work", cls="text-2xl font-semibold mb-4"),
        *[work_item(*r) for r in roles],
        P("Check out my ", hx_link("About", about), " page or my ", A("CV", href="/static/CV_Jack_Hogan.pdf", cls="text-primary underline", target="_blank"), " for more details.", cls="text-sm text-muted-foreground mt-4")
    )

def intro():
    return Article(
        H3("Welcome", cls="text-2xl font-semibold mb-4"),
        Div(cls="text-base text-muted-foreground leading-relaxed space-y-4")(
            P("I'm an AI research scientist based in London, UK."),
            P("This website is both an excuse to teach myself web development and part of an effort to write more, as a way of solidifying and sharing my thoughts about the topics that interest me. It will most likely cover machine learning, software engineering, startups and entrepreneurship; we'll see what else."),
            P("To learn more about me, check out my ", hx_link("About", about), " page. ",
            "See my latest blog posts below or find the full list on my ", hx_link("Blog", blog), " page. ",
            "Or to find out what I'm up to ", Em("right now"), ", check out my ", hx_link("Now", now), " page."),
        )
    )

def span_token(name, pat, attr, prec=5):
    class T(mst.span_token.SpanToken):
        precedence,parse_inner,parse_group,pattern = prec,False,1,re.compile(pat)
        def __init__(self, match): setattr(self, attr, match.group(1))
    T.__name__ = name
    return T

FootnoteRef = span_token('FootnoteRef', r'\[\^([^\]]+)\](?!:)', 'target')
YoutubeEmbed = span_token('YoutubeEmbed', r'\[yt:([a-zA-Z0-9_-]+)\]', 'video_id', 6)

def extract_footnotes(content):
    pat = re.compile(r'^\[\^([^\]]+)\]:\s*(.+?)(?=(?:^|\n)\[\^|\n\n|\Z)', re.MULTILINE | re.DOTALL)
    defs = {m.group(1): m.group(2).strip() for m in pat.finditer(content)}
    for m in pat.finditer(content): content = content.replace(m.group(0), '', 1)
    return content.strip(), defs

class ContentRenderer(FrankenRenderer):
    def __init__(self, *extras, img_dir=None, footnotes=None, **kwargs):
        super().__init__(*extras, img_dir=img_dir, **kwargs)
        self.footnotes,self.fn_counter = footnotes or {},0
    
    def render_footnote_ref(self, token):
        self.fn_counter += 1
        n,target = self.fn_counter,token.target
        content = self.footnotes.get(target, f"[Missing footnote: {target}]")
        rendered = mst.markdown(content, partial(ContentRenderer, img_dir=self.img_dir)).strip()
        if rendered.startswith('<p>') and rendered.endswith('</p>'): rendered = rendered[3:-4]
        style = "text-sm leading-relaxed border-l-2 border-amber-400 dark:border-blue-400 pl-3 text-neutral-500 dark:text-neutral-400 transition-all duration-500 w-full my-2 xl:my-0"
        toggle_hs = f"on click if window.innerWidth >= 1280 then add .hl to #sn-{n} then wait 1s then remove .hl from #sn-{n} else toggle .open on me then toggle .show on #sn-{n}"
        ref = Span(id=f"snref-{n}", role="doc-noteref", aria_label=f"Sidenote {n}", cls="sidenote-ref cursor-pointer", _=toggle_hs)
        note = Span(NotStr(rendered), id=f"sn-{n}", role="doc-footnote", aria_labelledby=f"snref-{n}", cls=f"sidenote {style}")
        hide = lambda c: to_xml(Span(c, cls="hidden", aria_hidden="true"))
        return hide(" (") + to_xml(ref) + to_xml(note) + hide(")")
    
    def render_youtube_embed(self, token):
        iframe = Iframe(src=f"https://www.youtube.com/embed/{token.video_id}", title="YouTube video player", frameborder="0",
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share",
                        referrerpolicy="strict-origin-when-cross-origin", allowfullscreen=True, cls="w-full aspect-video rounded-lg my-6")
        return to_xml(iframe)
    
    def render_link(self, token):
        href,inner,title = token.target,self.render_inner(token),f' title="{token.title}"' if token.title else ''
        is_internal = href.startswith('/') and not href.startswith('//') and '.' not in href.split('/')[-1]
        hx = f' hx-get="{href}" hx-target="#main-content" hx-push-url="true" hx-swap="innerHTML show:window:top"' if is_internal else ''
        ext = '' if is_internal else ' target="_blank" rel="noopener noreferrer"'
        return f'<a href="{href}"{hx}{ext} class="text-primary underline"{title}>{inner}</a>'

sidenote_css = Style("""
.sidenote-ref { 
    color: rgb(221, 166, 55); background-color: rgba(221, 166, 55, 0.15);
    display: inline-block; transition: transform 0.2s;
    font-size: 0.6rem; vertical-align: top; line-height: 1;
    padding: 0 0.15rem; border-radius: 0.2rem; margin-left: 0.1rem;
}
.sidenote-ref:after { content: "›"; }
.dark .sidenote-ref { color: rgb(96, 165, 250); background-color: rgba(96, 165, 250, 0.15); }
.sidenote { display: none; }
@media (max-width: 1279px) {
    .sidenote-ref:after { content: "⌃"; }
    .sidenote-ref { transform: rotate(180deg); }
    .sidenote-ref.open { transform: rotate(0deg); }
    .sidenote.show { display: block; float: left; clear: both; width: 95%; margin: 0.75rem 2.5%; position: relative; }
}
@media (min-width: 1280px) {
    .sidenote { display: block; float: right; clear: right; width: 14rem; margin-right: -16rem; margin-top: 0.25rem; margin-bottom: 0.75rem; }
    .sidenote.hl { background-color: rgba(221, 166, 55, 0.1); }
    .dark .sidenote.hl { background-color: rgba(96, 165, 250, 0.1); }
}
""")

def from_md(content, img_dir='/static/images'):
    content, footnotes = extract_footnotes(content)
    mods = {'pre': 'border border-gray-300 rounded-md my-4', 'p': 'text-base leading-relaxed mb-6', 'li': 'text-base leading-relaxed',
            'ul': 'uk-list uk-list-bullet space-y-2 mb-6 ml-6 text-base', 'ol': 'uk-list uk-list-decimal space-y-2 mb-6 ml-6 text-base', 'hr': 'border-t border-border my-8'}
    rendered = render_md(content, class_map_mods=mods, img_dir=img_dir, renderer=partial(ContentRenderer, FootnoteRef, YoutubeEmbed, footnotes=footnotes))
    return Div(sidenote_css, rendered, cls="w-full")

@rt
def index(htmx): return layout(intro(), blog_section(), work_section(), title="Jack Hogan - Home", htmx=htmx)

@rt
def about(htmx):
    content = Path('content/about.md').read_text()
    _, body_md = content.split('\n', 1)
    img = Img(src="/static/images/portrait.jpg", alt="Jack Hogan", cls="w-2/5 md:w-1/3 float-left mr-4 md:mr-6 mb-4 rounded-lg")
    return layout(H2("About"), Div(img, from_md(body_md)), title="Jack Hogan - About", htmx=htmx)

@rt
def now(htmx):
    post = frontmatter.load('content/now.md')
    updated = post.metadata.get('updated')
    updated_str = updated.strftime('%B %d, %Y') if updated else None
    content = re.sub(r'^#\s+.+\n', '', post.content, count=1)
    header = Div(H2("Now"), Span(f"Last updated: {updated_str}", cls="text-sm text-muted-foreground") if updated_str else None, cls="flex justify-between items-baseline")
    return layout(header, from_md(content), title="Jack Hogan - Now", htmx=htmx)

@rt
def blog(htmx, tags:str=None):
    selected = {unquote(t.strip()) for t in (tags or '').split(',') if t.strip()}
    all_posts = get_posts()
    filtered = all_posts.filter(lambda p: selected <= set(p.tags))
    posts_content = Ul(*filtered.map(post_card), cls="list-none") if filtered else Div(P("No posts found matching those tags.", cls="text-muted-foreground"), cls="py-8 text-center")
    posts_div = Div(posts_content, id="posts-list")
    tag_filt = tag_filter(selected, all_posts, filtered)
    if htmx and htmx.target == "posts-list":
        tag_filt.attrs['hx-swap-oob'] = 'true'
        return posts_div, tag_filt
    return layout(H2("Blog"), tag_filt, posts_div, subscribe_form(), title="Jack Hogan - Blog", htmx=htmx)

@rt('/blog/{slug}')
def blogpost(htmx, slug:str):
    post_path = Path('posts') / f'{slug}.md'
    if not post_path.exists(): return layout(H1("Post Not Found", cls="text-4xl font-bold mb-4"), P("Sorry, this blog post doesn't exist."), title="Post Not Found", htmx=htmx)
    p = Post(post_path)
    if p.external_url: return Response(headers={"HX-Redirect": p.external_url})
    content = re.sub(r'^#\s+.+\n', '', p.content, count=1)
    tags = Div(*p.tags.map(partial(tag_pill, link=True)), cls="flex gap-2 flex-wrap") if p.tags else None
    return layout(Article(H1(p.title, cls="text-3xl font-bold mb-3"),
                          Div(Span(p.date.strftime("%B %d, %Y"), cls="text-muted-foreground text-sm"), tags, cls="flex justify-between items-center mb-8 flex-wrap gap-4"),
                          from_md(content, img_dir=f'/static/images/posts/{slug}'), cls="mb-8"),
                  title=f"Jack Hogan - {p.title}", htmx=htmx)

@rt
def subscribe(email:str):
    if list(subscribers.rows_where("email = ?", [email], limit=1)): return P("You're already subscribed!", cls="text-sm text-muted-foreground mt-6")
    subscribers.insert(Subscriber(email=email, created_at=datetime.now().isoformat()))
    return P("Thanks for subscribing!", cls="text-sm text-green-600 mt-6")

@rt('/rss.xml')
def rss_feed():
    base,posts = "https://jackhogan.net",get_posts()
    def item(p): return f"<item><title>{p.title}</title><link>{base}/blog/{p.slug}</link><guid>{base}/blog/{p.slug}</guid><pubDate>{p.date.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate><description><![CDATA[{p.excerpt}]]></description>{''.join(f'<category>{t}</category>' for t in p.tags)}</item>"
    items = ''.join(item(p) for p in posts if not p.external_url)
    rss = f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>Jack Hogan</title><link>{base}</link><description>AI research, software engineering, startups and more</description><language>en-us</language><lastBuildDate>{posts[0].date.strftime('%a, %d %b %Y %H:%M:%S +0000') if posts else ""}</lastBuildDate><atom:link href="{base}/rss.xml" rel="self" type="application/rss+xml"/>{items}</channel></rss>'
    return Response(rss, media_type="application/rss+xml")

@rt
def contact(): return RedirectResponse(f'mailto:{os.environ.get('EMAIL')}', status_code=302)

serve()
