/* globals fetch */

function main () {
  allPublic()
}

function allPublic () {
  const allPubButton = document.querySelector('#all-pub-btn')
  allPubButton.addEventListener('click', getAllPublicSnippets)
}

function getAllPublicSnippets (event) {
  fetch('all-public/')
    .then(resp => resp.json())
    .then(jsonData => {
      console.log(jsonData)
    })
}


window.addEventListener('DOMContentLoaded', main)
