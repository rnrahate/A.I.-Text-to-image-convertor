document.getElementById("generateBtn").addEventListener("click", function () {
    const prompt = document.getElementById("prompt").value;

    if (prompt === "") {
        alert("Please enter a prompt.");
        return;
    }

    fetch('http://127.0.0.1:5000/generate-image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: prompt }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to generate image.');
        }
        return response.json();
    })
    .then(data => {
        if (data.image_url) {
            const imgElement = document.createElement('img');
            imgElement.src = `http://127.0.0.1:5000${data.image_url}`;
            imgElement.alt = 'Generated Image';
            document.getElementById('image-container').innerHTML = '';
            document.getElementById('image-container').appendChild(imgElement);
        } else {
            alert('No image URL received.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Image generation failed.');
    });
});
