/* globals fetch */

function main () {
  allPublic()
  search()
}

function search () {
  q('form.search-bar').addEventListener('submit', (e) => {
    e.preventDefault()
    getSearchResults()
  })
}

function getSearchResults () {
  const searchInput = q('#search').value
  fetch(`/search?q=${searchInput}`)
    .then(resp => resp.json())
    .then(jsonData => {
      renderPreviews(jsonData.snippets, 'Search Results')
    })
}

function allPublic () {
  const allPubButton = q('#all-pub-btn')
  allPubButton.addEventListener('click', getAllPublicSnippets)
}

function getAllPublicSnippets (event) {
  // const myHeader = new Headers()
  // myHeader.append('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest')
  fetch('/all-public/')
    .then(resp => resp.json())
    .then(jsonData => {
      renderPreviews(jsonData.snippets, 'All public snippets')
    })
}

function renderPreviews (snippets, message) {
  const contentArea = q('#content')
  contentArea.innerHTML = ''
  contentArea.insertAdjacentHTML('afterbegin', `<h2 class="user-home-title">${message}</h2>`)
  const listContainer = document.createElement('div')
  contentArea.appendChild(listContainer)
  listContainer.classList.add('snippet-list')
  listContainer.innerHTML = ''

  for (const [id, info] of Object.entries(snippets)) {
    const preview = `<div class="snippet-item">
<a href="/snippet/${id}">
<div class="preview-title">
<h4 class="snippet-title-preview">${info.title}<span class="preview">-- Author: ${info.owner}</span></h4>
<span class="preview">Preview</span>
</div>
<figure class="code-fig">
<pre class="line-numbers"><code class="lang-${info.language}" data-lang="${info.language}" id="snip${info.id}"></code>
</pre>
</figure>
</a>
</div>`
    listContainer.innerHTML += preview
    q(`#snip${info.id}`).textContent = info.code
  }
  // window.history.pushState('/', 'All public snippets', '?all-public')
  reloadPrism()
}

function reloadPrism () {
  const oldScript = q('#prism-js')
  oldScript.remove()
  const tag = document.createElement('script')
  tag.id = 'prism-js'
  tag.src = '/static/js/prism.js'
  q('head').appendChild(tag)
}

function q (selector) {
  return document.querySelector(selector)
}

window.addEventListener('DOMContentLoaded', main)
