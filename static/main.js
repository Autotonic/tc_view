var request = new XMLHttpRequest()

request.open('GET', 'http://localhost:8000/api', true)

request.onload = function () {
  var json = JSON.parse(this.response)
  document.getElementsByTagName("body").innerText = json
}
request.send()
