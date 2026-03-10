<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Coderr Backend - ReadMe</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        h1, h2 {
            color: #2c3e50;
        }
        code {
            background-color: #eee;
            padding: 2px 6px;
            border-radius: 4px;
        }
        pre {
            background-color: #eee;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
        ul {
            margin-top: 0;
        }
    </style>
</head>
<body>
    <h1>Coderr (Backend) - ReadMe</h1>

    <p>Mit <strong>Coderr</strong> erstellst du ein Backend für eine Freelancer-Entwickler-Plattform. Deine Frontend-Kollegen haben das Frontend schon auf die Beine gestellt. Deine Aufgabe ist es nun, die Plattform mit allen Funktionalitäten zum Laufen zu bekommen und Frontend und Backend zu verheiraten. Das Projekt lässt sich beliebig erweitern und anpassen.</p>

    <h2>Versionen</h2>
    <ul>
        <li>asgiref==3.11.1</li>
        <li>Django==6.0.3</li>
        <li>djangorestframework==3.16.1</li>
        <li>sqlparse==0.5.5</li>
        <li>tzdata==2025.3</li>
        <li>Python 3.14.2</li>
    </ul>

    <h2>Installation</h2>
    <p>Schritte, um das Projekt lokal zum Laufen zu bringen:</p>
    <ol>
        <li>Repository klonen:<br>
            <pre><code>git clone https://github.com/Greedrache/Coderr</code></pre>
        </li>
        <li>Virtuelle Umgebung aktivieren:<br>
            <pre><code>env dings</code></pre>
        </li>
        <li>Abhängigkeiten installieren:<br>
            <pre><code>pip install -r requirements.txt</code></pre>
        </li>
        <li>Migrations erstellen und Datenbank migrieren:<br>
            <pre><code>python manage.py makemigrations
python manage.py migrate</code></pre>
        </li>
        <li>Server starten:<br>
            <pre><code>python manage.py runserver</code></pre>
        </li>
    </ol>

    <h2>Hinweise</h2>
    <p>Stelle sicher, dass du die <code>settings.py</code> entsprechend konfiguriert hast, insbesondere die Datenbankeinstellungen und die REST-Framework-Authentifizierung.</p>

    <p>Jetzt bist du bereit, mit <strong>Coderr</strong> zu arbeiten!</p>
</body>
</html>
