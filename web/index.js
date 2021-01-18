fetch("/api.php?data=raw").then(Response => Response.json()).then(data => {
  fetch("/api.php?data=avg_lastweek").then(Response => Response.text()).then(avglastweek => {
      var sum = Object.keys(data).length;


      //Calculate how much was drank today
      var sumToday = 0;
      for(var x in data) {
          var dataDay = new Date(x * 1000).getDay();
          var currentDay = new Date().getDay();
          if(dataDay == currentDay) {
              sumToday += data[x] > 0 ? 1 : 0;
          }
      }


      //Process data so that chartjs can make a nice chart out of it
      var processed_data = []
      var hours = []
      for(var x in data) {
        var h = new Date(x * 1000).getHours();
        var v = data[x]
        processed_data.push({h,v});
        if(!hours.includes(h.toString())) {
          hours.push(h.toString())
        }
      }

      var breakdown_label = [];
      ts = Date.now() + 3600000
      indx = 0;
      for(var i = 0; i < 24; i++) {
        breakdown_label[indx] = new Date(ts).getHours().toString()
        ts += 3600000
        indx++
      }

      var breakdown_data = new Array(24).fill(0)
      for(x in processed_data) {
        var pos = ind(breakdown_label, processed_data[x]["h"].toString())
        breakdown_data[pos] += 1
      }

      //Update values
      var _avgLastWeek = parseFloat(avglastweek);
      document.getElementById("today").innerHTML = sumToday;
      document.getElementById("last24h").innerHTML = sum;
      document.getElementById("avg24h").innerHTML = _avgLastWeek.toFixed(0);
      if(sum > _avgLastWeek) {
        var val = (((sum / _avgLastWeek) * 100) - 100).toFixed(1);
        document.getElementById("avg24hchange").innerHTML = "+" + val + "%";
        if(val > 15) {
          document.getElementById("avg24hchange").style.color = "#58bf5a";
        }
      }
      else {
        var val = ((_avgLastWeek - sum) / _avgLastWeek * 100).toFixed(1);
        document.getElementById("avg24hchange").innerHTML = "-" + val + "%";
        if(val > 15) {
          document.getElementById("avg24hchange").style.color = "#b34640";
        }
      }

      //Draw chart
      new Chart(document.getElementById("chart"), {
          type: 'bar',
          data: {
            labels: breakdown_label,
            datasets: [
              {
                label: "Amount Drank",
                backgroundColor: "#21719c",
                data: breakdown_data
              }
            ]
          },
          options: {
            legend: { display: false }
          }
      });
  });
});

//Built-in function returned incorrect values in some scenarios
function ind(arr, val) {
  for(var i = 0; i < arr.length; i++) {
    if(arr[i] == val) {
      return i;
    }
  }
}