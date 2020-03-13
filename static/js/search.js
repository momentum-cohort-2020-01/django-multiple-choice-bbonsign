/* globals fetch */

function main () {
  allPublic()
}

function allPublic () {
  const allPubButton = q('#all-pub-btn')
  allPubButton.addEventListener('click', getAllPublicSnippets)
}

function getAllPublicSnippets (event) {
  fetch('/all-public/')
    .then(resp => resp.json())
    .then(jsonData => {
      console.log(jsonData)
      renderPreviews(jsonData.snippets)
    })
}

function renderPreviews (snippets) {
  const contentArea = q('#content')
  contentArea.innerHTML = ''
  const listContainer = document.createElement('div')
  contentArea.appendChild(listContainer)
  listContainer.classList.add('snippet-list')
  listContainer.innerHTML = ''

  for (const [id, info] of Object.entries(snippets)) {
    const preview = `<div class="snippet-item">
<a href="/snippet/${id}">
<div class="preview-title">
<h4 class="snippet-title-preview">${info.title}</h4>
<span class="preview">Preview</span>
</div>
<figure class="code-fig">
<pre class="line-numbers"><code class="lang-${info.language}" data-lang="${info.language}">${info.preview}</code>
</pre>
</figure>
</a>
</div>`
    listContainer.innerHTML += preview
  }
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
