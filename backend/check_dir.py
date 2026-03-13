import os

print('Aktuelles Arbeitsverzeichnis:')
print(os.getcwd())
print('\nInhalt dieses Verzeichnisses:')
for entry in os.listdir():
    print('  ', entry)

print('\napp-Verzeichnis-Inhalt (falls vorhanden):')
if os.path.isdir('app'):
    for entry in os.listdir('app'):
        print('  ', entry)
else:
    print('  (kein app-Verzeichnis gefunden)')
