/*$.ajaxSetup({
    cache: false
});

$(function() {
    setTimeout(setBoxHeight, 2000);

    $( window ).resize(function() {
        setBoxHeight();
    });
	
    var gaugeValue = 0;
	
	writeDate();
	setInterval(writeDate, 5000);

    // pri nacitani stranky sa zavola metoda transfer
    transfer('{{ hodnotenie|tojson|safe }}');
	
    setInterval(transfer, 5000);
    // bary sa nastavia az po 7 sekundach, aby sa zobrazili spravne percenta
    setTimeout(setBars, 7000);

    setGauge(gaugeValue);
});

var oldShiftCol;
var oldGaugeValue = 0;
var oldAllWidthsOfMonth = [];

/*
    metoda, v ktorej sa prijimaju a spracuvavaju data prijate cez JSON
*/
function transfer(data, tab) {
    
		

        // pole zmien a indikatorov
		
		var firstThreeLettersFromPU = "PU1";
		
		if(firstThreeLettersFromPU === "FIP") {
			var shifts = ["A_PU1", "B_PU1", "A_PU2", "B_PU2"];
		} else {
			var shifts = ["A", "B", "C", "D"];
		}
        
        //var performanceIndicators = ["QUAL", "PERF", "EHS", "SAU", "ATT"];

        // cyklus prejde vsetky zmeny, v kazdej zmene prejde vsetky indikatory,
        // vytvori sa nazov indikatora zhodneho s tym, ktory prichadza cez JSON,
        // metodou eval (ak je nejaky sposob, bolo by najlepsie ju nahradit) sa
        // ulozi farba do premennej smile_color, vytvori sa cela cesta k obrazku
        // a nasledne sa konkretnemu td priradi konkretny obrazok
        /*console.log('{{ hodnotenie[1]|tojson|safe }}')
        for(var i = 0; i < shifts.length; i++) {
            for(var j = 0; j < performanceIndicators.length; j++) {
                var nameOfPerfInd = performanceIndicators[j] + "_" + shifts[i];
                var smileColor = eval("data." + nameOfPerfInd);
                var src = imgSrcStart + smileColor + imgSrcEnd;
                $("#" + nameOfPerfInd + "_smile").attr("src", src); 
            }
        }

        // v mesacnom hodnoteni sa zobrazi mesiac, ktory pride cez JSON 
        $("#mesacneHodnotenieMesiac").html(data.Month);*/

        // pole sirok vsetkych mesacnych barov
        var allWidthsOfMonth = [];
        //var tab = 1;
        // cyklus prejde vsetky zmeny, kde nastavi bar diagramy pre vsetky indikatory
        // a vsetky percenta pre tieto bary
        // (ak je nejaky sposob, treba zmenit metodu eval)
		// metoda zaroven vyfarbi percenta podla zadaneho minima, ak je pocet percent
        // mensi ako minimum, farba je cervena, inak zelena
        
		for(var i = 0; i < shifts.length; i++) {
            var w = eval("data.QU_" + shifts[i]);
            if (w == -1) w = 0;
			$("#mesacneHodnotenie1-" + shifts[i]+"-tab"+tab).width(Math.ceil(w) + "%");
            colorPercentage("mesacneHodnotenie1-" + shifts[i] + "_td-tab"+tab, w, 90);
            allWidthsOfMonth.push(w);
            document.getElementById("mesacneHodnotenie1-" + shifts[i] + "_td-tab"+tab).innerHTML = Math.ceil(w)+"%";


            w = eval("data.PE_" + shifts[i]);
            if (w == -1) w = 0;
			$("#mesacneHodnotenie2-" + shifts[i]+"-tab"+tab).width(Math.ceil(w) + "%");
            colorPercentage("mesacneHodnotenie2-" + shifts[i] + "_td-tab"+tab, w, 90);
            allWidthsOfMonth.push(w);
            document.getElementById("mesacneHodnotenie2-" + shifts[i] + "_td-tab"+tab).innerHTML = Math.ceil(w)+"%";

            w = eval("data.EH_" + shifts[i]);
            if (w == -1) w = 0;
			$("#mesacneHodnotenie3-" + shifts[i]+"-tab"+tab).width(Math.ceil(w) + "%");
            colorPercentage("mesacneHodnotenie3-" + shifts[i] + "_td-tab"+tab, w, 90);
            allWidthsOfMonth.push(w);
            document.getElementById("mesacneHodnotenie3-" + shifts[i] + "_td-tab"+tab).innerHTML = Math.ceil(w)+"%";

            w = eval("data.SA_" + shifts[i]);
            if (w == -1) w = 0;
			$("#mesacneHodnotenie4-" + shifts[i]+"-tab"+tab).width(Math.ceil(w) + "%");
            colorPercentage("mesacneHodnotenie4-" + shifts[i] + "_td-tab"+tab, w, 90);
            allWidthsOfMonth.push(w);
            document.getElementById("mesacneHodnotenie4-" + shifts[i] + "_td-tab"+tab).innerHTML = Math.ceil(w)+"%";

            w = eval("data.AT_" + shifts[i]);
            if (w == -1) w = 0;
			$("#mesacneHodnotenie5-" + shifts[i]+"-tab"+tab).width(Math.ceil(w) + "%");
            colorPercentage("mesacneHodnotenie5-" + shifts[i] + "_td-tab"+tab, w, 90);
            allWidthsOfMonth.push(w);
            document.getElementById("mesacneHodnotenie5-" + shifts[i] + "_td-tab"+tab).innerHTML = Math.ceil(w)+"%";			
        } 
        

        // prejde cele pole sirok mesacnych barov, ak sa nejaka hodnota zmenila, tak 
        // prekresli bary aj percenta, aby boli zobrazene korektne
        /*for (var i = 0; i < allWidthsOfMonth.length; i++) {
            if(oldAllWidthsOfMonth[i] != allWidthsOfMonth[i]){
                setBars();
                oldAllWidthsOfMonth = allWidthsOfMonth;
            }
        }*/
        
		
		//*************************************************************************************
}

function setGauge(gaugeValue) {
    $("#gauge").dxCircularGauge({
        scale: {
            startValue: 0,
            endValue: 100,
            tickInterval: 10,
            label: {
                customizeText: function (arg) {
                    return arg.valueText + " %";
                }
            }
        },
        rangeContainer: {
            ranges: [
                { startValue: 0, endValue: 50, color: "rgb(192, 0, 0)" }, // "#CE2029"
                { startValue: 50, endValue: 80, color: "rgb(255, 192, 0)" }, // "#FFD700"
                { startValue: 80, endValue: 100, color: "rgb(84, 130, 53)" }  // "#228B22"
            ]
        },
        "export": {
            enabled: false
        },
        title: {
            text: "Stav auditovania",
            font: { size: 25 }
        },
        value: gaugeValue
    });
}

/*
    pre kazdy bar sa zanimuje prechod z 0 na pocet percent, ktory je spravny
    prechod trva 1,2 sekundy 
    po 1,2 sekundach sa zobrazia percenta pre kazdy bar
*/
function setBars() {
    $(".meter > span").each(function() {
        $(this)
            .data("origWidth", $(this).width())
            .width(0)
            .animate({
                width: $(this).data("origWidth")
            }, 1200);
    });

		setTimeout(writePercentage, 1200);
}

function writePercentage() {
    var zmeny = ["A", "B", "C", "D"];
    var indicatorsNumbers = [1, 2, 3, 4, 5];

    for(var i = 0; i < zmeny.length; i++) {
        for(var j = 1; j < indicatorsNumbers.length + 1; j++) {
            var name = "#mesacneHodnotenie" + j + "-" + zmeny[i];
            var bar = $(name);
            var percentage = Math.ceil(bar.width() / bar.parent().width() * 100);
            $(name + "_td").html(percentage + "%");
        }
    }
}

function writePercentageFip() {
    var zmeny = ["A_PU1", "B_PU1", "A_PU2", "B_PU2"];
    var indicatorsNumbers = [1, 2, 3, 4, 5];

    for(var i = 0; i < zmeny.length; i++) {
        for(var j = 1; j < indicatorsNumbers.length + 1; j++) {
            var name = "#mesacneHodnotenie" + j + "-" + zmeny[i];
            var bar = $(name);
            var percentage = Math.ceil(bar.width() / bar.parent().width() * 100);
            $(name + "_td").html(percentage + "%");
        }
    }
}

/*
    metoda si vypyta datum, ak su hodiny, minuty, den alebo datum jednocifrove, tak nastavi prvu 
    cifru na 0, nasledne takto upraveny cas zobrazi
*/
function writeDate() {
    var d = new Date();

    var hours;
    (d.getHours() < 10) ? hours = "0" + d.getHours() : hours = d.getHours();

    var min;
    (d.getMinutes() < 10) ? min = "0" + d.getMinutes() : min = d.getMinutes();

    var dd;
    (d.getDate() < 10) ? dd = "0" + d.getDate() : dd = d.getDate();

    var mm;
    ((d.getMonth() + 1) < 10) ? mm = "0" + (d.getMonth() + 1) : mm = d.getMonth() + 1;
	
    $("#hhmm").html(hours + ":" + min);
    $("#ddmmyyyy").html(dd + "." + mm + "." + d.getFullYear());
}

function colorPercentage(id, percentage, min) {
	if(percentage < min) {
		$("#" + id).css("color", "red");
	} else {
		$("#" + id).css("color", "green");
	}
}

function setBoxHeight() {
	var boxHeight = $("#aktualne_pracovne_zmenyBox").height();
	$("#initPartBox").height(boxHeight);
    $("#mesacneHodnotenieBox").height(boxHeight);

    // var firstRowWidth = $("#initPartBox").width() +  $("#aktualne_pracovne_zmenyBox").width() + $("#mesacneHodnotenieBox").width() - 20;
    // $("#aktProblemyBox").width(firstRowWidth);
    // console.log(firstRowWidth);
}
