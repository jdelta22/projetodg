function myFunction() {
    const forms = document.querySelectorAll('.form-delete');
    for (const form of forms) {
        form.addEventListener('submit', function(event) {
            const confirmed = confirm('Are you sure you want to delete this recipe?');
            if (!confirmed) {
                event.preventDefault();
            }
        });
    }
}

myFunction();