function kontrola() {

	if (Number(document.getElementById("od_rok").value) > Number(document.getElementById("do_rok").value))
		alert("Zadali ste nesprávny rok. Zadané roky sú naopak.");
    
    
    if (Number(document.getElementById("od_rok").value) == Number(document.getElementById("do_rok").value))
        if (Number(document.getElementById("od_mesiac").value) > Number(document.getElementById("do_mesiac").value))
            alert("Zadali ste nesprávny mesiac. Zadané mesiace sú naopak.");            		
    }

function farba(data, IdElem) {	
	if (data == "[]")
		document.getElementById(IdElem).style.backgroundColor="#00d300"; 
	  	else
			document.getElementById(IdElem).style.backgroundColor="red"; 
	}

function vyber(t){
	switch(t){
		case "aktualny_mesiac":
			document.getElementById("obdobie").innerHTML = "Od začiatku aktuálneho mesiaca";
			document.getElementById("obdobie").value = "aktualny_mesiac";
		  	break;
		case "mesiac":
			document.getElementById("obdobie").innerHTML = "Posledný uzavretý mesiac";
			document.getElementById("obdobie").value = "mesiac";
			break;
		case "kvartal":
			document.getElementById("obdobie").innerHTML = "Posledný uzavretý obchodný kvartál";
			document.getElementById("obdobie").value = "kvartal";
			break;
		case "polrok":
			document.getElementById("obdobie").innerHTML = "Posledný uzavretý obchodný polrok";
			document.getElementById("obdobie").value = "polrok";
			break;
		case "rok":
			document.getElementById("obdobie").innerHTML = "Posledný uzavretý obchodný rok";
			document.getElementById("obdobie").value = "rok";
			break;
		case "vlastne":
			document.getElementById("obdobie").innerHTML = "Vlastné obdobie";
			document.getElementById("obdobie").value = "vlastne";
			break;
		default:
			document.getElementById("obdobie").innerHTML = "Od začiatku aktuálneho mesiaca";
			document.getElementById("obdobie").value = "aktualny_mesiac";
			break;
	}
}

function zobrazenie(PU){
	console.log(PU)
	switch(PU){
		case "PU1":
			document.getElementById("area4").hidden = true;
			document.getElementById("area8").hidden = true;

			document.getElementById("tab_audit_popis1").className = "tab_audit_popisPU1 bold";
			document.getElementById("tab_audit_status1").className = "tab_audit_statusPU1 bold";
			document.getElementById("tab_audit_datum1").className = "tab_audit_datumPU1 bold";
			$('.auditor').attr("class", "tab_audit_popisPU1 bold");
			$('.status').attr("class", "tab_audit_statusPU1 bold");
			$('.datum').attr("class", "tab_audit_datumPU1 bold");
			break;

		case "PU2":
			document.getElementById("tab_audit_popis1").className = "tab_audit_popisPU2 bold";
			document.getElementById("tab_audit_status1").className = "tab_audit_statusPU2 bold";
			document.getElementById("tab_audit_datum1").className = "tab_audit_datumPU2 bold";
			$('.auditor').attr("class", "tab_audit_popisPU2 bold");
			$('.status').attr("class", "tab_audit_statusPU2 bold");
			$('.datum').attr("class", "tab_audit_datumPU2 bold");
			break;

		case "PU3":
			document.getElementById("area3").hidden = true;
			document.getElementById("area4").hidden = true;
			document.getElementById("area7").hidden = true;
			document.getElementById("area8").hidden = true;

			document.getElementById("tab_audit_popis1").className = "tab_audit_popisPU3 bold";
			document.getElementById("tab_audit_status1").className = "tab_audit_statusPU3 bold";
			document.getElementById("tab_audit_datum1").className = "tab_audit_datumPU3 bold";
			$('.auditor').attr("class", "tab_audit_popisPU3 bold");
			$('.status').attr("class", "tab_audit_statusPU3 bold");
			$('.datum').attr("class", "tab_audit_datumPU3 bold");
			break;
		case "PU4":
			document.getElementById("area2").hidden = true;
			document.getElementById("area3").hidden = true;
			document.getElementById("area4").hidden = true;
			document.getElementById("area6").hidden = true;
			document.getElementById("area7").hidden = true;
			document.getElementById("area8").hidden = true;

			document.getElementById("tab_audit_popis1").className = "tab_audit_popisPU4 bold";
			document.getElementById("tab_audit_status1").className = "tab_audit_statusPU4 bold";
			document.getElementById("tab_audit_datum1").className = "tab_audit_datumPU4 bold";
			$('.auditor').attr("class", "tab_audit_popisPU4 bold");
			$('.status').attr("class", "tab_audit_statusPU4 bold");
			$('.datum').attr("class", "tab_audit_datumPU4 bold");
			break;
		case "FIP":
			document.getElementById("area2").hidden = true;
			document.getElementById("area3").hidden = true;
			document.getElementById("area4").hidden = true;
			document.getElementById("area6").hidden = true;
			document.getElementById("area7").hidden = true;
			document.getElementById("area8").hidden = true;

			document.getElementById("tab_audit_popis1").className = "tab_audit_popisPU4 bold";
			document.getElementById("tab_audit_status1").className = "tab_audit_statusPU4 bold";
			document.getElementById("tab_audit_datum1").className = "tab_audit_datumPU4 bold";
			$('.auditor').attr("class", "tab_audit_popisPU4 bold");
			$('.status').attr("class", "tab_audit_statusPU4 bold");
			$('.datum').attr("class", "tab_audit_datumPU4 bold");
			
			document.getElementById("shift_bar_1").innerHTML = "PU1 A";
			document.getElementById("shift_bar_2").innerHTML = "PU1 B";
			document.getElementById("shift_bar_3").innerHTML = "PU2 A";
			document.getElementById("shift_bar_4").innerHTML = "PU2 B";
			document.getElementById("shift_bar_5").innerHTML = "PU1 A";
			document.getElementById("shift_bar_6").innerHTML = "PU1 B";
			document.getElementById("shift_bar_7").innerHTML = "PU2 A";
			document.getElementById("shift_bar_8").innerHTML = "PU2 B";
			document.getElementById("shift_bar_9").innerHTML = "PU1 A";
			document.getElementById("shift_bar_10").innerHTML = "PU1 B";
			document.getElementById("shift_bar_11").innerHTML = "PU2 A";
			document.getElementById("shift_bar_12").innerHTML = "PU2 B";
			document.getElementById("shift_bar_13").innerHTML = "PU1 A";
			document.getElementById("shift_bar_14").innerHTML = "PU1 B";
			document.getElementById("shift_bar_15").innerHTML = "PU2 A";
			document.getElementById("shift_bar_16").innerHTML = "PU2 B";
			document.getElementById("shift_bar_17").innerHTML = "PU1 A";
			document.getElementById("shift_bar_18").innerHTML = "PU1 B";
			document.getElementById("shift_bar_19").innerHTML = "PU2 A";
			document.getElementById("shift_bar_20").innerHTML = "PU2 B";

			document.getElementById("prac_pozicia_1").innerHTML = "Kvalitár (LPA1)";
			document.getElementById("tab_audit_riadok2").hidden = true;
			document.getElementById("tab_audit_riadok3").hidden = true;
			break;
	}
}

function unhide(val){
	if (val=="vlastne")
		document.getElementById("vlastne_obdobie").hidden = false;
	else	
		document.getElementById("vlastne_obdobie").hidden = true;
}


function mesiac(m, element){
	switch(m){
		case "01":
			document.getElementById(element).innerHTML = "Január";
			document.getElementById(element).value = "1";
		  	break;
		case "02":
			document.getElementById(element).innerHTML = "Február";
			document.getElementById(element).value = "2";
			break;
		case "03":
			document.getElementById(element).innerHTML = "Marec";
			document.getElementById(element).value = "3";
			break;
		case "04":
			document.getElementById(element).innerHTML = "Apríl";
			document.getElementById(element).value = "4";
			break;
		case "05":
			document.getElementById(element).innerHTML = "Máj";
			document.getElementById(element).value = "5";
			break;
		case "06":
			document.getElementById(element).innerHTML = "Jún";
			document.getElementById(element).value = "6";
			break;
		case "07":
			document.getElementById(element).innerHTML = "Júl";
			document.getElementById(element).value = "7";
		  	break;
		case "08":
			document.getElementById(element).innerHTML = "August";
			document.getElementById(element).value = "8";
			break;
		case "09":
			document.getElementById(element).innerHTML = "September";
			document.getElementById(element).value = "9";
			break;
		case "10":
			document.getElementById(element).innerHTML = "Október";
			document.getElementById(element).value = "10";
			break;
		case "11":
			document.getElementById(element).innerHTML = "November";
			document.getElementById(element).value = "11";
			break;
		case "12":
			document.getElementById(element).innerHTML = "December";
			document.getElementById(element).value = "12";
			break;
		default:
			document.getElementById(element).innerHTML = "Január";
			document.getElementById(element).value = "1";
			break;
	}
}