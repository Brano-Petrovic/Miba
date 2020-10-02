function unhide(val){
	if (val=="vlastne"){
		document.getElementById("vlastne_obdobie").hidden = false;
		document.getElementById("ciara1").style.marginTop = "78px";
	}
	else{	
		document.getElementById("vlastne_obdobie").hidden = true;
		document.getElementById("ciara1").style.marginTop = "13px";
	}
}



function removeAllOptions(){
    var select = document.getElementById("area_select");
    select.options.length = 0;
}

function removeOption(){
	var select = document.getElementById("Produnit_select");
	select.options[select.options.length] = null;
}

function addOption(option, value){
    var select = document.getElementById("area_select");
    select.options[select.options.length] = new Option(option, value);
}



function PUareas(PU, area){
    if (PU == "FIP1" || PU == "FIP2")
        {PU = "FIP";}

    switch(PU){
		case "PU1":
            removeAllOptions()
            addOption("Lisovanie", "Lisovanie");
            addOption("Tepelné opracovanie", "Tepelné opracovanie");
            addOption("Kalibrovanie", "Kalibrovanie");
            break;
		case "PU2":
            removeAllOptions()
            addOption("Lisovanie", "Lisovanie")
            addOption("Tepelné opracovanie", "Tepelné opracovanie")
            addOption("Kalibrovanie", "Kalibrovanie")
            addOption("Mechanické opracovanie", "Mechanické opracovanie")
			break;
		case "PU3":
            removeAllOptions()
            addOption("Mechanické opracovanie 1", "Mechanické opracovanie 1")
            addOption("Mechanické opracovanie 2", "Mechanické opracovanie 2")
			break;
		case "PU4":
            removeAllOptions()
            addOption("Celá jednotka", "Celá jednotka")
            break;
        case "FIP":
            removeAllOptions()
            addOption("Konečná kontrola a balenie PU1", "Konečná kontrola a balenie PU1")
            addOption("Konečná kontrola a balenie PU2", "Konečná kontrola a balenie PU2")
            break;
    }

    var select = document.getElementById('area_select');
    var option;

    
    for (var i=1; i<select.length; i++) {
        option = select.options[i];

        if (option.value == area) {
            option.selected = true;
        }
    } 

    select = document.getElementById('Produnit_select');
    for (var i=1; i<select.length; i++) {
        option = select.options[i];

        if (option.value == PU) {
            option.selected = true;
        }
    } 

}
