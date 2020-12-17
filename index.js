fetch("/api.php?data=raw").then(Response => Response.json()).then(data => {
  fetch("/api.php?data=avg_lastweek").then(Response => Response.text()).then(avglastweek => {
      var sum = 0;
      for(var x in data) { sum += data[x] > 0 ? 1 : 0; }

      var sumToday = 0;
      for(var x in data) {
          var dataDay = new Date(x * 1000).getDay();
          var currentDay = new Date().getDay();
          if(dataDay == currentDay) {
              sumToday += data[x] > 0 ? 1 : 0;
          }
      }


      var processed_data = []
      for(var x in data) {
          var timestamp = new Date(x * 1000);
          var h = timestamp.getHours();
          var v = data[x];
          processed_data.push({h, v});
      }

      var breakdown_data = [];
      var breakdown_label = [];
      var hourCounter = processed_data[0]["h"];
      var sumCounter = 0
      for(var x in processed_data) {
          if(processed_data[x]["h"] != hourCounter) {
              breakdown_data.push(sumCounter);
              breakdown_label.push(hourCounter + "h");
              hourCounter = processed_data[x]["h"];
              sumCounter = 0;
          }
          if(processed_data[x]["v"] > 0) sumCounter++;
      }
      breakdown_data.push(sumCounter);
      breakdown_label.push(hourCounter + "h");

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

      new Chart(document.getElementById("chart"), {
          type: 'bar',
          data: {
            labels: breakdown_label,
            datasets: [
              {
                label: "Ivott mennyiseg",
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
