'use strict';
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
const menuToggle = $('.menu-toggle');
const mobileNav = $('#mobile-nav');
function closeMenu() { mobileNav.hidden = true; menuToggle.setAttribute('aria-expanded', 'false'); menuToggle.setAttribute('aria-label', 'メニューを開く'); }
menuToggle.addEventListener('click', () => {
  const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
  mobileNav.hidden = expanded;
  menuToggle.setAttribute('aria-expanded', String(!expanded));
  menuToggle.setAttribute('aria-label', expanded ? 'メニューを開く' : 'メニューを閉じる');
});
$$('#mobile-nav a').forEach(a => a.addEventListener('click', closeMenu));
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
window.matchMedia('(min-width:901px)').addEventListener('change', e => { if (e.matches) closeMenu(); });

$$('[data-filter]').forEach(button => button.addEventListener('click', () => {
  $$('[data-filter]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  let count = 0;
  $$('[data-category]').forEach(card => {
    const show = button.dataset.filter === 'all' || card.dataset.category.split(' ').includes(button.dataset.filter);
    card.hidden = !show;
    if (show) count++;
  });
  $('#case-count').textContent = `${count}件の実績を表示`;
}));

const serviceNames = {pickup:'回収・リユース',sourcing:'家具・家電の調達',moving:'運搬・引越しサポート',work:'作業サポート',other:'まずは相談したい'};
function updateService() {
  const type = $('#service').value;
  $('#items-label').textContent = type === 'sourcing' ? '欲しい物・サイズ・用途' : type === 'moving' ? '荷物・数量・お届け先' : type === 'work' ? '作業内容・数量・ご希望' : '品物・数量・ご希望';
  $('#items').placeholder = type === 'sourcing' ? '例：一人暮らし用の冷蔵庫。幅50cm以内。年式は相談したい。' : type === 'moving' ? '例：洗濯機と棚。大阪市内から泉南市へ。' : type === 'work' ? '例：同じ階での棚の移動、段ボールの仕分けをお願いしたい。' : '例：洗濯機1台。年式は2020年。';
  $('#message-result').hidden = true;
  $('#copy-status').textContent = '';
}
$('#service').addEventListener('change', updateService);
$$('[data-service]').forEach(button => button.addEventListener('click', () => {
  $('#service').value = button.dataset.service;
  updateService();
  if (button.dataset.example) $('#items').value = button.dataset.example;
  $('#consult').scrollIntoView({behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
  $('#service').focus({preventScroll:true});
}));
$('#consult-form').addEventListener('input', () => { $('#message-result').hidden = true; $('#copy-status').textContent = ''; });
$('#consult-form').addEventListener('submit', event => {
  event.preventDefault();
  const value = (id, fallback) => $(id).value.trim() || fallback;
  const text = [
    'ゴンゴリラサービス様',
    '無料見積もり・相談をお願いします。',
    '',
    `【相談内容】${serviceNames[$('#service').value]}`,
    `【作業場所・地域】${value('#area','相談時にお伝えします')}`,
    `【品物・数量・希望】${value('#items','写真と一緒にお伝えします')}`,
    `【希望時期】${value('#date','相談したいです')}`,
    `【搬出入の状況】${value('#stairs','未確認')}`,
    `【予算】${value('#budget','相談したいです')}`,
    '',
    '対応可否、作業範囲、支払総額と内訳、追加費用の条件を教えてください。',
    '支払方法・支払時期、日程変更やキャンセルの条件も確認したいです。',
    '写真はこの後お送りします。'
  ].join('\n');
  $('#message').value = text;
  $('#message-result').hidden = false;
  $('#copy-status').textContent = '相談文ができました。コピーしてLINEに貼り付けてください。';
  $('#message').focus({preventScroll:true});
  $('#message-result').scrollIntoView({behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block:'center'});
});
$('#copy-message').addEventListener('click', async () => {
  const text = $('#message').value;
  try {
    if (!navigator.clipboard?.writeText) throw new Error('clipboard unavailable');
    await navigator.clipboard.writeText(text);
    $('#copy-status').textContent = 'コピーしました。公式LINEを開いて貼り付けてください。';
  } catch {
    $('#message').focus();
    $('#message').select();
    $('#message').setSelectionRange(0,text.length);
    $('#copy-status').textContent = '相談文を選択しました。端末の「コピー」を使ってください。';
  }
});

const dialog = $('#photo-dialog');
let lastPhotoButton;
$$('[data-photo]').forEach(button => button.addEventListener('click', () => {
  lastPhotoButton = button;
  $('#large-photo').src = button.dataset.photo;
  $('#large-photo').alt = button.dataset.caption;
  $('#photo-caption').textContent = button.dataset.caption;
  dialog.showModal();
}));
$('#close-photo').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => { if (event.target === dialog) { const b = dialog.getBoundingClientRect(); if (event.clientX < b.left || event.clientX > b.right || event.clientY < b.top || event.clientY > b.bottom) dialog.close(); } });
dialog.addEventListener('close', () => lastPhotoButton?.focus({preventScroll:true}));
