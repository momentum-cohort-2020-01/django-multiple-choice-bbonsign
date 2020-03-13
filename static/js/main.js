/* globals fetch */

function main () {
  addListeners()
  showDetail()
}

function addListeners () {
  const snippetPreviews = qAll('.snippet-item')
}

function showDetail (id) {

}

function q (selector) {
  return document.querySelector(selector)
}

function qAll (selector) {
  return document.querySelectorAll(selector)
}

window.addEventListener('DOMContentLoaded', main)
