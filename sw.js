// Service Worker：离线缓存独立工具页
// 命名缓存版本，更新时改版本号即可让旧缓存失效
const CACHE = 'cz-tools-v1';
const TO_CACHE = [
  './',
  '产状测量.html',
  '无人机知识手册.html',
  '无人机学习中心.html',
  '软考学习中心.html',
  'https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js'
];

self.addEventListener('install', e=>{
  e.waitUntil(caches.open(CACHE).then(c=>c.addAll(TO_CACHE)).then(()=>self.skipWaiting()));
});

self.addEventListener('activate', e=>{
  e.waitUntil(caches.keys().then(keys=>Promise.all(
    keys.filter(k=>k!==CACHE).map(k=>caches.delete(k))
  )).then(()=>self.clients.claim()));
});

// 策略：优先缓存，缓存未命中走网络并把结果回填缓存（stale-while-revalidate）
self.addEventListener('fetch', e=>{
  const req = e.request;
  if(req.method !== 'GET') return;
  e.respondWith(
    caches.match(req).then(cached=>{
      const fetchPromise = fetch(req).then(res=>{
        // 只缓存同源或 CDN 资源的成功响应
        if(res && res.status===200 && (new URL(req.url).origin===location.origin || req.url.includes('cdn.jsdelivr.net'))){
          const copy=res.clone();
          caches.open(CACHE).then(c=>c.put(req, copy));
        }
        return res;
      }).catch(()=>cached); // 断网时返回缓存
      return cached || fetchPromise;
    })
  );
});