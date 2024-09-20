document.addEventListener('DOMContentLoaded', function() {
                const input = document.getElementById('movie-search');
                const datalist = document.getElementById('suggestions-list');

                input.addEventListener('input', function() {
                    let query = this.value;

                    // Clear previous options
                    datalist.innerHTML = '';

                    if (query.length > 0) {
                        fetch(`/search?query=${query}`)
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error('Network response was not ok');
                                }
                                return response.json();
                            })
                            .then(data => {
                                console.log('Received data:', data);  // Debugging response

                                if (Array.isArray(data)) {
                                    data.forEach(title => {
                                        console.log('Processing title:', title);  // Debugging each title
                                        let option = document.createElement('option');
                                        option.value = title;  // Ensure the value is set to the title
                                        datalist.appendChild(option);
                                    });
                                } else {
                                    console.error('Expected array but got:', data);
                                }
                            })
                            .catch(error => console.error('Error fetching data:', error));
                    }
                });
            });