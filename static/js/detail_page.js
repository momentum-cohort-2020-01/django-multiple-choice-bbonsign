/* globals fetch, confirm */

function main () {
  new ClipboardJS('.btn');
  const copyButton = q('.btn.copy')
  const deleteButton = q('.btn.delete')
  copyButton.addEventListener('click', copyEvent)
  deleteButton.addEventListener('click', deleteEvent)

}

function copyEvent (event) {
  const copied = q('.btn.copied')
  const copy = q('.btn.copy')
  switchHidden(copied, copy)
  setTimeout(() => { switchHidden(copy, copied) }, 1500)
}

function switchHidden (hidden, visible) {
  hidden.classList.remove('hidden')
  visible.classList.add('hidden')
}

function deleteEvent (event) {
  const result = confirm('Do you want to permanently delete this snippet?')
  if (result) {
    deleteAJAX()
  }

  function deleteAJAX () {
    return fetch(`/snippet/${q('#data').dataset.id}/delete/`, { method: 'DELETE' })
      .then((resp) => {
        return resp.json()
      })
      .then(jsonResp => {
        if (jsonResp.status === 'ok') {
          q('#content').insertAdjacentHTML('afterbegin', `<div class="confirm">${jsonResp.data}</div>`)
        }
      })
      .then(() => {
        setTimeout(() => { window.location.href = '/' }, 1000)
      })
  }
}

function q (selector) {
  return document.querySelector(selector)
}

window.addEventListener('DOMContentLoaded', main)
