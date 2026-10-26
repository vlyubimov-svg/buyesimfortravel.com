(function(){
  var t=document.querySelector('.nav-toggle'),n=document.querySelector('.nav');
  if(t&&n){t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o)})}
  var p=document.querySelector('.progress'),b=document.querySelector('.back-top');
  function onScroll(){
    var h=document.documentElement,max=h.scrollHeight-h.clientHeight;
    if(p)p.style.width=(max>0?(h.scrollTop/max*100):0)+'%';
    if(b)b.classList.toggle('show',h.scrollTop>900);
  }
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();
  if(b)b.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'})});
  var links=[].slice.call(document.querySelectorAll('.toc a'));
  if(links.length&&'IntersectionObserver' in window){
    var map={};links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.remove('active')});var a=map[e.target.id];if(a)a.classList.add('active')}})},{rootMargin:'-20% 0px -70% 0px'});
    Object.keys(map).forEach(function(id){var el=document.getElementById(id);if(el)io.observe(el)});
  }
})();
(function(){
  // Plan finder: route + daily use + days -> plan type (thresholds from the site's fact base)
  document.querySelectorAll('[data-finder]').forEach(function(box){
    var c=box.querySelector('select[name=countries]'),g=box.querySelector('input[name=gb]'),d=box.querySelector('input[name=days]'),
        gv=box.querySelector('[data-gb]'),dv=box.querySelector('[data-days]'),out=box.querySelector('.tool-out');
    function run(){
      var n=parseInt(c.value,10),gb=parseFloat(g.value),days=parseInt(d.value,10),title,body;
      gv.textContent=gb.toFixed(1)+' GB/day';dv.textContent=days+(days===1?' day':' days');
      var total=Math.ceil(gb*days*1.2);
      if(gb<1.5){
        title='Fixed plan';
        body='<p>About '+total+' GB for the trip with a 20% buffer. Under roughly 1.5 to 2 GB a day, a fixed plan usually costs less than unlimited.</p>'+
             (n>=3?'<p>With three or more countries, pick a regional fixed plan and check every country is on its list.</p>':'<p>One main country: a single-country fixed plan is enough.</p>');
      }else if(n>=3){
        title='Regional unlimited';
        body='<p>Several borders and a high daily use point to a regional unlimited plan. Compare the 5 GB per day plans in the ranking, and check the hotspot rule if you tether.</p>';
      }else{
        title='Single-country unlimited';
        body='<p>One or two countries and above 1.5 GB a day: a single-country unlimited plan is usually the cheaper route. Add a small fixed plan for a side trip.</p>'+
             (gb>=3?'<p>Above 3 GB a day, a 1 GB full-speed allowance will run out early. Look at plans with a larger daily allowance.</p>':'');
      }
      out.innerHTML='<span class="big">'+title+'</span>'+body;
    }
    box.addEventListener('input',run);run();
  });
})();
