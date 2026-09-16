import { menuPages, IMAGE_WIDTH, IMAGE_HEIGHT } from "@/data/menu-pages";

function absolute(url: string) {
  if (typeof window === "undefined") return url;
  return new URL(url, window.location.origin).href;
}

export function buildMenuHtml() {
  const items = menuPages
    .map(
      (p, i) => `    <figure id="${p.id}">
      <img src="${absolute(p.url)}" alt="${p.title} — ${p.subtitle}" width="${IMAGE_WIDTH}" height="${IMAGE_HEIGHT}" ${i === 0 ? 'fetchpriority="high"' : 'loading="lazy" decoding="async"'} />
    </figure>`,
    )
    .join("\n");

  return `<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Menu Kantin Inyong — Umaeh Inyong Purwokerto</title>
<style>
  :root { color-scheme: light; }
  body { margin:0; background:#faf5ea; font-family: system-ui, -apple-system, sans-serif; }
  main { display:flex; flex-direction:column; gap:12px; padding:12px; max-width:720px; margin:0 auto; }
  figure { margin:0; opacity:0; transform:translateY(12px); transition:opacity .5s ease, transform .5s ease; }
  figure.in { opacity:1; transform:none; }
  img { width:100%; height:auto; display:block; border-radius:14px; }
  @media (prefers-reduced-motion: reduce){ figure{opacity:1;transform:none;transition:none} }
</style>
</head>
<body>
<main>
${items}
</main>
<script>
  var els = document.querySelectorAll('figure');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target);} });
    }, { rootMargin: '80px' });
    els.forEach(function(el){ io.observe(el); });
  } else { els.forEach(function(el){ el.classList.add('in'); }); }
</script>
</body>
</html>`;
}

export function downloadMenuHtml() {
  const blob = new Blob([buildMenuHtml()], { type: "text/html;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "menu-kantin-inyong.html";
  a.click();
  URL.revokeObjectURL(url);
}
