Interactive Multimedia Information Retrieval
TU Dresden, Wintersemester 2016/17

Team: Finn Schlenk, Jonas Fischer, Julian Catoni, Stephan Dinter

Aufgabe 1 - Boolsche Suche

Programmiersprache: Python (Version 3.5)


1. Indexierung
======================================================================
Zum Starten der Indexierung muss die Datei 'index_parser.py' ausgeführt werden.
Dabei ist darauf zu achten, dass im entsprechenden Ordner ein Unterordner namens 'index' existiert.
Das Erstellen des Index wurde auf zwei Systemen getestet.
Es sollten mindestens 8GB Arbeitsspeicher vorhanden sein.
Um die Indexierung auch auf Systemen mit geringerem RAM durchführbar zu machen, muss in utilities.py
der Wert der Variable characters_group_size (Standard: 5) verringert werden.

System 1:
OS: Ubuntu 16.04
Prozessor: i3-3110M, 2.4GHz
RAM: 8GB
benötigte Zeit für Indexerstellung: ca. 26 Minuten

System 2:
OS: OS X El Capitan, Version 10.11.6
Prozessor: i7-4850HQ, 2.3GHz
RAM: 16GB
benötigte Zeit für Indexerstellung: ca. 24 Minuten

Unter Windows wurde die Indexierung ebenfalls getestet. Jedoch gibt es hier Probleme, da Python dort eine Sperre für zu große Variablen hat. Deswegen sollte er vorzugsweise auf einem Linux- oder MacOS-System ausgeführt werden.

Die Indexierung läuft so ab, dass für verschiedene Buchstabengruppen Index-Dateien erstellt werden.
In der aktuellen Konfiguration sind das 7 Index-Dateien (aäbcd, efghi, jklmn, oöpq, stuüv, wxyz, Sonderzeichen/Zahlen).
Zusätzlich wird eine Datei erstellt, die alle Abstract IDs beinhaltet, um die NOT-Suche effizienter zu ermöglichen.


2. Suche
======================================================================
Zum Starten der Suche muss die Datei 'search.py' gestartet werden.
Bei der Query-Formulierung gibt es folgende Regelungen:

- Suche einfacher Terme: Term ohne zusätzliche Sonderzeichen o.Ä.
- Suche von Phrasen: Phrase in Anführungszeichen, z.B. "das auto fährt"
- Boolsche Suche: Verknüpfung obiger Suchtypen mit AND/OR/NOT (unbedingt äußere Klammern nutzen), z.B. ((auto AND reifen) OR (NOT volkswagen))
