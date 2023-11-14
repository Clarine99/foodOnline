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
            else{
                $('#id_pin_code').val("");
            }
    }
// console.log(address)
}}