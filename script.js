async function generateDesign() {
    const prompt = document.getElementById("promptInput").value;
    const img = document.getElementById("designImage");
    const loadingText = document.getElementById("loading");
  
    if (!prompt) {
      alert("Please enter a prompt.");
      return;
    }
  
    loadingText.style.display = "block";
  
    try {
      const response = await fetch("http://127.0.0.1:5000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ prompt })
      });
  
      const data = await response.json();
  
      if (data.image_url) {
        // Force image refresh by adding a timestamp
        const newSrc = "http://127.0.0.1:5000" + data.image_url + "?t=" + new Date().getTime();
  
        // Update src after ensuring it's a new image to avoid flicker
        img.onload = () => {
          loadingText.style.display = "none";
          img.style.display = "block";
        };
  
        img.src = newSrc;
      } else {
        loadingText.style.display = "none";
        alert("Image generation failed.");
      }
    } catch (err) {
      console.error("Error:", err);
      loadingText.style.display = "none";
      alert("An error occurred while generating the image.");
    }
  }
  

  async function predictTrends() {
    const response = await fetch("http://127.0.0.1:5000/predict_trends");
    const data = await response.json();
  
    const labels = Object.keys(data);
    const values = Object.values(data);
  
    const ctx = document.getElementById("trendChart").getContext("2d");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [{
          label: "Predicted Popularity",
          data: values,
          backgroundColor: "rgba(54, 162, 235, 0.6)"
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  }
