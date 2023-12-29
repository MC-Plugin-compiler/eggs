import os
import json
from jinja2 import Template
from datetime import datetime

data = []
for root, dirs, files in os.walk("."):
    for filename in files:
        if filename.endswith(".json") and filename.startswith("egg-"):
            with open(os.path.join(root, filename)) as f:
                json_data = json.load(f)
            name = json_data.get("name")
            url = "https://github.com/parkervcp/eggs/blob/master/" + os.path.join(root, filename).replace("\\", "/").replace("./", "")
            d_url = os.path.join(root, filename).replace("\\", "/").replace("./", "")
            readme = os.path.join(root, "README.md").replace("\\", "/").replace("./", "")
            exported_at = json_data.get("exported_at")
            if exported_at:
                exported_at = datetime.fromisoformat(exported_at).strftime("%b %d, %Y %I:%M %p")
            filename = os.path.basename(url)
            readme_filename = os.path.basename(url).replace('egg-', '').replace('.json', '')
            author_email = json_data.get("author").replace('@', '[at]').replace('.', '[dØt]')
            data.append({"name": name, "url": url, "filename": filename, "exported_at": exported_at, "author_email": author_email, "d_url": d_url, "readme": readme, "readme_filename": readme_filename})

template = Template("""
<!DOCTYPE html>
<html lang="en">
<html>
    <head>
        <meta name="viewport" charset="UTF-8" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" />
        <title>Parkers Pterodactyl eggs</title>
        <link rel="shortcut icon" type="image/png" href="favicon.png" />
        <style>
            #color-toggle {
                position: fixed;
                top: 20px;
                right: 20px;
                background-color: transparent;
                border: none;
                outline: none;
                cursor: pointer;
                z-index: 9999;
            }
            #color-toggle i {
                font-size: 24px;
                color: #000;
            }
            .dark-mode #color-toggle i {
                color: #fff;
            }
            .container {
                display: flex;
                align-items: center;
                justify-content: center;
                height: 6vh; /* or any height you want */
                width: 80%;
                margin: 0 auto;
            }
            #search {
                /* add any styles you want for the input */
                width: 70%;
                height: 40px;
                padding: 8px;
                border-radius: 4px;
                border: none;
            }
            .github-icon {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 9999; /* Make sure it's on top of other elements */
                color: white; /* Set the icon color */
                background-color: black; /* Set the icon background color */
                padding: 10px;
                border-radius: 50%;
            }
            .discord-icon {
                position: fixed;
                bottom: 20px;
                left: 20px;
                margin: 10px;
                z-index: 9999;
                background-color: #8c9eff;
                padding: 10px;
                border-radius: 50%;
            }
            button {
                background-color: #4caf50; /* Set the background color */
                border: none; /* Remove the border */
                color: white; /* Set the text color */
                padding: 10px 20px; /* Add some padding */
                text-align: center; /* Center the text */
                text-decoration: none; /* Remove underline */
                display: inline-block; /* Make the button a block element */
                font-size: 16px; /* Set the font size */
                border-radius: 5px; /* Add rounded corners */
            }
            button:hover {
                background-color: #3e8e41; /* Change the background color on hover */
            }
            button:active {
                background-color: #135434; /* Change the background color on click */
            }
            /* Light mode */
            body {
                background-color: #f2f2f2;
                font-family: Arial, sans-serif;
            }
            table {
                border-collapse: collapse;
                margin: 20px auto;
                width: 80%;
                overflow-x: auto;
            }
            th,
            td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #4caf50;
                color: white;
            }
            tr:hover {
                background-color: #b0b0b0;
            }
            input[type="text"] {
                width: 100%;
                padding: 12px 20px;
                margin: 8px 0;
                box-sizing: border-box;
                border: 2px solid #ccc;
                border-radius: 4px;
            }
            /* Dark mode */
            body.dark-mode {
                background-color: #333333;
                color: #f2f2f2;
            }
            table.dark-mode {
                border-collapse: collapse;
                background-color: #333333;
                margin: 20px 0;
            }
            th.dark-mode,
            td.dark-mode {
                border: 1px solid #888888;
                padding: 8px;
                text-align: left;
            }
            th.dark-mode {
                background-color: #333333;
                color: white;
            }
            tr.dark-mode:hover {
                background-color: #333333;
            }
            input.dark-mode[type="text"] {
                width: 100%;
                padding: 12px 20px;
                margin: 8px 0;
                box-sizing: border-box;
                border: 2px solid #ccc;
                border-radius: 4px;
                background-color: #333333;
                color: #f2f2f2;
            }
            td.dark-mode a {
                color: #FFC0CB; /* Pink color in dark mode */
                text-decoration: none; /* Remove underline */
            }
        </style>
    </head>
    <body>
        <button id="color-toggle" title="DarkMode" onclick="toggleDarkMode()">
            <i class="fas fa-adjust"></i>
        </button>
        <div style="display: flex; align-items: center; justify-content: center;">
            <img src="favicon.png" alt="Logo" height="100" />
            <h1 style="margin: 0 20px;">Parkers Pterodactyl eggs</h1>
            <a href="https://github.com/parkervcp/eggs">
                <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" class="github-icon" alt="GitHub" style="width: 30px; height: 30px; margin-top: 5px; margin-right: 10px;" />
            </a>
            <a href="https://discord.gg/pterodactyl">
                <img src="https://cdn3.iconfinder.com/data/icons/popular-services-brands-vol-2/512/discord-1024.png" class="discord-icon"" alt="Discord" style="width:30px;height:30px;margin-top:5px;margin-right:10px;">
            </a>
        </div>
        <div class="container">
            <input type="text" id="search" onkeyup="search()" placeholder="Search for eggs or authors" />
        </div>
        <table id="table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>URL</th>
                    <th>Last updated At</th>
                    <th>Author</th>
                    <th>Download</th>
                </tr>
            </thead>
            <tbody>
                {% for item in data %}
                <tr>
                    <td>{{ item.name }}</td>
                    <td><a href="{{ item.url }}" title="{{ item.url }}">{{ item.filename }}</a></td>
                    <td>{{ item.exported_at }}</td>
                    <td>{{ item.author_email }}</td>
                    <td>
                        <button
                            onclick="downloadFile('https://raw.githubusercontent.com/parkervcp/eggs/master/{{ item.d_url }}', '{{ item.filename }}'), downloadFile('https://raw.githubusercontent.com/parkervcp/eggs/master/{{item.readme}}', 'README-{{item.readme_filename}}.md')"
                        >
                            Download
                        </button>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <script>
            function downloadFile(url, filename) {
                fetch(url)
                    .then((response) => response.blob())
                    .then((blob) => {
                        const url = window.URL.createObjectURL(new Blob([blob]));
                        const a = document.createElement("a");
                        a.href = url;
                        a.download = filename;
                        document.body.appendChild(a);
                        a.click();
                        a.remove();
                    });
            }
            function toggleDarkMode() {
                document.body.classList.toggle("dark-mode");
            }
function search() {
    var input, filter, table, tr, td1, td2, i, txtValue1, txtValue2;
    input = document.getElementById("search");
    filter = input.value.toLowerCase(); // Convert filter to lowercase
    table = document.getElementById("table");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td1 = tr[i].querySelector("td:nth-child(1)");
        td2 = tr[i].querySelector("td:nth-child(4)");
        if (td1 || td2) { // Check if both td1 and td2 exist
            txtValue1 = td1.textContent || td1.innerText;
            txtValue2 = td2.textContent || td2.innerText;
            txtValue1 = txtValue1.toLowerCase(); // Convert table cell value to lowercase
            txtValue2 = txtValue2.toLowerCase(); // Convert table cell value to lowercase   
            if (txtValue1.indexOf(filter) > -1 || txtValue2.indexOf(filter) > -1) {
            tr[i].style.display = "";
            } else {
            tr[i].style.display = "none";
            } 
        }   
    }
}
        </script>
    </body>
</html>
""")


html = template.render(data=data)

with open("index.html", "w") as f:
    f.write(html)
