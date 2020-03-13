/* globals fetch */

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
  let confirmHTML
  if (q('.confirm') == null) {
    confirmHTML = `
    <div class="confirm">
    Are you sure you want to permenently delete this snippet?
    <button class="btn delete confirm">
      Yes
    </button>
    <button class="btn cancel">
      Cancel
    </button>
  </div>`
  }
  else {
    confirmHTML = ''
  }

  q('#content').insertAdjacentHTML('afterbegin', confirmHTML)
  q('.btn.delete.confirm').addEventListener('click', deleteAJAX)
  q('.btn.cancel').addEventListener('click', cancelDelete)
  function cancelDelete (e) {
    q('.confirm').remove()
  }

  function deleteAJAX (e) {
    return fetch(`/snippet/${q('#data').dataset.id}/delete/`, { method: 'DELETE' })
      .then((resp) => {
        console.log(resp.json())
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
