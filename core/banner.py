from .colors import Colors


def Banner():
    print(
        Colors.RED
        + """
   ______            ____    
  / ____/___        /  _/___ 
 / /   / __ \______ / // __ \ 
/ /___/ /_/ /_____// // / / />
\____/\____/     /___/_/ /_/                
        """
        + Colors.YELLOW
        + """
    Developed by : """
        + Colors.GREEN
        + """ Mridupawan Bordoloi """
        + Colors.YELLOW
        + """
    Social Links:
    github : https://github.com/xxehacker
    gmail: mridupawan502@gmail.com

        """
        + Colors.ENDC
    )
