from computer import Computer
from network import Network
from page import Page
from tool import valid_ip


def build_network():
    network = Network()

    facebook = Page("facebook.com")
    youtube = Page("youtube.com")
    google = Page("google.com")

    c1 = Computer('10.168.292.133', 'South Africa', 'server')
    c1.page.extend([facebook, Page("google.co.za"), youtube])
    network.add_computer(c1)

    c2 = Computer('10.18.222.322', 'Reunion', 'server')
    c2.page.extend([Page("teletoon.fr"), Page("fr.tv"), Page("google.re")])
    network.add_computer(c2)

    c3 = Computer('11.13.20.24', 'Comores', 'server')
    network.add_computer(c3)

    c4 = Computer('10.102.328.23', 'Madagascar', 'server')
    c4.page.extend([Page("google.mg"), Page("fianarana.mg")])
    network.add_computer(c4)

    c5 = Computer('10.382.123.23', 'Nairobi', 'server')
    c5.page.extend([Page("google.ke")])
    network.add_computer(c5)

    c6 = Computer('8.102.32.23', 'New York', 'server')
    c6.page.extend([google, facebook, youtube, Page("twitter.com"), Page("instagram.com")])
    network.add_computer(c6)

    c7 = Computer('16.302.12.20', 'Caire', 'server')
    c7.page.extend([Page("google.eg"), Page("youchat.eg")])
    network.add_computer(c7)

    c8 = Computer('10.10.299.2', 'Paris', 'server')
    c8.page.extend([Page("google.fr"), Page("dior.fr"), Page("disney.fr"), facebook])
    network.add_computer(c8)

    c9 = Computer('11.8.79.34', 'UK', 'server')
    c9.page.extend([Page("google.uk"), facebook, youtube, Page("royal.uk"), google])
    network.add_computer(c9)

    c10 = Computer('29.193.20.10', 'China', 'server')
    c10.page.extend([Page("google.cn"), Page("wechat.com"), Page("baidu.com")])
    network.add_computer(c10)

    c11 = Computer('13.29.120.20', 'Madrid', 'server')
    c11.page.extend([Page("google.es"), google, Page("madrid.es")])
    network.add_computer(c11)

    network.add_link(c4, c1, 100)
    network.add_link(c4, c2, 50)
    network.add_link(c4, c3, 40)
    network.add_link(c4, c5, 120)
    network.add_link(c1, c6, 100)
    network.add_link(c5, c7, 20)
    network.add_link(c7, c8, 30)
    network.add_link(c8, c9, 5)
    network.add_link(c2, c10, 120)
    network.add_link(c11, c9, 40)
    network.add_link(c11, c8, 16)
    network.add_link(c11, c7, 10)
    network.add_link(c11, c6, 5)
    network.add_link(c9, c6, 5)

    return network


def show_menu():
    menu = ""
    menu += "\n0. Stop"
    menu += "\n1. Voir le réseau"
    menu += "\n2. Chercher une page à partir d'un ordinateur"
    menu += "\n3. Signaler une panne"
    menu += "\n4. Ajouter un lien / Réparer une panne"
    menu += "\n5. Ajouter un ordinateur"
    return menu


def ping(net):
    source_ip = input(f"{COLOR_BLUE}Entrer l'adresse IP source: {COLOR_RESET}")
    source = net.get_computer_by_ip(valid_ip(source_ip))
    if not source:
        raise ValueError(f"{COLOR_RED}⚠️ Il n'y a pas d'ordinateur avec cette adresse IP{COLOR_RED}")

    while True:
        destination_page = input(f"{COLOR_BLUE}Entrer la page à rechercher (0 pour annuler): {COLOR_RESET}")
        if destination_page == '0':
            break
        print(f"\n{COLOR_YELLOW}🔍 Recherche de {destination_page} à partir de {source_ip}{COLOR_RESET}")

        result = net.find_page_from(source, destination_page)
        print("-" * 50)
        if len(result[0]) == 0:
            print(f"{COLOR_RED}⛔️ La page {destination_page} est injoignable{COLOR_RESET}\n")
        else:
            print(f"{COLOR_GREEN}✅ La page {destination_page} est joignable{COLOR_RESET} en {len(result[0])} noeud(s)")
            print(f"⏰ Durée: {result[1]} ms")
            print(f"📡 Chemin:")
            for i in range(len(result[0])):
                print(f"\t{i + 1}. {result[0][i][0].__repr__()}: {COLOR_GREEN+result[0][i][1]} ms{COLOR_RESET}")
            page = result[0][-1][0].get_page(destination_page)
            print(f"📄 Contenu de la page {page}:\n{page.content}\n")


def panne(net):
    computer1_ip = input(f"{COLOR_BLUE}Entrer l'adresse IP du premier ordinateur: {COLOR_RESET}")
    computer1 = net.get_computer_by_ip(valid_ip(computer1_ip))
    if not computer1:
        raise ValueError(f"{COLOR_RED}⚠️ Il n'y a pas d'ordinateur avec cette adresse IP{COLOR_RESET}")

    computer2_ip = input(f"{COLOR_BLUE}Entrer l'adresse IP du deuxième ordinateur: {COLOR_RESET}")
    computer2 = net.get_computer_by_ip(valid_ip(computer2_ip))
    if not computer2:
        raise ValueError(f"{COLOR_RED}⚠️ Il n'y a pas d'ordinateur avec cette adresse IP{COLOR_RESET}")

    net.remove_link(computer1, computer2)
    print(f"{COLOR_YELLOW}❌🛜 Le réseau entre {computer1.__repr__()} et {computer2.__repr__()} a été coupé{COLOR_RESET}")


def ordinateur(net):
    ip = input(f"{COLOR_BLUE}Entrer l'adresse IP de l'ordinateur: {COLOR_RESET}")
    ip = valid_ip(ip)
    name = input(f"{COLOR_BLUE}Entrer le nom de l'ordinateur: {COLOR_RESET}")
    name = name if name else None
    computer_type = input(f"{COLOR_BLUE}Entrer le type de l'ordinateur (client/server): {COLOR_RESET}")
    computer_type = computer_type if computer_type else None

    computer = Computer(ip, name, computer_type)
    net.add_computer(computer)
    print(f"{COLOR_GREEN}✅ L'ordinateur {computer.__repr__()} a été ajouté au réseau{COLOR_RESET}")


def resolve_panne(net):
    computer1_ip = input(f"{COLOR_BLUE}Entrer l'adresse IP du premier ordinateur: {COLOR_RESET}")
    computer1 = net.get_computer_by_ip(valid_ip(computer1_ip))
    if not computer1:
        raise ValueError(f"{COLOR_RED}⚠️ Il n'y a pas d'ordinateur avec cette adresse IP{COLOR_RESET}")

    computer2_ip = input(f"{COLOR_BLUE}Entrer l'adresse IP du deuxième ordinateur: {COLOR_RESET}")
    computer2 = net.get_computer_by_ip(valid_ip(computer2_ip))
    if not computer2:
        raise ValueError(f"{COLOR_RED}⚠️ Il n'y a pas d'ordinateur avec cette adresse IP{COLOR_RESET}")

    distance = input(f"{COLOR_BLUE}Entrer la distance entre les deux ordinateurs: {COLOR_RESET}")
    distance = int(distance) if distance else None

    net.add_link(computer1, computer2, distance)
    print(f"{COLOR_GREEN}✅ Le réseau entre {computer1.__repr__()} et {computer2.__repr__()} a été corrigé{COLOR_RESET}")


if __name__ == '__main__':
    COLOR_RED = "\033[31m"
    COLOR_GREEN = "\033[32m"
    COLOR_YELLOW = "\033[33m"
    COLOR_BLUE = "\033[34m"
    COLOR_RESET = "\033[0m"

    network = build_network()

    stop = False

    print(f"{COLOR_BLUE}*** SIMULATION DE RESEAU 🛜 ***{COLOR_RESET}")

    while not stop:
        print(show_menu())
        choice = input(f"{COLOR_BLUE}Entrer votre choix: {COLOR_RESET}")
        print(COLOR_GREEN, end="")
        try:
            if choice == '1':
                network.draw()
            elif choice == '2':
                ping(network)
            elif choice == '3':
                panne(network)
            elif choice == '4':
                resolve_panne(network)
            elif choice == '5':
                ordinateur(network)
            elif choice == '0':
                stop = True
            else:
                print(f"{COLOR_YELLOW}⚠️🚨 Choix invalide")
        except ValueError as e:
            print(f"{COLOR_RED}{e}")
        finally:
            print(COLOR_RESET, end="")

    print(f"{COLOR_YELLOW}La simulation est terminée 🔚{COLOR_RESET}")
