# ***** HLAVNY REPORT URCENY PRE VELKOPLOSNE OBRAZOVKY VO VYROBE *****


import requests

from flask import Flask, render_template, session, request
from requests import Session

from dateutil.relativedelta import *
from datetime import datetime, timedelta, date
import datetime
import math
import pyodbc
import json
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


    return render_template("vykonane_audity.html")




@app.route('/vykonane_audity', methods=['GET', 'POST' ] )
def historia():
    PU = request.form['pu']
    t=request.form['range']
    area = request.form['area']
    now = datetime.datetime.now()          #https://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
    dataToSend = []
    stroje=[]
    
    
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

    #########################################################    Selects from database

    conn = pyodbc.connect("DRIVER={MariaDB ODBC 3.0 Driver};SERVER=172.23.11.100;PORT=5555;DATABASE=miba;UID=superuser;PWD=superuser")
    pom = conn.cursor()
    
    cas_od = date1[0:8]  
    cas_do = date2[0:8]           
    
    if (area == "Konečná kontrola a balenie PU1"):
        PU = "FIP1"
    else:
        if (area == "Konečná kontrola a balenie PU2"):
            PU = "FIP2"

    pom.execute("SELECT sNAME FROM machines WHERE sPU = '"+PU+"' AND sAREA = '"+area+"' AND nActive = 1 AND sNAME != 'SPOLOČNÉ PRIESTORY'")
    query_stroje = pom.fetchall()
    for i in query_stroje:
        stroje.append(i[0])

  
    # try:
    #     pom.execute("SELECT AVG(nPercentage) FROM audits WHERE CONCAT(SUBSTR(sAuditDate,7), SUBSTR(sAuditDate,4,2), SUBSTR(sAuditDate,1,2)) >= '"+cas_od+"' AND CONCAT(SUBSTR(sAuditDate,7), SUBSTR(sAuditDate,4,2), SUBSTR(sAuditDate,1,2)) <= '"+cas_do+"' AND sAuditedPU = '"+PU+"' AND sAuditedArea = '"+area+"'")
    #     avg_vykonanych_auditov = pom.fetchall()
    #     mach = {
    #         "average":round(avg_vykonanych_auditov[0][0]),
    #     }

    #     if (cas_od<'20190531'):
    #         mach = {
    #         "average":"nie_su_udaje",
    #         }
    #     dataToSend.append(mach)
    
    # except:
    #     mach = {
    #         "average":"nie_su_udaje",
    #     }
    #     dataToSend.append(mach)

    pocet_auditov = 0

    if (PU == "FIP1" or PU == "FIP2"):
        for i in stroje:
            #zapocita audit iba pri tych strojoch, kde boli vyplnene vsetky 3 kategorie(q,ehs,5s) alebo bol NA
            #pom.execute("SELECT COUNT(*) FROM (SELECT nAuditID, sAuditDate, nAuditedDaytime, sAuditedPU, sAuditedArea, sMachineName FROM audits, audited_machines WHERE CONCAT(SUBSTR(sAuditDate,7), SUBSTR(sAuditDate,4,2), SUBSTR(sAuditDate,1,2)) >= '"+cas_od+"' AND CONCAT(SUBSTR(sAuditDate,7), SUBSTR(sAuditDate,4,2), SUBSTR(sAuditDate,1,2)) <= '"+cas_do+"' AND sAuditedPU = '"+PU+"' AND sAuditedArea = '"+area+"' AND sMachineName = '"+i+"' AND audits.nID=audited_machines.nAuditID GROUP BY nAuditID HAVING (sum( CASE WHEN (sAuditedType = '5s' AND (nAuditedValue = 1 OR nAuditedValue = 2)) THEN 1 ELSE 0 END ) = 1 AND sum( CASE WHEN (sAuditedType = 'q' AND (nAuditedValue = 1 OR nAuditedValue = 2)) THEN 1 ELSE 0 END ) = 1 AND sum( CASE WHEN (sAuditedType = 'ehs' AND (nAuditedValue = 1 OR nAuditedValue = 2)) THEN 1 ELSE 0 END ) = 1) OR sum( CASE WHEN (sAuditedType = 'na' AND nAuditedValue = 1) THEN 1 ELSE 0 END ) = 1) AS audity")
            #zapocita audit iba pri tych strojoch, kde boli vyplnene vsetky 3 kategorie(q,ehs,5s)
            pom.execute("SELECT COUNT(*) FROM (SELECT nAuditID, sAuditDate, nAuditedDaytime, sAuditedPU, sAuditedArea, sMachineName FROM audits_fip, \
            audited_machines_fip WHERE CONCAT(SUBSTR(sAuditDate,7), SUBSTR(sAuditDate,4,2), SUBSTR(sAuditDate,1,2)) >= '"+cas_od+"' AND \
            CONCAT(SUBSTR(sAuditDate,7), SUBSTR(sAuditDate,4,2), SUBSTR(sAuditDate,1,2)) <= '"+cas_do+"' AND sAuditedPU = '"+PU+"' \
            AND sAuditedArea = '"+area+"' AND sMachineName = '"+i+"' AND audits_fip.nID=audited_machines_fip.nAuditID \
            GROUP BY nAuditID HAVING sum( CASE WHEN (sAuditedType = '5s' AND (nAuditedValue = 1 OR nAuditedValue = 2)) THEN 1 ELSE 0 END ) = 1 \
            AND sum( CASE WHEN (sAuditedType = 'q' AND (nAuditedValue = 1 OR nAuditedValue = 2)) THEN 1 ELSE 0 END ) = 1 AND \
            sum( CASE WHEN (sAuditedType = 'ehs' AND (nAuditedValue = 1 OR nAuditedValue = 2)) THEN 1 ELSE 0 END ) = 1) AS audity")
            result = pom.fetchall()

            pocet_auditov = pocet_auditov + result[0][0]

            mach = {
                "machine":i,
                "result":result[0][0] 
            }

            dataToSend.append(mach)
    else:
        for i in stroje:
            #zapocita audit iba pri tych strojoch, kde boli vyplnene vsetky 3 kategorie(q,ehs,5s)
            pom.execute("SELECT COUNT(*) FROM (SELECT nAuditID, sAuditDate, nAuditedDaytime, sAuditedPU, sAuditedArea, \
                        sMachineName FROM audits, audited_machines WHERE CONCAT(SUBSTR(sAuditDate,7), SUBSTR(sAuditDate,4,2), \
                        SUBSTR(sAuditDate,1,2)) >= '"+cas_od+"' AND CONCAT(SUBSTR(sAuditDate,7), SUBSTR(sAuditDate,4,2), \
                        SUBSTR(sAuditDate,1,2)) <= '"+cas_do+"' AND sAuditedPU = '"+PU+"' AND sAuditedArea = '"+area+"' \
                        AND sMachineName = '"+i+"' AND audits.nID=audited_machines.nAuditID GROUP BY nAuditID \
                        HAVING sum( CASE WHEN (sAuditedType = '5s' AND (nAuditedValue = 1 OR nAuditedValue = 2)) THEN 1 ELSE 0 END ) = 1 \
                        AND sum( CASE WHEN (sAuditedType = 'q' AND (nAuditedValue = 1 OR nAuditedValue = 2)) THEN 1 ELSE 0 END ) = 1 AND \
                        sum( CASE WHEN (sAuditedType = 'ehs' AND (nAuditedValue = 1 OR nAuditedValue = 2)) THEN 1 ELSE 0 END ) = 1) AS audity")
            result = pom.fetchall()

            pocet_auditov = pocet_auditov + result[0][0]

            mach = {
                "machine":i,
                "result":result[0][0] 
            }

            dataToSend.append(mach)

    
    date1_dateformat = datetime.datetime(int(date1[0:4]),int(date1[4:6]),int(date1[6:8]),6,0)
    date2_dateformat = datetime.datetime(int(date2[0:4]),int(date2[4:6]),int(date2[6:8]),int(date2[8:10]),0)

    if (date2_dateformat > now):
        date2_dateformat = now
        
    try:
        pocet_smien = int(((date2_dateformat-date1_dateformat).total_seconds()/3600)//8)+1
        pocet_auditov_percenta = pocet_auditov / (len(stroje) * pocet_smien) * 100  
        mach = {
                "average":round(pocet_auditov_percenta),
            }
        dataToSend.append(mach)
    except:
        mach = {
                "average":"nie_su_udaje",
            }
        dataToSend.append(mach)

    dataToSend.append({"pocet_smien":pocet_smien,})

    pom.close()
    conn.close()
    dataToSendJson = json.dumps(dataToSend)
    
    return dataToSendJson


# region System parts and flask parts

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'memcached'
    sess = Session()
    app.debug = True
    app.run(threaded=True, host='0.0.0.0', port=5091)

# endregion