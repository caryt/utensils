from application import CLIApplication

class Utensils(CLIApplication):
    """Utensils: A Collection of python utility classes."""

if __name__ == '__main__':
    print Utensils.run_application(default='--help')
