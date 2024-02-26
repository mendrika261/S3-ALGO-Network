def valid_ip(ip):
    try:
        ips = str(ip).split('.')
        if len(ips) != 4:
            raise
        for elem in ips:
            if str(elem) == '' or len(str(elem)) > 3:
                raise
            float(elem)
        return ip
    except Exception:
        raise ValueError(f"({ip}) n'est pas une adresse ipv4 valide")
