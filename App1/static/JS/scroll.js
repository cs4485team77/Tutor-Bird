const pContainer = document.querySelector(".p_container");
const p2 = pContainer.querySelector(".p2");

window.addEventListener('scroll', () => {
  if (window.scrollY >= window.innerHeight) {
    p2.style.animationPlayState = 'paused';
  } else {
    p2.style.animationPlayState = 'running';
  }
});




