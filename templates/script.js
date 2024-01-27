function updateVendor(vendorId) {
    var name = prompt('Enter the new name:');
    var email = prompt('Enter the new email:');
    var contact = prompt('Enter the new contact:');
    var serviceType = prompt('Enter the new service type:');

    if (name && email && contact && serviceType) {
        fetch(`/update_vendor/${vendorId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `name=${name}&email=${email}&contact=${contact}&service_type=${serviceType}`,
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    }
}

function deleteVendor(vendorId) {
    var confirmDelete = confirm('Are you sure you want to delete this vendor?');
    if (confirmDelete) {
        fetch(`/delete_vendor/${vendorId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    }
}
