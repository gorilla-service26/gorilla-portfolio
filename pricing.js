'use strict';
document.querySelectorAll('[data-price-filter]').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('[data-price-filter]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  let count = 0;
  document.querySelectorAll('[data-price-category]').forEach(group => {
    const show = button.dataset.priceFilter === 'all' || group.dataset.priceCategory === button.dataset.priceFilter;
    group.hidden = !show;
    if (show) count += group.querySelectorAll('[data-price-row]').length;
  });
  document.querySelector('#pricing-grid').classList.toggle('is-filtered', button.dataset.priceFilter !== 'all');
  document.querySelector('#price-count').textContent = `${count}メニューを表示`;
}));

document.querySelectorAll('[data-price-service]').forEach(button => button.addEventListener('click', () => {
  document.querySelector('#service').value = button.dataset.priceService;
  updateService();
  document.querySelector('#items').value = `${button.dataset.priceMenu}を相談したいです。\n掲載料金目安：${button.dataset.priceAmount}（税込・正式料金は見積もり）\n基本条件：${button.dataset.priceCondition}\n品物・数量・詳しい状況：`;
  document.querySelector('#consult').scrollIntoView({behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
  document.querySelector('#items').focus({preventScroll:true});
}));
