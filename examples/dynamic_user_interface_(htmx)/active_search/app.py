from fasthtml.common import *

app, rt = fast_app()

# Example contacts data
contacts = [
    {"first_name": "Venus", "last_name": "Grimes", "email": "lectus.rutrum@Duisa.edu"},
    {"first_name": "Fletcher", "last_name": "Owen", "email": "metus@Aenean.org"},
    {"first_name": "William", "last_name": "Hale", "email": "eu.dolor@risusodio.edu"},
    {"first_name": "TaShya", "last_name": "Cash", "email": "tincidunt.orci.quis@nuncnullavulputate.co.uk"},
    {"first_name": "Kevyn", "last_name": "Hoover", "email": "tristique.pellentesque.tellus@Cumsociis.co.uk"},
    {"first_name": "Jakeem", "last_name": "Walker", "email": "Morbi.vehicula.Pellentesque@faucibusorci.org"},
    {"first_name": "Malcolm", "last_name": "Trujillo", "email": "sagittis@velit.edu"},
    {"first_name": "Wynne", "last_name": "Rice", "email": "augue.id@felisorciadipiscing.edu"},
    {"first_name": "Evangeline", "last_name": "Klein", "email": "adipiscing.lobortis@sem.org"},
    {"first_name": "Jennifer", "last_name": "Russell", "email": "sapien.Aenean.massa@risus.com"},
    {"first_name": "Rama", "last_name": "Freeman", "email": "Proin@quamPellentesquehabitant.net"},
    {"first_name": "Jena", "last_name": "Mathis", "email": "non.cursus.non@Phaselluselit.com"},
    {"first_name": "Alexandra", "last_name": "Maynard", "email": "porta.elit.a@anequeNullam.ca"},
    {"first_name": "Tallulah", "last_name": "Haley", "email": "ligula@id.net"},
    {"first_name": "Timon", "last_name": "Small", "email": "velit.Quisque.varius@gravidaPraesent.org"},
]

# Mapping of keys to clean labels
mapping = {
    "first_name": "First Name",
    "last_name": "Last Name",
    "email": "Email"
}
keys = list(mapping)

def show_contacts(contacts: list[dict]):
    # HTML rows for all given contacts
    return [Tr(*[Td(contact[col]) for col in keys]) for contact in contacts]

# POST request to handle search
@rt("/search")
def post(search: str = None):
    # Default search term is empty string, which shows all contacts
    # If a search term is provided, it is converted to lowercase
    search_term = search.lower() if search else ""
    # Filter contacts based on search term
    # Uses First Name, Last Name, and Email to search
    filtered_contacts = [
        contact for contact in contacts
        if any(search_term in str(contact[key]).lower() for key in keys)
    ]
    # Get HTML for each row in the filtered contacts
    return show_contacts(filtered_contacts)

@rt
def index():
    return Titled("Active Search",
                  Div(

                      H3("Search Contacts"),
                      # HTMX for searching contacts
                      Input(
                          type="search",
                          name="search",
                          # Default shown in search bar
                          placeholder="Begin Typing To Search Users...",
                          # Input is of a form type
                          class_="form-control",
                          # A POST request to '/search' is called when the user types
                          hx_post="/search",
                          # Search is delayed by 500ms to delay the search until the user has stopped typing
                          # 'changed' is to ensure that no new search are triggered when the 
                          # user doesn't change the input of pastes the same value.
                          # 'keyup[key=='Enter']' triggers the search once enter is pressed.
                          # 'load' is to show all results initially on the page load.
                          hx_trigger="input changed delay:500ms, keyup[key=='Enter'], load",
                          # Put results in the search-results div
                          hx_target="#search-results",
                      ),
                      # The table initially shows all contacts and 
                      # dynamically updates when the user types in the search bar.
                      Table(
                          Thead(
                              Tr(*[Th(mapping[key]) for key in keys])
                          ),
                          Tbody(*show_contacts(contacts), id="search-results"),
                          class_="table"
                      ),
                      class_="container"
                  )
                 )

serve()
