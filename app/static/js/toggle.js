function toggleDeliveryFields() {
    const delivery = document.querySelector('input[name="delivery_method"][value="delivery"]').checked;
    const pickupSection = document.getElementById("pickup-section");
    const deliverySection = document.getElementById("delivery-section");

    if (delivery) {
        pickupSection.classList.add("d-none");
        deliverySection.classList.remove("d-none");
    } else {
        pickupSection.classList.remove("d-none");
        deliverySection.classList.add("d-none");
    }
}

// при загрузке страницы — выставляем корректное состояние
document.addEventListener("DOMContentLoaded", toggleDeliveryFields);