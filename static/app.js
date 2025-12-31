const sid = window.serviceId

function showLoader(show=true){
  document.getElementById("loader").style.display = show?"block":"none"
}

function refreshAll(){
  showLoader(true)

  fetch("/api/logs/"+sid)
    .then(r=>r.json())
    .then(d=>{
      document.getElementById("logs").innerText = d.join("\n")
    })

  fetch("/api/metrics/"+sid)
    .then(r=>r.json())
    .then(m=>{
      cpu.data.datasets[0].data.push(m.cpu||0)
      ram.data.datasets[0].data.push(m.memory||0)
      cpu.update(); ram.update()
      showLoader(false)
    })
}

setInterval(refreshAll,5000)
