// Create Element.remove() function if not exist
if (!('remove' in Element.prototype)) {
  Element.prototype.remove = function () {
      if (this.parentNode) {
          this.parentNode.removeChild(this);
      }
  };
}

$(function() {
  $("#showResults").on("click", function() {
    var pu = $("#Produnit_select option:selected").val();
    var area = $("#area_select option:selected").val();
    var range = $("#obdobie_id option:selected").val();
    var od_mesiac =$("#od_mesiac option:selected").val();
    var od_rok =$("#od_rok").val();
    var do_mesiac = $("#do_mesiac option:selected").val();
    var do_rok =$("#do_rok").val();
  
    $.ajax({
      url: "/vykonane_audity",
       type: "POST",
       data: {
         "pu": pu,
         "area": area,
         "range": range,
         "od_rok": od_rok,
         "od_mesiac": od_mesiac,
         "do_rok": do_rok,
         "do_mesiac": do_mesiac,
       },
       success: function (data) {
         console.log("success");
         if (kontrola()==true){
           return;
         }
            
         
         
         data = JSON.parse(data);

         var resultMachines = [];
         var resultData = [];
         for(var i = 0; i < data.length-2; i++) {
           resultMachines.push(data[i].machine);
           resultData.push(data[i].result);           
         }

          
          document.getElementById("mibaSinterSlovakia").innerHTML = 'Audity '+pu+' - '+area;          
          document.getElementById("grafContainer").hidden = false;          
          document.getElementById("bar-chart").remove();
          document.getElementById("grafContainer").innerHTML = '<div style="display:block;"><h4>Počet</h4> <h4 style="color:rgb(192,0,0);"> vykonaných auditov*</h4> <h4>na jednotlivých pracoviskách</h4></div><canvas id="bar-chart" height="550px"></canvas>';
          document.getElementById("poznamka").hidden = false;

          // Bar chart
          Chart.defaults.global.elements.rectangle.borderWidth = 4;
          Chart.defaults.global.elements.rectangle.borderColor = '#fcc000';
          Chart.defaults.global.defaultFontColor = 'black';
          Chart.defaults.global.defaultFontSize = 13;
          new Chart(document.getElementById("bar-chart"), {
            
            type: 'bar',
            data: {
              labels: resultMachines,
              
              datasets: [
                {
                label: "Počet auditov",
                backgroundColor: 'rgba(0,32,96,0.8)',
                data: resultData,
                }
              ]
            },
            
            options: {
              maintainAspectRatio: false,
              scales: {
                xAxes: [{
                  ticks: {
                    autoSkip: false,
                    maxRotation: 90,
                    minRotation: 0,
                    stepSize:1
                  },
                  beginAtZero: true,
                  gridLines:{
                    display:false,
                    color:'#e7e6e6',
                  }
                  
                }],

                yAxes: [{
                  ticks:{
                    max: data[data.length-1].pocet_smien,
                    min: 0,
                    callback: function(value, index, values) {
                      if (Math.floor(value) === value) {
                          return value;
                      }
                    }
                  },
                  beginAtZero: true,
                  gridLines:{
                    display:true,
                    color:'rgb(178,178,178)',
                  }
                  
                }]
              },
              
              legend: { 
                display: false,
                label: {
                  fontColor: 'black',
                }
              },
              title: {
                  display: true,
                  text: ''
              },				
              
            }
          });
          

          if (data[data.length-2].average!="nie_su_udaje"){

            document.getElementById("meterContainer").hidden = false;
            document.getElementById("ciara2").hidden = false;
            document.getElementById("cvs").remove();
            document.getElementById("meterContainer").innerHTML = '<div style="display:block;"><h4>Percento</h4> <h4 style="color:rgb(192,0,0);">vykonaných auditov*</h4> <h4>pracovísk z celkového možného počtu</h4></div><canvas id="cvs" width="600px" height="450"></canvas>';
  
            // Meter chart
            // https://www.rgraph.net/demos/meter-black.html
            Chart.defaults.global.defaultFontColor = 'black';
            var canvas  = document.getElementById("cvs");
            var context = canvas.getContext('2d');         
            context.scale(0.7, 0.7);
            
            new RGraph.Meter({
              id: 'cvs',
              min: 0,
              max: 100,
              value:data[data.length-2].average,
              
              options: {
                scaleUnitsPost:'%',
                // radius: 250,            
                adjustable: true,
                anglesStart: RGraph.PI - 0.5,
                anglesEnd: RGraph.TWOPI + 0.5,
                centery: 300,
                linewidthSegments: 5,
                textSize: 17,
                textColor: 'black',
                colorsGreenColor: '#0a0',
                segmentsRadiusStart: 200,
                border: false,
                colorsStroke: 'white',
                tickmarksSmallCount: 0,
                tickmarksLargeCount: 0,
                needleRadius: 200,
                needleColor: 'gray',
                textValign: 'bottom',
                centerpinFill: 'white',
                centerpinStroke: 'gray',
                colorsRanges: [
                  [0,10,'Gradient(#f00:#f00:#c00:#300)'],
                  [10,20,'Gradient(#f00:#f00:#c00:#300)'],
                  [20,30,'Gradient(#f00:#f00:#c00:#300)'],
                  [30,40,'Gradient(#ffa:#ff0:#cc0:#330)'],
                  [40,50,'Gradient(#ffa:#ff0:#cc0:#330)'],
                  [50,60,'Gradient(#afa:#0f0:#0c0:#030)'],
                  [60,70,'Gradient(#afa:#0f0:#0c0:#030)'],
                  [70,80,'Gradient(#afa:#0f0:#0c0:#030)'],
                  [80,90,'Gradient(#afa:#0f0:#0c0:#030)'],
                  [90,100,'Gradient(#afa:#0f0:#0c0:#030)']
                ]
              }
            }).draw();
          }
          else{
            document.getElementById("meterContainer").hidden = true;
            document.getElementById("ciara2").hidden = true;
          }
       }
     });
  });
});


function kontrola() {
  var today = new Date();
  var mm = today.getMonth() + 1; //January is 0!
  var yyyy = today.getFullYear();

  if(document.getElementById("obdobie_id").value == "vlastne"){
 
    if ((Number(document.getElementById("od_rok").value) > yyyy) || (Number(document.getElementById("do_rok").value) > yyyy)  || (Number(document.getElementById("od_rok").value)==yyyy && (Number(document.getElementById("od_mesiac").value)) > Number(mm)) || (Number(document.getElementById("do_rok").value)==yyyy && (Number(document.getElementById("do_mesiac").value)) > Number(mm))){
      alert("Zadali ste nesprávny dátum. Zadaný dátum je budúcnosť.");
      document.getElementById("meterContainer").hidden = true;
      document.getElementById("grafContainer").hidden = true;
      document.getElementById("ciara2").hidden = true;
      return true;
    }
    
    if (Number(document.getElementById("od_rok").value) > Number(document.getElementById("do_rok").value)){
      alert("Zadali ste nesprávny rok. Zadané roky sú naopak.");
      document.getElementById("meterContainer").hidden = true;
      document.getElementById("grafContainer").hidden = true;
      document.getElementById("ciara2").hidden = true;
      return true;
    }
      
      
    if (Number(document.getElementById("od_rok").value) == Number(document.getElementById("do_rok").value))
      if (Number(document.getElementById("od_mesiac").value) > Number(document.getElementById("do_mesiac").value)){
        document.getElementById("meterContainer").hidden = true;
        document.getElementById("grafContainer").hidden = true;
        document.getElementById("ciara2").hidden = true;
        alert("Zadali ste nesprávny mesiac. Zadané mesiace sú naopak."); 
        return true;
      } 
  }
}