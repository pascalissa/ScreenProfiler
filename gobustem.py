from subprocess import Popen, PIPE

with open("Top200.txt") as domain_file:
    domains = domain_file.readlines()

for domain in domains:
    process = Popen(["gobuster", "dir" ,"-u",f"{domain.strip()}", "-w", "./web-dir-list.txt", "-k"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    # print(output.decode())
    with open(f"./results/{domain[8:].strip()}.txt", "w") as f: #needs proper domain parsing with error checks
        f.write(output.decode())
    #print(domain.strip())