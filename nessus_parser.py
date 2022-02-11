from xml.dom.minidom import parse

nessus_filename=""

def get_webpages_from_nessus(nessusFilename, plugins=None):
    if plugins is None:
        plugins = ["22964"]

    results = []
    with open(nessusFilename) as nessusFile:
        dom = parse(nessusFile)
    hosts = dom.getElementsByTagName("ReportHost")
    for host in hosts:
        ip = host.getAttribute('name')
        for finding in host.getElementsByTagName("ReportItem"):
            if finding.getAttribute('pluginID') in plugins:
                if "web server" in finding.getElementsByTagName("plugin_output")[0].firstChild.nodeValue.lower():
                    if ("TLS" or "SSL") in finding.getElementsByTagName("plugin_output")[0].firstChild.nodeValue.upper():
                        results.append(f"https://{ip}:{finding.getAttribute('port')}")
                    else:
                        results.append(f"http://{ip}:{finding.getAttribute('port')}")

    return results

links = get_webpages_from_nessus(nessus_filename)
with open(nessus_filename+".txt", "w") as links_file:
    for link in links:
        links_file.writelines(link+"\n")

