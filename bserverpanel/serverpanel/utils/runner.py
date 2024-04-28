import os
import subprocess
import multiprocessing

def executer_commande(commande, dossier):
    try:
        os.chdir(dossier)
        process = subprocess.Popen(commande, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        process.wait()
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    multiprocessing.freeze_support()

    commande_a_executer = "java -jar paper-1.20.4-496.jar --nogui"
    dossier_execution = "test-folder/paper"
    processus_detache = multiprocessing.Process(target=executer_commande, args=(commande_a_executer, dossier_execution))
    processus_detache.start()
    print("Démarré avec succès")