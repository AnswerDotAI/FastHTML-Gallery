from fasthtml.common import FastHTML, Div, Img, Button, Container, Title, Script  
  
# Create the FastHTML app instance  
app = FastHTML()  
  
# Define the app route  
@app.get("/")  
def carousel_app():  
    # Sample images for the carousel  
    images = [  
        Img(src="/files/examples/widgets/carousel/image1.jpg", alt="Image 1", style="width: 100%;"),  
        Img(src="/files/examples/widgets/carousel/image2.jpg", alt="Image 2", style="width: 100%;"),  
        Img(src="/files/examples/widgets/carousel/image3.jpg", alt="Image 3", style="width: 100%;")  
    ]  
      
    # Create the carousel layout using FastHTML  
    carousel_items = Div(  
        *[Div(img, cls="carousel-item", style="display: none;") for img in images],  
        cls="carousel",  
        style="position: relative; width: 100%; overflow: hidden;"  
    )  
  
    # JavaScript for carousel functionality  
    js = Script("""  
        let currentIndex = 0;  
        const items = document.querySelectorAll('.carousel-item');  
        const totalItems = items.length;  
  
        function showSlide(index) {  
            items.forEach((item, idx) => {  
                item.style.display = idx === index ? 'block' : 'none';  
            });  
        }  
  
        function nextSlide() {  
            currentIndex = (currentIndex + 1) % totalItems;  
            showSlide(currentIndex);  
        }  
  
        function prevSlide() {  
            currentIndex = (currentIndex - 1 + totalItems) % totalItems;  
            showSlide(currentIndex);  
        }  
  
        // Show the first slide initially  
        showSlide(currentIndex);  
    """)  
  
    # Add navigation buttons with centered styling  
    navigation_buttons = Div(  
        Button("Previous", cls="carousel-control-prev", onclick="prevSlide()"),  
        Button("Next", cls="carousel-control-next", onclick="nextSlide()"),  
        cls="carousel-controls",  
        style="display: flex; justify-content: center; position: absolute; width: 100%; top: 50%; transform: translateY(-50%);"  
    )  
  
    return (  
        Title("Carousel Example"),  
        Container(carousel_items, navigation_buttons),  
        js  
    )  
  
# Ensure to run the app if this file is executed directly  
if __name__ == "__main__":  
    app.run()  
