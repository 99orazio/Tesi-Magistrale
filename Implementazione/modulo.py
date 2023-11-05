import time
import nmap3
import json
import requests
import re
from datetime import datetime
import schedule
import nmap as nm
import sys

flag = False


def scans(indirizzo):
    """
    SCANSIONE CLASSICA
    :param indirizzo: Indirizzo IP da scansionare.
    :return: 0 se l'IP non è corretto, altrimenti i JSON contenenti gli host attivi e inattivi.
    """
    nmap = nmap3.Nmap()
    # found = re.search(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{2}", indirizzo)  # regex per controllare l'ip
    found = True
    if found:  # se l'ip è nella forma corretta
        print("IP SINTATTICAMENTE CORRETTO")
        print("ESEGUO LA SCANSIONE DELLA RETE: ", indirizzo)
        print(type(indirizzo))
        result = nmap.scan_top_ports(indirizzo, args="-sn -PR", default=2)  # scansiono le porte più importanti
        print(json.dumps(result, indent=2), file=open("output_scans " + str(datetime.now()) + ".txt", "w+"))  # scrivo l'output totale su file in modo leggibile
        rs1 = result.copy()  # risultati per i down
        rs2 = result.copy()  # risultati per gli up
        for x in result:
            if "state" in result[x] and result[x]["state"]["state"] == "up":  # contollo se l'host è up, se si allora lo elimino da rs1
                rs1.pop(x)  # lo elimino così posso creare un 2° file con solo gli IP down nella sottorete
        filename_down = "output_scans_down " + str(datetime.now()) + ".txt"
        print(json.dumps(rs1, indent=2), file=open(filename_down, "w+"))  # scrivo l'output parziale su file in modo leggibile
        print("INVIO OUTPUT DELLA SCANSIONE PARZIALE UP AL SERVER")
        f = open(filename_down)
        json_data1 = json.load(f)  # carico il file della scansione come un json
        r = requests.post("http://google.it", json=json_data1)  # invio json al server
        print(f"Status Code: {r.status_code}")
        for x in result:
            if "state" in result[x] and result[x]["state"]["state"] == "down":  # contollo se l'host è down, se si allora lo elimino da rs2
                rs2.pop(x)  # lo elimino così posso creare un 2° file con solo gli IP up nella sottorete
        filename_up = "output_scans_up " + str(datetime.now()) + ".txt"
        print(json.dumps(rs2, indent=2), file=open(filename_up, "w+"))  # scrivo l'output parziale su file in modo leggibile
        print("INVIO OUTPUT DELLA SCANSIONE PARZIALE DOWN AL SERVER")
        f = open(filename_up)
        json_data2 = json.load(f)  # carico il file della scansione come un json
        r = requests.post("http://google.it", json=json_data2)  # invio json al server
        print(f"Status Code: {r.status_code}")
        return json_data1, json_data2
    else:
        print("RITENTA LA SCANSIONE CON UN IP CORRETTO")
        return 0


def scan_time(indirizzo):  # crea dei file con nomi diversi rispetto alla scansione precedente
    """
    SCANSIONE PERIODICA.
    :param indirizzo: Indirizzo IP da scansionare.
    :return: 0 se l'IP non è corretto, altrimenti i JSON contenenti gli host attivi e inattivi
    """
    nmap = nmap3.Nmap()
    found = re.search(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{2}", indirizzo)  # regex per controllare l'ip
    if found:  # se l'ip è nella forma corretta
        print("IP SINTATTICAMENTE CORRETTO")
        print("ESEGUO LA SCANSIONE DELLA RETE: ", indirizzo)
        result = nmap.scan_top_ports(indirizzo, args="-sn -PR", default=2)  # scansiono le porte più importanti
        print(json.dumps(result, indent=2), file=open("output_scans_time " + str(datetime.now()) + ".txt", "w+"))  # scrivo l'output totale su file in modo leggibile
        rs1 = result.copy()  # risultati per i down
        rs2 = result.copy()  # risultati per gli up
        for x in result:
            if "state" in result[x] and result[x]["state"]["state"] == "up":  # contollo se l'host è up, se si allora lo elimino da rs1
                rs1.pop(x)  # lo elimino così posso creare un 2° file con solo gli IP down nella sottorete
        filename_down = "output_scans_time_down " + str(datetime.now()) + ".txt"
        print(json.dumps(rs1, indent=2), file=open(filename_down, "w+"))  # scrivo l'output parziale su file in modo leggibile
        print("INVIO OUTPUT DELLA SCANSIONE PARZIALE UP AL SERVER")
        f = open(filename_down)
        json_data1 = json.load(f)  # carico il file della scansione come un json
        r = requests.post("http://google.it", json=json_data1)  # invio json al server
        print(f"Status Code: {r.status_code}")
        for x in result:
            if "state" in result[x] and result[x]["state"]["state"] == "down":  # contollo se l'host è down, se si allora lo elimino da rs2
                rs2.pop(x)  # lo elimino così posso creare un 2° file con solo gli IP up nella sottorete
        filename_up = "output_scans_time_up " + str(datetime.now()) + ".txt"
        print(json.dumps(rs2, indent=2), file=open(filename_up, "w+"))  # scrivo l'output parziale su file in modo leggibile
        print("INVIO OUTPUT DELLA SCANSIONE PARZIALE DOWN AL SERVER")
        f = open(filename_up)
        json_data2 = json.load(f)  # carico il file della scansione come un json
        r = requests.post("http://google.it", json=json_data2)  # invio json al server
        print(f"Status Code: {r.status_code}")
        return json_data1, json_data2
    else:
        print("RITENTA LA SCANSIONE CON UN IP CORRETTO")
        return 0


""""
def scans_time(indirizzo, timer):
    if flag == False:
        while flag== False:
            print("VAL: ", flag)
            scan_time(indirizzo)
            schedule.every(int(timer)).minutes.do(scan_time, indirizzo=indirizzo)
            while True:
                if flag:
                    print("VAL2: ", flag)
                    sys.exit(0)
                schedule.run_pending()
                time.sleep(1)
    else:
        sys.exit(0)


def stop():
    global flag
    flag = True
"""


def scans_time(indirizzo, timer):
    """
    FUNZIONE RICHIAMANTE SCAN_TIME (UTILIZZA IL FILE FLAG INIZIALMENTE CONTENENTE FALSE).
    :param indirizzo: Indirizzo IP da scansionare.
    :param timer: Tempo di ripetizione della scansione.
    :return: 0 se il file "flag.txt" non è stato trovato
    """
    try:
        file = open("flag.txt", "r")
    except:
        print("FILE FLAG.TXT NON PRESENTE")
        return 0
    val = file.read()
    file.close()
    if val == "False":
        file = open("flag.txt", "r")
        val = file.read()
        file.close()
        while val == "False":
            print("VAL: ", val)
            scan_time(indirizzo)
            schedule.every(int(timer)).minutes.do(scan_time, indirizzo=indirizzo)
            while True:
                file = open("flag.txt", "r")
                val = file.read()
                file.close()
                if val == "True":
                    print("VAL2: ", val)
                    file = open("flag.txt", "w+")
                    file.write("False")
                    file.close()
                    sys.exit(0)
                schedule.run_pending()
                time.sleep(1)
    else:
        sys.exit(0)


def stop():  # funzione che setta scrive True nel file flag così da poter bloccare la scansione periodica
    """
    FUNZIONE DI STOP PER LA SCANSIONE AUTOMATICA. FERMA OGNI COMPITO IN ESECUZIONE.
    :return: 1 se riesce a scrivere correttamente nel file "flag.txt"
    """
    file = open("flag.txt", "w+")
    file.write("True")
    file.close()
    return 1


def scan_port(indirizzo, porte):
    """
    FUNZIONE DI SCANSIONE DI DETERMINATE PORTE.
    :param indirizzo: Indirizzo IP da scansionare.
    :param porte: Porte da scansionare da inserire nella forma "range", "elenco", "singola".
    :return: 1 se la scansione va a buon fine, 0 se l'IP è scorretto.
    """
    nmap = nmap3.Nmap()
    found = re.fullmatch(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", indirizzo)  # regex per controllare l'ip
    found2 = re.fullmatch(r"[0-9]{1,5}", porte)  # regex controllo singola porta
    found3 = re.fullmatch(r"[0-9]{1,5}\-[0-9]{1,5}", porte)  # regex controllo intervallo porte
    found4 = re.fullmatch(r"[0-9]{1,5}.*", porte)  # regex controllo elenco porte
    if found and (found2 or found3 or found4):  # se l'ip è nella forma corretta
        print("IP E PORTE SINTATTICAMENTE CORRETTI")
        print("ESEGUO LA SCANSIONE DELL'IP: ", indirizzo)
        result = nmap.scan_top_ports(indirizzo, args="-p" + porte)  # scansiono le porte prese in input
        print(json.dumps(result, indent=2), file=open("output_scan_port " + str(datetime.now()) + ".txt", "w+"))  # scrivo l'output totale su file in modo leggibile
        return 1
    else:
        print("RITENTA LA SCANSIONE CON UN IP CORRETTO")
        return 0


def scan_service(indirizzo):
    """
    SCANSIONE PER I SERVIZI DISPONIBILI SULL'HOST.
    :param indirizzo: Indirizzo IP da scansionare.
    :return: 1 se la scansione va a buon fine, 0 se l'IP è scorretto.
    """
    nmap = nmap3.Nmap()
    found = re.fullmatch(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", indirizzo)  # regex per controllare l'ip
    if found:
        print("IP SINTATTICAMENTE CORRETTO")
        print("ESEGUO LA SCANSIONE DELL'IP: ", indirizzo)
        result = nmap.nmap_version_detection(indirizzo, args="-v -p1-500")  # scansiono i servizi
        print(json.dumps(result, indent=2), file=open("output_scan_service " + str(datetime.now()) + ".txt", "w+"))  # scrivo l'output totale su file in modo leggibile
        return 1
    else:
        print("RITENTA LA SCANSIONE CON UN IP CORRETTO")
        return 0


def scan_os(indirizzo):
    """
    SCANSIONE OS DETECTION DI UN CERTO HOST.
    :param indirizzo: Indirizzo IP da scansionare.
    :return: 1 se la scansione va a buon fine, 0 se l'IP è scorretto.
    """
    nmap = nmap3.Nmap()
    found = re.fullmatch(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", indirizzo)  # regex per controllare l'ip
    if found:
        print("IP SINTATTICAMENTE CORRETTO")
        print("ESEGUO LA SCANSIONE DELL'IP: ", indirizzo)
        result = nmap.nmap_os_detection(indirizzo, args="--osscan-guess")  # scansiono per trovare il SO dell'host
        print(json.dumps(result, indent=2), file=open("output_scan_os " + str(datetime.now()) + ".txt", "w+"))  # scrivo l'output totale su file in modo leggibile
        return 1
    else:
        print("RITENTA LA SCANSIONE CON UN IP CORRETTO")
        return 0


"""
def scan_vuln2(indirizzo):
    nmap = nmap3.Nmap()
    found = re.fullmatch(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", indirizzo)  # regex per controllare l'ip
    if found:
        print("IP SINTATTICAMENTE CORRETTO")
        print("ESEGUO LA SCANSIONE DELL'IP: ", indirizzo)
        result = nmap.scan_top_ports(target=indirizzo, args="-sV --script vuln")
        print(json.dumps(result, indent=2), file=open("output_scan_vuln " + str(datetime.now()) + ".txt", "w+"))  # scrivo l'output totale su file in modo leggibile
        return 1
    else:
        print("RITENTA LA SCANSIONE CON UN IP CORRETTO")
        return 0
"""


def scan_vuln(indirizzo):
    """
    SCANSIONE VULNERABLITÀ PRESENTI IN UN HOST.
    :param indirizzo: Indirizzo IP da scansionare.
    :return: 1 se la scansione va a buon fine, 0 se l'IP è scorretto.
    """
    nmap = nm.PortScanner()
    found = re.fullmatch(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", indirizzo)  # regex per controllare l'ip
    if found:
        print("IP SINTATTICAMENTE CORRETTO")
        print("ESEGUO LA SCANSIONE DELL'IP: ", indirizzo)
        nmap.scan(indirizzo, arguments="-sV --script vuln")
        print(json.dumps(nmap[indirizzo], indent=2), file=open("output_scan_vuln " + str(datetime.now()) + ".txt", "w+"))  # scrivo l'output totale su file in modo leggibile
        return 1
    else:
        print("RITENTA LA SCANSIONE CON UN IP CORRETTO")
        return 0
