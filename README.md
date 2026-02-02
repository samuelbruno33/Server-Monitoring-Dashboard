# ProgettoPPM - Server Monitoring Dashboard

Questo progetto è stato sviluppato come elaborato d’esame per il corso di Progettazione e Produzione Multimediale.  
Si tratta di una semplice applicazione web realizzata con Django che permette di monitorare lo stato di alcuni server di una rete locale tramite ping e di verificare la raggiungibilità dei servizi associati controllando l’apertura delle relative porte TCP.

L’accesso alla dashboard è consentito solo agli utenti autenticati. La gestione dei server, dei servizi e delle impostazioni avviene tramite il pannello di amministrazione di Django, a cui può accedere solo l'utente admin. È possibile configurare l’intervallo di aggiornamento automatico della dashboard.

Nel repository sono inclusi il file `requirements.txt` con tutte le dipendenze necessarie e il database `db.sqlite3` già popolato con alcuni dati di esempio, in modo da poter avviare il progetto e visualizzarne subito il funzionamento senza dover inserire manualmente i dati.

Per eseguire il progetto è sufficiente aprire un terminale nella cartella principale (dove si trova il file `manage.py`), creare e attivare un ambiente virtuale (venv) Python, installare le dipendenze tramite `pip install -r requirements.txt` e avviare il server con il comando `python manage.py runserver`. Non è necessario eseguire migrazioni perché il database è già incluso.

Una volta avviato il server, la dashboard è accessibile all’indirizzo http://127.0.0.1:8000/ mentre il pannello di amministrazione è disponibile all’indirizzo http://127.0.0.1:8000/admin/.

Sono già presenti utenti di esempio per il test dell’applicazione. L’account amministratore ha username `admin` e password `admin`, mentre è disponibile anche un utente normale per la sola visualizzazione della dashboard con username `test_staff` e password `test`.

-----------------------------------------------------------------------------------------------------------------------------------------------------------

This project was developed as an exam paper for the Multimedia Design and Production course.  
It is a simple web application created with Django that allows you to monitor the status of certain servers on a local network via ping and to check the reachability of associated services by checking the openness of the relevant TCP ports.

Access to the dashboard is restricted to authenticated users only. Servers, services, and settings are managed through the Django admin panel, which can only be accessed by the admin user. The automatic refresh interval of the dashboard can be configured.

The repository includes the `requirements.txt` file with all the necessary dependencies and the `db.sqlite3` database already populated with some sample data, so you can start the project and immediately see how it works without having to manually enter data.

To run the project, simply open a terminal in the main folder (where the `manage.py` file is located), create and activate a Python virtual environment (venv), install the dependencies using `pip install -r requirements.txt`, and start the server with the command `python manage.py runserver`. There is no need to perform migrations because the database is already included.

Once the server has been started, the dashboard can be accessed at http://127.0.0.1:8000/, while the administration panel is available at http://127.0.0.1:8000/admin/.

Sample users are already present for testing the application. The administrator account has the username `admin` and password `admin`, while a normal user is also available for viewing the dashboard only, with the username `test_staff` and password `test`.



Translated with DeepL.com (free version)
