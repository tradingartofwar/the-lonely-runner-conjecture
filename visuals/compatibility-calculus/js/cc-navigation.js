/* One chapter router; each chapter retains its own controls between visits. */
(() => {
  const chapters=['cap','joint','representation'];
  function navigate(){
    const hash=location.hash.slice(1),chapter=chapters.includes(hash)?hash:'cap';
    for(const id of chapters){
      const active=id===chapter;
      CC.el(`${id}-chapter`).hidden=!active;
      if(active)CC.el(`nav-${id}`).setAttribute('aria-current','page');
      else CC.el(`nav-${id}`).removeAttribute('aria-current');
    }
    document.dispatchEvent(new CustomEvent('cc:chapter',{detail:{chapter}}));
    window.scrollTo({top:0,behavior:'auto'});
  }
  window.addEventListener('hashchange',navigate);
  navigate();
})();
