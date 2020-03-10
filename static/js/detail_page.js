function main () {
  console.log('hi')
  new ClipboardJS('.btn');
  const button = document.querySelector('.btn')
  button.addEventListener('click', copyEvent)
}

function copyEvent (event) {
  const copied = document.querySelector('.hidden')
  const copy = document.querySelector('.visible')
  switchHidden(copied, copy)
  setTimeout(() => { switchHidden(copy, copied) }, 1500)
  console.log('g')
}

function switchHidden (hidden, visible) {
  hidden.classList.remove('hidden')
  hidden.classList.add('visible')
  visible.classList.add('hidden')
  visible.classList.remove('visible')
}

window.addEventListener('DOMContentLoaded', main)


