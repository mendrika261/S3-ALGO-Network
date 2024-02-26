from tool import valid_ip


class Computer:
    def __init__(self, ip, name=None, computer_type=None):
        self.ip = valid_ip(ip)
        self.name = name
        self.computer_type = computer_type
        self.page = []

    def __str__(self):
        if self.computer_type and str(self.computer_type) == 'server':
            view = f"{self.ip}\n{self.name}"
            for page in self.page:
                view += f"\n{page}"
            return view
        return f"PC: {str(self.name).capitalize()}"

    def __repr__(self):
        return f"({self.ip}, {self.name})"

    def get_page(self, page_domain):
        for page in self.page:
            if page.domain == str(page_domain).lower():
                return page
        return False
