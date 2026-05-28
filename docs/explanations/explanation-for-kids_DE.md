# "Wer sagt dem Auto eigentlich, was es tun soll?"

Ein Auto ist ein bisschen wie der menschliche Körper. Unser Körper besteht aus vielen verschiedenen Körperteilen und sie alle haben eine bestimmte Aufgabe. Genau so ist es auch beim Auto: Das Fahrgestell gibt dem Auto Stabilität und seine Form. Bei dir hält das Skelett, also deine Knochen, deinen Köper zusammen. Der Motor pumpt Energie durch das Auto, wie das Herz bei dir Blut pumpt. Damit dein Herz pumpen kann, musst du essen. Das Auto "isst" Benzin oder Strom von der Zapfsäule. Die Räder und Reifen bewegen das Auto von einem Ort zum anderen, so wie dich deine Beine und Füße tragen. 

Damit die Körperteile wissen, wann sie eine Aufgabe wie erledigen sollen, gibt es ein ganzes Team von kleinen Nervenknoten, die über Nervenbahnen mit deinem Gehirn verbunden sind. Das Gehirn in deinem Kopf ist der Chef, der alle möglichen Informationen aus dem Körper sammelt, verarbeitet und Befehle zurück sendet. Stell dir zum Beispiel vor, du berührst mit deinem Finger eine heiße Herdplatte. Dann sendet der Nervenknoten an deiner Hand über die Nervenbahnen das Signal "HEIß" an dein Gehirn. Das überlegt nicht lange und schickt den Befehl "Hand sofort wegziehen" zurück.

<div align="center" style="margin: 30px 0;">
  <div style="max-width: 600px; text-align: left;">
    <img src="../assets/img-comparison-body-car.png"alt="Body car comparison" width="100%">
    <br>
    <small><em>Schematischer Vergleich von Körper und Auto. Links: Silhouette eines menschlichen Körpers, blau leuchtend sind das Gehirn und Nervensystem dargestellt. Rechts: Silhouette eines Autos, die ein blau leuchtendes Motorsteuergerät und einen Kabelbaum (CAN-Bus) zeigt.</em></small>
  </div>
</div>

Und wie ist das beim Auto? Dort gibt es auch kleine Nervenknoten, sogenannte Steuergeräte. Das Bremssteuergerät zum Beispiel kümmert sich um das Bremsen der Räder. Es gibt auch Nervenbahnen im Auto: Kabel die durch das ganze Auto laufen und verschiedene Steuergeräte miteinander verbinden. Diese Kabel haben ganz verrückte Namen wie CAN-Bus (das Hauptkabel im Auto, ähnlich deiner Wirbelsäule) oder LIN-Bus (ein kleines, kurzes Kabel, ähnlich wie die feinen Nervenbahnen in deinen Fingerspitzen). Das Gehirn ist ebenfalls ein Steuergerät. In den meisten Autos ist es das Motorsteuergerät, welches Informationen von zahlreichen Sensoren (den Augen/Ohren des Autos) verarbeitet und für einen reibungslosen Motorlauf sorgt.

Die Steuergeräte sagen dem Auto also was es tun soll. Aber wer sagt es den Steuergeräten? Hier kommen die Softwarentwickler ins Spiel. Sie schreiben Anweisungen in einer speziellen Sprache, die dem Steuergerät ganz genau sagen, wie es sich verhalten soll. Man nennt das auch Programmieren oder, auf englisch, Coden. Am Ende sind es viele Millionen Zeilen Code, die dem Auto Befehle geben.

# "Wer entscheidet, an welche Befehle sich das Auto halten muss?"

Die Steuergeräte im Auto müssen extrem zuverlässig sein. Würde dein Gehirn bei der heißen Herdplatte sagen "Heiß? Ist mir egal.", dann verbrennst du dir die Hand. Auch beim Auto lauern viele solcher Gefahren. Wenn zum Beispiel das Bremssteuergerät bei voller Fahrt plötzlich vergisst, wie man bremst, ist das ein riesiges Problem. Damit das niemals passiert, gibt es ein strenges Regelbuch für alle Leute, die Autos bauen. Dieses Regelbuch heißt ISO 26262.

Die ISO 26262 wird auch "Funktionale Sicherheit" oder "FuSi" genannt, weil sie genau das sicherstellen soll: Fehler sollen erkannt und so abgefangen werden, dass keine gefährlichen Situationen für Menschen entsteht. Das Ziel ist, dass ein Steuergerät bei einem Fehler immer noch sicher funktioniert. Denken wir beispielsweise an unser Motorsteuergerät. Wenn die Elektronik im Auto spinnt und das Motorsteuergerät die Anweisung "Vollgas nach vorne!" bekommt, obwohl wir gar nicht das Gaspedal durchdrücken, könnten wir einen schlimmen Unfall bauen. Damit das nicht passiert, bauen Softwareentwickler "Wächter" in ihre Programme ein. So schaut das Motorsteuergerät nicht nur auf das fehlerhafte Signal "Vollgas nach vorne!", sondern rückversichert sich bei dem Gaspedal, ob da wirklich jemand durchgedrückt hat. So merkst das Motorsteuergerät, "Achtung, hier stimmt was nicht" und anstatt einfach loszurasen, macht das Auto sofort alle Motoren aus. So bleibt das Auto einfach stehen - was vielleicht blöd ist, wenn ihr gerade auf den Weg in den Urlaub seid - aber das Auto fährt auch nicht gegen den nächsten Baum.

Das ISO 26262 Regelbuch lässt sich dabei in folgende Schritte einteilen: 

## 1. Risiko bewerten

Die Experten machen eine sogenannte Gefahrenanalyse & Risikobewertung (auf englisch Hazard Analysis and Risk Assessment, oder kurz HARA). Das ist richtige Detektivarbeit. Verschiedene Leute setzen sich zusammen und überlegen: "In einer bestimmten Situation, was passiert, wenn eine Funktion ausfällt oder falsch reagiert?" und "Welche konkreten Gefahren entstehen?". Zum Beispiel:

| 🕵️ Situation | ⚠️ Fehler | 🛑 Gefahr |
| --------- | --------- |---------- |
| Wir fahren in einer Spielstraße. | Das Motorsteuergerät bekommt das fehlerhafte Signal "Vollgas nach vorne!" und folgt dem Signal.| Spielende Kinder werden überfahren. |
| Wir fahren tagsüber durch einen Tunnel in der Stadt. | Das linke Scheinwerferlicht fällt aus. | Wir werden in dem Tunnel schlecht gesehen. |
| Wir wollen in eine enge Parklücke einparken. | Die Rückfahrkamera zeigt ein "alles ist frei" Bild. | Wir knallen an ein Fahrrad, was hinter uns steht, die Kamera aber nicht gesehen hat. |

## 2. ASIL (Automotive Safety Integrity Level) bestimmen

Dem Risiko wird eine "Wichtigkeits-Note" verliehen:
    
* 🔴 ASIL D: Extrem wichtig – wenn hier ein Fehler passiert, ist das Leben von Menschen in Gefahr!
* 🟠 ASIL C: Sehr wichtig, da es schwierig ist die Kontrolle in der Situation zu behalten.
* 🟡 ASIL B: Wichiger, denn wenn hier etwas passiert, könnte es brenzelig werden, aber ein guter Fahrer kann das meist locker händeln.
* 🟢 ASIL A: Wichtig, aber die Situation lässt sich gut meistern und es passiert nichts schlimmes.
* ⚪ QM (Normal und egal für die Sicherheit - z.B. das Autoradio)

| 🕵️ Situation | ⚠️ Fehler | 🪜 Einstufung |
| --------- | --------- | ---------- |
| Spielstraße | Motor gibt grundlos Vollgas. | Super kritisch, da der Fahrer keine Chance hat zu reagieren: 🔴 ASIL D |
| Stadt/Tunnel | Scheinwerfer fällt aus. | Kaum gefährlich, da immer noch das andere Licht funktioniert: 🟢 ASIL A |
| Einparken  | Kamera zeigt falsches Bild. | Gefährlich, aber wenn der Fahrer vorsichtig fährt und über die Schulter blickt, kein Unfall: 🟠 ASIL C. |

## 3. Sicherheitsziele definieren

Es wird festgelegt, wie sich das System im Fehlerfall verhalten muss, um den Fahrer zu schützen.

| 🕵️ Situation | ⚠️ Fehler | 🛡️ Sicherheitsziel |
| --------- | --------- | ---------- |
| Spielstraße | Motor gibt grundlos Vollgas.  | Das Auto darf niemals von alleine schneller werden. |
| Stadt/Tunnel | Scheinwerfer fällt aus. | Das Auto muss immer sichtbar sein, zum Beispiel durch ein Ersatzlicht. |
| Einparken  | Kamera zeigt falsches Bild. | Warnung an den Fahrer, wenn das Bild nicht stimmt. |

## 4. Sicherheitsmechanismen entwickeln

Es werden konkrete Lösungen gebaut (programmiert), die Fehler erkennen und vermeiden.

| 🕵️ Situation | ⚠️ Fehler | 🎯 Sicherheitsmechanismus |
| --------- | --------- | ---------- |
| Spielstraße | Motor gibt grundlos Vollgas.  | Doppel-Check: Das Motorsteuergerät glaubt dem Befehl „Vollgas“ nur, wenn auch ein zweiter Sensor sagt: „Ja, das Pedal ist wirklich gedrückt!“ <br> <img src="../assets/graph-saftey-mechanism.svg" width="400">|
| Stadt/Tunnel | Scheinwerfer fällt aus. | Das Steuergerät am Scheinwerferlicht prüft sich immer wieder selbst, ob alles funktioniert. |
| Einparken  | Kamera zeigt falsches Bild. | Das Steuergerät an der Rückfahrkamera merkt, dass das Bild eingefroren ist und schickt ein "nur schwarzes Bild anzeigen" Signal heraus. |

## 5. Verifizierung & Validierung

Durch Tests wird bewiesen, dass die Sicherheitsziele erreicht wurden. Dabei wird auf vielen verschiedenen Ebenen geprüft:
   
- 🟦 **Einheitstest (Unit Test)**: Der "Einzelteil-Check". Hier wird jeder winzige Baustein vom Computer-Code einzeln geprüft. 
  - *Beispiel*: Wir fragen einen Baustein, was $2+2$ ist. Wenn er mit $4$ antwortet, hat er den Test bestanden. Da ist es erstmal egal, dass der Baustein später hilft, die Bremse zu steuern.
  
- 🧩 **Integrationstest**: Der "Zusammenspiel-Check". Hier werden zwei oder mehrere Bausteine des Computer-Codes gemeinsam getestet. 
  - *Beispiel*: Wenn der eine Baustein sagt: "Ich habe den Bremsknopf bedient", dann schauen wir, ob der zweite Baustein diese Nachricht richtig versteht und nicht etwa denkt, er soll das Radio lauter machen.

- 🚗 **Systemtest**: Der "Gesamt-Check". Hier wird das fertige Auto (oder das ganze Gerät) so getestet, wie es später auf der Straße fährt.
    - *Beispiel*: Ein Testfahrer fährt auf einer Teststrecke und drückt bei Vollgas auf die Bremse. Wir prüfen: Hält das ganze Auto sicher an, so wie wir es versprochen haben?


# "Wie schreibt man Millionen von Befehlen ohne Fehler zu machen?"

Jetzt wissen wir: Es gibt ein strenges Regelbuch (die ISO 26262). Aber wie schaffen wir es, dass wir beim Programmieren von so vielen Steuergeräten nicht den Überblick verlieren?

Stell dir vor, du willst ein großes LEGO-Haus bauen. Du öffnest die Verpackung und dir purzeln super viele verschieden bunte Bausteine entgegen. Und jetzt stell dir vor, die Bauanleitung besteht nur aus Text - Das wäre wahnsinnig kompliziert! Stattdessen besteht die Anleitung aus Bildern, die dir Schritt für Schritt erklären, welches Steinchen du wohin setzen sollst. In der Automobilindustrie ist das ganz ähnlich. Wir programmieren nicht nur Text, sondern wir nutzen auch Modelle. Man nennt das **Modellbasierte Entwicklung**, auf Englisch **Model-Based Design**, kurz **MBD**.

Diese Modelle sehen aus wie Bilder, wie ein Bauplan. In Programmen wie **MATLAB/Simulink** zeichnen wir Kästchen und verbinden sie mit Linien.

<div align="center" style="margin: 30px 0;">
  <div style="max-width: 600px; text-align: left;">
    <img src="../assets/img-simulink.png" alt="Simulink model" width="100%">
    <br>
    <small><em>Beispiel eines Modells. Links kommt ein Signal an ("Signal_Input"), welches nacheinander an zwei Kästchen weitergeleitet wird ("Check_Function1" und "Check_Function2"). Innerhalb dieser Kästchen erfolgt eine Prüfung des Signals und am Schluss werden zwei Signale raus geschickt ("Signal_Output1" und "Signal_Output2")</em></small>
  </div>
</div>

Die Eingangssignale können zum Beispiel vom Gaspedal-Sensor kommen. Die Signale gehen dann an eine "Wächter"-Funktion, welche das Ergebnis in Form von Signalen weiterleitet.

Der Riesenvorteil: Wir können am Computer auf "Play" drücken und das Auto virtuell fahren lassen, noch bevor das echte Auto überhaupt gebaut wurde! Das nennt man **Simulation**. Wir testen so, ob unsere "Wächter" auch wirklich aufpassen. Das ist unglaublich praktisch, denn so können wir schon früh prüfen, dass unser Sicherheitsmechanismus auch wirklich funktioniert. Und noch praktischer, aus den Modellen können wir automatisch den Code erzeugen lassen, dafür gibt es extra Programme, damit sich durch vertippen keine Fehler einschleichen.


# "Wie verhindert man ein riesiges Durcheinander bei so vielen Nachrichten?"

Ihr könnt euch vorstellen, bei all den Signalen und Sicherheitsvorkehrungen glühen die Drähte im Auto. Damit dabei kein riesiges Chaos entsteht, gibt es einen **Masterplan der Zusammenarbeit**.

In der Autowelt heißt dieser Plan ARXML-Datei. Sie ist wie ein riesiges, digitales Architekten-Handbuch für das ganze Auto. Darin steht ganz genau:

- Der **Aufgaben-Steckbrief**: Welches Programm (Software-Komponente) ist für was zuständig? Zum Beispiel: „Ich kümmere mich nur um das Fensterheben.“
- Die **Sprache**: Wird die Geschwindigkeit in „km/h“ oder in „Metern pro Sekunde“ gemessen? Die ARXML sorgt dafür, dass alle die gleichen Einheiten (Datentypen) benutzen, damit niemand aneinander vorbeiredet.
- Die **Anschlüsse**: Wer darf mit wem reden? Das ist wie bei Puzzleteilen: Nur wenn die Anschlüsse (Schnittstellen) exakt zusammenpassen, fließen die Informationen auch richtig.
- Das **Netzwerk**: Über welches „Kabel-Labyrinth“ (Bus-System) müssen die Nachrichten fließen, um blitzschnell am Ziel anzukommen?

Das Problem: Dieser Masterplan ist kein normales Buch. Es ist eine digitale Datei mit Millionen von Zeilen. Wenn ein Mensch darin nach einem Fehler sucht, ist das so, als müsste er eine Nadel in einem Heuhaufen finden, der so groß ist wie ein Fußballstadion. 

Weil wir uns aber keine Fehler erlauben dürfen (erinnert ihr euch an die ISO 26262?), habe ich ein spezielles Werkzeug gebaut: Einen Python Parser. Mein Programm liest diesen riesigen Masterplan blitzschnell durch und findet sofort die Stellen, die für unsere „Sicherheits-Wächter“ wichtig sind. So müssen wir nicht raten, sondern wissen sicher: Alle Programme arbeiten perfekt zusammen und das Auto bleibt sicher.