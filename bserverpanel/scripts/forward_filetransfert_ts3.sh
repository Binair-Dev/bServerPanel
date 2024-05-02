#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <path_to_database> <port>"
    exit 1
fi
db_path="$1"
port="$2"
if [ ! -f "$db_path" ]; then
    echo "Le fichier de base de données n'existe pas : $db_path"
    exit 1
fi
sqlite_command="sqlite3 $db_path"
sql_query="UPDATE instance_properties
SET value = $port
WHERE ident = 'serverinstance_filetransfer_port';"
echo "Exécution de la requête SQL :"
echo "$sql_query"
echo "..."
$sqlite_command "$sql_query"
echo "Sortie de l'interface SQLite."
echo ".exit" | $sqlite_command