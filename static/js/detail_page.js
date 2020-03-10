function main () {
  console.log('hi')
  new ClipboardJS('.btn');
  const button = document.querySelector('.btn')
  button.addEventListener('click', copyEvent)
}

function copyEvent (event) {
  const copied = document.querySelector('.hidden')
  const copy = document.querySelector('.visible')
  switchHidden(hidden = copied, visible = copy)
  setTimeout(() => { switchHidden(hidden=copy, visible=copied) }, 1000)
  console.log('g')
}

function switchHidden (hidden, visible) {
  hidden.classList.remove('hidden')
  hidden.classList.add('visible')
  visible.classList.add('hidden')
  visible.classList.remove('visible')
}

window.addEventListener('DOMContentLoaded', main)


