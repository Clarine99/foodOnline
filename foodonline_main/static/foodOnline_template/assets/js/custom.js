let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in','id']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing.";
    }
    else{
        // console.log('place name=>', place.name)
    }
    // console.log(place)
    // get the address components and assign them to the fields
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value
    
    geocoder.geocode({'address':address},function(results, status){
        console.log(google.maps.GeocoderStatus.OK)
        if (status === google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();
            // console.log('lat=>',latitude);
            // console.log('lng=>',longitude);

            $('#id_longitude').val(longitude);
            $('#id_latitude').val(latitude);

            $('#id_address').val(address);
        }
        console.log(place)
    
    })
    for (var i=0; i<place.address_components.length; i++ ){
        for (var j=0; j<place.address_components[i].types.length; j++){
            //Get country
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name);

            }
            // Get state
            if(place.address_components[i].types[j] == 'sublocality'){
                console.log(place.address_components[i].types[j])
                $('#id_state').val(place.address_components[i].long_name);
            }
            //Get Postal code
            if(place.address_components[i].types[j] == 'postal_code'){
                console.log(place.address_components[i].types[j])
                $('#id_pin_code').val(place.address_components[i].long_name);
            }
            //Get City
            if (place.address_components[i].types[j] == 'administrative_area_level_2'){
                console.log(place.address_components[i].types[j])
                $('#id_city').val(place.address_components[i].long_name);
                }
            else{
                $('#id_pin_code').val("");
            }
    }
// console.log(address)
}}

$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');


        $.ajax({
            type:'GET',
            url:url,
            success: function(response){
                console.log('this is',response)
                 if (response.status === "Failed"){
                    console.log(response)
                    console.log("faileddd")
                }
                else{
                    
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)
                    console.log("suksessss", response.cart_amount['get_cart_counter'])
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )
                    

                }
                // $('#cart_counter').html(response.cart_counter['cart_count'])
                // $('#qty-'+food_id).html(response.cart_counter['qty'])
            }

        })
    })
    // place the cart item quantity on load

    $('.item_qty').each(function(){
        let the_id = $(this).attr('id');
        let qty = $(this).attr('data-qty');
        console.log(qty);
        console.log(the_id);
        $('#'+the_id).html(qty);
    })
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('cart-id');
        

        $.ajax({
            type:'GET',
            url:url,
            success: function(response){
                console.log('this is decrease',response)
                if (response.status === "Failed"){
                    console.log(response)
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )
                    if (window.location.pathname == '/cart/'){
                        removeCartItem(response.qty, cart_id)
                        checkEmptyCart()
                    }

                }
            }

        })
    })

    // DELETE CART ITEM
    $('.delete_cart').on('click', function(e){
        e.preventDefault();
       
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        

        $.ajax({
            type:'GET',
            url:url,
            success: function(response){
                console.log('this is delete',response)
                if (response.status === "Failed"){
                    console.log(response)
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )
                    removeCartItem(0, cart_id)
                    checkEmptyCart()

                }
        
            }

        })
    })
});

function removeCartItem (cartItemQty, cartId ){
    if (cartItemQty <= 0) {
        //Delete cart item
        document.getElementById("cart-item-"+cartId).remove()
        
    }
}
function checkEmptyCart (){
    let cart_counter = document.getElementById('cart_counter').innerHTML
    if (cart_counter == 0){
        console.log("Cart is empty")
        document.getElementById("empty-cart").style.display = "block";
    }
}
function applyCartAmounts(subtotal, tax, grand_total){
    if (window.location.pathname == "/cart/"){
        $('#subtotal').html(subtotal)
        $('#tax').html(tax)
        $('#total').html(grand_total)
        }
    }