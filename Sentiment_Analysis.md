# Sentiment Analysis
## Inhalt
1. [Was ist Sentiment Analysis](#heading1) <br>
2. [Projekt: Klassifizieren von Filmreviews](#heading2) <br>
	2.1 [DistelBERT Modell](#heading3) <br>
	2.2 [Skript Initialisieren](#heading4) <br>
	2.3 [Test- und Trainingsdaten vorbereiten](#heading5) <br>
	2.4 [Importieren des DistelBERT NLP Modells](#heading6) <br>
	2.5 [Setzen der Trainingsparameter](#heading7) <br>
	2.6 [Trainieren, Evaluieren und Hochladen des Modells](#heading8) <br>
3. [Quellen](#heading9) <br>

## Was ist Sentiment Analysis <a name="heading1"></a>
Die Sentiment Analyse ermöglicht das verstehen von Gefühlen in Texten. Dabei werden diese in positive, negative oder auch neutrale Meinungen klassifiziert. Ein Beispiel für eine mögliche Anwendung kann sein, Social Media Posts und Kommentare zu bestimmten Aktien oder Unternehmen aus dem Internet zu ziehen und die allgemeine Meinung zu analysieren um eventuell vorhersagen zu können, ob der Aktienpreis sinken oder steigen wird.
## Projekt: Klassifizieren von Filmreviews<a name="heading2"></a>
Dieses Anwendungsbeispiel hat uns gezeigt, wie man ein Machine-Learning Modell zum Erkennen von Gefühlen in Bewertungen nutzen kann. Dafür wurde das DistilBERT-Modell verwendet und weitertrainiert.
### DistelBERT Modell <a name="heading3"></a>
DistilBERT ist die kleine Variante des BERT-Modells (Bidirectional Encoder Representations from Transformers). Diese beiden Modelle sind auf Natural Language Processing (NLP) spezialisiert. In unserem Fall wollen wir also die Sprachverarbeitung dieses bereits trainierten Modells nutzen, und auf unseren Anwendungsfall (Ob ein Text schlecht oder gut gemeint ist) anpassen, also trainieren. Der Vorteil von DistilBERT ist, dass es viel kleiner ist als das Original, aber dabei nur 5% der Genauigkeit des großen Bruders einbüßt. Diese Kompression wird durch mehrere Prozesse erreicht:

-   Destillation (deswegen  **Distil**BERT):
    -   Man kann sich dieses Verfahren wie ein Kind vorstellen, dass seinen Vater nachahmt: Das kleine Modell (Student-Modell) wird darauf trainiert, das Verhalten des großen Modells (Teacher-Modell) nachzuahmen. Dabei werden die Wahrscheinlichkeiten des großen Modells als Ziele für das kleine Modell genommen.
-   Kombination der Schichten (Transformer-Blöcke):
    -   Um zu verstehen was die Schichten überhaupt sind, hier eine kurze Erklärung zu den Transformer-Blöcken:
        -   Diese sind die elementaren Bausteine der Transformer-Architektur, welche aus jeweils  **zwei**  Komponenten bestehen:  **Multi-Head Attention Mechanismus**  (Das Modell konzentriert sich auf verschiedene Teile des Eingabetextes. Der Mechanismus besteht aus verschiedenen Heads, die sich jeweils ihre eigene Aufmerksamkeitsverteilung berechnen. Dadurch werden Beziehungen und Abhängigkeiten zwischen Wörtern erkannt.) und  **Feedforward Neural Network**  (Verarbeitet die Ausgabe des Mechanismus um Muster im Text zu erfassen und nutzt zum Beispiel die GELU-Funktion* als Aktivierungsfunktion).
    -   Die Schichtkombination bedeutet einfach nur, dass der Output mehrerer Schichten zusammengefasst wird. Das sorgt dafür dass DistelBERT ein kleineres Modell ist, jedoch trotzdem komplexe Beziehungen in Texten erfassen kann.
-   Parameter-Sharing
    -   Mehrere Schichten im Modell teilen sich die Parameter, statt jeweils eigene zu haben. Dadurch wird die Gesamtanzahl der Parameter deutlich reduziert, was das Modell kompakter und schneller als BERT macht.

*Die GELU-Funktion (Gaussian Error Linear Unit) kombiniert eine lineare Funktion mit einer Gaußschen Fehlerfunktion und kann dadurch eine nicht-lineare Aktivierung erzeugen. Das hilft dem Modell dabei, auch nicht lineare Zusammenhänge und komplexe Muster und Strukturen in Texten zu erkennen und diese zu lernen.
### Skript initialisieren <a name="heading4"></a>
Um mit dem Aufbau und Trainieren des Modells zu beginnen müssen wir die nötigen Pakete mittels des Python Paketmanagers PIP installieren. (Der Code auf der Webseite wird mit Deepnote angezeigt, nutzt aber bitte Google Colab da der Huggingface Login in Deepnote buggt)

Beim Installieren der Pakete müssen wir auf eine ältere Version von Transformer zurückgreifen, da die aktuelle Fehler wirft. <br> <br>
![image](https://github.com/bladerunner-avalanche/Sentiment_Analysis/assets/117034924/7d8a2799-b148-4f32-bc2b-47e919e2c067) <br> <br>
Diese Pakete werden dann importiert: <br> <br>
![image](https://github.com/bladerunner-avalanche/Sentiment_Analysis/assets/117034924/a20043d8-b3b0-4f16-8cc3-4883dd283965) <br> <br>
Da wir das vortrainierte NLP-Modell DistelBERT nutzen, müssen wir unsere Umgebung bei Huggingface.co anmelden, um dieses zu laden. Außerdem können wir dadurch unser trainiertes Modell in ein Repository hochladen. <br> <br>
![image](https://github.com/bladerunner-avalanche/Sentiment_Analysis/assets/117034924/df688ad1-0910-474f-9516-2ac838b6ed1b) <br> <br>
Anschließend laden wir das bereits für uns vorbereitete IMDB Review Dataset herunter, und testen dann, ob in unserer Runtime eine GPU verfügbar ist: <br> <br>
![image](https://github.com/bladerunner-avalanche/Sentiment_Analysis/assets/117034924/761e2e17-bf35-4907-804f-536d603fce10) <br> <br>
