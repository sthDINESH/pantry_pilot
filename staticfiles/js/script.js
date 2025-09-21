document.addEventListener("DOMContentLoaded", function () {
    console.log("DEBUG: Hello world!");

    gsap.from(".auth-grid-container .square-card",
    {
        y: 1000,
        duration: 1,
        stagger: 0.1
    }
) 
});