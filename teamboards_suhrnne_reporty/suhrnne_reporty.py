# ***** HLAVNY REPORT URCENY PRE VELKOPLOSNE OBRAZOVKY VO VYROBE *****


import requests

from flask import Flask, render_template, session, request
from requests import Session

from dateutil.relativedelta import *
from datetime import datetime, timedelta, date
import datetime
import math
import json
import pyodbc
import xlsxwriter 
import openpyxl
from openpyxl import Workbook
import threading 
import sys
import os
    
# Local imports
def GetHigherLevelPath(level:int):                          # requires import os
    os.chdir(os.path.dirname(__file__))
    cur_path = str(os.getcwd()) + chr(92)
    c1 = cur_path.count(chr(92))
    if level>=c1:
        return "error"
    c21 = c1-level
    c11 = 0
    result = ""
    for znak in cur_path:
        result = result + znak
        if znak == chr(92):
            c11 = c11 + 1
            if c11 == c21:
                break
    return result

sys.path.insert(0, GetHigherLevelPath(1))                   # requires import sys
import support_global





def mesiac_slovensky(month):
    if((month + datetime.timedelta(days = -1)).strftime("%B")=="January"):
        mesiac = "Január"
    else:
        if((month + datetime.timedelta(days = -1)).strftime("%B")=="February"):
            mesiac = "Február"
        else:
            if((month + datetime.timedelta(days = -1)).strftime("%B")=="March"):
                mesiac = "Marec"
            else:
                if((month + datetime.timedelta(days = -1)).strftime("%B")=="April"):
                    mesiac = "Apríl"
                else:
                    if((month + datetime.timedelta(days = -1)).strftime("%B")=="May"):
                        mesiac = "Máj"
                    else:
                        if((month + datetime.timedelta(days = -1)).strftime("%B")=="June"):
                            mesiac = "Jún"
                        else:
                            if((month + datetime.timedelta(days = -1)).strftime("%B")=="July"):
                                mesiac = "Júl"
                            else:
                                if((month + datetime.timedelta(days = -1)).strftime("%B")=="August"):
                                    mesiac = "August"
                                else:
                                    if((month + datetime.timedelta(days = -1)).strftime("%B")=="September"):
                                        mesiac = "September"
                                    else:
                                        if((month + datetime.timedelta(days = -1)).strftime("%B")=="October"):
                                            mesiac = "Október"
                                        else:
                                            if((month + datetime.timedelta(days = -1)).strftime("%B")=="November"):
                                                mesiac = "November"
                                            else:
                                                if((month + datetime.timedelta(days = -1)).strftime("%B")=="December"):
                                                    mesiac = "December"    
    return(mesiac)


def zmena(cas):
    if(str(cas.strftime("%H"))=="14"):
        zmena="poobedná"
        return(zmena)
    if(str(cas.strftime("%H"))=="22"):
        zmena="nočná"
        return(zmena)
    if(str(cas.strftime("%H"))=="06"):
        zmena="ranná"
        return(zmena)


def export():
    PU = ["PU1", "PU2", "PU3", "PU4"]
    teamboard = ["quality", "performance", "ehs", "5s", "attendance"]
    results=[]

    conn = pyodbc.connect("DRIVER={MariaDB ODBC 3.0 Driver};SERVER=172.23.11.100;PORT=5555;DATABASE=miba;UID=superuser;PWD=superuser")
    pom = conn.cursor()
    actual_date = datetime.datetime.now()
    last_month = actual_date - relativedelta(months=1)

    for j in teamboard:
        for i in PU:
            pom.execute("SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+str(last_month.month).zfill(2)+"' AND sYear='"+str(last_month.year).zfill(2)+"' AND sPU='"+i+"' AND sType='"+j+"'")
            result= pom.fetchall()
            results.append(result[0][0])
    
    pom.close()
    conn.close()
    
    book = openpyxl.load_workbook('//SXFILMIB011SK/work/public/DASHBOARD/Shopfloor/Dashboard_DATA.xlsx')
    #book = openpyxl.load_workbook('K:\public\!Erkal\__prenos\Dashboard_DATA.xlsx')
    sheet = book["Data"]
    
    n=0
    columns="FGHIJ"

    for j in columns:
        for i in range(73, 77, 1):
            sheet[j+str(i)] = str(round(results[n], 2))+'%'
            n+=1        

    book.save('//SXFILMIB011SK/work/public/DASHBOARD/Shopfloor/Dashboard_DATA.xlsx')
    #book.save('K:\public\!Erkal\__prenos\Dashboard_DATA.xlsx')
    book.close() 
    return()


def kvartal(t1):
    if (t1.month==1):
        t1 = datetime.datetime.strptime(str(t1.year-1)+' 11', '%Y %m')
    else:
        if (t1.month>=2 and t1.month<=4):
            t1 = datetime.datetime.strptime(str(t1.year)+' 02', '%Y %m')
        else:
            if (t1.month>=5 and t1.month<=7):
                t1 = datetime.datetime.strptime(str(t1.year)+' 05', '%Y %m')
            else:
                if (t1.month>=8 and t1.month<=10):
                    t1 = datetime.datetime.strptime(str(t1.year)+' 08', '%Y %m')
                else:
                    if (t1.month>=11 and t1.month<=12):
                        t1 = datetime.datetime.strptime(str(t1.year)+' 11', '%Y %m')
    return(t1)


def nevykonane_audity_majstri(t1, t2, j, PU, index):
    conn = pyodbc.connect("DRIVER={MariaDB ODBC 3.0 Driver};SERVER=172.23.11.100;PORT=5555;DATABASE=miba;UID=superuser;PWD=superuser")
    pom = conn.cursor()

    nevykonane_audity=[]
    while(t1 <= t2):      
        cas_od=t1.strftime("%Y")+t1.strftime("%m")+t1.strftime("%d")+t1.strftime("%H")            
        cas_do=(t1 + datetime.timedelta(hours = 8)).strftime("%Y") + (t1 + datetime.timedelta(hours = 8)).strftime("%m") + (t1 + datetime.timedelta(hours = 8)).strftime("%d") + (t1 + datetime.timedelta(hours = 8)).strftime("%H")
                    
        pom.execute("SELECT sDate1 FROM audits, auditors, audited_machines WHERE CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2), substr(audits.sDate1,1,2), substr(audits.sTime1,1,2)) >= '"+cas_od+"' and CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2), substr(audits.sDate1,1,2), substr(audits.sTime1,1,2)) < '"+cas_do+"' and sAuditedArea='"+j+"' and audits.sAuditedPU='"+PU+"' and (audits.nAuditorID1=auditors.nOSC OR audits.nAuditorID2=auditors.nOSC OR audits.nAuditorID3=auditors.nOSC OR audits.nAuditorID4=auditors.nOSC) AND audits.nID=audited_machines.nAuditID AND audited_machines.nAuditorID=auditors.nOSC GROUP BY audited_machines.nAuditID HAVING COUNT(audited_machines.nAuditID)>=6")
        result = pom.fetchall()
        if(result==[]):
            nevykonane_audity += [[t1.strftime("%d")+"."+t1.strftime("%m")+"."+t1.strftime("%Y")+"-"+zmena(t1)+"-"+support_global.GiveShift(int(t1.strftime("%H")), int(t1.strftime("%d")), int(t1.strftime("%m")), int(t1.strftime("%Y")))]]
        
        pom.execute("SELECT sDate1, nAuditedDaytime, sAuditedShift FROM audits, auditors, audited_machines WHERE CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2), substr(audits.sDate1,1,2), substr(audits.sTime1,1,2)) >= '"+cas_od+"' and CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2), substr(audits.sDate1,1,2), substr(audits.sTime1,1,2)) < '"+cas_do+"' and sAuditedArea='"+j+"' and audits.sAuditedPU='"+PU+"' and (audits.nAuditorID1=auditors.nOSC OR audits.nAuditorID2=auditors.nOSC OR audits.nAuditorID3=auditors.nOSC OR audits.nAuditorID4=auditors.nOSC) AND audits.nID=audited_machines.nAuditID AND audited_machines.nAuditorID=auditors.nOSC GROUP BY audited_machines.nAuditID HAVING COUNT(audited_machines.nAuditID)>=6 and COUNT(audited_machines.nAuditID)/4 = sum( CASE WHEN (sAuditedType = 'na' AND nAuditedValue = 1) THEN 1 ELSE 0 END )")
        result = pom.fetchall()
        if(result!=[]):
            nevykonane_audity += [[t1.strftime("%d")+"."+t1.strftime("%m")+"."+t1.strftime("%Y")+"-"+zmena(t1)+"-"+support_global.GiveShift(int(t1.strftime("%H")), int(t1.strftime("%d")), int(t1.strftime("%m")), int(t1.strftime("%Y")))+" *all NA*"]]


        t1 = t1 + datetime.timedelta(hours = 8)
       
    pom.close()
    conn.close()
   
    global vysledok
    vysledok.pop(index)
    vysledok.insert(index, nevykonane_audity)
    return ()

def nevykonane_audity_majstri_FIP(t1, t2, area, PU):
    conn = pyodbc.connect("DRIVER={MariaDB ODBC 3.0 Driver};SERVER=172.23.11.100;PORT=5555;DATABASE=miba;UID=superuser;PWD=superuser")
    pom = conn.cursor()
    
    nevykonane_audity=[]
    while(t1 <= t2):      
        cas_od=t1.strftime("%Y")+t1.strftime("%m")+t1.strftime("%d")+t1.strftime("%H")            
        cas_do=(t1 + datetime.timedelta(hours = 8)).strftime("%Y") + (t1 + datetime.timedelta(hours = 8)).strftime("%m") + (t1 + datetime.timedelta(hours = 8)).strftime("%d") + (t1 + datetime.timedelta(hours = 8)).strftime("%H")
                    
        pom.execute("SELECT sDate1 FROM audits_fip, auditors, audited_machines_fip WHERE CONCAT(substr(audits_fip.sDate1,7), substr(audits_fip.sDate1,4,2), substr(audits_fip.sDate1,1,2), substr(audits_fip.sTime1,1,2)) >= '"+cas_od+"' and CONCAT(substr(audits_fip.sDate1,7), substr(audits_fip.sDate1,4,2), substr(audits_fip.sDate1,1,2), substr(audits_fip.sTime1,1,2)) < '"+cas_do+"' and sAuditedArea='"+area+"' and audits_fip.sAuditedPU='"+PU+"' and (audits_fip.nAuditorID1=auditors.nOSC OR audits_fip.nAuditorID2=auditors.nOSC OR audits_fip.nAuditorID3=auditors.nOSC OR audits_fip.nAuditorID4=auditors.nOSC) AND audits_fip.nID=audited_machines_fip.nAuditID AND audited_machines_fip.nAuditorID=auditors.nOSC GROUP BY audited_machines_fip.nAuditID HAVING COUNT(audited_machines_fip.nAuditID)>=6" )
        result = pom.fetchall()
        if(result==[]):
            nevykonane_audity += [[t1.strftime("%d")+"."+t1.strftime("%m")+"."+t1.strftime("%Y")+" - "+PU+" - "+zmena(t1)+"-"+support_global.GiveShiftFIP(int(t1.strftime("%H")), int(t1.strftime("%d")), int(t1.strftime("%m")), int(t1.strftime("%Y")))]]

        pom.execute("SELECT sDate1 FROM audits_fip, auditors, audited_machines_fip WHERE CONCAT(substr(audits_fip.sDate1,7), substr(audits_fip.sDate1,4,2), substr(audits_fip.sDate1,1,2), substr(audits_fip.sTime1,1,2)) >= '"+cas_od+"' and CONCAT(substr(audits_fip.sDate1,7), substr(audits_fip.sDate1,4,2), substr(audits_fip.sDate1,1,2), substr(audits_fip.sTime1,1,2)) < '"+cas_do+"' and sAuditedArea='"+area+"' and audits_fip.sAuditedPU='"+PU+"' and (audits_fip.nAuditorID1=auditors.nOSC OR audits_fip.nAuditorID2=auditors.nOSC OR audits_fip.nAuditorID3=auditors.nOSC OR audits_fip.nAuditorID4=auditors.nOSC) AND audits_fip.nID=audited_machines_fip.nAuditID AND audited_machines_fip.nAuditorID=auditors.nOSC GROUP BY audited_machines_fip.nAuditID HAVING COUNT(audited_machines_fip.nAuditID)>=6 and COUNT(audited_machines_fip.nAuditID)/4 = sum( CASE WHEN (sAuditedType = 'na' AND nAuditedValue = 1) THEN 1 ELSE 0 END )" )
        result = pom.fetchall()
        if(result!=[]):
            nevykonane_audity += [[t1.strftime("%d")+"."+t1.strftime("%m")+"."+t1.strftime("%Y")+" - "+PU+" - "+zmena(t1)+"-"+support_global.GiveShiftFIP(int(t1.strftime("%H")), int(t1.strftime("%d")), int(t1.strftime("%m")), int(t1.strftime("%Y")))+" *all NA*"]]


        t1 = t1 + datetime.timedelta(hours = 8)
        
        if (t1.strftime("%H")=="22"):
            t1 = t1 + datetime.timedelta(hours = 8)
        
        if (t1.strftime("%A")=="Saturday"):
            t1 = t1 + datetime.timedelta(hours = 48)

    pom.close()
    conn.close()

    global vysledok
    vysledok.insert(0, nevykonane_audity)
    return ()
    


app = Flask(__name__)
app.secret_key = 'some secret key'

# THIS SHOULD PREVENT CACHING OF JS AND CSS FILES
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r 

# MAIN PAGE
@app.route('/')
def main_page():

    ##################################################################################################################
    #########################################################    REGION AUDITY #########################################################
    now = datetime.datetime.now()
    pracoviskaPU1 = ["Lisovanie", "Tepelné opracovanie", "Kalibrovanie"]
    global vysledok
    vysledok=[]
    dataToSend=[]
    #inicializacia aktualneho datumu v spravnej forme, aby som ho vedel porovnat s retazcom v databaze
    date1=str(now.year) + str(now.month).zfill(2) + "0106"
    date2=str(now.year) + str(now.month).zfill(2) + str(int(now.strftime("%d"))).zfill(2) + str(now.hour).zfill(2)


    #do premennych t1 a t2 nacitam tieto datumy, aby som s nimi v pythone mohol pracovat ako s datumovou premennou(pripocitavat hodiny, dni, mesiace, roky)
    t2 = datetime.datetime.strptime(date2[0:4]+' '+date2[4:6]+' '+date2[6:8]+' '+date2[8:10] , '%Y %m %d %H')

    #cyklus ktory prejde reporty majstrov(M) na kazdom pracovisku v PU1
    thread_list = []
    index = 0
        
    for j in pracoviskaPU1:
        vysledok+=[[]]
        t1 = datetime.datetime.strptime(date1[0:4]+' '+date1[4:6]+' '+date1[6:8]+' 06', '%Y %m %d %H')

        thread = threading.Thread(target=nevykonane_audity_majstri, name=j, args = (t1, t2, j, "PU1", index))
        thread_list.append(thread)
        thread.start()
        index += 1

    for thread in thread_list:
        thread.join()   


    
    #cyklus ktory prejde reporty Koordinatorov(PK) na kazdom pracovisku v PU1    
    conn = pyodbc.connect("DRIVER={MariaDB ODBC 3.0 Driver};SERVER=172.23.11.100;PORT=5555;DATABASE=miba;UID=superuser;PWD=superuser")
    pom = conn.cursor()

    nevykonane_audity=[]
    t1 = datetime.datetime.strptime(date1[0:4]+' '+date1[4:6]+' '+date1[6:8], '%Y %m %d')
    n = t1.strftime("%w")
    #cyklus ktory skontroluje ci v zadanom rozmedzi pribudol do databazy kazdych 7 dni, respektive kazdy tyzden aspon jeden zaznam od koordinatora v konkretnej PU na konkretnom pracovisku
    #ak najde zaznam nevykona nic pripocita 7 dni a ide odznova
    #ak nenajde zaznam zapise cislo tyzdna v roku do pola
    t1 = t1 + datetime.timedelta(days = -int(n)+1)
    while(t1 < t2):
        cas_od=t1.strftime("%Y")+t1.strftime("%m")+t1.strftime("%d")
        t1 = t1 + datetime.timedelta(days = 7)
        cas_do=t1.strftime("%Y")+t1.strftime("%m")+t1.strftime("%d")

        pom.execute("SELECT DISTINCT sDate1 FROM audits, auditors, audited_machines WHERE CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2), substr(audits.sDate1,1,2)) >= '"+cas_od+"' and CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2), substr(audits.sDate1,1,2)) < '"+cas_do+"' and audits.sAuditedPU='PU1' and (audits.nAuditorID1=auditors.nOSC OR audits.nAuditorID2=auditors.nOSC OR audits.nAuditorID3=auditors.nOSC OR audits.nAuditorID4=auditors.nOSC) and sSTATUS3='PK' AND audits.nID=audited_machines.nAuditID AND audited_machines.nAuditorID=auditors.nOSC GROUP BY audited_machines.nAuditID HAVING COUNT(audited_machines.nAuditID)>=6" )
        result = pom.fetchall()
        if(result==[]):
            nevykonane_audity += [[t1.strftime("%W")+". týždeň "+t1.strftime("%Y")]]
        
    vysledok += [nevykonane_audity]
    

    
    #cyklus ktory prejde reporty PU lidrov(PUL) na kazdom pracovisku v PU1
    nevykonane_audity=[]
    t1 = datetime.datetime.strptime(date1[0:4]+' '+date1[4:6], '%Y %m')
    #cyklus ktory skontroluje ci v zadanom rozmedzi pribudol do databazy kazdy mesiac aspon jeden zaznam od PU lidra v konkretnej PU na konkretnom pracovisku
    #ak najde zaznam nevykona nic pripocita 1 mesiac a ide odznova
    #ak nenajde zaznam zapise mesiac v roku do pola
    while(t1 < t2):
        cas_od=t1.strftime("%Y")+t1.strftime("%m")
        t1 = t1 + relativedelta(months=+1)
        t1 = t1 + datetime.timedelta(days = -1)
        cas_do=t1.strftime("%Y")+t1.strftime("%m")
        t1 = t1 + datetime.timedelta(days = +1)
        pom.execute("SELECT DISTINCT sDate1 FROM audits, auditors, audited_machines WHERE CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2)) >= '"+cas_od+"' and CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2)) <= '"+cas_do+"' and audits.sAuditedPU='PU1' and (audits.nAuditorID1=auditors.nOSC OR audits.nAuditorID2=auditors.nOSC OR audits.nAuditorID3=auditors.nOSC OR audits.nAuditorID4=auditors.nOSC) and sSTATUS3='PUL' AND audits.nID=audited_machines.nAuditID AND audited_machines.nAuditorID=auditors.nOSC GROUP BY audited_machines.nAuditID HAVING COUNT(audited_machines.nAuditID)>=6" )
        result = pom.fetchall()
        #iba aby vypisalo dany mesiac po slovensky a nie po anglicky
        if(result==[]):
            nevykonane_audity += [[mesiac_slovensky(t1)+" "+(t1 + datetime.timedelta(days = -1)).strftime("%Y")]]
        
    vysledok += [nevykonane_audity]
  
    

    
    # #cyklus ktory prejde reporty EHS manazera, PM(vyrobneho manazera) a QM(kvalitoveho menezera) v PU1
    #cyklus ktory skontroluje ci v zadanom rozmedzi pribudol do databazy kazdy mesiac aspon jeden zaznam od PU lidra v konkretnej PU na konkretnom pracovisku
    #ak najde zaznam nevykona nic pripocita 1 mesiac a ide odznova
    #ak nenajde zaznam zapise mesiac v roku do pola
    status_LPA4 = ["EHS", "PM", "QM"]    
    for i in status_LPA4:
        t1 = datetime.datetime.strptime(date1[0:4]+' '+date1[4:6], '%Y %m')
        t1 = kvartal(t1)
        nevykonane_audity=[]
        while(t1 < t2):
            cas_od=t1.strftime("%Y")+t1.strftime("%m")
            t1 = t1 + relativedelta(months=+3)
            t1 = t1 + datetime.timedelta(days = -1)
            cas_do=t1.strftime("%Y")+t1.strftime("%m")

            # print(cas_od, cas_do)
            t1 = t1 + datetime.timedelta(days = +1)
            pom.execute("SELECT DISTINCT sDate1 FROM audits, auditors, audited_machines WHERE CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2)) >= '"+cas_od+"' and CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2)) <= '"+cas_do+"' and (audits.nAuditorID1=auditors.nOSC OR audits.nAuditorID2=auditors.nOSC OR audits.nAuditorID3=auditors.nOSC OR audits.nAuditorID4=auditors.nOSC) and sSTATUS3='"+i+"' AND audits.nID=audited_machines.nAuditID AND audited_machines.nAuditorID=auditors.nOSC GROUP BY audited_machines.nAuditID HAVING COUNT(audited_machines.nAuditID)>=6" )
            result = pom.fetchall()
            #iba aby vypisalo dany mesiac po slovensky a nie po anglicky
            if(result==[]):
                nevykonane_audity += [[mesiac_slovensky(t1 + relativedelta(months=-2))+" - "+mesiac_slovensky(t1)+" "+(t1 + datetime.timedelta(days = -1)).strftime("%Y")]]
            
        vysledok += [nevykonane_audity]


    ##################################################################################################################
    #########################################################   REGION BARY #########################################################
    #v tomto cykle sa vyberu hodnoty pre kazdu tabulku barov na stranke
    #v kazdom cykle sa ulozia hodnoty do noveho jsonu a z kazdeho jsonu potom pomocou js vykreslia bary v html
    for i, j in zip (pracoviskaPU1,range(3)):
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='A' AND sType='quality'"
        pom.execute(sCommand)
        results= pom.fetchall()
        QU_A = results

        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='B' AND sType='quality'"
        pom.execute(sCommand)
        results= pom.fetchall()
        QU_B = results

        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='C' AND sType='quality'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='C' AND sType='quality'"
        pom.execute(sCommand)
        results= pom.fetchall()
        QU_C = results

        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='D' AND sType='quality'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='D' AND sType='quality'"
        pom.execute(sCommand)
        results= pom.fetchall()
        QU_D = results


        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='A' AND sType='performance'"
        pom.execute(sCommand)
        results= pom.fetchall()
        PE_A = results


        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='B' AND sType='performance'"
        pom.execute(sCommand)
        results= pom.fetchall()
        PE_B = results


        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='C' AND sType='performance'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='C' AND sType='performance'"
        pom.execute(sCommand)
        results= pom.fetchall()
        PE_C = results


        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='D' AND sType='performance'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='D' AND sType='performance'"
        pom.execute(sCommand)
        results= pom.fetchall()
        PE_D = results


        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='A' AND sType='ehs'"
        pom.execute(sCommand)
        results= pom.fetchall()
        EH_A = results


        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='B' AND sType='ehs'"
        pom.execute(sCommand)
        results= pom.fetchall()
        EH_B = results


        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='C' AND sType='ehs'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='C' AND sType='ehs'"
        pom.execute(sCommand)
        results= pom.fetchall()
        EH_C = results


        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='D' AND sType='ehs'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='D' AND sType='ehs'"
        pom.execute(sCommand)
        results= pom.fetchall()
        EH_D = results


        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='A' AND sType='5s'"
        pom.execute(sCommand)
        results= pom.fetchall()
        SA_A = results


        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='B' AND sType='5s'"
        pom.execute(sCommand)
        results= pom.fetchall()
        SA_B = results


        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='C' AND sType='5s'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='C' AND sType='5s'"
        pom.execute(sCommand)
        results= pom.fetchall()
        SA_C = results


        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='D' AND sType='5s'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='D' AND sType='5s'"
        pom.execute(sCommand)
        results= pom.fetchall()
        SA_D = results

        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='A' AND sType='attendance'"
        pom.execute(sCommand)
        results= pom.fetchall()
        AT_A = results


        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='B' AND sType='attendance'"
        pom.execute(sCommand)
        results= pom.fetchall()
        AT_B = results


        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='C' AND sType='attendance'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='C' AND sType='attendance'"
        pom.execute(sCommand)
        results= pom.fetchall()
        AT_C = results


        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='D' AND sType='attendance'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE sMonth='"+date1[4:6]+"' AND sYear='"+date1[0:4]+"' AND sPU='PU1' AND sArea='"+i+"' AND sShift='D' AND sType='attendance'"
        pom.execute(sCommand)
        results= pom.fetchall()
        AT_D = results

        #vytvori json do ktoreho sa ulozia vsetky hodnoty, vdaka ktorym sa vykreslia bary
        dataToSend.append(json.dumps({
        'QU_A': str(QU_A[0][0]),
        'QU_B': str(QU_B[0][0]),
        'QU_C': str(QU_C[0][0]),
        'QU_D': str(QU_D[0][0]),
        'PE_A': str(PE_A[0][0]),
        'PE_B': str(PE_B[0][0]),
        'PE_C': str(PE_C[0][0]),
        'PE_D': str(PE_D[0][0]),
        'EH_A': str(EH_A[0][0]),
        'EH_B': str(EH_B[0][0]),
        'EH_C': str(EH_C[0][0]),
        'EH_D': str(EH_D[0][0]),
        'SA_A': str(SA_A[0][0]),
        'SA_B': str(SA_B[0][0]),
        'SA_C': str(SA_C[0][0]),
        'SA_D': str(SA_D[0][0]),
        'AT_A': str(AT_A[0][0]),
        'AT_B': str(AT_B[0][0]),
        'AT_C': str(AT_C[0][0]),
        'AT_D': str(AT_D[0][0]),
        }))


    pom.close()
    conn.close()        # zavri bazu pred kazdym returnom, alebo hned, ako ju prestanes potrebovat

    dataToSend.append(json.dumps({}))

    #vyrenderovanie templatu so vsetkymi hodnotami, ktore sa v cykloch ulozili do poli
    #je dolezite aby boli v spravnom poradi inac sa nezobrazia na spravnom mieste napr.:do premennej majstri_1 sa musi priradit vysledok[0]!!! nesmie tam byt ina premenna napr. vysledok[1]  
    return render_template("suhrn_report.html", date2_r=date2[0:4], date2_m=date2[4:6], date1_r=date1[0:4], date1_m=date1[4:6], 
                            hodnotenie_tab1=dataToSend[0], hodnotenie_tab2=dataToSend[1], hodnotenie_tab3=dataToSend[2], hodnotenie_tab4=dataToSend[3], 
                            pracovisko1=pracoviskaPU1[0], pracovisko2=pracoviskaPU1[1], pracovisko3=pracoviskaPU1[2], 
                            PU="PU1", vybrate="aktualny_mesiac", 
                            majstri_1=vysledok[0], majstri_2=vysledok[1], majstri_3=vysledok[2], 
                            koordinatori_1=vysledok[3], PUL_1=vysledok[4], EHSmanager_1=vysledok[5], Qmanager_1=vysledok[6], Pmanager_1=vysledok[7])


    ###################################################################################################################
    ###################################################################################################################
    ###################################################################################################################
    ###################################################################################################################


@app.route('/suhrnny_report', methods=['GET', 'POST' ] )
def example():
    global vysledok
    vysledok=[]
    dataToSend=[]
    PU = request.form['ProdUnit']
    t=request.form['obdobie']
    now = datetime.datetime.now()          #https://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
    
    #potrebujem zistit ktoru moznost si uzivatel vybral z moznosti a podla toho nacitat do premennych date1 a date2 datum v takom stringovom retazci aby som ho vedel porovnat s datumami v databaze
    #napr. ak si uzivatel vyberie posledny kvartal do premennej date1 sa nacita zaciatocny datum tohto obdobia (11.1.2018 ->"2018110106") a do date2 a zapise koncovy datum tohto obdobia (31.1.2019 ->"2019013122")
    if (t!="vlastne"):
        if (t=="aktualny_mesiac"):
            date1 = str(now.year) + str(now.month).zfill(2) + "01" + "06"
            date2 = str(now.year) + str(now.month).zfill(2) + str(int(now.strftime("%d"))).zfill(2) + str(now.hour).zfill(2)
        else: 
            if (t=="mesiac" and now.strftime("%m")=="01"):
                date1 = str(now.year-1) + "12" + "01" + "06"
                date2 = str(now.year-1) + "12" + "31" + "22"
            else:
                if (t=="mesiac" and now.strftime("%m")!="01"):
                    date1 = str(now.year) + str(now.month-1).zfill(2) + "01" + "06"
                    date2 = str(now.year) + str(now.month-1).zfill(2) + str((now - datetime.timedelta(days = now.day)).day) + "22"
                else:            
                    if (t == "kvartal" and now.month<=4 and now.month>=2):
                        date1 = str(now.year-1) + "11"  + "01" + "06"
                        date2 = str(now.year) + "01"  + "31" + "22"
                    else:
                        if (t == "kvartal" and now.month>4):
                            date1 = str(now.year) + str(math.floor((now.month-5)/3)*3+2).zfill(2) + "01" + "06"
                            date2 = str(now.year) + str(math.floor((now.month-2)/3)*3+1).zfill(2) + str((date(now.year, (math.floor((now.month-2)/3)*3+2), 1) - date(now.year, (math.floor((now.month-2)/3)*3+1), 1)).days) + "22"
                        else:
                            if (t == "kvartal" and now.month==1):
                                date1 = str(now.year-1) + "08"  + "01" + "06"
                                date2 = str(now.year-1) + "10"  + "31" + "22"
                            else:
                                if (t == "polrok" and now.month<=7 and now.month>=2):
                                    date1 = str(now.year-1) + "08"  + "01" + "06"
                                    date2 = str(now.year) + "01"  + "31" + "22"
                                else:
                                    if (t == "polrok" and now.month>7):
                                        date1 = str(now.year) + "02"  + "01" + "06"
                                        date2 = str(now.year) + "07"  + "31" + "22"
                                    else:
                                        if (t == "polrok" and now.month==1):
                                            date1 = str(now.year-1) + "02"  + "01" + "06"
                                            date2 = str(now.year-1) + "07"  + "31" + "22"
                                        else:
                                            if (t == "rok" and now.month==1):
                                                date1 = str(now.year-2) + "02"  + "01" + "06"
                                                date2 = str(now.year-1) + "01"  + "31" + "22"
                                            else:
                                                if (t == "rok" and now.month>=2):
                                                    date1 = str(now.year-1) + "02"  + "01" + "06"
                                                    date2 = str(now.year) + "01"  + "31" + "22"
    else:
        date1 = request.form['od_rok'] + (request.form['od_mesiac']).zfill(2) + "01" + "06"
        date2 = request.form['do_rok'] + (request.form['do_mesiac']).zfill(2) + str(datetime.datetime (int(request.form['do_rok']), int(request.form['do_mesiac']), 1) + relativedelta(months=+1) + relativedelta(days=-1))[8:10] + "22"                                             

    ###################################################################################################################
    #########################################################    REGION AUDITY #######################################################
    if (PU != "FIP"):
        pracoviskaPU1 = ["Lisovanie", "Tepelné opracovanie", "Kalibrovanie"]
        pracoviskaPU2 = ["Lisovanie", "Tepelné opracovanie", "Kalibrovanie", "Mechanické opracovanie"]
        pracoviskaPU3 = ["Mechanické opracovanie 1", "Mechanické opracovanie 2"]
        pracoviskaPU4 = ["Celá jednotka"]


        #podla toho ktora PU bola vybrata, tak sa do x zapise pole s pracoviskami v tejto PU
        if (PU=="PU1"):
            x = pracoviskaPU1
        else:
            if (PU=="PU2"):
                x = pracoviskaPU2
            else:
                if (PU=="PU3"):
                    x = pracoviskaPU3
                else:
                    if (PU=="PU4"):
                        x = pracoviskaPU4

        #do premennych t1 a t2 nacitam tieto datumy, aby som s nimi v pythone mohol pracovat ako s datumovou premennou(pripocitavat hodiny, dni, mesiace, roky)
        t2 = datetime.datetime.strptime(date2[0:4]+' '+date2[4:6]+' '+date2[6:8]+' '+date2[8:10], '%Y %m %d %H')

        #cyklus ktory prejde reporty majstrov(M) na kazdom pracovisku v PU
        thread_list = []
        index = 0
        
        for j in x:
            vysledok+=[[]]
            t1 = datetime.datetime.strptime(date1[0:4]+' '+date1[4:6]+' '+date1[6:8]+' 06', '%Y %m %d %H')

            thread = threading.Thread(target=nevykonane_audity_majstri, name=j, args = (t1, t2, j, PU, index))
            thread_list.append(thread)
            thread.start()
            index += 1

        for thread in thread_list:
            thread.join()



        #conn = sqlite3.connect('miba.db')
        conn = pyodbc.connect("DRIVER={MariaDB ODBC 3.0 Driver};SERVER=172.23.11.100;PORT=5555;DATABASE=miba;UID=superuser;PWD=superuser")
        pom = conn.cursor()
        #cyklus ktory prejde reporty koordinatorov(PK) na kazdom pracovisku v PU  

        nevykonane_audity=[]
        t1 = datetime.datetime.strptime(date1[0:4]+' '+date1[4:6]+' '+date1[6:8], '%Y %m %d')
        n = t1.strftime("%w")

        #cyklus ktory skontroluje ci v zadanom rozmedzi pribudol do databazy kazdych 7 dni, respektive kazdy tyzden aspon jeden zaznam od koordinatora v konkretnej PU na konkretnom pracovisku
        #ak najde zaznam nevykona nic pripocita 7 dni a ide odznova
        #ak nenajde zaznam zapise cislo tyzdna v roku do pola
        t1 = t1 + datetime.timedelta(days = -int(n)+1)
        while(t1 < t2):
            cas_od=t1.strftime("%Y")+t1.strftime("%m")+t1.strftime("%d")
            t1 = t1 + datetime.timedelta(days = 7)
            cas_do=t1.strftime("%Y")+t1.strftime("%m")+t1.strftime("%d")

            pom.execute("SELECT sDate1 FROM audits, auditors, audited_machines WHERE CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2), substr(audits.sDate1,1,2)) >= '"+cas_od+"' and CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2), substr(audits.sDate1,1,2)) < '"+cas_do+"' and audits.sAuditedPU='"+PU+"' and (audits.nAuditorID1=auditors.nOSC OR audits.nAuditorID2=auditors.nOSC OR audits.nAuditorID3=auditors.nOSC OR audits.nAuditorID4=auditors.nOSC) and sSTATUS3='PK' AND audits.nID=audited_machines.nAuditID AND audited_machines.nAuditorID=auditors.nOSC GROUP BY audited_machines.nAuditID HAVING COUNT(audited_machines.nAuditID)>=6" )
            result = pom.fetchall()
            if(result==[]):  
                if(t1.strftime("%Y")=="2019"):
                    nevykonane_audity += [[t1.strftime("%W")+". týždeň "+t1.strftime("%Y")]]
                else:
                    nevykonane_audity += [[(t1 + datetime.timedelta(days = -7)).strftime("%W")+". týždeň "+(t1 + datetime.timedelta(days = -7)).strftime("%Y")]]
            
        vysledok += [nevykonane_audity]



        #cyklus ktory prejde reporty PU lidri(PUL) na kazdom pracovisku v PU  
        nevykonane_audity=[]
        t1 = datetime.datetime.strptime(date1[0:4]+' '+date1[4:6], '%Y %m')

        #cyklus ktory skontroluje ci v zadanom rozmedzi pribudol do databazy kazdy mesiac aspon jeden zaznam od PU lidra v konkretnej PU na konkretnom pracovisku
        #ak najde zaznam nevykona nic pripocita 1 mesiac a ide odznova
        #ak nenajde zaznam zapise mesiac v roku do pola
        while(t1 < t2):
            cas_od=t1.strftime("%Y")+t1.strftime("%m")
            t1 = t1 + relativedelta(months=+1)
            t1 = t1 + datetime.timedelta(days = -1)
            cas_do=t1.strftime("%Y")+t1.strftime("%m")
            t1 = t1 + datetime.timedelta(days = +1)

            pom.execute("SELECT sDate1 FROM audits, auditors, audited_machines WHERE CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2)) >= '"+cas_od+"' and CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2)) <= '"+cas_do+"' and audits.sAuditedPU='"+PU+"' and (audits.nAuditorID1=auditors.nOSC OR audits.nAuditorID2=auditors.nOSC OR audits.nAuditorID3=auditors.nOSC OR audits.nAuditorID4=auditors.nOSC) and sSTATUS3='PUL' and audits.nID=audited_machines.nAuditID AND audited_machines.nAuditorID=auditors.nOSC GROUP BY audited_machines.nAuditID HAVING COUNT(audited_machines.nAuditID)>=6" )
            result = pom.fetchall()
            #vypis konkretneho mesiaca nie po anglicky ale po slovensky
            if(result==[]):
                nevykonane_audity += [[mesiac_slovensky(t1)+" "+(t1 + datetime.timedelta(days = -1)).strftime("%Y")]]
                
        vysledok += [nevykonane_audity]



        status_LPA4 = ["EHS", "PM", "QM"]        
        for i in status_LPA4:
            t1 = datetime.datetime.strptime(date1[0:4]+' '+date1[4:6], '%Y %m')
            t1 = kvartal(t1)
            nevykonane_audity=[]
            while(t1 < t2):
                cas_od=t1.strftime("%Y")+t1.strftime("%m")
                t1 = t1 + relativedelta(months=+3)
                t1 = t1 + datetime.timedelta(days = -1)
                cas_do=t1.strftime("%Y")+t1.strftime("%m")

                t1 = t1 + datetime.timedelta(days = +1)
                pom.execute("SELECT DISTINCT sDate1 FROM audits, auditors, audited_machines WHERE CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2)) >= '"+cas_od+"' and CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2)) <= '"+cas_do+"' and (audits.nAuditorID1=auditors.nOSC OR audits.nAuditorID2=auditors.nOSC OR audits.nAuditorID3=auditors.nOSC OR audits.nAuditorID4=auditors.nOSC) and sSTATUS3='"+i+"' AND audits.nID=audited_machines.nAuditID AND audited_machines.nAuditorID=auditors.nOSC GROUP BY audited_machines.nAuditID HAVING COUNT(audited_machines.nAuditID)>=6" )
                result = pom.fetchall()
                #iba aby vypisalo dany mesiac po slovensky a nie po anglicky
                if(result==[]):
                    nevykonane_audity += [[mesiac_slovensky(t1 + relativedelta(months=-2))+" - "+mesiac_slovensky(t1)+" "+(t1 + datetime.timedelta(days = -1)).strftime("%Y")]]

            vysledok += [nevykonane_audity]


        ##################################################################################################################
        #########################################################   REGION BARY #########################################################
        #v tomto cykle sa vyberu hodnoty pre kazdu tabulku barov na stranke
        #v kazdom cykle sa ulozia hodnoty do noveho jsonu a z kazdeho jsonu potom pomocou js vykreslia bary v html
        
        for i in (x):
            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='A' AND sType='quality'"
            pom.execute(sCommand)
            results= pom.fetchall()
            QU_A = results


            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='B' AND sType='quality'"
            pom.execute(sCommand)
            results= pom.fetchall()
            QU_B = results

            #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='C' AND sType='quality'"
            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='C' AND sType='quality'"
            pom.execute(sCommand)
            results= pom.fetchall()
            QU_C = results

            #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='D' AND sType='quality'"
            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='D' AND sType='quality'"
            pom.execute(sCommand)
            results= pom.fetchall()
            QU_D = results


            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='A' AND sType='performance'"
            pom.execute(sCommand)
            results= pom.fetchall()
            PE_A = results


            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='B' AND sType='performance'"
            pom.execute(sCommand)
            results= pom.fetchall()
            PE_B = results


            #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='C' AND sType='performance'"
            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='C' AND sType='performance'"
            pom.execute(sCommand)
            results= pom.fetchall()
            PE_C = results


            #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='D' AND sType='performance'"
            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='D' AND sType='performance'"
            pom.execute(sCommand)
            results= pom.fetchall()
            PE_D = results


            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='A' AND sType='ehs'"
            pom.execute(sCommand)
            results= pom.fetchall()
            EH_A = results


            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='B' AND sType='ehs'"
            pom.execute(sCommand)
            results= pom.fetchall()
            EH_B = results


            #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='C' AND sType='ehs'"
            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='C' AND sType='ehs'"
            pom.execute(sCommand)
            results= pom.fetchall()
            EH_C = results


            #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='D' AND sType='ehs'"
            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='D' AND sType='ehs'"
            pom.execute(sCommand)
            results= pom.fetchall()
            EH_D = results


            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='A' AND sType='5s'"
            pom.execute(sCommand)
            results= pom.fetchall()
            SA_A = results


            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='B' AND sType='5s'"
            pom.execute(sCommand)
            results= pom.fetchall()
            SA_B = results


            #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='C' AND sType='5s'"
            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='C' AND sType='5s'"
            pom.execute(sCommand)
            results= pom.fetchall()
            SA_C = results


            #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='D' AND sType='5s'"
            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='D' AND sType='5s'"
            pom.execute(sCommand)
            results= pom.fetchall()
            SA_D = results

            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='A' AND sType='attendance'"
            pom.execute(sCommand)
            results= pom.fetchall()
            AT_A = results


            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='B' AND sType='attendance'"
            pom.execute(sCommand)
            results= pom.fetchall()
            AT_B = results


            #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='C' AND sType='attendance'"
            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='C' AND sType='attendance'"
            pom.execute(sCommand)
            results= pom.fetchall()
            AT_C = results


            #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='D' AND sType='attendance'"
            sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='"+PU+"' AND sArea='"+i+"' AND sShift='D' AND sType='attendance'"
            pom.execute(sCommand)
            results= pom.fetchall()
            AT_D = results

            #vytvori json do ktoreho sa ulozia vsetky hodnoty, vdaka ktorym sa vykreslia bary
            dataToSend.append(json.dumps({
            'QU_A': str(QU_A[0][0]),
            'QU_B': str(QU_B[0][0]),
            'QU_C': str(QU_C[0][0]),
            'QU_D': str(QU_D[0][0]),
            'PE_A': str(PE_A[0][0]),
            'PE_B': str(PE_B[0][0]),
            'PE_C': str(PE_C[0][0]),
            'PE_D': str(PE_D[0][0]),
            'EH_A': str(EH_A[0][0]),
            'EH_B': str(EH_B[0][0]),
            'EH_C': str(EH_C[0][0]),
            'EH_D': str(EH_D[0][0]),
            'SA_A': str(SA_A[0][0]),
            'SA_B': str(SA_B[0][0]),
            'SA_C': str(SA_C[0][0]),
            'SA_D': str(SA_D[0][0]),
            'AT_A': str(AT_A[0][0]),
            'AT_B': str(AT_B[0][0]),
            'AT_C': str(AT_C[0][0]),
            'AT_D': str(AT_D[0][0]),
            }))

        pom.close()
        conn.close()        # zavri bazu pred kazdym returnom, alebo hned, ako ju prestanes potrebovat

        #vyrenderovanie templatu so vsetkymi hodnotami, ktore sa v cykloch ulozili do poli
        #je dolezite aby boli v spravnom poradi inac sa nezobrazia na spravnom mieste napr.:do premennej majstri_1 sa musi priradit vysledok[0]!!! nesmie tam byt ina premenna napr. vysledok[1]
        #podla toho ktora PU je zvolena sa musi vybrat moznost vyrenderovania templatu, pretoze pri kazdej moznosti sa posiela ine mnozstvo premennych a tym padom aj v inom poradi
        if (PU=="PU1"):
            dataToSend.append(json.dumps({}))
            return render_template("suhrn_report.html", date2_r=date2[0:4], date2_m=date2[4:6], date1_r=date1[0:4], date1_m=date1[4:6], 
                                hodnotenie_tab1=dataToSend[0], hodnotenie_tab2=dataToSend[1], hodnotenie_tab3=dataToSend[2], hodnotenie_tab4=dataToSend[3], 
                                pracovisko1=pracoviskaPU1[0], pracovisko2=pracoviskaPU1[1], pracovisko3=pracoviskaPU1[2], 
                                PU=PU, vybrate=t, 
                                majstri_1=vysledok[0], majstri_2=vysledok[1], majstri_3=vysledok[2], 
                                koordinatori_1=vysledok[3], PUL_1=vysledok[4], EHSmanager_1=vysledok[5], Pmanager_1=vysledok[6], Qmanager_1=vysledok[7])    
        else:
            if (PU=="PU2"):
                return render_template("suhrn_report.html", date2_r=date2[0:4], date2_m=date2[4:6], date1_r=date1[0:4], date1_m=date1[4:6], 
                                    hodnotenie_tab1=dataToSend[0], hodnotenie_tab2=dataToSend[1], hodnotenie_tab3=dataToSend[2], hodnotenie_tab4=dataToSend[3], 
                                    pracovisko1=pracoviskaPU2[0], pracovisko2=pracoviskaPU2[1], pracovisko3=pracoviskaPU2[2], pracovisko4=pracoviskaPU2[3], 
                                    PU=PU, vybrate=t, 
                                    majstri_1=vysledok[0], majstri_2=vysledok[1], majstri_3=vysledok[2], majstri_4=vysledok[3], 
                                    koordinatori_1=vysledok[4], PUL_1=vysledok[5], EHSmanager_1=vysledok[6], Pmanager_1=vysledok[7], Qmanager_1=vysledok[8])
            else:
                if (PU=="PU3"):
                    dataToSend.append(json.dumps({}))
                    dataToSend.append(json.dumps({}))
                    return render_template("suhrn_report.html", date2_r=date2[0:4], date2_m=date2[4:6], date1_r=date1[0:4], date1_m=date1[4:6], 
                                        hodnotenie_tab1=dataToSend[0], hodnotenie_tab2=dataToSend[1], hodnotenie_tab3=dataToSend[2], hodnotenie_tab4=dataToSend[3], 
                                        pracovisko1=pracoviskaPU3[0], pracovisko2=pracoviskaPU3[1], 
                                        PU=PU, vybrate=t, 
                                        majstri_1=vysledok[0], majstri_2=vysledok[1], 
                                        koordinatori_1=vysledok[2], PUL_1=vysledok[3], EHSmanager_1=vysledok[4], Pmanager_1=vysledok[5], Qmanager_1=vysledok[6])
                else:
                    if (PU=="PU4"):
                        dataToSend.append(json.dumps({}))
                        dataToSend.append(json.dumps({}))
                        dataToSend.append(json.dumps({}))
                        return render_template("suhrn_report.html", date2_r=date2[0:4], date2_m=date2[4:6], date1_r=date1[0:4], date1_m=date1[4:6], 
                                            hodnotenie_tab1=dataToSend[0], hodnotenie_tab2=dataToSend[1], hodnotenie_tab3=dataToSend[2], hodnotenie_tab4=dataToSend[3], 
                                            pracovisko1=pracoviskaPU4[0], 
                                            PU=PU, vybrate=t, 
                                            majstri_1=vysledok[0], koordinatori_1=vysledok[1], PUL_1=vysledok[2], EHSmanager_1=vysledok[3], Pmanager_1=vysledok[4], Qmanager_1=vysledok[5])
    
    ###################################################################################################################
    ###################################################################################################################
    ###################################################################################################################
    ###################################################################################################################    
    ###################################################################################################################
    ##########################################################  FIP #########################################################
    else:


        #do premennych t1 a t2 nacitam tieto datumy, aby som s nimi v pythone mohol pracovat ako s datumovou premennou(pripocitavat hodiny, dni, mesiace, roky)
        t2 = datetime.datetime.strptime(date2[0:4]+' '+date2[4:6]+' '+date2[6:8]+' '+date2[8:10], '%Y %m %d %H')        
        t1 = datetime.datetime.strptime(date1[0:4]+' '+date1[4:6]+' '+date1[6:8]+' 06', '%Y %m %d %H')

        nevykonane_audity=[]
        #cyklus ktory skontroluje ci v zadanom rozmedzi pribudol do databazy kazdych 8 hodin aspon jeden zaznam od majstra v konkretnej PU na konkretnom pracovisku
        #ak najde zaznam nevykona nic pripocita 8 hodin a ide odznova
        #ak nenajde zaznam zapise dany datum do pola

        thread1 = threading.Thread(target=nevykonane_audity_majstri_FIP, args = (t1, t2, "Konečná kontrola a balenie PU2", "FIP2"))
        thread1.start()
        
        t1 = datetime.datetime.strptime(date1[0:4]+' '+date1[4:6]+' '+date1[6:8]+' 06', '%Y %m %d %H')
        thread2 = threading.Thread(target=nevykonane_audity_majstri_FIP, args = (t1, t2, "Konečná kontrola a balenie PU1", "FIP1"))
        thread2.start()
        

        thread1.join()
        thread2.join()

        
        #conn = sqlite3.connect('miba.db')
        conn = pyodbc.connect("DRIVER={MariaDB ODBC 3.0 Driver};SERVER=172.23.11.100;PORT=5555;DATABASE=miba;UID=superuser;PWD=superuser")
        pom = conn.cursor()
        

        status_LPA4 = ["EHS", "PM", "QM"]
        
        for i in status_LPA4:
            t1 = datetime.datetime.strptime(date1[0:4]+' '+date1[4:6], '%Y %m')
            t1 = kvartal(t1)
            nevykonane_audity=[]
            while(t1 < t2):
                cas_od=t1.strftime("%Y")+t1.strftime("%m")
                t1 = t1 + relativedelta(months=+3)
                t1 = t1 + datetime.timedelta(days = -1)
                cas_do=t1.strftime("%Y")+t1.strftime("%m")

                t1 = t1 + datetime.timedelta(days = +1)
                pom.execute("SELECT sDate1 FROM audits, auditors, audited_machines WHERE CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2)) >= '"+cas_od+"' and CONCAT(substr(audits.sDate1,7), substr(audits.sDate1,4,2)) <= '"+cas_do+"' and (audits.nAuditorID1=auditors.nOSC OR audits.nAuditorID2=auditors.nOSC OR audits.nAuditorID3=auditors.nOSC OR audits.nAuditorID4=auditors.nOSC) and sSTATUS3='"+i+"' AND audits.nID=audited_machines.nAuditID AND audited_machines.nAuditorID=auditors.nOSC GROUP BY audited_machines.nAuditID HAVING COUNT(audited_machines.nAuditID)>=6" )
                result = pom.fetchall()
                #iba aby vypisalo dany mesiac po slovensky a nie po anglicky
                if(result==[]):
                    nevykonane_audity += [[mesiac_slovensky(t1 + relativedelta(months=-2))+" - "+mesiac_slovensky(t1)+" "+(t1 + datetime.timedelta(days = -1)).strftime("%Y")]]

            vysledok += [nevykonane_audity]



        ##################################################################################################################
        #########################################################   REGION BARY #########################################################
        #v tomto cykle sa vyberu hodnoty pre kazdu tabulku barov na stranke
        #v kazdom cykle sa ulozia hodnoty do noveho jsonu a z kazdeho jsonu potom pomocou js vykreslia bary v html
        
        
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP1' AND sArea='Konečná kontrola a balenie PU1' AND sShift='A' AND sType='quality'"
        pom.execute(sCommand)
        results= pom.fetchall()
        QU_A = results


        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP1' AND sArea='Konečná kontrola a balenie PU1' AND sShift='B' AND sType='quality'"
        pom.execute(sCommand)
        results= pom.fetchall()
        QU_B = results

        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='C' AND sType='quality'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP2' AND sArea='Konečná kontrola a balenie PU2' AND sShift='A' AND sType='quality'"
        pom.execute(sCommand)
        results= pom.fetchall()
        QU_C = results

        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='D' AND sType='quality'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP2' AND sArea='Konečná kontrola a balenie PU2' AND sShift='B' AND sType='quality'"
        pom.execute(sCommand)
        results= pom.fetchall()
        QU_D = results


        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP1' AND sArea='Konečná kontrola a balenie PU1' AND sShift='A' AND sType='performance'"
        pom.execute(sCommand)
        results= pom.fetchall()
        PE_A = results


        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP1' AND sArea='Konečná kontrola a balenie PU1' AND sShift='B' AND sType='performance'"
        pom.execute(sCommand)
        results= pom.fetchall()
        PE_B = results


        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='C' AND sType='performance'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP2' AND sArea='Konečná kontrola a balenie PU2' AND sShift='A' AND sType='performance'"
        pom.execute(sCommand)
        results= pom.fetchall()
        PE_C = results


        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='D' AND sType='performance'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP2' AND sArea='Konečná kontrola a balenie PU2' AND sShift='B' AND sType='performance'"
        pom.execute(sCommand)
        results= pom.fetchall()
        PE_D = results


        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP1' AND sArea='Konečná kontrola a balenie PU1' AND sShift='A' AND sType='ehs'"
        pom.execute(sCommand)
        results= pom.fetchall()
        EH_A = results


        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP1' AND sArea='Konečná kontrola a balenie PU1' AND sShift='B' AND sType='ehs'"
        pom.execute(sCommand)
        results= pom.fetchall()
        EH_B = results


        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='C' AND sType='ehs'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP2' AND sArea='Konečná kontrola a balenie PU2' AND sShift='A' AND sType='ehs'"
        pom.execute(sCommand)
        results= pom.fetchall()
        EH_C = results


        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='D' AND sType='ehs'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP2' AND sArea='Konečná kontrola a balenie PU2' AND sShift='B' AND sType='ehs'"
        pom.execute(sCommand)
        results= pom.fetchall()
        EH_D = results


        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP1' AND sArea='Konečná kontrola a balenie PU1' AND sShift='A' AND sType='5s'"
        pom.execute(sCommand)
        results= pom.fetchall()
        SA_A = results


        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP1' AND sArea='Konečná kontrola a balenie PU1' AND sShift='B' AND sType='5s'"
        pom.execute(sCommand)
        results= pom.fetchall()
        SA_B = results


        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='C' AND sType='5s'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP2' AND sArea='Konečná kontrola a balenie PU2' AND sShift='A' AND sType='5s'"
        pom.execute(sCommand)
        results= pom.fetchall()
        SA_C = results


        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='D' AND sType='5s'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP2' AND sArea='Konečná kontrola a balenie PU2' AND sShift='B' AND sType='5s'"
        pom.execute(sCommand)
        results= pom.fetchall()
        SA_D = results

        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP1' AND sArea='Konečná kontrola a balenie PU1' AND sShift='A' AND sType='attendance'"
        pom.execute(sCommand)
        results= pom.fetchall()
        AT_A = results


        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP1' AND sArea='Konečná kontrola a balenie PU1' AND sShift='B' AND sType='attendance'"
        pom.execute(sCommand)
        results= pom.fetchall()
        AT_B = results


        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='C' AND sType='attendance'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP2' AND sArea='Konečná kontrola a balenie PU2' AND sShift='A' AND sType='attendance'"
        pom.execute(sCommand)
        results= pom.fetchall()
        AT_C = results


        #sCommand="SELECT * FROM sumarizer_months WHERE sMonth='"+xmonth+"' AND sYear='"+xyear+"' AND sPU='"+xpu+"' AND sArea='"+xarea+"' AND sShift='D' AND sType='attendance'"
        sCommand="SELECT AVG(nValue) FROM sumarizer_months WHERE (CONCAT(sYear, sMonth) >='"+date1[0:6]+"') AND (CONCAT(sYear, sMonth) <='"+date2[0:6]+"') AND sPU='FIP2' AND sArea='Konečná kontrola a balenie PU2' AND sShift='B' AND sType='attendance'"
        pom.execute(sCommand)
        results= pom.fetchall()
        AT_D = results

        #vytvori json do ktoreho sa ulozia vsetky hodnoty, vdaka ktorym sa vykreslia bary
        dataToSend.append(json.dumps({
        'QU_A': str(QU_A[0][0]),
        'QU_B': str(QU_B[0][0]),
        'QU_C': str(QU_C[0][0]),
        'QU_D': str(QU_D[0][0]),
        'PE_A': str(PE_A[0][0]),
        'PE_B': str(PE_B[0][0]),
        'PE_C': str(PE_C[0][0]),
        'PE_D': str(PE_D[0][0]),
        'EH_A': str(EH_A[0][0]),
        'EH_B': str(EH_B[0][0]),
        'EH_C': str(EH_C[0][0]),
        'EH_D': str(EH_D[0][0]),
        'SA_A': str(SA_A[0][0]),
        'SA_B': str(SA_B[0][0]),
        'SA_C': str(SA_C[0][0]),
        'SA_D': str(SA_D[0][0]),
        'AT_A': str(AT_A[0][0]),
        'AT_B': str(AT_B[0][0]),
        'AT_C': str(AT_C[0][0]),
        'AT_D': str(AT_D[0][0]),
        }))

        pom.close()
        conn.close()        # zavri bazu pred kazdym returnom, alebo hned, ako ju prestanes potrebovat

        #vyrenderovanie templatu so vsetkymi hodnotami, ktore sa v cykloch ulozili do poli
        #je dolezite aby boli v spravnom poradi inac sa nezobrazia na spravnom mieste napr.:do premennej majstri_1 sa musi priradit vysledok[0]!!! nesmie tam byt ina premenna napr. vysledok[1]
        #podla toho ktora PU je zvolena sa musi vybrat moznost vyrenderovania templatu, pretoze pri kazdej moznosti sa posiela ine mnozstvo premennych a tym padom aj v inom poradi
        dataToSend.append(json.dumps({}))
        dataToSend.append(json.dumps({}))
        dataToSend.append(json.dumps({}))
        return render_template("suhrn_report.html", date2_r=date2[0:4], date2_m=date2[4:6], date1_r=date1[0:4], date1_m=date1[4:6], 
                            hodnotenie_tab1=dataToSend[0], hodnotenie_tab2=dataToSend[1], hodnotenie_tab3=dataToSend[2], hodnotenie_tab4=dataToSend[3], 
                            pracovisko1="Konečná kontrola a balenie", 
                            PU=PU, vybrate=t, 
                            majstri_1=vysledok[0]+vysledok[1], EHSmanager_1=vysledok[2], Pmanager_1=vysledok[3], Qmanager_1=vysledok[4])   



@app.route('/export', methods=['GET', 'POST' ] )
def aktualizovat():    
    try:
        export()
    except:
        return render_template("export.html", message="Aktualizácia neprebehla. Súbor Dashboard_DATA.xlsx uz je otvorený alebo sa nenachádza v priečinku K:\public\!Erkal\__prenos\.")
    else:
        return render_template("export.html", message="V Excel súbore boli aktualizované priemerné hodnoty pre každú PU za minulý mesiac.")



# region System parts and flask parts

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'memcached'
    sess = Session()
    app.debug = True
    app.run(threaded=True, host='0.0.0.0', port=5080)

# endregion

