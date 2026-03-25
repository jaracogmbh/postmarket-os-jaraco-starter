**Titel: postmarketOS als echtes Linux‑Smartphone – und wie Codex die App‑Entwicklung direkt auf dem Gerät beschleunigt**

Wer Linux liebt, kennt den Moment, in dem sich „Mobile“ plötzlich nicht mehr wie eine Sonderwelt anfühlt. postmarketOS bringt genau dieses Gefühl zurück: ein Smartphone, das sich wie ein vollwertiges Alpine‑Linux‑System benimmt. Nicht nur ein Skin, nicht nur eine App‑Schicht – sondern das echte System, mit echten Paketen, echten Tools, und echtem Build‑Workflow.

Aber wir sind ehrlich: postmarketOS ist noch im Bootstrap‑Modus. Vieles funktioniert, aber vieles ist noch roh. Genau diese Frühphase macht die Plattform so spannend – und so kompromisslos: Wer hier entwickelt, baut nicht nur Apps, sondern auch die Grundlage des Ökosystems mit auf.

Als Beispiel dafür nehme ich hier `Jaraco Starter`, eine kleine GTK4/libadwaita‑App, die wir direkt auf postmarketOS entwickeln – mit Codex als Co‑Pilot. Warum gerade diese App? Weil sie klein genug ist, um sie komplett zu verstehen, aber vollständig genug, um alle typischen Herausforderungen zu zeigen: UI, Prozesse, Privilegien, Packaging und Integration in das System.

**Projektüberblick: Was ist `Jaraco Starter`?**

`Jaraco Starter` ist eine simple, aber produktive Utility‑App. Sie liest eine JSON‑Konfiguration aus `~/.config/jaraco/starter.json` und rendert daraus eine Liste von Actions. Jede Action bekommt zwei kleine Radio‑Buttons „Off“ und „On“. Das Ziel ist klar: Dienste, Skripte oder Hintergrundjobs mit einem Finger‑Tap starten oder stoppen – auf einem mobilen Gerät, das sich wie ein echtes Linux‑System verhält.

Was die App besonders macht:
- Konfigurationsgetrieben: Jede Action besteht aus `name`, `script`, `sudo` und optional `kill_command` sowie `kill_sudo`.
- Sauberes Start/Stop‑Handling: Beim Stop wird zuerst `SIGTERM` gesendet; wenn der Prozess nach 3 Sekunden nicht beendet ist, folgt `SIGKILL`.
- Privilege‑Handling über Polkit: Actions mit Root‑Rechten laufen über `pkexec` und eine Polkit‑Policy. Dazu existiert ein kleiner Runner, der `run`, `pgrep`, `shell` und `kill` kapselt.

**Warum Codex direkt auf postmarketOS?**

Der große Unterschied zwischen „Mobile‑Entwicklung“ und „Linux‑Entwicklung“ ist meistens der Umweg: Emulatoren, entfernte Builds, proprietäre Toolchains. postmarketOS kürzt das radikal ab. Du baust auf dem Gerät, testest auf dem Gerät, und installierst auf dem Gerät – ohne die Plattform zu verlassen.

Codex passt perfekt in dieses Setup, weil es direkt auf dem System arbeitet:
- Konfigurationslogik erklären lassen
- Signal‑Handling überprüfen
- UI‑Komponenten refactoren
- Packaging‑Schritte nachvollziehen
- Fehler schneller lokalisieren

Und genau hier wird es für AI‑Devs interessant: Ist das die grüne Wiese, auf die man gewartet hat? Eine Plattform, die noch nicht festbetoniert ist, sondern mit neuen Tools, neuen Ideen und neuen Workflows gestaltet werden kann.

**postmarketOS als echtes Alpine‑Linux‑System**

postmarketOS ist keine exotische Sonderdistribution, sondern basiert auf Alpine Linux. Dadurch bekommst du `apk` als Paketmanager, Alpine‑Pakete, bekannte Build‑Konzepte und eine sehr klare, minimalistische Systemlogik.

Das wirkt erstmal wie ein Detail, ist aber für Entwicklung entscheidend:
- Systemupdates laufen wie gewohnt über `apk`.
- Pakete sind klein, sauber getrennt, skriptbar.
- Build‑Workflows lassen sich sauber automatisieren.

Kurz: Du bist nicht „auf einem Smartphone“, sondern auf einem richtigen Linux‑System – nur mit Touchscreen.

**Tool‑Ökosystem: Was ist schon da?**

postmarketOS bringt nicht nur Alpine‑Pakete mit, sondern ein eigenes, aktives Ökosystem an Tools.

- `pmbootstrap` ist das zentrale CLI‑Werkzeug für postmarketOS‑Entwicklung. Es erstellt Images, baut Pakete und unterstützt das Flashing auf reale Geräte.
- `pmaports` ist das Repository der Package‑Build‑Definitionen, also die Paketrezepte, auf denen das System aufbaut.
- `apk` bleibt die Basis für Paketverwaltung und Updates – ganz klassisch Alpine.

Für Linux‑Enthusiast:innen ist das der entscheidende Punkt: Das System ist nicht nur „nutzbar“, es ist entwickelbar. Und zwar mit Werkzeugen, die man bereits kennt und schätzt.

**Fairphone 6 als europäischer Kontext**

Technik ist nie nur Technik. Mit der Fairphone‑Reihe sehen wir ein europäisches Hardware‑Signal, das Reparierbarkeit und nachhaltige Produktgestaltung ernst nimmt. Der Fairphone 6 wurde in Europa gelauncht und steht als Beispiel dafür, dass europäische Hardware auch im Smartphone‑Bereich wieder Relevanz gewinnt.

Warum das im Kontext von postmarketOS wichtig ist? Weil Hardware‑Souveränität ohne Software‑Souveränität unvollständig bleibt. Wenn Europa eigene Hardware‑Leuchttürme baut, braucht es auch eigene Betriebssystem‑Optionen und App‑Ökosysteme, die nicht vollständig von US‑ oder China‑Plattformen abhängen.

**Vision: Ein europäisches Mobile‑Ökosystem**

Stell dir ein Europa vor, das nicht nur nachhaltige Hardware liefert, sondern auch ein eigenes, offenes mobiles Software‑Ökosystem.
postmarketOS ist kein Endprodukt – aber es zeigt, dass die Grundlagen existieren:
- eine modulare, kontrollierbare Linux‑Basis
- transparente Paketierung
- offene Toolchains
- eine Community, die echte Geräte supported

Das ist der strategische Hebel: Wenn postmarketOS und ähnliche Systeme reifen, entsteht Raum für europäische Apps, europäische Services und langfristig auch europäische digitale Unabhängigkeit.

**Warum gerade dieses Projekt als Beispiel?**

`Jaraco Starter` ist ein idealer Showcase, weil es drei Dinge gleichzeitig demonstriert:

1. Real‑World‑Funktionalität: Es ist keine Demo, sondern ein echtes Tool, das Prozesse starten/stoppen kann.
2. Mobile‑taugliches UI: GTK4/libadwaita läuft mobil solide, klar und angenehm.
3. Linux‑Logik bleibt erhalten: Prozesse, Signals, Polkit, Packaging – alles ist echtes Linux.

Damit wird der Entwicklungsprozess greifbar: Man sieht, wie Apps auf postmarketOS tatsächlich entstehen, und man kann den kompletten Weg von JSON‑Config bis Paketbau nachvollziehen.

**Fazit**

postmarketOS verändert nicht nur wo man entwickelt, sondern wie. Es ist eine Rückkehr zu einem direkten, transparenten Entwicklungsgefühl, das viele Linux‑Enthusiast:innen vermisst haben. `Jaraco Starter` zeigt, dass mobile App‑Entwicklung nicht zwingend Spezial‑SDKs oder verschlossene Plattformen braucht – sondern dass ein sauberes Linux‑System reicht, wenn die Werkzeuge stimmen.

Mit Codex direkt auf dem Gerät wird die Loop noch kürzer: lesen, verstehen, ändern, testen – alles in einem einzigen Arbeitsraum. Und damit rückt die provokante Frage ins Zentrum: Ist postmarketOS in dieser frühen Bootstrap‑Phase genau die Plattform, auf die AI‑Devs gewartet haben – eine grüne Wiese, die man jetzt erobern und neu denken kann?

**Appendix: Befehle & Kurzbeschreibungen**

- `apk update`
Aktualisiert die Paketlisten von Alpine/postmarketOS.

- `apk add <paket>`
Installiert ein Paket aus den Repositories.

- `pmbootstrap init`
Initialisiert die pmbootstrap‑Umgebung für ein Gerät.

- `pmbootstrap build <pkg>`
Baut ein Paket aus `pmaports`.

- `pmbootstrap install`
Erstellt ein vollständiges postmarketOS‑Image.

- `abuild`
Standard‑Tool zum Bauen von APK‑Paketen aus `APKBUILD`.

- `pkexec <command>`
Startet einen Befehl mit Polkit‑Authentifizierung.

- `pgrep <pattern>`
Findet laufende Prozesse anhand eines Namensmusters.
