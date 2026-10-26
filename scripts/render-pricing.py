"""Render the public tariff menu as accessible static HTML."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUPS = [
    ('single','単品','単品のリユース引取・搬出','pickup',[
        ('小型家電・小型家具','1点 / 小棚・電子レンジなど','5,500円〜'),
        ('縦型洗濯機','1台 / 1名で対応できる物','6,600円〜'),
        ('小型冷蔵庫','1台 / 170L未満・条件確認','8,800円〜'),
        ('ベッドフレーム','1台 / 解体は追加オプション','8,800円〜'),
        ('棚・タンス','1点 / 1名で対応できる物','6,600円〜')
    ],'近隣出張・現場作業30分までを含む。再使用可能品の引取相談と搬出作業が対象です。'),
    ('pack','軽バンパック','軽バンまとめてパック','pickup',[
        ('ミニパック','荷室の約1/4 / 作業45分まで','6,600円〜'),
        ('Sパック','荷室の約1/2 / 作業60分まで','9,900円〜'),
        ('Mパック','荷室の約3/4 / 作業90分まで','13,200円〜'),
        ('Lパック','軽バン1台分 / 作業120分まで','17,600円〜')
    ],'リユース対象品・荷物は仕分け済みが前提。写真で荷室・積載重量・対象品を確認します。積み放題の保証ではありません。'),
    ('transport','運搬','家具・家電の運搬','moving',[
        ('家具・家電1点','運搬5km以内 / 全作業60分まで','8,800円〜'),
        ('家具・家電2〜3点','運搬5km以内 / 全作業90分まで','13,200円〜'),
        ('軽バン1台分','運搬10km以内 / 全作業120分まで','16,500円〜'),
        ('店舗・個人宅で受取→配送','運搬5km以内 / 全作業60分まで','8,800円〜')
    ],'梱包済み・積載可能な荷量が前提。全作業時間は引取場所での作業開始からお届け完了までです。'),
    ('move','引越し','近距離の引越しサポート','moving',[
        ('少量の1Rサポート','10km以内 / 1台1行程 / 2時間まで','19,800円〜'),
        ('1R・1Kサポート','20km以内 / 1台1行程 / 3時間まで','26,400円〜'),
        ('搬出入のお手伝いだけ','1名・1時間 / 車両での運搬なし','5,500円〜')
    ],'荷造り済みの荷物が対象。間取り名だけで量は決めず、事前に荷物一覧を確認します。大型品・複数行程は別見積もりです。'),
    ('sourcing','調達','家具・家電の調達セット','sourcing',[
        ('縦型洗濯機のお探し・お届け','中古 / 4.5〜6kgの目安','13,200円〜'),
        ('小型冷蔵庫のお探し・お届け','中古 / 120〜170Lの目安','16,500円〜'),
        ('洗濯機＋冷蔵庫','中古家電2点セット','27,500円〜'),
        ('洗濯機＋冷蔵庫＋チェスト','中古の家具・家電3点セット','33,000円〜'),
        ('調達＋少量1R引越し','3点セット＋10km・2時間の引越し','49,500円〜')
    ],'中古商品代・お探し・近隣配送込み。商品条件・在庫により用意できない場合があります。設置範囲・保証は見積時に明示。引越しセットは調達・配送と引越しが各1回です。'),
    ('work','作業サポート','作業サポート','work',[
        ('家具の室内移動','同一階・1名 / 1時間まで','5,500円〜'),
        ('粗大ごみ出しのお手伝い','指定の収集場所まで / 1時間','5,500円〜'),
        ('ベッドの分解だけ','1台 / 単独出張・1時間まで','8,800円〜'),
        ('荷物の仕分け・梱包','1名 / 1時間まで・資材別','5,500円〜'),
        ('倉庫・店舗の整理サポート','1名 / 3時間まで・処分別','16,500円〜')
    ],'近隣出張込み。ごみ出しは現地での搬出作業のみ。収集の申込・指定券・処分代は別。1名で安全に扱えない物は増員を見積もります。'),
    ('options','追加料金','追加オプション','',[
        ('階段作業','大型品1点・1階分','1,100円〜'),
        ('ベッド・家具の簡易解体','他のサービスと同日・1点','3,300円〜'),
        ('家具の簡易組立','他のサービスと同日・1点','3,300円〜'),
        ('基本の作業時間超過','1名・30分ごと','2,750円'),
        ('スタッフ1名の追加','最初の1時間 / 出張含む','6,600円'),
        ('追加スタッフの時間超過','1名・30分ごと','3,300円'),
        ('遠方出張・規定距離超過','距離・所要時間で事前見積もり','個別見積もり'),
        ('有料駐車場・高速道路','必要な利用を事前確認','実費')
    ],'基本料金・パックの範囲を超える場合のみ。追加項目も事前に総額へ反映します。')
]

filters = '<button type="button" data-price-filter="all" aria-pressed="true" aria-controls="pricing-grid">すべて</button>'
cards = ''
for index, (key,label,title,service,rows,note) in enumerate(GROUPS,1):
    filters += f'<button type="button" data-price-filter="{key}" aria-pressed="false" aria-controls="pricing-grid">{label}</button>'
    table = ''
    for n,(name,condition,price) in enumerate(rows,1):
        choice = escape(price)
        if service:
            choice = f'<button type="button" class="price-choose" data-price-service="{service}" data-price-menu="{escape(name,quote=True)}" data-price-condition="{escape(condition,quote=True)}" data-price-amount="{price}" aria-label="{escape(name,quote=True)} {price}の料金目安で相談"><strong>{price}</strong><small>この内容で相談 ↗</small></button>'
        else:
            choice = f'<strong class="option-amount">{price}</strong>'
        table += f'<tr data-price-row><th scope="row">{name}<small>{condition}</small></th><td>{choice}</td></tr>'
    cards += f'<article class="price-group" data-price-category="{key}" aria-labelledby="price-{key}"><div class="price-group-title"><span>{index:02}</span><h3 id="price-{key}">{title}</h3><small>{len(rows)}メニュー</small></div><table class="price-menu-table"><caption class="sr-only">{title}の税込料金目安</caption><thead class="sr-only"><tr><th scope="col">メニュー・基本条件</th><th scope="col">税込料金目安</th></tr></thead><tbody>{table}</tbody></table><p class="price-group-note">{note}</p></article>'

block = f'''<!-- pricing:start -->
<section class="pricing-section" id="pricing" aria-labelledby="pricing-title"><div class="wrap section">
 <div class="section-heading"><div><p class="eyebrow">PRICE MENU / 全34メニュー</p><h2 id="pricing-title">依頼に合う料金を、見つけよう。</h2></div><a class="button button-small price-pdf" href="assets/gongorilla-price-menu.pdf" target="_blank" rel="noopener noreferrer">料金表PDFを見る <span aria-hidden="true">↗</span></a></div>
 <div class="pricing-intro"><span class="draft-label">料金目安・すべて税込</span><p>掲載額は、下記の基本条件での料金目安です。品物・数量・搬出入条件・距離を確認して、作業前に支払総額をご案内します。</p></div>
 <div class="pricing-basics"><strong>基本料金に含む条件</strong><p>近隣エリア・1階またはエレベーター利用・通常の搬出入経路・作業員1名。近隣は稼働拠点から片道10km以内を想定し、拠点と対象地域は見積時に明示します。</p></div>
 <div class="price-filters" role="group" aria-label="料金表の絞り込み">{filters}</div>
 <p class="price-count" id="price-count" aria-live="polite">34メニューを表示</p>
 <div class="pricing-grid" id="pricing-grid">{cards}</div>
 <div class="pricing-conditions"><div><h3>同じ作業に、単品とパックを重ねません。</h3><p>適した見積方法を1つ選びます。買取・無料引取は状態と需要により別査定。成立した買取額は了承のうえ作業総額から差し引きます。</p></div><div><h3>別途確認する費用・品物</h3><p>処分代・家電リサイクル関連費用・有料駐車場・高速料金は含みません。ドラム式・大型冷蔵庫・重量楽器・危険物などは、一律料金の対象にせず対応可否から確認します。</p></div></div>
 <p class="note price-update">料金表 v1.0 / 2026年10月27日。下の実績欄にある知人向け価格とは区別しています。</p>
</div></section>
<!-- pricing:end -->'''

path=ROOT/'index.html'; html=path.read_text()
if '<!-- pricing:start -->' in html:
    start=html.index('<!-- pricing:start -->');end=html.index('<!-- pricing:end -->')+len('<!-- pricing:end -->');html=html[:start]+block+html[end:]
else:
    html=html.replace('  <section class="cases-section"',block+'\n  <section class="cases-section"',1)
path.write_text(html)
assert sum(len(g[4]) for g in GROUPS)==34
print('Rendered 34 price rows in 7 categories')
