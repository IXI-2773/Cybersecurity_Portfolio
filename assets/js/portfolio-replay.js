/* Finite, user-controlled playback. No automatic restart after visibility changes. */
(function(root){
  'use strict';
  function createReplay({count,intervalMs=1200,onChange,element,scheduler=root}){
    if(!Number.isInteger(count)||count<1||typeof onChange!=='function')throw new TypeError('Replay needs a count and onChange');
    let index=0,timer=null,disposed=false;
    const media=root.matchMedia?root.matchMedia('(prefers-reduced-motion: reduce)'):null;
    const emit=()=>onChange(index,timer!==null);
    function stop(){if(timer!==null)scheduler.clearInterval(timer);timer=null;}
    function pause(){stop();if(!disposed)emit();}
    function select(value){if(disposed)return;stop();index=Math.max(0,Math.min(count-1,Math.trunc(value)||0));emit();}
    function advance(){index=Math.min(index+1,count-1);if(index===count-1)stop();emit();}
    function play(){if(disposed||timer!==null)return;if(media&&media.matches){step();return;}if(index===count-1)index=0;timer=scheduler.setInterval(advance,intervalMs);emit();}
    function step(){if(disposed)return;stop();advance();}
    function reset(){select(0);}
    const visibility=()=>{if(root.document.hidden)pause();};
    const reduced=()=>{if(media.matches)pause();};
    if(root.document)root.document.addEventListener('visibilitychange',visibility);
    if(media&&media.addEventListener)media.addEventListener('change',reduced);
    let observer;
    if(element&&root.IntersectionObserver){observer=new root.IntersectionObserver(entries=>{if(!entries[0].isIntersecting&&timer!==null)pause();});observer.observe(element);}
    function dispose(){stop();disposed=true;if(observer)observer.disconnect();if(root.document)root.document.removeEventListener('visibilitychange',visibility);if(media&&media.removeEventListener)media.removeEventListener('change',reduced);}
    emit();return {play,pause,step,reset,select,dispose};
  }
  root.PortfolioReplay={createReplay};if(typeof module!=='undefined')module.exports={createReplay};
})(globalThis);
