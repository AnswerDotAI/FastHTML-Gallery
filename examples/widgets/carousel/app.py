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
    
    # Create indicators with updated positioning for bottom overlay
    indicators = Div(
        *[Button(str(i + 1), cls="carousel-indicator", onclick=f"showSlide({i})", 
                 style="margin: 0 5px; padding: 5px 10px; border-radius: 50%; background: #fff;") 
          for i in range(len(images))],
        cls="carousel-indicators",
        style="display: flex; justify-content: center; position: absolute; bottom: 20px; left: 0; width: 100%; z-index: 2;"
    )
    
    # Create the carousel layout with relative positioning and include indicators and navigation inside
    carousel_items = Div(
        *[Div(img, cls="carousel-item", style="display: none;") for img in images],
        indicators,  # Indicators inside the carousel container
        navigation_buttons := Div(
            Button("⟨", cls="carousel-control-prev", onclick="prevSlide()",
                   style="font-size: 24px; padding: 10px 20px; border-radius: 50%; background: #fff;"),
            Button("⟩", cls="carousel-control-next", onclick="nextSlide()",
                   style="font-size: 24px; padding: 10px 20px; border-radius: 50%; background: #fff;"),
            cls="carousel-controls",
            style="display: flex; justify-content: space-between; position: absolute; width: 100%; top: 50%; transform: translateY(-50%);"
        ),
        cls="carousel",
        style="position: relative; width: 100%; overflow: hidden;"
    )

    # Enhanced JavaScript with indicator functionality
    js = Script("""
        let currentIndex = 0;
        const items = document.querySelectorAll('.carousel-item');
        const indicators = document.querySelectorAll('.carousel-indicator');
        const totalItems = items.length;

        function updateIndicators(index) {
            indicators.forEach((ind, idx) => {
                ind.style.backgroundColor = idx === index ? '#666' : '#ddd';
            });
        }

        function showSlide(index) {
            currentIndex = index;
            items.forEach((item, idx) => {
                item.style.display = idx === index ? 'block' : 'none';
            });
            updateIndicators(index);
        }

        function nextSlide() {
            showSlide((currentIndex + 1) % totalItems);
        }

        function prevSlide() {
            showSlide((currentIndex - 1 + totalItems) % totalItems);
        }

        // Auto-advance slides every 5 seconds
        setInterval(nextSlide, 5000);

        // Show the first slide initially
        showSlide(0);
    """)

    return (
        Title("Carousel"),
        Container(
            carousel_items,
        ),
        js
    )
  
# Ensure to run the app if this file is executed directly  
if __name__ == "__main__":  
    app.run()
