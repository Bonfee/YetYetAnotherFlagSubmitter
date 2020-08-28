// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';



var init_data;
var xhr = new XMLHttpRequest();
xhr.open("GET", "../dispatching_ajax", false);
xhr.send(null); 
 if (xhr.status === 200) {
     init_data= JSON.parse(xhr.responseText);
    } else {
      console.error(xhr.statusText);
    };

 // Pie Chart Example
var ctx = document.getElementById("myPieChart");
 document.getElementById("pieRecap").innerHTML = "<b>U</b>: " + init_data.unsubmitted + ", <b>S</b>: "+ init_data.submitted + ", <b>F</b>: "+ init_data.failed + ", <b>P</b>: "+ init_data.pending;
 var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ["Unsubmitted","Submitted", "Failed", "Pending"],
    datasets: [{
      data: [init_data.unsubmitted,init_data.submitted, init_data.failed, init_data.pending],
      backgroundColor: ['#4c61ff','#056517', '#d21e1e', '#ff9800'],
      hoverBackgroundColor: [ '#6778f8','#3f8f29', '#f04141', '#ffcc00'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});


setInterval(function(){
var xhr = new XMLHttpRequest();
xhr.open("GET", "../dispatching_ajax", true);
xhr.onload = function (e) {
  if (xhr.readyState === 4) {
    if (xhr.status === 200) {
     dispatcher_json= JSON.parse(xhr.responseText);
   data=[dispatcher_json.unsubmitted,dispatcher_json.submitted, dispatcher_json.failed, dispatcher_json.pending]
    myPieChart.data.datasets[0].data = data;
   myPieChart.update()
   document.getElementById("pieRecap").innerHTML = "<b>U</b>: " + dispatcher_json.unsubmitted + ", <b>S</b>: "+ dispatcher_json.submitted + ", <b>F</b>: "+ dispatcher_json.failed + ", <b>P</b>: "+ dispatcher_json.pending;
     
    } else {
      console.error(xhr.statusText);
    }
  }
};
xhr.onerror = function (e) {
  console.error(xhr.statusText);
};
xhr.send(null); 
}, 2000)

