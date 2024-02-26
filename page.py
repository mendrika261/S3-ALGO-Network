class Page:
    def __init__(self, domain):
        self.domain = domain
        self.content = f"<h1>Welcome on {domain}</h1>"

    def __str__(self):
        return self.domain
