/* 主题增强：目录、代码复制、图片放大、懒加载、阅读进度、返回顶部 */
(function () {
  'use strict';
  var reduce = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var content = document.querySelector('.post-entry');

  // 懒加载
  function lazy(root) { if (!root) return; root.querySelectorAll('img').forEach(function (img) { img.loading = 'lazy'; img.decoding = 'async'; }); }
  lazy(content);
  document.querySelectorAll('.summary img').forEach(function (i) { i.loading = 'lazy'; i.decoding = 'async'; });

  // 宽表格包一层
  document.querySelectorAll('.post-entry table').forEach(function (tb) {
    if (tb.parentElement && tb.parentElement.classList.contains('scroll-x')) return;
    var w = document.createElement('div'); w.className = 'scroll-x';
    tb.parentNode.insertBefore(w, tb); w.appendChild(tb);
  });

  // 图片放大
  var lb = document.createElement('div'); lb.id = 'lb'; lb.innerHTML = '<img alt="">';
  document.body.appendChild(lb);
  var lbImg = lb.querySelector('img');
  document.addEventListener('click', function (e) {
    var img = e.target.closest && e.target.closest('.post-entry img');
    if (img && !img.closest('a')) { e.preventDefault(); lbImg.src = img.currentSrc || img.src; lb.classList.add('show'); return; }
    if (e.target === lb || e.target === lbImg) { lb.classList.remove('show'); lbImg.removeAttribute('src'); }
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { lb.classList.remove('show'); } });

  // 目录 + 滚动高亮
  if (content) {
    var hs = [].slice.call(content.querySelectorAll('h2, h3')).filter(function (h) { return h.textContent.trim(); });
    if (hs.length >= 3) {
      var used = {};
      hs.forEach(function (h) {
        if (!h.id) {
          var base = h.textContent.trim().toLowerCase().replace(/[^\w\u4e00-\u9fa5]+/g, '-').replace(/^-+|-+$/g, '') || 'sec';
          var id = base, n = 1; while (used[id] || document.getElementById(id)) { id = base + '-' + (++n); }
          h.id = id;
        }
        used[h.id] = 1;
        var an = document.createElement('a'); an.className = 'h-anchor'; an.href = '#' + h.id; an.textContent = '#'; an.setAttribute('aria-label', '锚点'); h.appendChild(an);
      });
      var ol = document.createElement('ol');
      hs.forEach(function (h) {
        var li = document.createElement('li'); li.className = 'toc-' + h.tagName.toLowerCase();
        var a = document.createElement('a'); a.href = '#' + h.id; a.textContent = h.textContent.trim();
        li.appendChild(a); ol.appendChild(li);
      });
      var box = document.createElement('nav'); box.className = 'toc'; box.setAttribute('aria-label', '目录');
      var title = document.createElement('div'); title.className = 'toc-title';
      title.innerHTML = '<span>目录</span><span aria-hidden="true">▾</span>';
      box.appendChild(title); box.appendChild(ol);
      content.parentNode.insertBefore(box, content);
      title.addEventListener('click', function () { box.classList.toggle('collapsed'); });
      if (window.innerWidth < 680) box.classList.add('collapsed');
      if ('IntersectionObserver' in window) {
        var links = {}; box.querySelectorAll('a').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
        var io = new IntersectionObserver(function (ents) {
          ents.forEach(function (en) { if (en.isIntersecting) { for (var k in links) links[k].classList.remove('active'); var a = links[en.target.id]; if (a) a.classList.add('active'); } });
        }, { rootMargin: '-88px 0px -70% 0px', threshold: 0 });
        hs.forEach(function (h) { io.observe(h); });
      }
    }
  }

  // 代码复制
  if (content) {
    content.querySelectorAll('pre').forEach(function (pre) {
      var btn = document.createElement('button'); btn.className = 'copy-btn'; btn.type = 'button'; btn.textContent = '复制';
      btn.addEventListener('click', function () {
        var code = pre.querySelector('code') || pre; var text = code.innerText;
        var done = function (ok) { btn.textContent = ok ? '已复制' : '失败'; if (ok) btn.classList.add('done'); setTimeout(function () { btn.textContent = '复制'; btn.classList.remove('done'); }, 1200); };
        if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); }); }
        else { var ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); done(true); } catch (e) { done(false); } document.body.removeChild(ta); }
      });
      pre.appendChild(btn);
    });
  }

  // 返回顶部 + 阅读进度
  var top = document.createElement('button'); top.id = 'to-top'; top.type = 'button'; top.title = '回到顶部'; top.setAttribute('aria-label', '回到顶部'); top.textContent = '↑'; document.body.appendChild(top);
  var bar = document.createElement('div'); bar.id = 'read-progress'; document.body.appendChild(bar);
  function onScroll() {
    var y = window.scrollY || document.documentElement.scrollTop || 0;
    top.classList.toggle('show', y > 500);
    var h = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (h > 0 ? (y / h * 100) : 0) + '%';
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  // 相关文章（按标签）
  (function () {
    var post = document.getElementById('post'); if (!post) return;
    var tags = (post.getAttribute('data-tags') || '').split(',').map(function (s) { return s.trim(); }).filter(Boolean);
    if (!tags.length) return;
    var here = ''; try { here = decodeURIComponent(location.pathname.split('/').pop() || ''); } catch (e) {}
    fetch('search.json').then(function (r) { return r.json(); }).then(function (docs) {
      var scored = docs.map(function (d) {
        if (d.u === here || !d.k) return null;
        var dt = d.k.split('|'), n = 0;
        tags.forEach(function (tg) { if (dt.indexOf(tg) >= 0) n++; });
        return n > 0 ? { d: d, n: n } : null;
      }).filter(Boolean).sort(function (a, b) { return b.n - a.n; }).slice(0, 5);
      if (!scored.length) return;
      var box = document.createElement('nav'); box.className = 'related'; box.setAttribute('aria-label', '相关文章');
      var h = document.createElement('div'); h.className = 'related-title'; h.textContent = '相关文章'; box.appendChild(h);
      var ul = document.createElement('ul');
      scored.forEach(function (x) { var li = document.createElement('li'); var a = document.createElement('a'); a.href = x.d.u; a.textContent = x.d.t; li.appendChild(a); ul.appendChild(li); });
      box.appendChild(ul);
      if (post.parentNode) post.parentNode.insertBefore(box, post.nextSibling);
    }).catch(function () {});
  })();
})();
